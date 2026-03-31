import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

MODEL_PATH = "models/tourism_model.pkl"

def train_model(df: pd.DataFrame):
    print("🔥 TRAINING STARTED")

    print("Columns available:", df.columns)

    # Check required columns
    if 'month_num' not in df.columns or 'total_tourists' not in df.columns:
        raise ValueError("Required columns missing!")

    X = df[['month_num']]
    y = df['total_tourists']

    print("Training data shape:", X.shape)

    model = LinearRegression()
    model.fit(X, y)

    # Create folder if not exists
    os.makedirs("models", exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print("✅ Model trained and saved at:", MODEL_PATH)