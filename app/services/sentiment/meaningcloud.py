# # app/services/sentiment/meaningcloud_sentiment.py

# import requests
# import os

# MEANINGCLOUD_API_KEY = os.getenv("MEANINGCLOUD_API_KEY")

# def analyze_sentiment(text: str):
#     """
#     Uses MeaningCloud API to analyze sentiment of the given text.
#     Returns: polarity (e.g., 'P+', 'P', 'NEU', 'N', 'N+')
#     """
#     url = "https://api.meaningcloud.com/sentiment-2.1"
#     payload = {
#         "key": MEANINGCLOUD_API_KEY,
#         "lang": "en",
#         "txt": text
#     }

#     response = requests.post(url, data=payload)
#     data = response.json()

#     if data.get("status", {}).get("code") == "0":
#         return {
#             "score_tag": data["score_tag"],     # e.g., P+, NEU, N
#             "agreement": data["agreement"],     # e.g., AGREEMENT, DISAGREEMENT
#             "subjectivity": data["subjectivity"],
#             "confidence": data["confidence"]
#         }

#     return {"error": data.get("status", {}).get("msg", "Unknown error")}
