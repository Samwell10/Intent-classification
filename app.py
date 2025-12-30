from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from utill.predict import predict_intent

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESPONSES_PATH = os.path.join(BASE_DIR, "response.json")

# Load intent responses at startup
with open(RESPONSES_PATH, "r", encoding="utf-8") as f:
    INTENT_RESPONSES = json.load(f)

app = FastAPI(
    title="Banking Intent Assistant API",
    description="NLP-powered API that classifies user messages into intents and returns support responses.",
    version="1.0.0",
)

# CORS so frontend (Vite/React) can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://intentclass.netlify.app/"],  # in production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    text: str


class PredictionResponse(BaseModel):
    intent: str
    response: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(query: Query):
    """
    Predict intent for a given user message and return both the intent and
    a friendly explanation from responses.json.
    """
    text = query.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    try:
        intent = predict_intent(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {e}")

    # Get response text from JSON, fall back to default
    response_text = INTENT_RESPONSES.get(intent, INTENT_RESPONSES.get("default", ""))

    return PredictionResponse(intent=intent, response=response_text)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
