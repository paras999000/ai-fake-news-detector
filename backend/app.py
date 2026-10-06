from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os

app = FastAPI(title="Fake News Detection API")

# Enable CORS so the frontend can make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model at startup
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "fake_news_model.pkl")

# We will load it dynamically or on startup
model = None

@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print("Model loaded successfully.")
    else:
        print("Warning: Model not found. Please run model_trainer.py first.")

class NewsInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze_news(news: NewsInput):
    if not model:
        raise HTTPException(status_code=500, detail="AI Model is not loaded. Please train the model first.")

    text = news.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="News text cannot be empty.")

    # Predict the label and probability
    # label 1 = Real, label 0 = Fake
    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]

    # Calculate trust score
    # probabilities[1] is the probability of being class 1 (Real)
    # probabilities[0] is the probability of being class 0 (Fake)
    is_real = bool(prediction == 1)
    
    # Trust score is out of 100%
    if is_real:
        trust_score = round(probabilities[1] * 100, 2)
        message = "This text appears to be legitimate news based on our analysis."
    else:
        trust_score = round(probabilities[1] * 100, 2)  # Overall credibility is low
        message = "Caution: This text exhibits patterns commonly found in fake news or misinformation."

    return {
        "is_real": is_real,
        "prediction_label": "Real News" if is_real else "Fake News",
        "trust_score": trust_score,
        "explanation": message
    }
