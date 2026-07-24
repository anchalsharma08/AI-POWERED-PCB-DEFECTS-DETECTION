from ultralytics import YOLO

# Load pretrained YOLOv8 Nano model
model = YOLO("yolov8n.pt")

# Train the model
model.train(
    data="dataset/data.yaml",
    epochs=5,
    imgsz=640,
    batch=16,
    project="results",
    name="pcb_detector"
)