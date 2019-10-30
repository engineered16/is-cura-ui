# StlReader.py
# Teton Simulation
# Authored on   October 29, 2019
# Last Modified October 29, 2019


import sys, os
sys.path.append('/usr/lib/python3.7')
sys.path.append(os.getcwd())

import CGAL

from CGAL.CGAL_Kernel import Point_3
from CGAL.CGAL_Kernel import Vector_3

from bitstream import *
from numpy import int16, int32, uint32

from FaceDetection import FaceWithNormal

import struct


class StlReader:
    def __init__(self, filename):
        self._file = open(filename, "rb")
        self._tris = 0
        self._extracted_shapes = []

    def readFile(self):
        data = self._file.read()
        stream = BitStream(data)
        stream.read(bytes, 80)  #  Ignore 80 Character Heading

        # Number of Triangles
        self._tris = int(stream.read(int32, 1))
        print ("# of Triangles: " + str(self._tris))

        #  For Each Triangle
        for _triangle in range(0, self._tris):
            #  Read Normal Vector
            x = float(stream.read(uint32, 1))
            y = float(stream.read(uint32, 1))
            z = float(stream.read(uint32, 1))
            norm = Vector_3(x, y, z)

            #  Read Vertex One
            x = float(stream.read(uint32, 1))
            y = float(stream.read(uint32, 1))
            z = float(stream.read(uint32, 1))
            p1 = Point_3(x, y, z)

            #  Read Vertex Two
            x = float(stream.read(uint32, 1))
            y = float(stream.read(uint32, 1))
            z = float(stream.read(uint32, 1))
            p2 = Point_3(x, y, z)

            #  Read Vertex Three
            x = float(stream.read(uint32, 1))
            y = float(stream.read(uint32, 1))
            z = float(stream.read(uint32, 1))
            p3 = Point_3(x, y, z)

            #  Read Attribute Byte Count
            attr = int(stream.read(int16, 1))

            verts = [p1, p2, p3]
            
            fwn = FaceWithNormal(verts, norm)
            fwn.printDetails()

            self._extracted_shapes.append(FaceWithNormal(verts, norm))



##  TESTING
s = StlReader("test.stl")

s.readFile()

