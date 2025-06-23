# app/services/fallback/news_fallback.py

from app.services.fetchers import gnews, newsapi, marketaux

def get_latest_news(topic: str = "Stock Market", limit: int = 5):
    """
    Try fetching news from multiple sources in order of priority.
    Returns a list of news articles (title, url, published_at).
    """
    news_sources = [
        lambda: newsapi.get_news(topic, limit),
        lambda: gnews.get_news(topic, limit),
        lambda: marketaux.get_market_news(symbols=[topic], limit=limit),
    ]

    for source in news_sources:
        try:
            articles = source()
            if articles and len(articles) > 0:
                return articles
        except Exception as e:
            print(f"[news_fallback] Source failed: {e}")

    return []  # All sources failed
