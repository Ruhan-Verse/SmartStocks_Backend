import requests

def get_sentiment(symbol: str):
    url = f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        messages = response.json().get("messages", [])
        sentiments = [msg.get("entities", {}).get("sentiment", {}).get("basic") for msg in messages if msg.get("entities", {}).get("sentiment")]
        bullish = sentiments.count("Bullish")
        bearish = sentiments.count("Bearish")
        total = bullish + bearish
        if total == 0:
            return "Neutral (no sentiment messages)"
        score = bullish / total
        if score > 0.6:
            return f"Bullish ({bullish}/{total})"
        elif score < 0.4:
            return f"Bearish ({bearish}/{total})"
        else:
            return f"Mixed ({bullish} Bullish / {bearish} Bearish)"
    except Exception as e:
        return f"StockTwits error: {str(e)}"