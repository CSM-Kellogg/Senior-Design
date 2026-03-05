"""
Tracks the rubber band in the video clip

Needs to also be trained on the target
https://docs.ultralytics.com/usage/python/
 - Training for a model: https://docs.ultralytics.com/modes/train/

Or, a marker (arcu) can be used:
https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html

TODO:
Instead of a .mp4 file, run a video stream
Get orientation data (?) (arcu?, multiple targets)

save the output video
"""

import cv2
from ultralytics import YOLO

# Object detection
model = YOLO("./best.pt")

# Run validation
metrics = model.val(data="../datasets/rubberband/data.yaml")

print(f"mAP 50-95: {metrics.box.map}")    # Mean Average Precision (strict)
print(f"mAP 50:    {metrics.box.map50}")  # Mean Average Precision (standard)
print(f"Precision: {metrics.box.mp}")     # Precision
print(f"Recall:    {metrics.box.mr}")     # Recall

# Load video
cap = cv2.VideoCapture('motrack test.mp4')

# load tracker
while cap.isOpened():
    ret, frame = cap.read()

    if not ret: break
    
    # Detect
    results = model.track(frame, persist=True)

    # Annotate
    annotated_frame = results[0].plot()

    cv2.imshow("Frame", annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()