from svg.path import parse_path
from xml.dom import minidom
from path import Path
from vector import Vector
import cmath
import re

class Reader:
    def __init__(self, n, upr, width, height, path_width):
        self.n = n # Number of circles
        self.upr = upr # Number of updates per rotation
        self.path_width = path_width # width of the trace/path
        self.offset = complex(width/2, height/2) # Offset to make drawing appear in the middle of the screen

    def read_svg(self, file):
        # Read an SVG, and return the paths wih computed vectors
        document = minidom.parse(file) # Open and parse SVG file

        # find all path strings, and their fill(color) styling.
        # paths_info: [[path, color]...]
        paths_info = [[parse_path(p.getAttribute('d')), re.findall("(?<=fill:)([^;]*)", p.getAttribute('style'))[0]] for p in document.getElementsByTagName('path')]
        document.unlink()

        return self.create_paths(paths_info)

    def average_point(self, list):
        return complex(sum(list).real/len(list), sum(list).imag/len(list)) # Average of list of complex numbers
    def points(self, path):
        return [path[0].point(t/self.upr) for t in range(self.upr)] # Points along an SVG path object

    def create_paths(self, paths_info):
        paths = [] # List of path objects containing the calculated vectors for that path


        # Compute the average point of the drawing, and the average point for each path
        points = []
        for path in paths_info:
            avg_point = self.average_point(self.points(path))
            path.append(avg_point)
            points.append(avg_point)

        self.avg_point = self.average_point(points)


        # Create a set of points around the drawing, evenly spread. These are the starting positions of the different path arms
        radius = 300
        points = [radius * cmath.exp( 1j * 2 * cmath.pi * x/len(paths_info)) for x in range(1, 1 + len(paths_info))]
        for i in range(len(paths_info)):
            path = paths_info[i]
            path[2] = path[2] - self.avg_point

            # Select point
            lst = {abs(points[index] - path[2]): index for index in range(len(points))}
            index = lst[min(lst)]
            startpoint = points[index]
            points.pop(index)

            # Calculate vectors
            vectors = self.calculate_vectors(path[0], path[2], startpoint)
            # Create path objects
            paths.append(Path(vectors, self.offset + startpoint, path[1], self.path_width))

        return paths

    def calculate_vectors(self, path, path_avg_point, path_arm_offset):
        dt = 1.0 / self.upr

        vectors = []
        # find starting positions for each of the vectors
        for c in range(self.n):
            c -= (self.n-1)/2
            sum_points = 0
            for time in range(self.upr):
                t = dt * time
                sum_points += (path.point(t) - self.avg_point - path_arm_offset) * cmath.exp( -c * 2 * cmath.pi * complex(0,1) * t) * dt

            vectors.append(Vector(c, sum_points))
        return vectors
