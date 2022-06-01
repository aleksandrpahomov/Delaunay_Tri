import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri
import matplotlib.collections
from delaunay import Delaunay

if __name__ == '__main__':
    numPoints = 50
    radius = 1000
    points = radius * np.random.random((numPoints, 2))
    print("points:\n", points)

    center = np.mean(points, axis=0)
    dt = Delaunay(center, 50 * radius)

    # Insert all points one by one
    for s in points:
        dt.addPoint(s)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    plt.axis([-100, radius+100, -100, radius+100])
    plt.grid(True)

    x_coords, y_coords = zip(*points)
    dt_tris = dt.exportTriangles()
    ax.triplot(matplotlib.tri.Triangulation(x_coords, y_coords, dt_tris), 'bo--')
    plt.show()


    
