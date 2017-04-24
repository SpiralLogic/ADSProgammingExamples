# 3D Polyline Optimisation

This program takes in a set of 3D coordinates and finds the optimal path to span from the first point to the last

The points are plotted using the Matplotlib library

What determines an optimal path is described in the PDF provided

# Complexities

Complexity is O(N^3)

every iteration of N where N is the number of points
it needs to go through all previously calculated points and work out
the new optimal path and the line_segment_cost for that point

For each point P in N:
    (calculation of the optimal path to point P happens here)
    For every previous point Q:
        (calculation of perpendicular line segment costs for point Q happens here)
        For every point R in between the point P and point Q
            (A single perpendicular distance is calculated for R to P and Q here)

For example when the Nth point is calculated to the first point, It will need to calculate
the perpendicular distance of every point between the first and N. It will then need to calculate
the next point to the Nth point and so on


By the last calculation there will be N Ps, (N-1) Qs and (N-1) Rs

There are 3 nested loops which depend on N, which gives a space complexity of O(N^3)

There is also an additional O(N) time to create the final optimal path but this cost
is negligible compared to (N^3)


For each point in a set of points of size N except for the first and last points there are 2
possibilities, that the endpoint is included in the polyline summary or not included.

All of the combinations of these possibilities for N endpoints =

1 * 2 * 2 ..... * 2 * 1

1 * (2^(N-2)) * 1

if we assume that N is the number of points, and we need at least 2 points to find a path

number of possible paths = 2^(N - 2) where n > 1

in other words each new endpoint in a set of points will have a new possible path
from all of the previous possible path endpoints.

Space Complexity
----------------
O(N)