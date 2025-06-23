# # app/services/fetchers/yahoo_finance.py

# import yfinance as yf

# def get_quote(symbol: str):
#     try:
#         stock = yf.Ticker(symbol)
#         hist = stock.history(period="1d")
#         info = stock.info

#         if hist.empty:
#             return None

#         latest = hist.iloc[-1]
#         return {
#             "source": "yfinance",
#             "price": float(latest["Close"]),
#             "high": float(latest["High"]),
#             "low": float(latest["Low"]),
#             "prev_close": float(latest["Open"]),
#             "currency": info.get("currency", "INR")
#         }
#     except Exception as e:
#         print(f"[yfinance] Error fetching data for {symbol}: {e}")
#         return None
