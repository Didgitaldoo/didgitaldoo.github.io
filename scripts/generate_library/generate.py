import os
import json
import shutil
import matplotlib.pyplot as plt

import sys
from pydub import AudioSegment

sys.path.append("../../../didge-lab/src/")
from didgelab.calc.geo import Geo
from didgelab.util.didge_visualizer import vis_didge
from didgelab.calc.sim.sim import compute_impedance_iteratively, get_notes, compute_impedance, create_segments, get_log_simulation_frequencies, interpolate_spectrum, compute_ground_spektrum

outfolder = "../../didge_database/"

archive_path = "../../../didge-archive"

def create_safe_name(shape):
    return shape["name"].lower().replace(" ", "-")

def create_didge_page(shape):
    safe_name = create_safe_name(shape)

    asset_folder = os.path.join(outfolder, safe_name)
    if not os.path.exists(asset_folder):
        os.mkdir(asset_folder)

    md_path = os.path.join(asset_folder, safe_name + ".md")

    content = f"""---
layout: default
title: {shape['name']}
---

# {shape['name']}"""
    if "images" in shape.keys():    
        image_path = shape['images'][0]
        filename = os.path.basename(image_path)
        content += f"\n\n<img class=\"didge_image\" src=\"{filename}\" width=\"200\"/>"
        shutil.copyfile(os.path.join(archive_path, image_path), os.path.join(asset_folder, filename))

    if "description" in shape.keys():    
        content += f"\n\n{shape['description']}"
 
    # audio example
    song_filename = shape["audio-samples"]["song"]
    song_filename = song_filename[song_filename.rfind("/")+1:]
    song_filename = song_filename[0:-4] + ".mp3"
    infile = os.path.join(archive_path, shape["audio-samples"]["song"])
    outfile = os.path.join(asset_folder, song_filename)

    if not os.path.exists(outfile):
        AudioSegment.from_wav(infile).export(outfile, format="mp3")
        print("created " + song_filename)

    content += f"""\n\n<audio controls>
    <source src="{song_filename}" type="audio/mp3">
    Your browser does not support the audio element.
</audio>

"""
    # geometry

    geo = json.load(open(os.path.join(archive_path, shape["geometry"])))
    geo = Geo(geo)

    freqs = get_log_simulation_frequencies(1, 1000, 10)
    segments = create_segments(geo)
    impedances = compute_impedance(segments, freqs)
    notes = get_notes(freqs, impedances).round(2)
    ground_freqs, imp_ip = interpolate_spectrum(freqs, impedances)
    ground = compute_ground_spektrum(ground_freqs, imp_ip)

    content += f"""## Basic info

* Tuning: {notes.note_name.iloc[0][0:-1]}
* Length: {round(geo.geo[-1][0])}mm
* Mouthpiece diameter: {round(geo.geo[0][1])}mm
* Bell diameter: {round(geo.geo[-1][1])}

[Download shape as JSON](geo.json)
"""
    
    if "thingiverse" in shape.keys():
        content += f"\n[Download STL files for 3D printing from Thingiverse]({shape['thingiverse']})"
    
    outfile = os.path.join(asset_folder, "geo.json")
    if not os.path.exists(outfile):
        shutil.copyfile(os.path.join(archive_path, shape["geometry"]), outfile)
        print("created outfile")
    
    # didge geometry image
    outfile = os.path.join(asset_folder, "geo.png")
    if not os.path.exists(outfile):
        plt.clf()
        vis_didge(geo)
        plt.savefig(outfile)
        print("created " + outfile)
    content += f'\n\n<img src="geo.png" size="200"/>'

    # sonic properties
    notes = notes[["note_name", "freq", "cent_diff", "rel_imp"]]
    notes.columns = ["Note Name", "Frequency", "Tuning (in Cent)", "Relative Impedance"]

    table = "<table class=\"analysis_table\">\n"
    table += "<tr class='even'><td><strong>\n" + "</strong></td>\n<td><strong>".join(notes.columns) + "</strong>\n</td></tr>\n"
    i=0
    for ix, row in notes.iterrows():
        row = dict(row)
        even = "" if i%2==0 else ' class="even"'
        table += f"<tr{even}><td>\n" + "</td>\n<td>".join([str(x) for x in row.values()]) + "\n</td></tr>\n"
        i+=1
    table += "\n</table>"

    outfile = os.path.join(asset_folder, "impedance_plot.png")
    if not os.path.exists(outfile):
        plt.clf()
        plt.plot(freqs, impedances)
        plt.xlabel("Frequency")
        plt.ylabel("Impedance")
        plt.title("Impedance Spektrum")
        plt.savefig(outfile)
        plt.clf()
        plt.cla()
        plt.close()

    outfile = os.path.join(asset_folder, "sound_plot.png")
    if not os.path.exists(outfile):
        plt.clf()
        plt.plot(ground_freqs, ground)
        plt.xlabel("Frequency")
        plt.ylabel("Amplitude")
        plt.title("Sound Spektrum")
        plt.savefig(outfile)
        plt.clf()
        plt.cla()
        plt.close()

    content += f"""
    
## Sonic properties
    
[Here is information how to read these technical information.](/2025/02/13/how-to-read-outputs-of-didgelab.html)

### Resonant frequencies

{table}

<img src="impedance_plot.png" />
<img src="sound_plot.png" />
"""
    
    content += f"\n\n## License\n{shape['license']}"

    # write output file
    with open(md_path, "w") as f:
        f.write(content)
        print("wrote " + md_path)


# create overview
def create_overview(archive):
    content = """---
layout: default
title: Didge Database
---
<h1>Didge Database</h1>
<p>Didgeridoo geometries and information about them.</p>

<div class="gallery">
"""

    for shape in archive:
        safe_name = create_safe_name(shape)
        basename = os.path.dirname(outfolder)
        basename = os.path.basename(basename)
        url = "/" + basename + "/" + safe_name + "/" + safe_name + ".html"

        image = ""
        if "images" in shape.keys():
            image_path = "/" + basename + "/" + safe_name + "/" + os.path.basename(shape["images"][0])
            image = f"<img src=\"{image_path}\" />"
        content += f"""

  <a class="tile" href="{url}">
    {image}
    <div class="name">{shape['name']}</div>
  </a>
"""

    content += "</div>"

    path = os.path.join(outfolder, "..", "didge-database.html")
    with open(path, "w") as f:
        f.write(content)
        print("wrote " + path)

if __name__ == "__main__":

    # if os.path.exists(outfolder):
    #     shutil.rmtree(outfolder)

    if not os.path.exists(outfolder):
        os.mkdir(outfolder)

    # create individual pages
    archive = json.load(open(os.path.join(archive_path, "didge-archive.json")))

    shapes_to_render = ["Malveira", "Arusha", "Open Didgeridoo"]

    archive = list(filter(lambda x:x["name"] in shapes_to_render, archive))
    
    for shape in archive:
        url = create_didge_page(shape)

    create_overview(archive)