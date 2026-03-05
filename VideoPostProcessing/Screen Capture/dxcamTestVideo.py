import dxcam, cv2

target_fps = 20
clip_duration = int(float(input("Length of video (s): ")) * target_fps)

camera = dxcam.create(output_color="BGR", output_idx=0)
camera.start(target_fps=target_fps, video_mode=True)

writer = cv2.VideoWriter(
    "video.mp4", cv2.VideoWriter_fourcc(*"mp4v"), target_fps, (1920, 1080)
)

someCounter = 0

i = 0
while i < clip_duration:
    frame = camera.get_latest_frame()
    writer.write(frame)
    someCounter += frame.all

    i += 1

print(someCounter)

camera.stop()
writer.release()