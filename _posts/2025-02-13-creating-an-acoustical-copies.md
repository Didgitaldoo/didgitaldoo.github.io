---
layout: default
title: Creating an acoustical copy of a Didgeridoo
date: 2025-02-13
---

## Creating an acoustical copy of a Didgeridoo

The first question that I wanted to solve with Didgelab was: How can I find a Didgeridoo geometry or shape that can produce certain impedance and sound spektra. So I want a Didgeridoo with this and that property and then the software computes a shape that produdces these properties. After a while this worked and I built the first Didgeridoos. They had exactly the sonic properties I wanted, but they sounded boring. So my second question was: Which sound- or impedance spectrum sounds good?

Frank Geipel mentioned the method of the acoustical copy **PUT LINK HERE**. So I looked on Youtube for a didgeridoo with a sound that I like very much and found this black eucalyptus didgeridoo **PUT LINK HERE**. After some data science magic I created the Malveira didge. Here is the original sound sample and the sound sample that it produced:

**PUT SOUND SAMPLES HERE**

Here is a more technical explanation of the acoustical copy method:

1. Find a nice sound sample of a didgeridoo.
2. Cut a short segment of about one second with the didgeridoo only. Generally I am looking for a constant "o" sound on the didgeridoo that has no rhythm and does not change. A constant drone sound makes sense. The "o" sound is more intuitive then sensible, it would probably work with any vocal.
3. Compute an FFT analysis of that sample to convert that sample into a sound spektrum.
4. Compute peaks of that sound spektrum.
5. Use didgelab to find a didgeridoo shape that has the same peaks in the sound spektrum.

Here are the source codes that produce the acoustical copy.

**ADD LINKS**