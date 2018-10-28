import os
from pdb import pdb
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri
from scipy.spatial import Delaunay
from scipy.spatial import ConvexHull
import numpy as np
import matplotlib.animation as animation

def getSlices(point_cloud, slice_thickness):
    '''
    Takes in a point cloud and generates 2d slices, flattened
    based on the slice thickness.
    '''

    # XY plane, slice thru the Z

    plane_points = []
    # get min & max
    min_z = np.amin(point_cloud[:,2])
    max_z = np.amax(point_cloud[:,2])

    slice_pos = min_z - slice_thickness

    while slice_pos < max_z:
        slice_pos += slice_thickness

        plane_i = np.where((point_cloud[:,2] > slice_pos) & (point_cloud[:,2] < slice_pos+slice_thickness))
        slice_points = np.stack([point_cloud[i] for i in plane_i])
        plane_points.append(slice_points[0][:,[0,1]])

    return plane_points


def findHull(point_cloud):
    hull = ConvexHull(point_cloud)
    shell = np.stack([hull.points[i] for i in hull.vertices])

    return shell
    
def createMesh(points):
    tri = Delaunay(points)
    return tri

if __name__ == '__main__':
    a = pdb()
    a.parsePDB(os.path.join('test', '1fjg.pdb'))
    # hull = findHull(a.np_points)
    # tri = createMesh(hull)

    # hijacking this just to look at
    a_slice = getSlices(a.np_points, 2.0)

    for idx, layer in enumerate(a_slice):
        x = layer[:,0]
        y = layer[:,1]
        plt.scatter(x, y, s=0.1)
        plt.xlim(0, 300)
        plt.ylim(0, 200)
        plt.savefig(os.path.join('imgs','%i.png' % idx))
        plt.clf()

    # for plotting hull points
    # tri_x = tri.points[:,0]
    # tri_y = tri.points[:,1]
    # tri_z = tri.points[:,2]
    # ax.scatter(tri_x, tri_y, tri_z, s=0.1)

    #for plotting surface points
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1, projection='3d')
    # ax.plot_trisurf(tri_x, tri_y, tri_z, triangles=tri.simplices, cmap=plt.cm.Spectral)

    # plt.show()
