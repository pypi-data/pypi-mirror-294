# windcomponents
Python library for calculating aircraft cross- and tailwind components on a runway.

# Example Case Study - Input Data:
Before using the lib, prepare your input data:

1. Consider that the runway orientation (99% of the cases) is reference to magnetic north, while wind data (e.g. from airport METAR) is reference to true north.
2. Hence, apply magnetic variation (inclination) to convert the runway heading to true north reference:
```python
True runway heading = magnetic runway heading - variation west --> Pilot rule of thumb "variation west, magnetic best" (so magnetic is the larger number).
True runway heading = magnetic runway heading + variation east --> Pilot rule of thumb "variation east, magnetic least" (so magnetic is the smaller number).
```
3. For consistency with METAR data, round the runway heading (now relative to true north) to the nearest 10 degrees, as METAR wind data is also rounded to the nearest 10 degrees.
4. Now that you have the runway heading/orientation relative to true north, you can apply it in the windcomponents lib


# Code Example:
```python
import pandas
from windcomponents import RunwayWindComponents

runway_direction_true_north_rounded = 10
# compass direction (and ref. to true north), NOT RWY designator! So eg RWY 01 should be inserted as 10, RWY10 as 100, RWY 09 as 90, RWY27 as 270, etc!

cross_tail_wind_directions = RunwayWindComponents(runway_direction_true_north_rounded)
# call outside of for-loop, since rwy cross/tail/headwind sectors only need to be calculated once - RWY heading is fixed obviously

for wind_direction, wind_speed in zip(df['wind_direction_true_north'], df['windspeed_kts']):
# assumes you have a pandas df with METAR observations, where for each observation row with a wind direction and speed, you want to calculate the pertaining cross-, tail- and headwind components on the runway
    wind_direction = int(wind_direction)
    wind_speed = int(wind_speed)
    
    crosswind_angle, crosswind_speed, tailwind_speed, headwind_speed = RunwayWindComponents.calculate_cross_tail_head_wind(cross_tail_wind_directions, wind_direction, wind_speed)
```

# Status of the Lib:
Initial tests passed, but still conceptual, refer to license. Crosscheck outcomes for your dataset with tools like: https://aerotoolbox.com/crosswind/ (Not affiliated in any sense).
