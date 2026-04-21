import joblib
import pickle

def load_model(path):
    """Loads models in either .joblib or .pkl format."""
    if path.endswith('.pkl'):
        with open(path, 'rb') as f:
            return pickle.load(f)
    return joblib.load(path)