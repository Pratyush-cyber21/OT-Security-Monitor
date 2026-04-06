import pandas as pd
import time

def load_data(path='data/batadal_train2.csv'):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.upper()
    if 'DATETIME' in df.columns:
        df['DATETIME'] = pd.to_datetime(df['DATETIME'], format='%d/%m/%y %H', errors='coerce')
    df = add_features(df)
    return df

def add_features(df):
    # Rolling statistics — critical for OT anomaly detection
    df['TANK_LEVEL_ROLLING_MEAN_5'] = df['L_T1'].rolling(5).mean()
    df['TANK_LEVEL_ROLLING_STD_5']  = df['L_T1'].rolling(5).std()
    df['PUMP_FLOW_DELTA']           = df['F_PU1'].diff()
    df['PRESSURE_RATIO']            = df['P_J280'] / (df['P_J269'] + 1e-6)
    return df.fillna(0)

def stream_data(df, speed=1):
    for _, row in df.iterrows():
        yield row.to_dict()
        time.sleep(1.0 / max(speed, 1))

def inject_attack(row_dict):
    attacked = row_dict.copy()
    for key in attacked:
        if 'L_T' in str(key):
            try:
                attacked[key] = float(attacked[key]) * 3.5
            except:
                pass
        if 'F_PU' in str(key):
            try:
                attacked[key] = 0.0
            except:
                pass
    return attacked
