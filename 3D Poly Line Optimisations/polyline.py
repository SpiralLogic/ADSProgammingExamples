"""
@author: Sol Jennings 26356015
@created: 2016-04-03
@description:

FIT2004 Prac 6

Will calculate and plot the optimal cost and optimal path for a 3D set of points.

To calculate the optimal path for a point summary run:

python polyline.py [filename]

e.g.
python polyline.py points_file1.txt

"""

import sys


class Point:
    def __init__(self, coords):
        """
        Object for storing the cost and the optimal path to a particular point

        :param cost: The cost to the point
        :param path: The optimal previous point to this point
        """
        self.coords = coords
        self.cost = None
        self.path = None

    def __str__(self):
        """
        Represent the optimal path as a string

        :return: string
        """
        return "Point " + str(self.coords) + "\n Cost:" + str(self.cost) + "\n Path: " + str(
            self.path)


class PolyLineSummary:
    def __init__(self):
        """
        Class for determining the optimal path summary in 3D
        """
        self.points = []

    def read_file(self, filename):
        """
        Read in a file containing coordinates for points represented in 3D space

        Note: As each new line is the optimal path to that line is calculated. If this calculation
        was done in a separate step it would add another iteration of the input values N, 1
        when reading in and 1 when calculating the optimal cost and path

        :param filename: The filename containing the coordinates
        """
        file = open(filename)

        # Store each point as a tuple of (x,y,z) coordinates
        for line in file:
            line = line.strip()
            point = line.strip().split()
            if len(point) != 3:
                raise ValueError("Invalid point summary file")
            point = Point((float(point[0]), float(point[1]), float(point[2])))

            # Add the point to the list
            self.points.append(point)

            # Calculate the optimal to the new point
            self.calc_optimal_for_point(len(self.points) - 1)

    def distance_between_points(self, point1, point2):
        """
        Calculate the distance between 2 points in 3D space. The point parameters are given as
        integers and the point coordinates are taken from self.points

        :param point1: int first point
        :param point2: int second point
        :return: float distance between 2 points
        """
        point1 = self.points[point1].coords
        point2 = self.points[point2].coords

        if len(point1) != len(point2):
            raise ValueError("Point 1 and Point 2 dimensions don't match")

        """
        Length is calculated using
        length = ((x1-x2)^2 + (y1-y2)^2 + (z1-z2)^2)^.5
        """
        length = 0
        for i in range(len(point1)):
            length += (point1[i] - point2[i]) ** 2

        return length ** .5

    def perp_line_distance(self, line_seg_start, line_seg_end, point, line_seg_length):
        """
        Calculate the perpendicular distance of a point to a line connected by 2 points

        :param line_seg_start:  line segment start point
        :param line_seg_end:   line segment end point
        :param point:  point to find perpendicular distance from
        :param line_seg_length: float The length of the line segment
        :return:  the perpendicular distance
        """

        """
        length_b is the length from the end of the line segment to the point
        length_c is the length from the start of the line segment to the point
        """

        length_b = self.distance_between_points(line_seg_end, point)
        length_c = self.distance_between_points(line_seg_start, point)

        """
        Using Heron's formula to find the area of the triangle. Where a b and c are the
        lengths of the sides of a triangle.
        A = .25 (4 * a^2 * b^2 - (a^2 + b^2 - c^2)^2)
        """

        part_a = line_seg_length ** 2 * length_b ** 2
        part_b = (line_seg_length ** 2) + (length_b ** 2) - (length_c ** 2)
        part_b **= 2

        if 4 * part_a < part_b:
            raise ValueError("Trying to use imaginary numbers!")
        area = .25 * ((4 * part_a - part_b) ** .5)

        """
        A = (1/2)B*H
        H = 2*A/B
        """
        distance = (area * 2) / line_seg_length

        return distance

    def line_segment_cost(self, point1, point2):
        """
        Calculate the cost between 2 points

        :param point1: point 1
        :param point2: point 2
        :return: line segment cost
        """
        if point1 >= point2:
            raise ValueError("Point1 must be less than Point2")
        if point1 >= len(self.points) or point2 >= len(self.points):
            raise IndexError("Points are out of range")

        line_seg_length = self.distance_between_points(point1, point2)
        sum_of_perp_distances = 0

        # Find the sum of the perpendicular distances from point1 + 1 to point2 - 1
        for i in range(point1 + 1, point2):
            # Line segment length is passed so that it isn't calculated on every iteration
            sum_of_perp_distances += self.perp_line_distance(point1, point2, i, line_seg_length)

        cost = 2 * line_seg_length + sum_of_perp_distances

        return cost

    def calc_optimal_for_point(self, point):
        """
        Calculate the optimal cost for a point.

        Precondition is that all of the previous points have had their optimal paths calculated

        :param point: point to calculate the optimal cost for
        :return: float the optimal cost for the point, list of the optimal path
        """

        # Base Case: first point will always have a cost of 0 and be the only endpoint in it's path
        if point == 0:
            self.points[0].cost, self.points[0].path = 0.0, 0
            return self.points[0].cost, self.points[0].path

        # Find the cost to the previous point
        optimal_point = point - 1
        optimal_cost = self.points[optimal_point].cost
        optimal_cost += self.line_segment_cost(optimal_point, point)

        # For all the remaining previous point calculate their costs
        for i in range(point - 2, -1, -1):
            optimal_cost_to_point = self.points[i].cost
            point_cost = self.line_segment_cost(i, point)
            next_cost = optimal_cost_to_point + point_cost

            # If the new cost is less than the current optimal cost, update the current optimal cost
            if next_cost < optimal_cost:
                optimal_cost = next_cost
                optimal_point = i

        # Store the optimal cost and optimal path for the point
        self.points[point].cost = optimal_cost
        self.points[point].path = optimal_point

        return optimal_cost, optimal_point

    def get_optimal_path(self):
        endpoint = len(self.points) - 1
        optimal_path = [endpoint]
        while endpoint > 0:
            endpoint = self.points[endpoint].path
            optimal_path.insert(0, endpoint)
        return optimal_path

    def get_optimal_polyline(self):
        """
        Get the optimal cost and path for all of points

        :return: the optimal cost and path for all of the points
        """
        if len(self.points) < 1:
            raise ValueError("Not a enough points to calculate")
        endpoint = len(self.points) - 1
        optimal_cost = self.points[endpoint].cost
        optimal_path = self.get_optimal_path()
        return optimal_cost, optimal_path

    def plot(self):
        """
        Plot all of the points and plot the optimal path
        """
        try:
            from mpl_toolkits.mplot3d import Axes3D
            import matplotlib.pyplot as plt
        except ImportError:
            print("\nMatplotlib library missing! Plotting skipped")
            return

        if len(self.points) < 2:
            raise IndexError("There aren't enough points to plot!")

        if self.points[1] is None:
            self.get_optimal_polyline()

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # plot a path between all of the points in order
        x, y, z = [], [], []
        for i in self.points:
            x.append(i.coords[0])
            y.append(i.coords[1])
            z.append(i.coords[2])
        ax.plot(x, y, z, c='r', marker='o')

        # plot the optimal path between all of the points
        optimal_path = self.get_optimal_path()
        x, y, z = [], [], []
        for i in optimal_path:
            x.append(self.points[i].coords[0])
            y.append(self.points[i].coords[1])
            z.append(self.points[i].coords[2])
        ax.plot(x, y, z, c='b', marker='o')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()


if __name__ == "__main__":
    """
    Take file as input from the user and process the polyline summary for it
    """
    if len(sys.argv) < 2:
        print("No point summary given")
        exit()

    ps = PolyLineSummary()
    try:
        ps.read_file(sys.argv[1])
        print("Calculating optimal cost and path for " + str(len(ps.points)) + " points")
        cost, path = ps.get_optimal_polyline()
        print("Optimal cost: ", cost)
        print("Optimal path: ", path)
        ps.plot()
    except IOError:
        print("Unable to open point summary file")
    except (ValueError) as e:
        print(e)

"""
2)

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

3)

For each point in a set of points of size N except for the first and last points there are 2
possibilities, that the endpoint is included in the polyline summary or not included.

All of the combinations of these possibilities for N endpoints =

1 * 2 * 2 ..... * 2 * 1

1 * (2^(N-2)) * 1

if we assume that N is the number of points, and we need at least 2 points to find a path

number of possible paths = 2^(N - 2) where n > 1

in other words each new endpoint in a set of points will have a new possible path
from all of the previous possible path endpoints.

4)


I modified my program for submission so that the path can be stored in N space.

This adds an iteration at the end of the calculation to retrieve the optimal path, but this is
probably a lot less costly than copying a list every time a new point is stored
"""
