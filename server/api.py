import os
import uvicorn
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()

# Load model with error handling
try:
    model = joblib.load("model.joblib")
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Model loading failed: {str(e)}")
    raise RuntimeError("Failed to load model") from e

class InputData(BaseModel):
    features: list[float]

@app.get("/")
def home():
    return {"message": "FastAPI Model API is running!"}

@app.post("/predict")
def predict(data: InputData):
    try:
        # Validate input length
        expected_features = 8  # Update this with your actual feature count
        if len(data.features) != expected_features:
            raise HTTPException(
                status_code=400,
                detail=f"Expected {expected_features} features, got {len(data.features)}"
            )
        
        # Convert to numpy array and reshape
        X_input = np.array(data.features).reshape(1, -1)
        logger.info(f"Input shape: {X_input.shape}")
        
        # Make prediction
        prediction = model.predict(X_input)
        return {"prediction": prediction.tolist()}
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)