import math

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)

        return Vector2(self.x * other, self.y * other)

    def __rmul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)

        return Vector2(self.x * other, self.y * other)

    def __div__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)

        if other == 0.0:
            other = 1e-32

        return Vector2(self.x / other, self.y / other)

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)

        if other == 0.0:
            other = 1e-32

        return Vector2(self.x / other, self.y / other)

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)

        return Vector2(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)

        return Vector2(self.x - other, self.y - other)

    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __max__(self, other):
        if isinstance(other, Vector2):
            return Vector2(max(self.x, other.x), max(self.y, other.y))

        return Vector2(max(self.x, other), max(self.y, other))

    def __min__(self, other):
        if isinstance(other, Vector2):
            return Vector2(min(self.x, other.x), min(self.y, other.y))

        return Vector2(min(self.x, other), min(self.y, other))

    def __pow__(self, other):
        if isinstance(other, Vector2):
            return Vector2(pow(self.x, other.x), pow(self.y, other.y))

        return Vector2(pow(self.x, other), pow(self.y, other))

    def __mod__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x % other.y, self.y % other.y)

        return Vector2(self.x % other, self.y % other)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def length(self):
        return math.sqrt(self.dot(self))

    def normalize(self):
        return self / self.length()
    
    def floor(self):
        return Vector2(math.floor(self.x), math.floor(self.y))
    
    def __str__(self):
        return f"({self.x}, {self.y})"