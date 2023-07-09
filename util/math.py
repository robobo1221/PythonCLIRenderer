from vector.Vector2 import Vector2
from vector.Vector3 import Vector3
import math

def mix(a, b, c):
    return a * (1.0 - c) + b * c

def fract(x):
    return mod(x, 1.0)

def clamp(x, a, b):
    return (x.min(b)).max(a)

def smoothstep(edge0, edge1, x):
    t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (-2.0 * t + 3.0)

def floor(x):
    if isinstance(x, (Vector2, Vector3)):
        return x.floor()
    
    return math.floor(x)

def mod(x, y):
    if isinstance(x, (Vector2, Vector3)):
        return x.__mod__(y)
    
    return math.fmod(x, y)