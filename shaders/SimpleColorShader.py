import imp
from ShaderBase import ShaderBase
from vector.Vector2 import Vector2
from vector.Vector3 import Vector3
from util.math import *
import math

class SimpleColorShader(ShaderBase):
    def main(self):
        viewWidth = self.getUniform("viewWidth")
        viewHeight = self.getUniform("viewHeight")
        compute_size_x = self.getUniform("compute_size_x")
        compute_size_y = self.getUniform("compute_size_y")

        pixelSize = Vector2(viewWidth, viewHeight)
        
        uv = self.position / pixelSize

        return Vector3(uv.x, uv.y, 0.0)