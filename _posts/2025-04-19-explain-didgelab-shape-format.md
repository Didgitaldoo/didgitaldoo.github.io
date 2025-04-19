---
layout: default
title: Explaining the Didgelab shape format
date: 2025-04-19
summary: This article explains how to format a Didgeridoo shape in Didgelab.
---

# Explaining the Didgelab shape format

A didgelab shape is a list of segments. Each segment is a pair of numbers; the first number in a segment is the distance from the mouth piece, the second is the diameter of the didgeridoo (the inner diameter) at that point. The unit is mm. So, for example, the pair `0 32` means that the didgeridoo has a diameter of 32mm at the mouthpiece.

Lets describe a cylindrical didgeridoo that has a length of 1.50m and a constant diameter of 40mm:

```
0 40
1500 40
```

Next, lets add a bell of length 200mm and a bell diameter of 90mm to that cylindrical didgeridoo:

```
0 40
1500 40
1700 90
```

Didgelab internally uses JSON to encode these lists. JSON is a dataformat that is easier to read for machines. Above Didgeridoo will look like this in JSON:

```
[[0,40], [1500, 40], [1700, 90]]
```