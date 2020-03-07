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
    plastic_number = 1.324717957244746025960908854
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

            normal_vector = numpy.cross(vector_b - vector_a,
                                        vector_c - vector_a
                                        )
            norm = numpy.linalg.norm(normal_vector, ord=1)
            normal_vector = normal_vector/norm
            normal_as_list = [float(entry) for entry in normal_vector.tolist()]
            normal_vector = Vector_3(*normal_as_list)

            surface_points = []
            vector_ab = vector_b - vector_a
            vector_ac = vector_c - vector_a
            for point_n in range(1, 201):
                a1 = 1.0 / self.plastic_number
                a2 = (1.0 / self.plastic_number)**2
                r_1 = (0.5 + a1 * point_n) % 1
                r_2 = (0.5 + a2 * point_n) % 1
                if (r_1 + r_2) <= 1:
                    location_vector = vector_ac * r_1 + vector_ab * r_2
                else:
                    location_vector = vector_ac * (1 - r_1) + vector_ab * (1 - r_2)
                location_vector += vector_a
                location_as_list = [float(entry) for entry in location_vector.tolist()]
                all_coodinates_as_str_in_list = [str(x) for x in location_as_list + normal_as_list]
                print(",".join(all_coodinates_as_str_in_list))
                location_vector = Point_3(*location_as_list)
                surface_points.append(location_vector)

            for surface_point in surface_points:
                self._point_cloud.insert(surface_point, normal_vector)
                if face_id not in self._point_face.keys():
                    self._point_face[face_id] = ()
                self._point_face[face_id] += (surface_point, )

    def analysePointCloud(self, cloud=None):
        if not cloud:
            cloud = self.point_cloud

        Logger.log("d", "Running efficient_RANSAC...")
        Logger.log("d", "Inspecting {} points...".format(self.point_cloud.number_of_points()))
        shape_map = self._point_cloud.int_map(self.shape_index_name)
        shapes = efficient_RANSAC(self._point_cloud,
                                  shape_map,
                                  # probability=5,  # [%]
                                  min_points=5,
                                  epsilon=1.,
                                  normal_threshold=0.85,
                                  # cluster_epsilon=1.2,
                                  planes=True,
                                  cylinders=True,
                                  spheres=False,
                                  cones=False,
                                  tori=False
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
