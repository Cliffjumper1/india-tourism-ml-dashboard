import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Drop duplicates
    df = df.drop_duplicates()

    # Handle missing values
    df = df.fillna(method='ffill')

    return df


def format_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df