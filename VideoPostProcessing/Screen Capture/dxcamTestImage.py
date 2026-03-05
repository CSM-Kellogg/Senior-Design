import dxcam
camera = dxcam.create(output_color="GRAY", max_buffer_len=10)

# region select
left, top = 400, 200
right, bottom = 1000, 800
region = (left, top, right, bottom)
frame = camera.grab(region=region)  # numpy.ndarray of size (640x640x3) -> (HXWXC)

# Displays image
from PIL import Image
Image.fromarray(frame).show()