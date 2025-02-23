import os
import json

import sys
sys.path.append("../../../didgelab/didge-lab/src/")
from didgelab.calc.sim.cadsd import CADSD

outfolder = "../../tmp/"

if not os.path.exists(outfolder):
    os.mkdir(outfolder)

archive_path = "/Users/jannehring/workspaces/music/didge-archive"

archive = json.load(open(os.path.join(archive_path, "didge-archive.json")))

def create_safe_name(shape):
    return shape["name"].lower().replace(" ", "-")

def create_didge_page(shape):
    content = f"""---
layout: default
title: {shape['name']}
---

# {shape['name']}

bla bla
"""
    safe_name = create_safe_name(shape)

    asset_folder = os.path.join(outfolder, safe_name)
    if not os.path.exists(asset_folder):
        os.mkdir(asset_folder)

    md_path = os.path.join(asset_folder, safe_name + ".md")

    with open(md_path, "w") as f:
        f.write(content)
        print("wrote " + md_path)

# create individual pages
for shape in archive:
    url = create_didge_page(shape)

# create overview
def create_overview(archive):
    content = """---
layout: default
title: Shape Gallery
---
<h1>Shape Library</h1>
<p>Didgeridoo geometries and information about them.</p>

<div class="gallery">
"""

    for shape in archive:
        safe_name = create_safe_name(shape)

        basename = os.path.dirname(outfolder)
        basename = os.path.basename(basename)
        url = "/" + basename + "/" + safe_name + "/" + safe_name + ".html"
        content += f"""

  <a class="tile" href="{url}">
    <img src="shapes/arusha/image.jpg" />
    <div class="name">{shape['name']}</div>
  </a>
"""

    content += "</div>"

    path = os.path.join(outfolder, "library.html")
    with open(path, "w") as f:
        f.write(content)
        print("wrote " + path)

create_overview(archive)