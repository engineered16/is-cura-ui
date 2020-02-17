
from UM.Mesh.MeshData import MeshData

def makeInteractiveMesh(mesh_data : MeshData) -> 'pywim.geom.tri.Mesh':
    import pywim

    int_mesh = pywim.geom.tri.Mesh()

    verts = mesh_data.getVertices()

    for i in range(mesh_data.getVertexCount()):
        int_mesh.add_vertex(i, verts[i][0], verts[i][1], verts[i][2])
    
    faces = mesh_data.getIndices()

    if faces is not None:
        for i in range(mesh_data.getFaceCount()):
            v1 = int_mesh.vertices[faces[i][0]]
            v2 = int_mesh.vertices[faces[i][1]]
            v3 = int_mesh.vertices[faces[i][2]]

            int_mesh.add_triangle(i, v1, v2, v3)
    else:
        for i in range(0, len(int_mesh.vertices), 3):
            v1 = int_mesh.vertices[i]
            v2 = int_mesh.vertices[i+1]
            v3 = int_mesh.vertices[i+2]

            int_mesh.add_triangle(i // 3, v1, v2, v3)

    int_mesh.analyze_mesh()

    return int_mesh
