import pandas as pd
import joblib

MODEL_PATH = "models/tourism_model.pkl"

def predict_future(months=12):
    model = joblib.load(MODEL_PATH)

    future = pd.DataFrame({
        "month_num": list(range(1, months + 1))
    })

    predictions = model.predict(future)
    future['predicted_tourists'] = predictions

    return future