# # app/services/fetchers/iex_cloud.py
# import os
# import requests

# IEX_TOKEN = os.getenv("IEX_CLOUD_API_KEY")
# IEX_BASE_URL = "https://cloud.iexapis.com/stable"

# def get_iex_quote(symbol):
#     url = f"{IEX_BASE_URL}/stock/{symbol}/quote?token={IEX_TOKEN}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
#         return {
#             "symbol": data.get("symbol"),
#             "price": data.get("latestPrice"),
#             "high": data.get("high"),
#             "low": data.get("low"),
#             "prev_close": data.get("previousClose")
#         }
#     except Exception as e:
#         return {"error": str(e)}
