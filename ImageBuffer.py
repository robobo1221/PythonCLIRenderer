from vector.Vector3 import Vector3


class ImageBuffer:
    def __init__(self, width, height, start_values = Vector3(0, 0, 0), id = None, name = None):
        self.width = width
        self.height = height
        self.id = id
        self.name = name

        self.set_values(start_values)

    def __str__(self):
        ret_str = ""

        for y in self.data:
            for x in y:
                ret_str += str(x)

            ret_str += "\n"

        return ret_str

    def set_values(self, value):
        self.data = [[value for x in range(self.width)] for y in range(self.height)]

    def set_value(self, value, x, y):
        self.data[x][y] = value

    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name