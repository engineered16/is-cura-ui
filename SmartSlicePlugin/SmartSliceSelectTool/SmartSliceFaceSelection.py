#   SmartSliceFaceSelection.py
#   Teton Simulation


class SelectablePoint():
    def __init__(self, pid, x, y, z):
        self._id = pid
        self.x = x
        self.y = y
        self.z = z

class SelectableTri():
    def __init__(self, tid, points, normals):
        self._id = tid

        self._points = points
        self._normals = normals

class SelectableFace():
    def __init__(self, fid, tri):
        self._id = fid

        self._tris = [tri]
        self._points = tri._points


class SelectableMesh():
    def __init__(self, mesh_data):
        
