import numpy
import stl

from mpl_toolkits import mplot3d
from matplotlib import pyplot

figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

f = stl.mesh.Mesh.from_file('test/4ur0_render.stl')

axes.add_collection3d(mplot3d.art3d.Poly3DCollection(f.vectors))

scale = f.points.flatten(-1)
axes.auto_scale_xyz(scale, scale, scale)

pyplot.show()
