
import numpy as np
from math import sqrt, fabs


class Delaunay:
    def __init__(self, center=(0, 0), radius=9999):
        center = np.asarray(center)
        # Create coordinates for the corners of the frame
        self.coords = [center+radius*np.array((-1, -1)),
                       center+radius*np.array((+1, -1)),
                       center+radius*np.array((+1, +1)),
                       center+radius*np.array((-1, +1))]

        # Create two dicts to store triangle neighbours and circumcircles.
        self.triangles = {}
        self.circles = {}

        # Сreate two initial triangles
        T1 = (0, 1, 3)
        T2 = (2, 3, 1)
        self.triangles[T1] = [T2, None, None]
        self.triangles[T2] = [T1, None, None]

        # find circumcenters and radius
        for t in self.triangles:
            self.circles[t] = self.circumcenter(t)

    """
    func to compute circumcenter and squared radius for triangle
    """
    def circumcenter(self, tri):
        pts = np.asarray([self.coords[v] for v in tri])
        ax = pts[0][0]
        ay = pts[0][1]
        bx = pts[1][0]
        by = pts[1][1]
        cx = pts[2][0]
        cy = pts[2][1]
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
        uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
        center = (ux, uy)
        radius = np.sum(np.square(pts[0] - center))
        return (center,radius)

    """
     func to check if point inside circle
    """
    def inCircle(self, tri, p):
        center, radius = self.circles[tri]
        return np.sum(np.square(center - p)) <= radius

    """
    func add point in triangulation
    """
    def addPoint(self, p):
        p = np.asarray(p)
        idx = len(self.coords)
        self.coords.append(p)

        # Search the triangles whose circle contains p
        bad_triangles = []
        for T in self.triangles:
            #check if point inside tri
            if self.inCircle(T, p):
                bad_triangles.append(T)

        # Add edges of bad triangles which is not connected to other bad triangles to boundary ( polygon)
        boundary = []
        T = bad_triangles[0]
        edge = 0

        while True:
            # get the opposite triangle of this edge
            tri_op = self.triangles[T][edge]
            # Check if opposite tri is good or not
            if tri_op not in bad_triangles:
                # Insert edge and external triangle into boundary list
                boundary.append((T[(edge+1) % 3], T[(edge-1) % 3], tri_op))

                # change edge(step)
                edge = (edge + 1) % 3

                # if polygon is completed - break while loop
                if boundary[0][0] == boundary[-1][1]:
                    break
            else:
                #if oppositr tri is bad - go to the opposite tri for search
                edge = (self.triangles[tri_op].index(T) + 1) % 3
                T = tri_op

        #delete bad triangles from triangulation
        for T in bad_triangles:
            del self.triangles[T]
            del self.circles[T]

        # retriangulate polygon by adding new point
        new_triangles = []
        for (e0, e1, tri_op) in boundary:
            T = (idx, e0, e1)
            self.circles[T] = self.circumcenter(T)
            self.triangles[T] = [tri_op, None, None]
            if tri_op:
                # search the neighbour of tri_op that use edge (e1, e0)
                for i, neigh in enumerate(self.triangles[tri_op]):
                    if neigh:
                        if e1 in neigh and e0 in neigh:
                            # change link to use our new triangle
                            self.triangles[tri_op][i] = T
            new_triangles.append(T)
        # Link the new triangles each another
        N = len(new_triangles)
        for i, T in enumerate(new_triangles):
            self.triangles[T][1] = new_triangles[(i+1) % N]   # next
            self.triangles[T][2] = new_triangles[(i-1) % N]   # previous

    """
    func for export resulted triangles
    """
    def exportTriangles(self):
        return [(a-4, b-4, c-4)
                for (a, b, c) in self.triangles if a > 3 and b > 3 and c > 3]

    """
    func for export resulted circles
    """
    def exportCircles(self):
        return [(self.circles[(a, b, c)][0], sqrt(self.circles[(a, b, c)][1]))
                for (a, b, c) in self.triangles if a > 3 and b > 3 and c > 3]
