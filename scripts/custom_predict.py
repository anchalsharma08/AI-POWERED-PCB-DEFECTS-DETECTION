from pathlib import Path
import cv2
from ultralytics import YOLO
from datetime import datetime

# ----------------------------
# Project Paths
# ----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

model_path = (
    PROJECT_ROOT
    / "trained_results"
    / "runs"
    / "detect"
    / "results"
    / "pcb_detector"
    / "weights"
    / "best.pt"
)

image_path = PROJECT_ROOT / "test_images" / "pcb8.jpg"

# ----------------------------
# Load Model
# ----------------------------
model = YOLO(str(model_path))

# ----------------------------
# Class Names
# ----------------------------
class_names = {
    0: "Open Circuit",
    1: "Short Circuit",
    2: "Mouse Bite",
    3: "Spur",
    4: "Spurious Copper",
    5: "Missing Hole"
}

# ----------------------------
# Run Prediction
# ----------------------------
results = model(str(image_path), conf=0.25)

# ----------------------------
# Read Image
# ----------------------------
img = cv2.imread(str(image_path))

# Different colors for each defect
colors = {
    0: (0, 0, 255),        # Red
    1: (255, 0, 0),        # Blue
    2: (0, 255, 0),        # Green
    3: (0, 255, 255),      # Yellow
    4: (255, 0, 255),      # Purple
    5: (255, 255, 0)       # Cyan
}

# ----------------------------
# Draw Bounding Boxes
# ----------------------------
for result in results:

    for box in result.boxes:

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cls = int(box.cls[0])

        conf = float(box.conf[0])

        color = colors.get(cls, (255,255,255))

        label = f"{class_names[cls]} ({conf:.1f})"

        # Draw Rectangle
        cv2.rectangle(
            img,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        # Background for Label
        (w, h), _ = cv2.getTextSize(
            label,
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            2
        )

        cv2.rectangle(
            img,
            (x1, y1-h-10),
            (x1+w+6, y1),
            color,
            -1
        )

        # White Text
        cv2.putText(
            img,
            label,
            (x1+3, y1-5),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (240,86,25),
            2
        )

# ----------------------------
# Save Result
# ----------------------------
output_dir = PROJECT_ROOT / "runs" / "custom_results"
output_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

output_path = output_dir / f"{image_path.stem}_{timestamp}.jpg"

cv2.imwrite(str(output_path), img)

# ----------------------------
# Display Result
# ----------------------------
cv2.namedWindow("PCB Defect Detection", cv2.WINDOW_NORMAL)

# Resize the window (optional)
cv2.resizeWindow("PCB Defect Detection", 640, 640)

cv2.imshow("PCB Defect Detection", img)

print("\nPress any key to close the image window...")

cv2.waitKey(0)
cv2.destroyAllWindows()

print("\n======================================")
print("Prediction Completed Successfully")
print("Saved at:")
print(output_path)
print("======================================")