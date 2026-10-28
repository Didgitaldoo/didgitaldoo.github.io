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

## How much does it matter?

The resonant frequencies of a tube are proportional to the speed of sound. A change of the speed of sound therefore shifts all resonances by the same musical interval. In cent (100 cent are one semitone) this is `1200 * log2(c2 / c1)`. With the formulas above we get these speeds of sound:

| Temperature | 0% humidity | 50% humidity | 100% humidity |
| --- | --- | --- | --- |
| 10 °C | 337.6 m/s | 337.9 m/s | 338.2 m/s |
| 20 °C | 343.5 m/s | 344.1 m/s | 344.7 m/s |
| 28 °C | 348.1 m/s | 349.2 m/s | 350.2 m/s |
| 35 °C | 352.2 m/s | 353.7 m/s | 355.3 m/s |

This results in the following shifts:

* **Temperature:** Every degree Celsius raises the pitch by about 3.5 cent. Between 20 °C and 30 °C at 100% humidity, the resonances move up by about 34 cent, a third of a semitone.
* **Humidity:** Going from dry air to saturated air raises the pitch by about 3 cent at 10 °C, 6 cent at 20 °C, 10 cent at 28 °C and 15 cent at 35 °C. The warmer the air, the more water vapor it can carry, so humidity matters more.
* **Both together:** A didgeridoo that is tuned with dry air of 20 °C is about 34 cent higher when it is played with the saturated breath of 28 °C. Between dry air at 10 °C and saturated air at 35 °C, the difference is about 88 cent.

These numbers are computed from the speed of sound alone. In the full simulation, density and viscosity change slightly as well, so the exact shift can differ a little from case to case. The example notebook shows the effect for a concrete didgeridoo.

Differences of a few cent are hardly audible, but 30 cent or more are. This is why it is a good idea to simulate with the temperature at which you want to play, and why a didgeridoo that is perfectly in tune with your drone in a warm room can sound flat in a cold one.
