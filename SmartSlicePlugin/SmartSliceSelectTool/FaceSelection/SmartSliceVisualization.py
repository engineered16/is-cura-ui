# SmartSliceVisualization.py
# Teton Simulation
# Authored on   November 4, 2019
# Last Modified November 4, 2019

#
# Contains functionality for drawing Smart Slice Face Selection in UI
#


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class SmartSliceSelectionVisualizer:
    def __init__(self, fs):
        fig = plt.figure()
        self._canvas = fig.add_subplot(111, projection='3d')

        #  Add Selectable Faces to Visualizer 
        for _face in fs.faces:
            xs = []
            ys = []
            zs = []

            #  Draw/Colorize Face Surface
            for _edge in _face.edges:
                xs.append([_edge.p1.x(), _edge.p2.x()])
                ys.append([_edge.p1.y(), _edge.p2.y()])
                zs.append([_edge.p1.z(), _edge.p2.z()])

            if (_face.selected):
                self._canvas.plot_surface(np.array(xs), np.array(ys), np.array(zs), color="#5555ff")
            else:
                self._canvas.plot_surface(np.array(xs), np.array(ys), np.array(zs), color="#bbbbbb")


            #  Draw/Colorize Face Edges
            for _edge in _face.edges:
                self._canvas.plot([_edge.p1.x(), _edge.p2.x()], [_edge.p1.y(), _edge.p2.y()], [_edge.p1.z(), _edge.p2.z()], color="#000000")


            #  Draw/Colorize Face Points
            for _point in _face.points:
                xs = [_point.x()]
                ys = [_point.y()]
                zs = [_point.z()]
                if (_face.selected):
                    self._canvas.scatter(xs, ys, zs, color="#0000dd")
                else:
                    self._canvas.scatter(xs, ys, zs, color="#000000")

        plt.show()

