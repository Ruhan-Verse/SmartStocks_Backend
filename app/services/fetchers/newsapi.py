# app/services/fetchers/newsapi.py

import httpx
from app.config import Config
from datetime import datetime

BASE_URL = "https://newsapi.org/v2"

async def get_company_news(company: str, language="en", count=5):
    url = f"{BASE_URL}/everything"
    params = {
        "q": company,
        "sortBy": "publishedAt",
        "language": language,
        "pageSize": count,
        "apiKey": Config.NEWSAPI_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return [
                {
                    "title": a["title"],
                    "url": a["url"],
                    "published": a["publishedAt"],
                    "source": a["source"]["name"],
                }
                for a in articles
            ]
        raise Exception(f"NewsAPI error: {response.text}")
