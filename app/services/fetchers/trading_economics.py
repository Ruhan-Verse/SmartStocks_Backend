import os
import requests

TRADING_ECONOMICS_KEY = os.getenv("TRADING_ECONOMICS_KEY")
TRADING_ECONOMICS_BASE_URL = "https://api.tradingeconomics.com"

def get_indicator(country="India", indicator="GDP"):
    url = f"{TRADING_ECONOMICS_BASE_URL}/historical/country/{country}/indicator/{indicator}?c={TRADING_ECONOMICS_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data:
            return {"error": "No data returned"}
        latest = sorted(data, key=lambda x: x['Date'], reverse=True)[0]
        return {
            "date": latest.get("Date"),
            "value": latest.get("Value"),
            "unit": latest.get("Unit")
        }
    except Exception as e:
        return {"error": str(e)}