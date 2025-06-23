import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
    FINNHUB_KEY = os.getenv("FINNHUB_KEY")
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID")
    ONESIGNAL_API_KEY = os.getenv("ONESIGNAL_API_KEY")
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
