import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import joblib
import os

FEATURE_COLS = [
    'L_T1','L_T2','L_T3','L_T4','L_T6','L_T7',
    'F_PU1','F_PU2','F_PU3','F_PU4','F_PU6',
    'F_PU7','F_PU8','F_PU9','F_PU10','F_PU11',
    'P_J280','P_J269','P_J300','P_J256','P_J289',
    'P_J415','P_J302','P_J306','P_J307','P_J317',
    'P_J14','P_J422',
    'TANK_LEVEL_ROLLING_MEAN_5', 'TANK_LEVEL_ROLLING_STD_5',
    'PUMP_FLOW_DELTA', 'PRESSURE_RATIO'
]

def train_models(csv_path='data/batadal_train1.csv'):
    from data_pump import add_features
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.upper()
    df = add_features(df)
    available = [c for c in FEATURE_COLS if c in df.columns]
    X = df[available].fillna(0).values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    iso = IsolationForest(n_estimators=200, contamination=0.06, max_features=0.8, bootstrap=True, random_state=42)
    iso.fit(X_scaled)
    svm = OneClassSVM(kernel='rbf', nu=0.05, gamma='auto')
    svm.fit(X_scaled)
    os.makedirs('models', exist_ok=True)
    joblib.dump(iso, 'models/isolation_forest.pkl')
    joblib.dump(svm, 'models/ocsvm.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(available, 'models/feature_cols.pkl')
    print(f"Trained on {len(available)} features. Models saved.")
    return available

def load_models():
    iso = joblib.load('models/isolation_forest.pkl')
    svm = joblib.load('models/ocsvm.pkl')
    scaler = joblib.load('models/scaler.pkl')
    cols = joblib.load('models/feature_cols.pkl')
    return iso, svm, scaler, cols

def predict(row_dict, iso, svm, scaler, cols):
    values = []
    for c in cols:
        try:
            values.append(float(row_dict.get(c, 0)))
        except:
            values.append(0.0)
    X = np.array(values).reshape(1, -1)
    X_scaled = scaler.transform(X)
    iso_pred = iso.predict(X_scaled)[0]
    svm_pred = svm.predict(X_scaled)[0]
    iso_score = float(iso.decision_function(X_scaled)[0])
    svm_score = float(svm.decision_function(X_scaled)[0])
    
    # Weighted hard voting
    combined = (iso_pred * 0.6) + (svm_pred * 0.4)
    is_attack = combined < 0

    confidence = min(100, abs(iso_score) * 200)
    mean_vals = scaler.mean_
    deviations = [abs(values[i] - mean_vals[i]) for i in range(len(cols))]
    top3_idx = sorted(range(len(deviations)), key=lambda i: deviations[i], reverse=True)[:3]
    triggered = [cols[i] for i in top3_idx]
    return {
        'is_attack': is_attack,
        'iso_score': round(iso_score, 4),
        'svm_score': round(svm_score, 4),
        'confidence': round(confidence, 2),
        'triggered_features': triggered
    }
