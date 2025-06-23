import os
import requests
from requests.auth import HTTPBasicAuth

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

def get_reddit_token():
    auth = HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
    data = {"grant_type": "client_credentials"}
    headers = {"User-Agent": "StockBot/1.0"}

    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

def get_reddit_sentiment(query: str):
    try:
        token = get_reddit_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "StockBot/1.0"
        }

        search_url = f"https://oauth.reddit.com/r/stocks/search?q={query}&limit=10&sort=new"
        response = requests.get(search_url, headers=headers)
        posts = response.json().get("data", {}).get("children", [])

        titles = [p["data"]["title"] for p in posts]
        mentions = [t.lower() for t in titles if query.lower() in t.lower()]
        sentiment_score = len(mentions) / len(titles) if titles else 0

        if sentiment_score > 0.5:
            return f"Reddit Mood: Bullish ({len(mentions)}/{len(titles)})"
        elif sentiment_score < 0.2:
            return f"Reddit Mood: Bearish ({len(mentions)}/{len(titles)})"
        else:
            return f"Reddit Mood: Mixed ({len(mentions)}/{len(titles)})"

    except Exception as e:
        return f"Reddit error: {str(e)}"
    
def get_reddit_posts(query: str):
    try:
        token = get_reddit_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "StockBot/1.0"
        }

        search_url = f"https://oauth.reddit.com/r/stocks/search?q={query}&limit=15&sort=top"
        response = requests.get(search_url, headers=headers)
        posts = response.json().get("data", {}).get("children", [])

        # Filter high-upvote relevant posts
        top_posts = []
        for post in posts:
            data = post.get("data", {})
            title = data.get("title", "")
            upvotes = data.get("ups", 0)
            permalink = f"https://reddit.com{data.get('permalink')}"
            if query.lower() in title.lower() and upvotes > 5:
                top_posts.append({
                    "title": title,
                    "upvotes": upvotes,
                    "permalink": permalink
                })

        return sorted(top_posts, key=lambda x: x["upvotes"], reverse=True)[:5]

    except Exception as e:
        return []