from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import os

app = FastAPI()

# === Load Clustering Models ===
kmeans = joblib.load("kmeans_model.joblib")
scaler_for_clustering = joblib.load("scaler_for_clustering.joblib")

# === Column Definitions ===
categorical_cols = ['make', 'model', 'trim', 'state', 'color', 'interior']
numerical_cols = ['year', 'condition', 'odometer', 'mmr',
                  'age', 'odometer_per_year', 'mmr_odometer_ratio', 'year_condition_interaction']
cluster_features = ['year', 'condition', 'odometer', 'mmr']

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Input Schema ===
class CarInput(BaseModel):
    year: int
    make: str
    model: str
    trim: str
    state: str
    condition: int
    odometer: int
    color: str
    interior: str
    mmr: int

# === Feature Engineering ===
def add_interaction_features(df):
    df["age"] = 2024 - df["year"]
    df["odometer_per_year"] = df["odometer"] / (df["age"] + 1e-3)
    df["mmr_odometer_ratio"] = df["mmr"] / (df["odometer"] + 1e-3)
    df["year_condition_interaction"] = df["year"] * df["condition"]
    return df

# === Prediction Endpoint ===
@app.post("/predict")
def predict(car: CarInput):
    try:
        car_df = pd.DataFrame([car.dict()])
        print("Received DataFrame:", car_df)
        # Cluster prediction
        cluster_input = car_df[cluster_features]
        cluster_scaled = scaler_for_clustering.transform(cluster_input)
        cluster = kmeans.predict(cluster_scaled)[0]

        # Feature engineering
        car_df = add_interaction_features(car_df)

        # Load preprocessors & model
        label_encoders = joblib.load(f"models_by_cluster/label_encoders_cluster_{cluster}.joblib")
        scaler = joblib.load(f"models_by_cluster/scaler_cluster_{cluster}.joblib")
        model = joblib.load(f"models_by_cluster/lightgbm_model_cluster_{cluster}.joblib")['model']

        for col in categorical_cols:
            car_df[col] = label_encoders[col].transform(car_df[col].astype(str))

        X_cat = car_df[categorical_cols].values
        X_num = scaler.transform(car_df[numerical_cols])
        X_input = np.hstack((X_cat, X_num)).astype(np.float32)

        y_log_pred = model.predict(X_input)
        y_pred = np.expm1(y_log_pred)

        return {
            "cluster": int(cluster),
            "predicted_price": float(round(y_pred[0], 2))
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
