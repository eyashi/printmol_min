"""
Goal is to extract point cloud from a PDB file.
"""
import os
import matplotlib
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from pdb import pdb
import random

def downsample(points, percent):
    """
    To reduce the number of points for easier plotting and resolution settings.
    """
    num_points = len(points)
    points_to_keep = int(num_points*percent)

    index_array = random.sample(range(num_points), points_to_keep)

    ds_points = [points[i] for i in index_array]

    return ds_points

def plotTheDots(p_raw, ds_percent):
    """
    Takes points, an array of (x,y,z), and plots in 3d space.
    """
    p_raw_ds = downsample(p_raw, ds_percent)
    points = []
    for i in p_raw_ds:
        point = [0,0,0]
        for idx, coord in enumerate(i):
            try:
                point[idx] = float(coord)
            except ValueError:
                continue
        points.append(point)

    x = [i[0] for i in points]
    y = [i[1] for i in points]
    z = [i[2] for i in points]

    fig = pyplot.figure()
    ax = Axes3D(fig)

    ax.scatter(x, y, z, s=0.1)
    pyplot.show()

if __name__ == '__main__':
    parser = pdb()
    parser.parsePDB(os.path.join('test', '1fjg.pdb'))

    print('%s, incoming!' % parser.header)
    plotTheDots(parser.points)

