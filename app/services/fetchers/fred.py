import os
import requests

FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_BASE_URL = "https://api.stlouisfed.org/fred"

def get_gdp():
    url = f"{FRED_BASE_URL}/series/observations?series_id=GDP&api_key={FRED_API_KEY}&file_type=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        latest = data["observations"][-1]
        return {
            "date": latest["date"],
            "gdp": latest["value"]
        }
    except Exception as e:
        return {"error": str(e)}