import imp
from ShaderBase import ShaderBase
from vector.Vector2 import Vector2
from vector.Vector3 import Vector3
from util.math import *
import math

def hash12(p: Vector2) -> float:
    p *= 243421.0
    p3 = fract(Vector3(p.x, p.y, p.x) * .1031)
    p3 += p3.dot(Vector3(p3.y, p3.z, p3.x) + 33.33)
    return fract((p3.x + p3.y) * p3.z)

def noise(n: Vector2) -> float:
    b = floor(n)
    f = fract(n)

    return mix(mix(hash12(b), hash12(b + Vector2(1.0, 0.0)), f.x), mix(hash12(b + Vector2(0.0, 1.0)), hash12(b + 1.0), f.x), f.y);

class SimpleColorShader(ShaderBase):
    def main(self):
        viewWidth = self.getUniform("viewWidth")
        viewHeight = self.getUniform("viewHeight")
        compute_size_x = self.getUniform("compute_size_x")
        compute_size_y = self.getUniform("compute_size_y")

        pixelSize = Vector2(viewWidth, viewHeight)
        
        uv = self.position / pixelSize
        hash = noise(uv * 10.0)

        return Vector3(hash, hash, hash)