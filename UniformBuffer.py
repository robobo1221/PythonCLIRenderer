class UniformBuffer:
    buffer = {}

    def __init__(self) -> None:
        pass

    def register(self, key, value):
        self.buffer[key] = value

    def get(self, key):
        return self.buffer.get(key)