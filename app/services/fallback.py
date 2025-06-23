# app/services/fallback.py
from app.services.fetchers import finnhub, alphavantage

async def get_stock_data(symbol: str):
    try:
        return await finnhub.get_quote(symbol)
    except Exception as e1:
        try:
            return await alphavantage.get_quote(symbol)
        except Exception as e2:
            return {"error": "All APIs failed", "details": [str(e1), str(e2)]}
