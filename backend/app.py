from fastapi import FastAPI
from backend.predictor import get_model_info
from fastapi import UploadFile, File
from pathlib import Path
import shutil

from backend.predictor import predict_image

app = FastAPI(
    title="AI Powered PCB Defect Detection using YOLOv8",
    description="Backend API for PCB Defect Detection",
    version="1.0"
)


UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = predict_image(str(file_path))

    return {
    "status": "success",
    "filename": file.filename,
    "detections": result["detections"],
    "result_image": result["result_image"]
}


@app.get("/")
def home():
    return {
        "message": "PCB Defect Detection API Running"
    }


@app.get("/model-info")
def model_info():
    return get_model_info()