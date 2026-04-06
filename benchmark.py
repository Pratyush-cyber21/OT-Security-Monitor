import pandas as pd
from ai_engine import load_models, predict
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

ZAHOOR_2025 = {
    'Model': 'Zahoor 2025 (Reference Paper)',
    'F1 Score': 0.91,
    'Precision': 0.89,
    'Recall': 0.93,
    'Accuracy': 0.92,
    'Latency (ms)': 120.0
}

def run_benchmark(csv_path='data/batadal_train2.csv'):
    try:
        iso, svm, scaler, cols = load_models()
    except Exception as e:
        print(f"Model load failed: {e}")
        return None, None
        
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.upper()
    
    if 'ATT_FLAG' not in df.columns:
        return None, None
        
    y_true, y_pred = [], []
    latencies = []
    import time
    for _, row in df.iterrows():
        # Force BATADAL labels into binary 0/1 format
        actual_label = 1 if int(row.get('ATT_FLAG', 0)) == 1 else 0
        
        row_dict = row.to_dict()
        t0 = time.time()
        result = predict(row_dict, iso, svm, scaler, cols)
        t1 = time.time()
        
        y_true.append(actual_label)
        y_pred.append(1 if result['is_attack'] else 0)
        latencies.append((t1 - t0) * 1000) # milliseconds
        
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        
    our_results = {
        'Model': 'DRIFTNET (Ours)',
        'F1 Score': round(f1_score(y_true, y_pred, average='weighted', zero_division=0), 3),
        'Precision': round(precision_score(y_true, y_pred, average='weighted', zero_division=0), 3),
        'Recall': round(recall_score(y_true, y_pred, average='weighted', zero_division=0), 3),
        'Accuracy': round(accuracy_score(y_true, y_pred), 3),
        'Latency (ms)': round(avg_latency, 2)
    }
    
    comparison_df = pd.DataFrame([our_results, ZAHOOR_2025])
    return our_results, comparison_df