"""Sound examples for the blog post "From shape and from impedance to sound".

For five didgeridoos of the Didge Archive (neutral drone and a song recorded):

* original:  the neutral drone from the archive
* geometry:  the measured bore played by the synthesizer (didgelab.synth)
* impedance: only the first six impedance peaks of the bore, played as a ModalBore

Each version is rendered as a neutral drone ("uh"), as a drone with the tongue gliding
from the front ("ee") to the back ("oo"), and as a 10 s groove (dong-tiki-ritititi, four
passes). Only the drone has an original recording. All clips are loudness-normalised and
written as MP3.

    DIDGE_ARCHIVE=/path/to/didge-archive python scripts/sound_examples/make_sound_examples.py

``--figure-only`` redraws only the figure.

Needs didgelab with didgelab.synth (ModalBore, render_song_loop_from_peaks) and ffmpeg.
"""
import os
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from scipy.io import wavfile

from didgelab.synth import SONGS, Bore, ModalBore, ModelParams, Synthesizer, archive, load_audio
from didgelab.synth import song as songs
from didgelab.synth.techniques import score_controls
from didgelab.sim.sim_interface import compute_moist_air_properties

FS = 48000
ROOT = Path(__file__).resolve().parents[2]
AUDIO = ROOT / "assets" / "audio" / "geometry_impedance_sound"
IMAGES = ROOT / "assets" / "images" / "geometry_impedance_sound"
DIDGES = ["Arusha", "Kizimkazi", "Malveira", "Nazare", "Open Didgeridoo"]
N_PEAKS = 6
TARGET_RMS_DB = -20.0
GROOVE, GROOVE_TEMPO, GROOVE_PASSES = "dong-tiki-ritititi", 96.0, 4   # 4 x 2.5 s = 10 s
TONGUE_SONG = """
title:  Drone, tongue front to back
tempo:  80
meter:  4/4

[rhythm]
| uh _ _ _ | _ _ _ _ | _ _ _ _ | _ _ _ _ |

[tongue]
| ee ~ ~ ~ | ~ ~ ~ ~ | ~ ~ ~ ~ | ~ ~ ~ oo |
"""


def slug(name):
    return name.lower().replace(" ", "-")


def normalise(y):
    y = np.asarray(y, dtype=float)
    rms = np.sqrt(np.mean(y ** 2)) + 1e-12
    y = y * 10 ** (TARGET_RMS_DB / 20) / rms
    peak = np.abs(y).max()
    return y / peak * 0.98 if peak > 0.98 else y


def fade(y, s=0.03):
    n = int(s * FS)
    w = np.ones(len(y))
    w[:n] = np.linspace(0, 1, n)
    w[-n:] = np.linspace(1, 0, n)
    return y * w


def write_mp3(path, y):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        wavfile.write(tmp.name, FS, (normalise(fade(y)) * 32767).astype(np.int16))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp.name, "-ac", "1",
                        "-b:a", "128k", str(path)], check=True)


def drone(bore, params):
    c = score_controls(bore, "tempo = 60\nuh:2.5", params)
    y = Synthesizer(bore, params, seed=0).render(c, reverb=0.15)
    return y[int(0.2 * FS):int(2.4 * FS)]


def tongue(bore, params):
    return songs.render(songs.parse(TONGUE_SONG), bore, fs=FS, params=params)


def groove(bore, params):
    return songs.render(songs.load(SONGS[GROOVE]), bore, tempo=GROOVE_TEMPO,
                        repeats=GROOVE_PASSES, loop=True, fs=FS, params=params)


def main(figure_only=False):
    constants = compute_moist_air_properties(temp_celsius=28.0)
    params = ModelParams()
    rows = []
    for name in DIDGES:
        inst = archive.get(name, os.environ.get("DIDGE_ARCHIVE"))
        geo = inst.geometry
        bore = Bore(geo, constants=constants)
        peaks = bore.resonances[:N_PEAKS]
        modal = ModalBore(peaks, mouth_diameter=geo[0][1], constants=constants)
        s = slug(name)
        rows.append((name, geo, bore, peaks, modal))
        if figure_only:
            continue

        x, _ = load_audio(inst.samples["neutral-sound"], FS)
        write_mp3(AUDIO / f"{s}-drone-original.mp3", x)
        write_mp3(AUDIO / f"{s}-drone-geometry.mp3", drone(bore, params))
        write_mp3(AUDIO / f"{s}-drone-impedance.mp3", drone(modal, params))
        for kind, render in (("tongue", tongue), ("groove", groove)):
            write_mp3(AUDIO / f"{s}-{kind}-geometry.mp3", render(bore, params))
            write_mp3(AUDIO / f"{s}-{kind}-impedance.mp3", render(modal, params))

        print(name, "drone %.1f Hz" % bore.drone, "peaks", [round(p.freq) for p in peaks], flush=True)

    figure(rows)


def figure(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    name, geo, bore, peaks, modal = rows[0]
    f = np.arange(30, 1500, 0.5)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 5.6), gridspec_kw={"height_ratios": [1, 2.2]})
    g = np.array(geo)
    a1.fill_between(g[:, 0], -g[:, 1] / 2, g[:, 1] / 2, color="#c8a27a", lw=0)
    a1.set(xlabel="position (mm)", ylabel="radius (mm)", title=f"{name}: the bore (same scale on both axes)")
    a1.set_aspect("equal")
    a1.set_xlim(-20, g[-1, 0] + 20)
    a1.set_ylim(-60, 60)
    a2.plot(f, np.abs(bore.interp("Zin", f)) / 1e6, color="#555", lw=1.2, label="from the geometry")
    a2.plot(f, np.abs(modal.interp("Zin", f)) / 1e6, color="#d62728", lw=1.2, ls="--",
            label=f"from {len(peaks)} peaks (impedance to sound)")
    a2.plot([p.freq for p in peaks], [p.impedance / 1e6 for p in peaks], "o", color="#d62728")
    a2.set(xlabel="frequency (Hz)", ylabel="|Z| (MPa s/m³)", yscale="log", title="impedance spectrum")
    a2.legend(frameon=False)
    fig.tight_layout()
    IMAGES.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMAGES / "arusha_impedance.png", dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    import sys
    main(figure_only="--figure-only" in sys.argv)
