from UM.View.View import View
from UM.Scene.Iterator.DepthFirstIterator import DepthFirstIterator
from UM.Resources import Resources
from UM.Math.Color import Color
from UM.View.GL.OpenGL import OpenGL
from UM.Scene.Platform import Platform

from cura.BuildVolume import BuildVolume
from cura.Scene.ConvexHullNode import ConvexHullNode

from .stage import SmartSliceScene

import math

class SmartSliceView(View):
    def __init__(self):
        super().__init__()
        self._shader = None

    def _checkSetup(self):
        if not self._shader:
            self._shader = OpenGL.getInstance().createShaderProgram(Resources.getPath(Resources.Shaders, "overhang.shader"))
            #self._shader.setUniformValue("u_diffuseColor", Color(0., 0., 1., 1.))
            self._shader.setUniformValue("u_overhangAngle", math.cos(math.radians(0)))
            self._shader.setUniformValue("u_faceId", -1)

    def beginRendering(self):
        scene = self.getController().getScene()
        renderer = self.getRenderer()

        self._checkSetup()

        for node in DepthFirstIterator(scene.getRoot()):
            if isinstance(node, (BuildVolume, ConvexHullNode, Platform)):
                continue

            uniforms = {}
            overlay = False

            if isinstance(node, SmartSliceScene.AnchorFace):
                uniforms['diffuse_color'] = [1., 0.4, 0.4, 1.]
                overlay = True
            elif isinstance(node, SmartSliceScene.LoadFace):
                uniforms['diffuse_color'] = [0.4, 0.4, 1., 1.]
                overlay = True
            
            if not node.render(renderer):
                if node.getMeshData() and node.isVisible() and not node.callDecoration("getLayerData"):
                    per_mesh_stack = node.callDecoration("getStack")

                    if node.callDecoration("isNonPrintingMesh"):
                        pass
                    elif per_mesh_stack and per_mesh_stack.getProperty("support_mesh", "value"):
                        pass
                    else:
                        if overlay:
                            renderer.queueNode(node, shader = self._shader, uniforms = uniforms, overlay = True)
                        else:
                            renderer.queueNode(node, shader = self._shader, uniforms = uniforms)

    def endRendering(self):
        pass
