import os, sys

"""
Ed Yashin 04/14/2018

From the wrl file we are interested in :
Shape, geometry, IndexedFaceSet
    coord Coordinate, point
    normal Normal, vector

This module will take in a VRML 2.0 formatted file and return a (quite large)
stl of the mesh. There are some duplicate vertices... I don't really know
if that will cause any issues along the way, it seems to open in some pretty
basic mesh editing software so far so I am not worried yet.

"""

class wrlToStl():
    def __init__(self, wrl):
        self.wrl_file = open(wrl, 'r')
        self.basename = os.path.splitext(wrl)[0]
        self.vertices = []
        self.vert_normals = []
        self.face_normals = []

        self.parseWrl()
        self.writeStl()

    def getVertices(self):
        # get to the list of vertices
        while 1:
            skip_the_line = self.wrl_file.readline().split(' ')
            if 'point' in skip_the_line:
                break

        while 1:
            line = self.wrl_file.readline().split(' ')

            if ']\n' in line:
                break

            line[2] = line[2][0:-2] # cut off the gross ,\n
            self.vertices.append([float(i) for i in line[0:3]])

    def getNormals(self):
        # get to the normals
        while 1:
            skip_the_line = self.wrl_file.readline().split(' ')
            if 'vector' in skip_the_line:
                break

        # take up them normals
        while 1:
            line = self.wrl_file.readline().split(' ')

            if ']' in line:
                break

            line[2] = line[2][0:-2]
            self.vert_normals.append([float(i) for i in line[0:3]])

    def calculateFaceNormals(self):
        # calculate face normals
        for idx, v in enumerate(self.vert_normals):
            i = idx * 3
            try:
                v_x1 = self.vert_normals[i][0]
                v_y1 = self.vert_normals[i][1]
                v_z1 = self.vert_normals[i][2]

                v_x2 = self.vert_normals[i+1][0]
                v_y2 = self.vert_normals[i+1][1]
                v_z2 = self.vert_normals[i+1][2]

                v_x3 = self.vert_normals[i+2][0]
                v_y3 = self.vert_normals[i+2][1]
                v_z3 = self.vert_normals[i+2][2]
            except IndexError:
                break

            vf_x = (v_x1 + v_x2 + v_x3)/3
            vf_y = (v_y1 + v_y2 + v_y3)/3
            vf_z = (v_z1 + v_z2 + v_z3)/3

            self.face_normals.append([vf_x, vf_y, vf_z])

    def parseWrl(self):
        self.getVertices()
        self.getNormals()
        self.calculateFaceNormals()

    def writeStl(self):
        output = open('%s.stl' % self.basename, 'w')
        output.write('solid %s\n' % self.basename)
        print('Writing triangles...')

        for idx, face in enumerate(self.face_normals):
            vert_i = idx*3
            try:
                x1 = self.vertices[vert_i][0]
                y1 = self.vertices[vert_i][1]
                z1 = self.vertices[vert_i][2]

                x2 = self.vertices[vert_i+1][0]
                y2 = self.vertices[vert_i+1][1]
                z2 = self.vertices[vert_i+1][2]

                x3 = self.vertices[vert_i+2][0]
                y3 = self.vertices[vert_i+2][1]
                z3 = self.vertices[vert_i+2][2]

                xn = face[0]
                yn = face[1]
                zn = face[2]

                output.write(' facet normal %f %f %f\n  outer loop\n' % (xn,yn,zn))
                output.write('   vertex %f %f %f\n' % (x1, y1, z1))
                output.write('   vertex %f %f %f\n' % (x2, y2, z2))
                output.write('   vertex %f %f %f\n' % (x3, y3, z3))
                output.write('  endloop\n endfacet\n')

                sys.stdout.write('\rWritten facet # %d of %d' % (idx, len(self.face_normals)))
            except IndexError:
                break

        output.write('endsolid %s' % self.basename)
        print('\nThank you')

if __name__ == '__main__':
    wrl_file = sys.argv[1]

    if os.path.splitext(wrl_file)[1] != '.wrl':
        print('This is not a wrl file, I will not parse this.')
        sys.exit()

    wrlToStl(wrl_file)
