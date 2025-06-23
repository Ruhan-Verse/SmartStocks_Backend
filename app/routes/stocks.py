# app/routes/stocks.py
from fastapi import APIRouter, Query
from app.services.fallback import get_stock_data

router = APIRouter()

@router.get("/quote")
async def get_quote(symbol: str = Query(..., description="Stock symbol, e.g. AAPL or RELIANCE.NS")):
    return await get_stock_data(symbol)
