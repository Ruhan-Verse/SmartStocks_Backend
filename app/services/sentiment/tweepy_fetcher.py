import os
import tweepy
from textblob import TextBlob

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

def get_twitter_sentiment(symbol: str):
    try:
        query = f"{symbol} stock lang:en -is:retweet"
        tweets = client.search_recent_tweets(query=query, max_results=10)
        sentiment_scores = []
        for tweet in tweets.data:
            blob = TextBlob(tweet.text)
            sentiment_scores.append(blob.sentiment.polarity)
        if not sentiment_scores:
            return {"score": 0.0, "status": "No tweets found"}
        avg_score = sum(sentiment_scores) / len(sentiment_scores)
        return {"score": avg_score}
    except Exception as e:
        return {"error": str(e)}