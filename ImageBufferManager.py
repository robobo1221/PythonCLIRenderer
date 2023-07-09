from ImageBuffer import ImageBuffer
import uuid
from typing import Union

class ImageBufferManager:
    image_buffers = {}

    def register(self, image_buffer: ImageBuffer) -> None:
        if not image_buffer.get_id():
            image_buffer.set_id(str(uuid.uuid4()))

        self.image_buffers[image_buffer.get_id()] = image_buffer

    def register(self, name, image_buffer: ImageBuffer) -> None:
        if not image_buffer.get_id():
            image_buffer.set_id(str(uuid.uuid4()))

        image_buffer.set_name(name)
        self.image_buffers[image_buffer.get_name()] = image_buffer

    def register(self, width, height, start_values) -> None:
        id = str(uuid.uuid4())

        image_buffer = ImageBuffer(width, height, start_values, id)
        self.image_buffers[id] = image_buffer

    def register(self, name, width, height, start_values) -> None:
        image_buffer = ImageBuffer(width, height, start_values, str(uuid.uuid4()), name=name)
        self.image_buffers[name] = image_buffer

    def deregister(self, name_id) -> Union[ImageBuffer, None]:
        return self.image_buffers.pop(name_id, None)
    
    def get(self, id_name) -> Union[ImageBuffer, None]:
        return self.image_buffers.get(id_name, None)