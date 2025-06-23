# # app/services/sentiment/twinword_sentiment.py

# import requests
# import os

# TWINWORD_API_KEY = os.getenv("TWINWORD_API_KEY")

# def analyze_sentiment(text: str):
#     """
#     Uses Twinword API to analyze sentiment of the given text.
#     Returns: score, sentiment (positive, neutral, negative)
#     """
#     url = "https://twinword-sentiment-analysis.p.rapidapi.com/analyze/"
#     headers = {
#         "X-RapidAPI-Key": TWINWORD_API_KEY,
#         "X-RapidAPI-Host": "twinword-sentiment-analysis.p.rapidapi.com"
#     }

#     response = requests.get(url, headers=headers, params={"text": text})
#     data = response.json()

#     if response.status_code == 200 and "type" in data:
#         return {
#             "score": data.get("score"),
#             "sentiment": data.get("type"),  # positive, neutral, negative
#             "keywords": data.get("keywords", {})
#         }

#     return {"error": data.get("message", "Unknown error")}
