import os

class pdb(object):
    def __init__(self):
        self.points = []
        self.title = 'None'

    def parseLine(self, line):
        units = line.split()

        if 'HEADER' in units[0]:
            self.header = units[1]
            self.date = units[2]
            self.id = units[3]
        
        if 'TITLE' in units[0]:
            # Extracts multi-part titles
            try:
                int(units[1])
                # if successful take the sentence after index 1
                self.title += ' ' + ' '.join(units[2:])
            except ValueError:
                self.title = ' '.join(units[1:])

        if 'ATOM' in units[0]:
            # get the 3d points [x, y, z]
            self.points.append([line[31:39], line[39:47], line[48:55]])

    def parsePDB(self, pdb_file):
        with open(pdb_file, 'r') as read_file:
            lines = read_file.readlines()

        for line in lines:
            self.parseLine(line)

if __name__ == "__main__":
    a = pdb()
    a.parsePDB(os.path.join('test', '1fjg.pdb'))

    print(a.points)