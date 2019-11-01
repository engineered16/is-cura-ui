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
from FaceSelection import FaceSelection
from Detessellate import detessellate
from Facet import SelectableFace, NormalVector

tris  = []
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
sface0 = SelectableFace([p1, p2, p4], NormalVector(p1, p2, p4))
sface1 = SelectableFace([p2, p4, p6], NormalVector(p2, p4, p6))
tris.append(sface0)
tris.append(sface1)

# Top Face
sface0 = SelectableFace([p3, p5, p8], NormalVector(p3, p5, p8))
sface1 = SelectableFace([p3, p7, p8], NormalVector(p3, p7, p8))
tris.append(sface0)
tris.append(sface1)

# Left Face
sface0 = SelectableFace([p1, p3, p4], NormalVector(p1, p3, p4))
sface1 = SelectableFace([p3, p4, p7], NormalVector(p3, p4, p7))
tris.append(sface0)
tris.append(sface1)

# Right Face
sface0 = SelectableFace([p2, p5, p6], NormalVector(p2, p5, p6))
sface1 = SelectableFace([p5, p6, p8], NormalVector(p5, p6, p8))
tris.append(sface0)
tris.append(sface1)

# Front Face
sface0 = SelectableFace([p4, p7, p6], NormalVector(p4, p7, p6))
sface1 = SelectableFace([p7, p8, p6], NormalVector(p7, p8, p6))
tris.append(sface0)
tris.append(sface1)

# Back Face
sface0 = SelectableFace([p1, p2, p3], NormalVector(p1, p2, p3))
sface1 = SelectableFace([p2, p3, p5], NormalVector(p2, p3, p5))
tris.append(sface0)
tris.append(sface1)


fs = FaceSelection(tris)


fs.select_face(fs.getFace(2)) #  Should report LEFT FACE

fs.selected_faces[0].printDetails()

