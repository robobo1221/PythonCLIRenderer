from ImageBuffer import ImageBuffer
from vector.Vector3 import Vector3

class ShaderCompute:
    def __init__(self, shader) -> None:
        self.shader = shader

    def transform(self, x, y):
        self.shader.setPosition(x, y)

        main_program = self.shader.main()
        buffers = self.shader.buffers

        for buffer in buffers:
            if not isinstance(main_program, Vector3):
                if isinstance(main_program, complex):
                    main_program = main_program.real

                buffer.data[y][x] = main_program
            else:
                if isinstance(main_program.x, complex):
                    main_program.x = main_program.x.real
                if isinstance(main_program.y, complex):
                    main_program.y = main_program.y.real
                if isinstance(main_program.z, complex):
                    main_program.z = main_program.z.real

                buffer.data[y][x] = main_program