from __future__ import print_function

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
        self._point_face.clear()
        if not self.mesh.hasIndices():
            return self._point_cloud

        # Preparing data for every face
        for face_id in range(self.mesh.hasIndices()):
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

            for surface_point in (surface_point_a,
                                  surface_point_b,
                                  surface_point_c):
                numpy_point_as_double = surface_point.tolist()
                numpy_normal_as_double = normal_vector.tolist()

                point = Point_3(*numpy_point_as_double)
                normal = Vector_3(*numpy_normal_as_double)

                Logger.log("d", "numpy_point_as_double: {}".format(repr(numpy_point_as_double)))
                Logger.log("d", "numpy_normal_as_double: {}".format(repr(numpy_normal_as_double)))

                self._point_cloud.insert(point, normal)
                if face_id not in self._point_face.keys():
                    self._point_face[face_id] = ()
                self._point_face[face_id] += (surface_point,)

    def analysePointCloud(self, cloud=None):
        if not cloud:
            cloud = self.point_cloud

        shape_map = self._point_cloud.add_int_map("shape_index")
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
        print(len(shapes), "shapes(s) detected, first 3 shapes are:")
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
            if _type == "planes":
                nb_planes += 1
            if _type == "spheres":
                nb_spheres += 1
            if _type == "torus":
                nb_tori += 1
        print("Number of shapes by type:")
        print(" *", nb_cones, "cone(s)")
        print(" *", nb_cylinders, "cylinder(s)")
        print(" *", nb_planes, "planes(s)")
        print(" *", nb_spheres, "spheres(s)")
        print(" *", nb_tori, "torus/i")

        for shape in shapes:
            print(shape)
        inliers_of_first_shape = Point_set_3()
        for idx in self._point_cloud.indices():
            if shape_map.get(idx) == 0:
                inliers_of_first_shape.insert(self._point_cloud.point(idx))
        print(inliers_of_first_shape.size(), "inliers(s) recovered")
