"""
Python script to train an object given data

Required data:
 - 50-100 images of object in different angles and lighting
 - draw boxes around object (roboflow)
 - Export to YOLOv8 (15% validate, 70% train, )
"""

from ultralytics import YOLO

# 1. Load a pretrained model (transfer learning)
# 'yolo11n.pt' is the "nano" model: fastest but least accurate.
# 'yolo11m.pt' is "medium": balanced speed and accuracy.
model = YOLO('yolo11n.pt') 

# 2. Train the model
results = model.train(
    data='datasets/rubberband/data.yaml', # Path to your config
    epochs=50,                                  # How many times to go through data
    imgsz=512,                                  # Image size
    name='rubber_band_model'                    # Name of the run
)