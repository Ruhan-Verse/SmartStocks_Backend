# app/services/fetchers/marketaux.py

import requests
import os
from typing import List, Optional

MARKETAUX_API_KEY = os.getenv("MARKETAUX_API_KEY")

BASE_URL = "https://api.marketaux.com/v1/news/all"

def get_market_news(symbols: Optional[List[str]] = None, limit: int = 5):
    params = {
        "api_token": MARKETAUX_API_KEY,
        "limit": limit,
        "language": "en",
        "sort_by": "published_at"
    }

    if symbols:
        params["symbols"] = ",".join(symbols)

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("data", [])
    else:
        raise Exception(f"MarketAux API failed: {response.status_code} → {response.text}")
