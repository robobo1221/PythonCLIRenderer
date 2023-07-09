import ImageBuffer
import os
import threading
import multiprocessing
from multiprocessing.pool import Pool
import time

from ShaderCompute import ShaderCompute
from UniformBuffer import UniformBuffer
from shaders.TestShader import TestShader
from shaders.SimpleColorShader import SimpleColorShader
from vector.Vector3 import Vector3

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{}\033[0m".format(r, g, b, text)

def rgb_to_8(rgb):
    rgb8 = rgb * 255

    r = int(rgb8.x)
    g = int(rgb8.y)
    b = int(rgb8.z)

    return r, g, b

class ImageRenderer:
    shades = " .-,;!LviFE#@"

    compute_size_x = 4
    compute_size_y = 4
    
    def render(self, buffer):
        buffer = self.optimized_renderer(SimpleColorShader, buffer)
        self.write_to_screen(buffer)

    def __init__(self):
        #self.lock = threading.Lock()
        pass

    def sub_renderer(self, Shader: object, buffer, subregion):
        transformer = self.create_shader(Shader, buffer)

        x_start, y_start, x_end, y_end = subregion

        # Perform expensive operations on the assigned subregion
        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                transformer.transform(x, y)
        
    def write_to_screen(self, buffer):
        os.system("cls")
        buildString = ""

        for y in reversed(range(buffer.height)):
            buildString = ""
            for x in range(buffer.width):
                buildString += self.decode_value(buffer.data[y][x])

            print(buildString)
        
        return buildString

    def optimized_renderer(self, Shader: object, buffer: ImageBuffer):
        self.compute_size_x = min(self.compute_size_x, buffer.width)
        self.compute_size_y = min(self.compute_size_y, buffer.height)

        cells_x = buffer.width // self.compute_size_x
        cells_y = buffer.height // self.compute_size_y

        total_threads = cells_x * cells_y

        threads = []
        for i in range(total_threads):
            threadidx = i % cells_x
            threadidy = i // cells_x

            # Define the subregion for each subprocess
            x_start = threadidx * self.compute_size_x
            y_start = threadidy * self.compute_size_y
            x_end = x_start + self.compute_size_x
            y_end = y_start + self.compute_size_y

            subregion = (x_start, y_start, x_end, y_end)

            t = threading.Thread(target=self.sub_renderer, args=(Shader, buffer, subregion))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()     

        return buffer

    def create_shader(self, Shader: object, buffer):
        shader = Shader([buffer])

        uniform_buffer = UniformBuffer()
        uniform_buffer.register("viewWidth", buffer.width)
        uniform_buffer.register("viewHeight", buffer.height)
        uniform_buffer.register("compute_size_x", self.compute_size_x)
        uniform_buffer.register("compute_size_y", self.compute_size_y)
        shader.bind_uniform_buffer(uniform_buffer)

        return ShaderCompute(shader)

    def decode_value(self, buffer_cell):
        #lum = buffer_cell.dot(Vector3(0.2125, 0.7154, 0.0721))

        buffer_cell.x = min(max(buffer_cell.x, 0.0), 1.0)
        buffer_cell.y = min(max(buffer_cell.y, 0.0), 1.0)
        buffer_cell.z = min(max(buffer_cell.z, 0.0), 1.0)

        lum = max(max(buffer_cell.x, buffer_cell.y), buffer_cell.z)

        #id = int(lum * len(self.shades) - 1e-10)
        #character = self.shades[id]

        r, g, b = rgb_to_8(buffer_cell)

        return colored(r, g, b, "█")
