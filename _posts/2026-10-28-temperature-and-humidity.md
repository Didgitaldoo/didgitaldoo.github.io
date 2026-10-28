---
layout: default
title: Temperature and humidity in DidgeLab
date: 2026-10-28
summary: How DidgeLab now accounts for the warm, moist air inside a didgeridoo.
---

# Temperature and humidity in DidgeLab

A didgeridoo does not sound the same on a cold winter day and in a warm room. The pitch of a didgeridoo depends on the speed of sound in the air inside the tube, and that depends on temperature and humidity. Until now, DidgeLab simulated dry air. It now models moist air, so you can simulate the conditions you actually play in.

## What changed

The simulation needs three properties of the air: its density, its dynamic viscosity and the speed of sound. DidgeLab used to compute them for dry air from the temperature alone. The new function `compute_moist_air_properties(temp_celsius, rel_humidity, pressure_pa)` takes the humidity into account:

* **Water vapor pressure** is estimated from the temperature with the Tetens formula. The relative humidity then tells us how much of the air is water vapor.
* **Density** is the sum of the contributions of dry air and water vapor. Water vapor is lighter than air, so moist air is slightly less dense.
* **Speed of sound** is computed for dry air first and then corrected for the vapor content. Moist air has a slightly higher speed of sound, and so does warmer air.
* **Viscosity** still uses Sutherland's law for dry air. The influence of humidity on it is below 0.5%, so we ignore it.

The defaults are 28 °C and a relative humidity of 100%, because the air inside a didgeridoo is mostly the breath of the player: warm and saturated. These constants are now used whenever you do not pass your own.

## How to use it

```python
from didgelab import acoustical_simulation, Geo, get_log_simulation_frequencies, \
    compute_moist_air_properties

constants = compute_moist_air_properties(temp_celsius=20, rel_humidity=0.5)
impedance = acoustical_simulation(geo, frequencies, constants=constants)
```

We also added an example notebook, [temperature_and_humidity.ipynb](https://github.com/Didgitaldoo/didge-lab/blob/main/doc/examples/temperature_and_humidity.ipynb). It simulates the same didgeridoo for a grid of temperatures and humidities and shows the fundamental frequency as a heatmap.

The changes are in these commits: [moist air model](https://github.com/Didgitaldoo/didge-lab/commit/4a8936fa0e060076495d51ae943445487f2b899f) and [documentation](https://github.com/Didgitaldoo/didge-lab/commit/e622cb1a8bc94621303983308f235523d5e3b0fa).
