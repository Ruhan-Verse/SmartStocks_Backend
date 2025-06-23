# app/services/fetchers/gnews.py

import httpx
from app.config import Config

BASE_URL = "https://gnews.io/api/v4/search"

async def get_company_news(company: str, lang="en", count=5):
    params = {
        "q": company,
        "lang": lang,
        "max": count,
        "token": Config.GNEWS_API_KEY  # Add this key in your .env file
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return [
                {
                    "title": a["title"],
                    "url": a["url"],
                    "published": a["publishedAt"],
                    "source": a["source"]["name"]
                }
                for a in articles
            ]
        raise Exception(f"GNews error: {response.text}")
