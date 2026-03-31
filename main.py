from src.ingestion import download_dataset, load_data, save_processed_data
from src.preprocessing import clean_data, format_columns
from src.feature_engg import create_features
from src.train import train_model

PROCESSED_PATH = "data/processed/cleaned_tourism.csv"

def run_pipeline():
    print("Starting pipeline...")

    
    download_dataset()

    
    df = load_data()
    print(" Data loaded")

    
    df = format_columns(df)
    print("Columns formatted")

    
    print("Columns:", df.columns)

    
    df = clean_data(df)
    print("Data cleaned")

    
    df = create_features(df)
    print("Features created")

    
    save_processed_data(df, PROCESSED_PATH)
    print("Processed data saved")

    
    train_model(df)
    print("Model trained")

    print("Pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()