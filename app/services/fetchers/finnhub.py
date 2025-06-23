# app/services/fetchers/finnhub.py
import httpx
from app.config import Config

BASE_URL = "https://finnhub.io/api/v1"

async def get_quote(symbol: str):
    url = f"{BASE_URL}/quote"
    params = {"symbol": symbol, "token": Config.FINNHUB_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                "source": "finnhub",
                "price": data.get("c"),
                "high": data.get("h"),
                "low": data.get("l"),
                "prev_close": data.get("pc")
            }
        raise Exception(f"Finnhub error: {response.text}")
