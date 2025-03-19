from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Load the trained model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

class InputData(BaseModel):
    features: list

@app.post("/predict")
def predict(data: InputData):
    X_input = np.array(data.features).reshape(1, -1)
    prediction = model.predict(X_input)
    return {"prediction": prediction.tolist()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
