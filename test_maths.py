# here we shall test some maths
import sys
import numpy as np
from vectors import Point, Vector
# z = int(sys.argv[1])
#
# # static points for testing
# x0, y0, z0 = [2,-1,3]
# x1, y1, z1 = [1,4,-3]
#
# dx = x0 - x1
# dy = y0 - y1
# dz = z0 - z1
#
# # equation 1:
# y = y0 + ((z - z0) / dz) * dy
#
# # equation 2:
# x = (dx / dy) * (y - y0) - x0

def getNewFace(v1, v2, v3, z_cut):
    #takes in 3 verticies, and a z-cutoff
    #returns value of new vert positions
    #currently only for the two below the z case
    safe_v = []
    cut_v = []
    for i in [v1, v2, v3]:
        if i[2] >= z_cut:
            safe_v.append(i)
        else:
            cut_v.append(i)

    if len(safe_v) == 1:
        #we are going down from the pivot point, which is why
        #the x values need to be made negative, i think.
        #I'll have to work this out on paper to be sure...
        v_pivot = safe_v[0]
        new_verts = []

        #first line
        x0, y0, z0 = v_pivot
        x1, y1, z1 = cut_v[1]

        dx = x0-x1
        dy = y0-y1
        dz = z0-z1

        y = y0 + ((z_cut - z0) / dz) * dy
        x = (dx / dy) * (y - y0) - x0
        new_verts.append([-x,y,z_cut])

        #second line
        x0, y0, z0 = v_pivot
        x1, y1, z1 = cut_v[0]

        dx = x0-x1
        dy = y0-y1
        dz = z0-z1

        y = y0 + ((z_cut - z0) / dz) * dy
        x = (dx / dy) * (y - y0) - x0
        new_verts.append([-x,y,z_cut])

        new_verts.append(v_pivot)

        print(new_verts)

def getFaceNormal(p1, p2, p3):
    v1 = Vector.from_points(p1, p2)
    v2 = Vector.from_points(p1, p3)

    c = v1.cross(v2)
    normal_c = c.multiply(1/c.magnitude())

    print(normal_c)

if __name__ == '__main__':
    v1 = [-10.1, 20.0, -4.0]
    v2 = [0.0, 2.0, 10.0]
    v3 = [10.0, 20.0, -4.0]
    z_cut = 3.0
    # getNewFace(v1, v2, v3, z_cut)
    p1 = Point.from_list(v1)
    p2 = Point.from_list(v2)
    p3 = Point.from_list(v3)

    getFaceNormal(p1,p2,p3)
