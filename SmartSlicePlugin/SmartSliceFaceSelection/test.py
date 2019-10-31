# test.py (FaceSelection)
# Teton Simulation
# Authored on   October 31, 2019
# Last Modified October 31, 2019

#
# Contains Test Cases for FaceSelection submodule
#

# System
import sys, os
sys.path.append('/usr/lib/python3')
sys.path.append(os.getcwd())

# CGAL
import CGAL
from CGAL.CGAL_Kernel import Point_3
from CGAL.CGAL_Kernel import Vector_3

# Local
from FaceSelection import FaceSelection, SelectableFace, NormalVector


faces  = []
points = []

#  Define Vertices of Regular Cube
p1 = Point_3(0, 0, 0)
p2 = Point_3(1, 0, 0)
p3 = Point_3(0, 1, 0)
p4 = Point_3(0, 0, 1)
p5 = Point_3(1, 1, 0)
p6 = Point_3(1, 0, 1)
p7 = Point_3(0, 1, 1)
p8 = Point_3(1, 1, 1)


# Bottom Face
sface = SelectableFace([p1, p2, p3], NormalVector(p1, p2, p3))  
faces.append(sface)

# Top Face
sface = SelectableFace([p4, p6, p7], NormalVector(p4, p6, p7))  
faces.append(sface)

# Left Face
sface = SelectableFace([p1, p2, p3], NormalVector(p1, p2, p4))  
faces.append(sface)

# Right Face
sface = SelectableFace([p1, p2, p3], NormalVector(p3, p5, p7))  
faces.append(sface)

# Front Face
sface = SelectableFace([p2, p5, p6], NormalVector(p2, p5, p6))  
faces.append(sface)

# Back Face
sface = SelectableFace([p1, p3, p4], NormalVector(p1, p3, p4))  
faces.append(sface)


fs = FaceSelection(faces)

fs.select_face(fs.getFace(2)) #  Should report LEFT FACE

fs.selected_faces[0].printDetails()
