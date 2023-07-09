from ImageBuffer import ImageBuffer
from ImageRenderer import ImageRenderer

window_width = 256
window_height = 128

image_buffer = ImageBuffer(window_width, window_height)
image_renderer = ImageRenderer()

if __name__ == '__main__':
    image_renderer.render(image_buffer)
