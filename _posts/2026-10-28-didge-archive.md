---
layout: default
title: Didge Archive - an open collection of didgeridoos
date: 2026-10-28
summary: Real didgeridoo shapes, recordings and 3D files, free to use.
---

# Didge Archive - an open collection of didgeridoos

The sound of a didgeridoo is determined almost entirely by the shape of its inside. Two instruments that look alike from the outside can sound completely different. To study this, you need real instruments, so we published the [Didge Archive](https://github.com/Didgitaldoo/didge-archive).

## What is in it?

For each didgeridoo, the archive can contain:

* the **bore geometry**: the inner diameter at every point along the length, as a simple JSON list of `[position, diameter]` points in millimetres
* **sound recordings**: a neutral drone, the same drone with the hand at the bell open and closed, and a short song
* **3D files** (STL and Blender) so you can print the didgeridoo yourself
* photos and a short description

At the moment there are nine instruments, among them Malveira, Arusha, Nazare, Kizimkazi and the Open Didgeridoo by Andrea Ferroni. Both straight didgeridoos and saxodidges, which are bent back on themselves like a saxophone, are included.

## Why?

I started the collection to evaluate my work on [DidgeLab](https://github.com/Didgitaldoo/didge-lab). To judge whether a simulated didgeridoo is any good, I need real instruments to compare against: measured shapes and real recordings. The geometry format is the one DidgeLab reads and writes, so you can load any archive geometry there directly.

The archive is useful for makers who want proven shapes as a starting point, players who want to hear an instrument before building it, and researchers working on acoustics, simulation or machine learning for instrument design.

## License and contributing

The data is licensed under CC BY-NC-SA 4.0. The Open Didgeridoo entries keep the license of their original design.

Contributions are very welcome. If you have a didgeridoo with a measured shape and a recording, fork the repository, add your files and the index entry, and open a pull request. The details are in the [README](https://github.com/Didgitaldoo/didge-archive).

You can also browse some of the instruments in our [didge database](/didge-database.html).
