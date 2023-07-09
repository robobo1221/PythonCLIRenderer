from UniformBuffer import UniformBuffer
from vector.Vector2 import Vector2


from vector.Vector2 import Vector2
from abc import ABC, abstractclassmethod

class ShaderBase(ABC):
    def __init__(self, buffers = []):
        self.position = Vector2(0, 0)
        self.buffers = buffers

    @abstractclassmethod
    def main(self):
        pass

    def setPosition(self, x, y):
        self.position = Vector2(x, y)

    def bind_uniform_buffer(self, uniformBuffer: UniformBuffer):
        self.uniformBuffer = uniformBuffer

    def getUniform(self, key):
        return self.uniformBuffer.get(key)