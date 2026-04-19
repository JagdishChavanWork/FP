import joblib

def load_fraud_model():
    data = joblib.load("models/fraud/fraud_model.pkl")
    
    # If you saved metadata
    if isinstance(data, dict):
        return data["model"]
    
    return data