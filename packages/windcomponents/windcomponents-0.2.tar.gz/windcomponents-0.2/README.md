# windcomponents
Python library for calculation of aircraft cross- and tailwind components on a runway.

Example:

Analysis of cross- and tailwind components on a runway based on airport METAR data.

1. Consider that the runway orientation (99% of the cases) is reference to magnetic north, while METAR wind data is reference to true north.
2. Apply magnetic variation (inclination) to convert runway heading relative to true north:
True runway heading = magnetic runway heading - variation west --> The pilots among us will rmember "variation west, magnetic best" (so magnetic is the larger number)
True runway heading = magnetic runway heading + variation east --> The pilots among us will rmember "variation east, magnetic least" (so magnetic is the smaller number)
3. For consistency, round the runway heading (relative true north) to the nearest 10 degrees, as METAR wind data is also rounded to nearest 10 degrees

Status of the library: still very conceptual, no guarantee, no liability as per license.
