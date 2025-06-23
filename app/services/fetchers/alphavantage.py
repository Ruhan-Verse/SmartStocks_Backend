# app/services/fetchers/alphavantage.py
import httpx
from app.config import Config

BASE_URL = "https://www.alphavantage.co/query"

async def get_quote(symbol: str):
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": Config.ALPHA_VANTAGE_KEY
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json().get("Global Quote", {})
            return {
                "source": "alphavantage",
                "price": data.get("05. price"),
                "high": data.get("03. high"),
                "low": data.get("04. low"),
                "prev_close": data.get("08. previous close")
            }
        raise Exception(f"Alpha Vantage error: {response.text}")
