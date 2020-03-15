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
    cgal_epsilon = 1.4142135623730950488
    cgal_cluster_epsilon = 1.4142135623730950488

    def __init__(self, node):
        self.mesh = node.getMeshData()
        self._point_cloud = Point_set_3()  # Our set of surface points
        self._point_face = {}  # Needed to trace back the inliers to faces

    @property
    def point_cloud(self):
        if self._point_cloud.is_empty():
            self.generatePointCloud()
        return self._point_cloud

    def getPointDistances(self, points):
        distances = []
        point_indicies = range(len(points))
        for i in point_indicies:
            for j in point_indicies:
                if j >= i:
                    continue
                p1 = points[i]
                p2 = points[j]
                dp = p2 - p1
                distance = (dp.x()**2 + dp.y()**2 + dp.z()**2)**(0.5)
                distances.append(distance)

        return distances

    def generatePoint(self, point_n, vector_a, vector_ab, vector_ac):
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
        location_vector = Point_3(*location_as_list)
        return location_vector

    def getTriangleArea(self, vector_ab, vector_ac):
        area_parallel = numpy.cross(vector_ab,
                                    vector_ac
                                    )
        area_triangle = area_parallel / 2
        area_abs = sum([a_dir**2 for a_dir in area_triangle])**0.5
        return area_abs

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
            vector_ab = vector_b - vector_a
            vector_ac = vector_c - vector_a

            normal_vector = numpy.cross(vector_ab,
                                        vector_ac
                                        )
            norm = numpy.linalg.norm(normal_vector, ord=1)
            normal_vector = normal_vector/norm
            normal_as_list = [float(entry) for entry in normal_vector.tolist()]
            normal_vector = Vector_3(*normal_as_list)

            surface_points = []
            point_n = 0
            point_min_count = self.getTriangleArea(vector_ab, vector_ac)  # Let's have one point per mm^2
            Logger.log("d", "Area of face #{}: {}".format(face_id,
                                                          self.getTriangleArea(vector_ab, vector_ac)))

            while len(surface_points) < point_min_count:
                surface_points.append(self.generatePoint(point_n, vector_a, vector_ab, vector_ac))
                point_n += 1

            # point_distance = None
            # while not point_distance or point_distance >= self.cgal_epsilon / 2:
            #     point_distances = self.getPointDistances(surface_points)
            #     point_distance = min(point_distances)

            #     Logger.log("d", "[{}] Point distance: {}".format(point_n,
            #                                                      point_distance))
            #     surface_points.append(self.generatePoint(point_n, vector_a, vector_ab, vector_ac))

            #     point_n += 1

            Logger.log("d", "Created #{} points for face #{}".format(point_n, face_id))

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
                                  epsilon=self.cgal_epsilon,
                                  # normal_threshold=7,
                                  cluster_epsilon=self.cgal_cluster_epsilon,
                                  planes=True,
                                  cylinders=False,
                                  spheres=False,
                                  cones=False,
                                  tori=False
                                  )
        print(len(shapes), "shapes(s) detected, first 10 shapes are:")

        index2point_map = {}
        for point_index in self._point_cloud.indices():
            shape_index = shape_map.get(point_index)
            if shape_index not in index2point_map.keys():
                index2point_map[shape_index] = []
            index2point_map[shape_index].append(self._point_cloud.point(point_index))

        # Getting a dict of shapes and related faces using common points
        shape2faces = {}
        for shape_index in index2point_map.keys():
            shape_points = index2point_map[shape_index]
            for shape_point in shape_points:
                for face_id in self._point_face.keys():
                    face_points = self._point_face[face_id]
                    if shape_point in face_points:
                        if not set(face_points) - set(shape_points):
                            if shape_index not in shape2faces.keys():
                                shape2faces[shape_index] = []
                            if face_id not in shape2faces[shape_index]:
                                shape2faces[shape_index].append(face_id)
        print(shape2faces)

        # Counting types of shapes
        nb_cylinders = 0
        nb_planes = 0
        for s in shapes:
            _type = s.split()[1]
            if _type == "cylinder":
                nb_cylinders += 1
            if _type == "plane":
                nb_planes += 1
        print("Number of shapes by type:")
        print(" *", nb_cylinders, "cylinder(s)")
        print(" *", nb_planes, "plane(s)")