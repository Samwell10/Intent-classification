# utils/predict.py
import joblib
import os
from typing import Tuple


# VECTORIZER_PATH = os.path.join("tfidf_vectorizer.pkl")
# MODEL_PATH = os.path.join("intent_model.pkl")

# Load once at startup (fast & scalable)
vectorizer = joblib.load("tfidf_vectorizer.pkl")
model = joblib.load("intent_model.pkl")


def predict_intent(text: str) -> str:
    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    return pred