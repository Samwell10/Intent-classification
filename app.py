from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from dotenv import load_dotenv
from utill.predict import predict_intent
from utill.llm_service import ClaudeLLMService

# Load environment variables
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESPONSES_PATH = os.path.join(BASE_DIR, "response.json")

# Load intent responses at startup
with open(RESPONSES_PATH, "r", encoding="utf-8") as f:
    INTENT_RESPONSES = json.load(f)

# Initialize Claude LLM service
try:
    llm_service = ClaudeLLMService()
    USE_LLM = True
except Exception as e:
    print(f"Warning: LLM service not available: {e}")
    USE_LLM = False

app = FastAPI(
    title="Banking Intent Assistant API",
    description="NLP-powered API that classifies user messages into intents and returns LLM-enhanced support responses.",
    version="2.0.0",
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
    llm_enhanced: bool = False


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(query: Query):
    """
    Hybrid approach: Use ML model for intent detection, then Claude LLM for
    generating personalized, contextual responses.
    """
    text = query.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    try:
        # Step 1: Use your existing model to detect intent (fast & cheap)
        intent = predict_intent(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {e}")

    # Step 2: Get template response from JSON
    template_response = INTENT_RESPONSES.get(intent, INTENT_RESPONSES.get("default", ""))

    # Step 3: Use Claude to generate personalized response (if enabled)
    if USE_LLM:
        try:
            response_text = llm_service.generate_response(
                user_query=text,
                detected_intent=intent,
                template_response=template_response
            )
            return PredictionResponse(
                intent=intent,
                response=response_text,
                llm_enhanced=True
            )
        except Exception as e:
            print(f"LLM enhancement failed, falling back to template: {e}")
            # Fallback to template if LLM fails
            return PredictionResponse(
                intent=intent,
                response=template_response,
                llm_enhanced=False
            )
    else:
        # LLM not available, use template response
        return PredictionResponse(
            intent=intent,
            response=template_response,
            llm_enhanced=False
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
