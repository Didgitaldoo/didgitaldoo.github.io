---
layout: default
title: Didgelab
---

# Didgelab

Didgelab is the swiss army knife for didgeridoo acoustics. It is a free open-source software.

Traditionally, building a didgeridoo is a random process. Builders know how the geometry influences the sound, but the exact sonic properties of the didgeridoo can only be determined after it was built. The Didgelab software helps didgeridoo builders to first define the sound and then compute the according geometry.

The main functionalities of Didgelab are:

1. Acoustical simulation to compute resonant frequencies of a didgeridoo geometry. This functionality is very similar to Didgmo and DidjiImp. We have our own software [Sketch](/sketch.html) on this website for acoustical simulation.

2. Computational evolution to find didgeridoo shapes with certain sonic properties.

So the first functionality takes a didgeridoo geometry as input and computes its sonic properties. The 2nd functionality works vice versa: It takes sonic properties as an input and generates a didgeridoo geometry with these sonic capabilities. Especially the 2nd functionality is super interesting. To the best of my knowledge, DidgeLab is the first open toolkit to implement this functionality.

What did we do with Didgelab?

* We computed Didgeridoos with precise acoustic properties, such as tuned peaks or resonance spektra.
* We created acoustic copies of a didgeridoo from a sound sample. We will write a blog article about this soon.
* Research on sound phenomena of Didgeridoos. We will blog articles about this soon.

In 2022, we released Didgelab 1.0, together with some documentation on [GitHub](https://github.com/didgitaldoo/didge-lab). We are building Didgelab 2.0 which is also in a stable state. Although the core-functionality is the same, the new version has many advantages over version 1.0. But it is still undocumented, so we advise everyone to use Didgelab 1.0.

Didgelab is not a consumer software. If you want to use it you need to program Python code.