# test.py
# Teton Simulation
# Authored on   October 29, 2019
# Last Modified October 29, 2019

#
# Automated test script for FaceDetection Library
#


import sys, os
sys.path.append('/usr/lib/python3.7')
sys.path.append(os.getcwd())

#  CGAL Imports
import CGAL
from CGAL.CGAL_Kernel import Point_3
from CGAL.CGAL_Kernel import Vector_3

#  Face Detection Imports
from FaceDetection import FaceDetection, PointWithNormal, FaceWithNormal


print ("CHECK 1: PointWithNormal\n")

#  Define 8 Points that make a cube
p1   = Point_3(0, 0, 0)
v1   = Vector_3(-1, -1, -1)
pwn1 = PointWithNormal(p1, v1)

p2 = Point_3(1, 0, 0)
v2 = Vector_3(1, -1, -1)
pwn2 = PointWithNormal(p2, v2)

p3 = Point_3(1, 1, 0)
v3 = Vector_3(1, 1, -1)
pwn3 = PointWithNormal(p3, v3)

p4 = Point_3(0, 1, 0)
v4 = Vector_3(-1, 1, -1)
pwn4 = PointWithNormal(p4, v4)

p5 = Point_3(0, 0, 1)
v5 = Vector_3(-1, -1, 1)
pwn5 = PointWithNormal(p5, v5)

p6 = Point_3(1, 0, 1)
v6 = Vector_3(1, -1, 1)
pwn6 = PointWithNormal(p6, v6)

p7 = Point_3(1, 1, 1)
v7 = Vector_3(1, 1, 1)
pwn7 = PointWithNormal(p7, v7)

p8 = Point_3(0, 1, 1)
v8 = Vector_3(-1, 1, 1)
pwn8 = PointWithNormal(p8, v8)

#  Put into List
pwns = [pwn1, pwn2, pwn3, pwn4, pwn5, pwn6, pwn7, pwn8]  #  CUBE
#pwns = [pwn1, pwn2, pwn3, pwn6]                         #  TETRAHEDRON
 
print ("CHECK 2: FaceWithNormal\n")

#points_neg_z = [pwn1, pwn2, pwn3, pwn4]
#normal_neg_z = (0, 0, -1)

#face = FaceWithNormal(points_neg_z)


print ("CHECK 3: FaceDetection\n")

#  Create new FaceDetection object from the cube's PointWithNormals
fd = FaceDetection(pwns)

#  Detect Faces
fd.detect()

#  Report Findings
print (str(fd.count()) + " shapes found\n")


print ("Shape 1:\n")
fd.getShape(0).printDetails()


