import math

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

        return Vector3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

        return Vector3(self.x * other, self.y * other, self.z * other)

    def __div__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)

        if other == 0.0:
            other = 1e-32

        return Vector3(self.x / other, self.y / other, self.z / other)

    def __truediv__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)

        if other == 0.0:
            other = 1e-32

        return Vector3(self.x / other, self.y / other, self.z / other)

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

        return Vector3(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

        return Vector3(self.x - other, self.y - other, self.z - other)

    def __abs__(self):
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def max(self, other):
        if isinstance(other, Vector3):
            return Vector3(max(self.x, other.x), max(self.y, other.y), max(self.z, other.z))

        return Vector3(max(self.x, other), max(self.y, other), max(self.z, other))

    def min(self, other):
        if isinstance(other, Vector3):
            return Vector3(min(self.x, other.x), min(self.y, other.y), min(self.z, other.z))

        return Vector3(min(self.x, other), min(self.y, other), min(self.z, other))

    def __pow__(self, other):
        if isinstance(other, Vector3):
            return Vector3(pow(self.x, other.x), pow(self.y, other.y), pow(self.z, other.z))

        return Vector3(pow(self.x, other), pow(self.y, other), pow(self.z, other))

    def __mod__(self, other):
        if isinstance(other, Vector3):
            return Vector3(math.fmod(self.x, other.x), math.fmod(self.y, other.y), math.fmod(self.z, other.z))

        return Vector3(math.fmod(self.x, other), math.fmod(self.y, other), math.fmod(self.z, other))

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def length(self):
        return math.sqrt(self.dot(self))

    def normalize(self):
        return self / self.length()

    def reflect(self, normal):
        return self - 2.0 * self.dot(normal) * normal
    
    def floor(self):
        return Vector3(math.floor(self.x), math.floor(self.y), math.floor(self.z))
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"