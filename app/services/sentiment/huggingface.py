import torch
from transformers import pipeline

# Initialize sentiment pipeline (only once)
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(text: str) -> str:
    try:
        result = sentiment_pipeline(text)
        if result:
            label = result[0]['label']
            score = round(result[0]['score'] * 100, 2)
            return f"{label} ({score}%)"
        else:
            return "Local sentiment model returned no result."
    except Exception as e:
        return f"Local sentiment error: {str(e)}"
