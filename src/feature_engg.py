import pandas as pd

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    
    df['month_num'] = pd.to_datetime(df['month'], format='%B').dt.month

    df['total_tourists'] = df['domestic_tourists'] + df['foreign_tourists']

    state_col = [col for col in df.columns if 'state' in col][0]

    print("Using state column:", state_col)

    df['growth_rate'] = df.groupby(state_col)['total_tourists'].pct_change()

    return df