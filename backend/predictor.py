import cv2
from pathlib import Path
from ultralytics import YOLO

#Project Root 
PROJECT_ROOT = Path(__file__).resolve().parent
#result directory 
RESULT_DIR = PROJECT_ROOT / "backend" / "results"
RESULT_DIR.mkdir(parents=True, exist_ok=True)
#Model Path 
MODEL_PATH = PROJECT_ROOT / "backend" / "models" / "best.pt"

print("=" * 50)
print("PROJECT_ROOT :", PROJECT_ROOT)
print("MODEL_PATH   :", MODEL_PATH)
print("MODEL EXISTS :", MODEL_PATH.exists())
print("=" * 50)

#load model only once
model = YOLO(str(MODEL_PATH))

def get_model_info():
    return {
        "model_path":str(MODEL_PATH),
        "classes":model.names
    }
# ==========================================
# Prediction Function
# ==========================================
def predict_image(image_path: str):

    results = model.predict(
        source=image_path,
        conf=0.05,
        save=False,
        verbose=False
    )
    result = results[0]

    # Draw YOLO annotations
    annotated_image = result.plot()

    # Create output filename
    output_path = RESULT_DIR / f"{Path(image_path).stem}_result.jpg"

    # Save image
    cv2.imwrite(str(output_path), annotated_image)

    detections = []

    for box in result.boxes:

        class_id = int(box.cls[0])

        confidence = round(float(box.conf[0]), 3)

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        detections.append({
            "type": model.names[class_id],
            "confidence": confidence,
            "bbox": [x1, y1, x2, y2]
        })

    return {
    "detections": detections,
    "result_image": str(output_path)
}