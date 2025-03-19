import os
import uvicorn
import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Load the trained model (Joblib instead of Pickle)
model = joblib.load("model.joblib")

# Define input data format
class InputData(BaseModel):
    features: list

@app.get("/")
def home():
    return {"message": "FastAPI Model API is running!"}

@app.post("/predict")
def predict(data: InputData):
    X_input = np.array(data.features).reshape(1, -1)
    prediction = model.predict(X_input)
    return {"prediction": prediction.tolist()}

# Run the server on the correct PORT from Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render assigns a dynamic port
    uvicorn.run(app, host="0.0.0.0", port=port)
