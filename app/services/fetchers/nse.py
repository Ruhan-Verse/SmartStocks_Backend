# app/services/fetchers/nse.py

import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

def get_nse_quote(symbol: str):
    try:
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol.upper()}"
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=HEADERS)  # get cookies
        response = session.get(url, headers=HEADERS)
        data = response.json()

        price = float(data["priceInfo"]["lastPrice"])
        high = float(data["priceInfo"]["intraDayHighLow"]["max"])
        low = float(data["priceInfo"]["intraDayHighLow"]["min"])
        prev_close = float(data["priceInfo"]["previousClose"])

        return {
            "source": "nse",
            "price": price,
            "high": high,
            "low": low,
            "prev_close": prev_close,
            "currency": "INR"
        }
    except Exception as e:
        print(f"[NSE] Error: {e}")
        return None
