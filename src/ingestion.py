import os
import pandas as pd
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

DATASET = "aishwaryapatidar/india-tourism-dataset-2025"
RAW_DIR = "data/raw"

def download_dataset():
    os.makedirs(RAW_DIR, exist_ok=True)

    api = KaggleApi()
    api.authenticate()

    print("Downloading dataset from Kaggle...")
    api.dataset_download_files(DATASET, path=RAW_DIR, unzip=False)

    zip_path = os.path.join(RAW_DIR, "india-tourism-dataset-2025.zip")

    print("Extracting dataset...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(RAW_DIR)

    print("Dataset ready!")


def load_data() -> pd.DataFrame:
    # Find CSV dynamically
    for file in os.listdir(RAW_DIR):
        if file.endswith(".csv"):
            file_path = os.path.join(RAW_DIR, file)
            print(f"Loading {file}...")
            return pd.read_csv(file_path)

    raise FileNotFoundError("No CSV file found in raw data folder!")


def save_processed_data(df: pd.DataFrame, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print("Processed data saved!")