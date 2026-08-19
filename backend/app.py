from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
import subprocess
print(subprocess.check_output(["pip", "freeze"]).decode())

from predictor import get_model_info
from fastapi import UploadFile, File, HTTPException
from pathlib import Path
from services.analysis import generate_analysis
from fastapi import Request
import shutil
import os
import traceback

from predictor import predict_image

app = FastAPI(
    title="AI Powered PCB Defect Detection using YOLOv8",
    description="Backend API for PCB Defect Detection",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-powered-pcb-defects-detection.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

RESULTS_DIR = BASE_DIR / "results"

UPLOADS_DIR = BASE_DIR / "uploads"


app.mount(
    "/results",
    StaticFiles(directory=RESULTS_DIR),
    name="results"
)


UPLOAD_DIR =  UPLOADS_DIR
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.post(
    "/predict",
    tags=["Prediction"],
    summary="Predict PCB Defects",
    description="""
Upload a PCB image and detect PCB manufacturing defects using the trained YOLOv8 model.

Returns:
- Detected defect names
- Confidence scores
- Bounding box coordinates
- URL of the annotated result image
"""
)
async def predict(request: Request, file: UploadFile = File(...)):

     # Check if a file was selected
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    # Check file extension
    allowed_extensions = {".jpg", ".jpeg", ".png"}

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG and PNG images are allowed."
        )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = predict_image(str(file_path))
        analysis = generate_analysis(
    result["detections"],
    file.filename
    )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

    result_filename = Path(result["result_image"]).name

    result_image_url = f"{request.base_url}results/{result_filename}"

    return {
    "status": "success",
    "filename": file.filename,
    "total_detections": len(result["detections"]),
    "detections": result["detections"],
    "result_image_url": result_image_url,
    "analysis": analysis
}


@app.get(
    "/",
    tags=["Home"],
    summary="Home",
    description="Welcome endpoint for the PCB Defect Detection API."
)
def home():
    return {
        "message": "PCB Defect Detection API Running"
    }


@app.get(
    "/model-info",
    tags=["Model"],
    summary="Model Information",
    description="Returns YOLO model information including available defect classes."
)
def model_info():
    return get_model_info()

@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
    description="Check whether the backend API is running correctly."
)
def health_check():

    model_info = get_model_info()

    return {
        "status": "healthy",
        "model_loaded": True,
        "version": app.version,
        "classes": len(model_info["classes"])
    }