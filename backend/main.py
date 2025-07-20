from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import fitz  # PyMuPDF
from fastapi.middleware.cors import CORSMiddleware
from backend.llm_extractor import extract_lab_data
import os

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and scaler
model = joblib.load("backend/wine_quality_model.pkl")
scaler = joblib.load("backend/scaler.pkl")

class WineInput(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

@app.post("/predict")
async def predict(data: WineInput):
    try:
        input_data = np.array([[
            data.fixed_acidity,
            data.volatile_acidity,
            data.citric_acid,
            data.residual_sugar,
            data.chlorides,
            data.free_sulfur_dioxide,
            data.total_sulfur_dioxide,
            data.density,
            data.pH,
            data.sulphates,
            data.alcohol
        ]])
        
        scaled = scaler.transform(input_data)
        prediction = model.predict(scaled)[0]
        label_map = {0: "Bad", 1: "Average", 2: "Good"}
        
        return {
            "prediction": int(prediction),
            "quality": label_map.get(prediction, "Unknown"),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/extract")
async def extract_from_report(file: UploadFile = File(...)):
    try:
        # Read PDF content
        contents = await file.read()
        
        # Extract text from PDF
        pdf = fitz.open(stream=contents, filetype="pdf")
        text = "\n".join([page.get_text() for page in pdf])
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="PDF contained no text")
        
        # Extract data using Groq/Llama
        extracted = extract_lab_data(text)
        
        if "error" in extracted:
            raise HTTPException(status_code=400, detail=extracted["error"])
        
        return {"status": "success", "extracted": extracted}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")