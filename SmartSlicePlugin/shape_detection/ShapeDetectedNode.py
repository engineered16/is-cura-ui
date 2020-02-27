from __future__ import print_function

# built-ins
import math

# Numpy
import numpy

# Cura/Uranium
from UM.Logger import Logger

# CGAL
from CGAL.CGAL_Kernel import Point_3
from CGAL.CGAL_Kernel import Vector_3
from CGAL.CGAL_Point_set_3 import Point_set_3
from CGAL.CGAL_Shape_detection import efficient_RANSAC


class ShapeDetectedNode():
    shape_index_name = "shape_index"

    def __init__(self, node):
        self.mesh = node.getMeshData()
        self._point_cloud = Point_set_3()  # Our set of surface points
        self._point_face = {}  # Needed to trace back the inliers to faces

    @property
    def point_cloud(self):
        if self._point_cloud.is_empty():
            self.generatePointCloud()
        return self._point_cloud

    def generatePointCloud(self):
        self._point_cloud.clear()
        self._point_cloud.add_normal_map()
        self._point_cloud.add_int_map(self.shape_index_name)
        self._point_face.clear()
        if not self.mesh.hasIndices():
            return self._point_cloud

        # Preparing data for every face
        face_ids = range(self.mesh.getFaceCount())
        Logger.log("d", "Processing {} faces.".format(len(face_ids)))
        for face_id in face_ids:
            vector_a, vector_b, vector_c = self.mesh.getFaceNodes(face_id)
            vector_centroid = (vector_a + vector_b + vector_c) / 3.0
            surface_point_to_centroid_weight = 0.5

            # Preparing our surface points on a face
            surface_point_a = (vector_centroid - vector_a) * \
                surface_point_to_centroid_weight
            surface_point_b = (vector_centroid - vector_b) * \
                surface_point_to_centroid_weight
            surface_point_c = (vector_centroid - vector_c) * \
                surface_point_to_centroid_weight

            normal_vector = numpy.cross(vector_b - vector_a,
                                        vector_c - vector_a
                                        )
            x, y, z = [float(entry) for entry in normal_vector.tolist()]
            normal = Vector_3(x, y, z)

            # Normalize vector as the direction matters only
            normal = normal / math.sqrt(normal.squared_length())

            for surface_point in (surface_point_a,
                                  surface_point_b,
                                  surface_point_c):
                x, y, z = [float(entry) for entry in surface_point.tolist()]
                point = Point_3(x, y, z)

                self._point_cloud.insert(point, normal)
                if face_id not in self._point_face.keys():
                    self._point_face[face_id] = ()
                self._point_face[face_id] += (surface_point, )

    def analysePointCloud(self, cloud=None):
        if not cloud:
            cloud = self.point_cloud

        Logger.log("d", "Running efficient_RANSAC...")
        shape_map = self._point_cloud.int_map(self.shape_index_name)
        shapes = efficient_RANSAC(self._point_cloud,
                                  shape_map,
                                  min_points=5,
                                  epsilon=1.,
                                  cluster_epsilon=1.2,
                                  normal_threshold=0.85,
                                  planes=True,
                                  cylinders=True,
                                  spheres=True,
                                  cones=True,
                                  tori=True
                                  )
        print(len(shapes), "shapes(s) detected, first 10 shapes are:")
        for s in range(min(len(shapes), 10)):
            print(" *", s, ":", shapes[s])

        # Counting types of shapes
        nb_cones = 0
        nb_cylinders = 0
        nb_planes = 0
        nb_spheres = 0
        nb_tori = 0
        for s in shapes:
            _type = s.split()[1]
            if _type == "cone":
                nb_cones += 1
            if _type == "cylinder":
                nb_cylinders += 1
            if _type == "plane":
                nb_planes += 1
            if _type == "sphere":
                nb_spheres += 1
            if _type == "torus":
                nb_tori += 1
        print("Number of shapes by type:")
        print(" *", nb_cones, "cone(s)")
        print(" *", nb_cylinders, "cylinder(s)")
        print(" *", nb_planes, "plane(s)")
        print(" *", nb_spheres, "sphere(s)")
        print(" *", nb_tori, "torus/i")

        for shape in shapes:
            print(shape)
        inliers_of_first_shape = Point_set_3()
        for idx in self._point_cloud.indices():
            if shape_map.get(idx) == 0:
                inliers_of_first_shape.insert(self._point_cloud.point(idx))
        print(inliers_of_first_shape.size(), "inliers(s) recovered")
