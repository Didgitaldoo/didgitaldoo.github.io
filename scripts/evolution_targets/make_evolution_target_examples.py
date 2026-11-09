"""Sound examples and figures for the blog post "Sound effects as evolution targets".

The bores and WAV files come from the evolution-target notebooks of the
didgelab-experiments repository (evolution_targets/<target>/<target>.ipynb), which evolve
ten didgeridoos in D per target and render a drone, a wa-wa drone and a groove for each.
This script converts the clips of three bores per target to loudness-normalised MP3 and
draws one figure per target with two of them: the bores and their impedance spectra,
with every peak labelled by its ratio to the drone.

    EVOLUTION_TARGETS_OUT=/path/to/didgelab-experiments/evolution_targets/out \
        python scripts/evolution_targets/make_evolution_target_examples.py

``--figure-only`` redraws only the figures.

Needs didgelab and ffmpeg.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks

from didgelab import Geo, acoustical_simulation

ROOT = Path(__file__).resolve().parents[2]
AUDIO = ROOT / "assets" / "audio" / "evolution_targets"
IMAGES = ROOT / "assets" / "images" / "evolution_targets"
OUT = Path(os.environ.get("EVOLUTION_TARGETS_OUT", ROOT.parent.parent / "didgelab-experiments" / "evolution_targets" / "out"))

SONGS = ["drone", "wawa", "groove"]
DRONE = 73.42
TARGET_RMS_DB = -20.0
CONE = ("modal_density/cone/cone", "Plain cone")


def runs(target, name, label, numbers):
    """[(path below OUT without suffix, "label (1)"), ...] for the given run numbers"""
    return [(f"{target}/run_{n:02d}/{name}", f"{label} ({i})") for i, n in enumerate(numbers, 1)]


# target -> the three bores per effect in the post (for Q factor three low-Q and three high-Q)
SAMPLES = {
    "q_factor": runs("q_factor", "low_q", "Low Q", [6, 5, 9]) + runs("q_factor", "high_q", "High Q", [6, 8, 9]),
    "integer_harmonic": runs("integer_harmonic", "integer_harmonic", "Integer harmonics", [7, 4, 3]),
    "near_integer": runs("near_integer", "near_integer", "Near-integer", [6, 2, 4]),
    "stretched_odd": runs("stretched_odd", "stretched_odd", "Stretched odd", [4, 3, 10]),
    "high_inharmonic": runs("high_inharmonic", "high_inharmonic", "High inharmonic", [4, 8, 10]),
    "modal_density": runs("modal_density", "modal_density", "Modal density", [2, 10, 3]),
    "harmonic_splitting": runs("harmonic_splitting", "harmonic_splitting", "Harmonic splitting", [4, 7, 9]),
}
# the bores in the figures: low Q (1) and high Q (1), for the others (1) and (2)
FIGURES = {t: [s[0], s[3]] if t == "q_factor" else s[:2] for t, s in SAMPLES.items()}


def slug(path):
    """q_factor/run_06/low_q -> q_factor-run06-low_q"""
    target, run, name = path.split("/")
    return f"{target}-{run.replace('_', '')}-{name}" if run != "cone" else "cone"


def normalise(y):
    rms = np.sqrt(np.mean(y ** 2)) + 1e-12
    y = y * 10 ** (TARGET_RMS_DB / 20) / rms
    peak = np.abs(y).max()
    return y / peak * 0.98 if peak > 0.98 else y


def write_mp3(wav, mp3):
    fs, y = wavfile.read(wav)
    y = normalise(y.astype(float) / 32768)
    mp3.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        wavfile.write(tmp.name, fs, (y * 32767).astype(np.int16))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp.name, "-ac", "1",
                        "-b:a", "96k", str(mp3)], check=True)


def load_geo(path):
    return Geo(json.loads((OUT / f"{path}_geo.json").read_text()))


def figure(target, rows):
    freqs = np.arange(40.0, 1000.0, 0.5)
    # per bore: the bore over the full width at true scale (same mm on both axes), its impedance below
    fig, axes = plt.subplots(2 * len(rows), 1, figsize=(12, 4.1 * len(rows)),
                             gridspec_kw={"height_ratios": [1.5, 2.2] * len(rows)})
    for (path, label), ax_geo, ax_z in zip(rows, axes[::2], axes[1::2]):
        geo = load_geo(path)
        x, d = np.array(geo.geo).T
        ax_geo.fill_between(x, -d / 2, d / 2, color="#c8a37a")
        ax_geo.set_xlim(0, 2100); ax_geo.set_ylim(-75, 75)
        ax_geo.set_aspect("equal")
        ax_geo.set_ylabel("radius (mm)")
        ax_geo.set_xlabel("position (mm)", labelpad=1)
        ax_geo.set_title(f"{label}: {geo.length():.0f} mm", fontsize=10)

        z = np.abs(np.asarray(acoustical_simulation(geo, freqs)))
        z = z / z.max()
        for n in range(1, 14):
            ax_z.axvline(n * DRONE, color="0.85", lw=0.8, zorder=0)
        ax_z.semilogy(freqs, z, color="0.3", lw=1)
        peaks, _ = find_peaks(z, prominence=0.002)
        f0 = freqs[peaks[0]]
        for p in peaks:
            ax_z.plot(freqs[p], z[p], "o", color="#d62728", ms=4)
            ax_z.annotate(f"{freqs[p] / f0:.2f}", (freqs[p], z[p]), textcoords="offset points",
                          xytext=(0, 5), ha="center", fontsize=8)
        ax_z.set_xlim(40, 1000); ax_z.set_ylim(z.min() * 0.8, 3)
        ax_z.set_ylabel("|Z| (normalised)")
        ax_z.set_xlabel("frequency (Hz); grey lines: harmonics of the drone, numbers: peak / drone")
    plt.tight_layout()
    IMAGES.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMAGES / f"{target}.png", dpi=100)
    plt.close(fig)


def main():
    for target, examples in FIGURES.items():
        # Q factor: low and high Q of one run against the cone; the others: the cone, then both bores
        figure(target, examples + [CONE] if target == "q_factor" else [CONE] + examples)
    if "--figure-only" in sys.argv:
        return
    for path in [CONE[0]] + [path for samples in SAMPLES.values() for path, _ in samples]:
        for song in SONGS:
            write_mp3(OUT / f"{path}_{song}.wav", AUDIO / f"{slug(path)}-{song}.mp3")
        print(path)


if __name__ == "__main__":
    main()
