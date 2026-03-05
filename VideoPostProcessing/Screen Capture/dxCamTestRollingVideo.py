"""
Use dxcam to get rolling image data
"""

import dxcam, sys, time
camera = dxcam.create(output_color="BGR", max_buffer_len=10)

target_fps = 10

region = (0, 0, 100, 100)

camera.start(video_mode=True, target_fps=target_fps)

time_start = time.time()
for _ in range(30):
    frame = camera.get_latest_frame()

    # Active processing

    # move cursor to beginning of previous line (one line up)
    # https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797

    # Calling frame[row][col] returns the pixel color at that point
    # The cursor is not tracked...
    print(f"{frame[10][10]}     \nTime: {time.time() - time_start:.2f}       \x1B[1F", end="")
    sys.stdout.flush()

del camera

# more processing can be done here