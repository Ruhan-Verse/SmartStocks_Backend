# ✅ rag.py (Updated for Gemini 1.5 Pro)
import os
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro")

async def generate(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "⚠️ Gemini failed to generate response."

from app.services.fetchers import (
    finnhub, 
    newsapi, gnews, marketaux,
    alphavantage, 
)

async def get_stock_context(symbol: str) -> str:
    context_parts = []

    # 1. Finnhub - Price Summary
    try:
        fh_data = await finnhub.get_quote(symbol)
        context_parts.append(
            f"📊 Finnhub:\nCurrent Price: ₹{fh_data['price']}\nHigh: ₹{fh_data['high']}\nLow: ₹{fh_data['low']}\nPrevious Close: ₹{fh_data['prev_close']}\n"
        )
    except Exception as e:
        context_parts.append("📊 Finnhub data unavailable.")

        try:
            av_data = await alphavantage.get_quote(symbol)
            context_parts.append(
                f"📊 **Alpha Vantage Data**\n"
                f"- Current Price: ₹{av_data['price']}\n"
                f"- Day High: ₹{av_data['high']}\n"
                f"- Day Low: ₹{av_data['low']}\n"
                f"- Previous Close: ₹{av_data['prev_close']}\n"
            )
        except Exception as e:
            context_parts.append("❌ Alpha Vantage data unavailable.")

    return "\n".join(context_parts)

from app.services.fetchers import (
    newsapi,
    marketaux,
    gnews,
    world_news
)

async def get_news_context(query: str) -> str:
    context_parts = []

    # 1. NewsAPI.org
    try:
        articles = await newsapi.get_company_news(query)
        if articles:
            context_parts.append("📰 NewsAPI Headlines:")
            for a in articles[:5]:
                context_parts.append(f"- {a['title']} ({a['source']})")
    except Exception as e:
        context_parts.append(f"📰 NewsAPI Error: {str(e)}")

    # 2. MarketAux
    try:
        articles = marketaux.get_market_news(symbols=[query])
        if articles:
            context_parts.append("\n📡 MarketAux Headlines:")
            for a in articles[:3]:
                context_parts.append(f"- {a['title']} ({a['source']})")
    except Exception as e:
        context_parts.append(f"📡 MarketAux Error: {str(e)}")

        # 3. GNews headlines
    try:
        # Use refined symbol or fallback to keyword
        company_name = extract_symbol(query)
        if not company_name or company_name == "":
            company_name = query.split(" ")[-1]  # fallback e.g., "Tesla" from "Should I buy Tesla today?"
        
        gnews_articles = await gnews.get_company_news(company_name, count=5)
        if gnews_articles:
            context_parts.append("\n🌍 GNews Headlines:")
            for a in gnews_articles:
                context_parts.append(f"- {a['title']} ({a['source']})")
        else:
            context_parts.append("🌍 GNews: No relevant headlines.")
    except Exception as e:
        context_parts.append(f"🌍 GNews Error: {str(e)}")



    return "\n".join(context_parts)

from app.services.sentiment import (
    huggingface,
    meaningcloud,
    twinword,
    stocktwits,
    reddit,
)

async def get_sentiment_context(query: str) -> str:
    context_parts = []

    # HuggingFace (brief summary + headlines analyzed)
    try:
        headlines = await newsapi.get_company_news(query, count=3)
        if headlines:
            combined = " ".join([h['title'] for h in headlines])
            result = huggingface.analyze_sentiment(combined)
            context_parts.append("🤖 HuggingFace Sentiment Summary:")
            context_parts.append(f"Sentiment Score: {result}")
            context_parts.append("Headlines analyzed:")
            for h in headlines:
                context_parts.append(f"- {h['title']} ({h['source']})")
    except Exception as e:
        context_parts.append(f"🤖 HuggingFace error: {str(e)}")

    # StockTwits sentiment
    try:
        twits_sentiment = stocktwits.get_sentiment(query)
        context_parts.append(f"📈 StockTwits Sentiment: {twits_sentiment}")
    except Exception as e:
        context_parts.append(f"📈 StockTwits failed: {str(e)}")

    # Reddit Sentiment + Posts
    try:
        symbol_keyword = extract_symbol(query) or query.split()[0]  # fallback to first word if unknown
        reddit_sentiment = reddit.get_reddit_sentiment(symbol_keyword)
        reddit_posts = reddit.get_reddit_posts(symbol_keyword)
        context_parts.append(f"👥 Reddit Sentiment Score: {reddit_sentiment}")

        if reddit_posts:
            context_parts.append("👥 Reddit Top Posts:")
            for post in reddit_posts[:3]:
                context_parts.append(f"- {post['title']} (👍 {post['upvotes']})")
        else:
            context_parts.append("👥 No significant Reddit posts found.")
    except Exception as e:
        context_parts.append(f"👥 Reddit data failed: {str(e)}")

    return "\n".join(context_parts)

from app.services.llm import gemini  # Gemini LLM wrapper

import re

def extract_symbol(query: str) -> str:
    query = query.upper()
    if "RELIANCE POWER" in query:
        return "RELIANCEP"
    elif "TESLA" in query or "TSLA" in query:
        return "TSLA"
    elif "APPLE" in query or "AAPL" in query:
        return "AAPL"
    elif "GOOGLE" in query or "GOOGL" in query:
        return "GOOGL"
    elif "MICROSOFT" in query or "MSFT" in query:
        return "MSFT"
    elif "AMAZON" in query or "AMZN" in query:
        return "AMZN"
    elif "RELIANCE" in query:
        return "RELIANCE"
    elif "INFY" in query or "INFOSYS" in query:
        return "INFY"
    elif "TATA" in query:
        return "TATAMOTORS"
    match = re.search(r'\b[A-Z]{3,5}\b', query)
    return match.group(0) if match else ""

async def build_context(query: str) -> str:
    context_parts = [f"🔍 User Question: {query}"]

    symbol = extract_symbol(query)
    if not symbol:
        context_parts.append("⚠️ Could not extract stock symbol from the query.")
        return "\n".join(context_parts)

    context_parts.append(f"\n📌 Interpreted Stock Symbol: {symbol}")

    try:
        stock = await get_stock_context(symbol)
    except Exception as e:
        stock = f"❌ Failed to fetch stock data: {e}"

    try:
        news = await get_news_context(query)
    except Exception as e:
        news = f"❌ Failed to fetch news data: {e}"

    try:
        sentiment = await get_sentiment_context(query)
    except Exception as e:
        sentiment = f"❌ Failed to fetch sentiment data: {e}"

    context_parts.append(f"\n📊 Stock Context:\n{stock}")
    context_parts.append(f"\n📰 News Context:\n{news}")
    context_parts.append(f"\n🧠 Sentiment Context:\n{sentiment}")

    context_parts.append("\n🔎 Data Confidence: This analysis is based on available data. Some services may have failed or returned partial results. Interpret insights accordingly.")

    return "\n".join(context_parts)

async def generate_answer(query: str) -> str:
    context = await build_context(query)

    prompt = f"""
You are SmartStocks, an intelligent financial assistant. Based on the following data:
{context}

Please generate a detailed, analytical, and helpful answer for the user question:
"{query}"

- Show the entire news availible to you to help the user decide if the stock is good or not in detail.
- Cross-analyze insights across stock data, news, and crowd sentiment.
- If data sources conflict, explain the discrepancy.
- Offer a balanced perspective, but do not guarantee outcomes.
- Close with a tip or market observation.
- If Reddit posts are available, quote 2-3 of the most relevant titles and summarize sentiment.
Answer:
"""

    answer = await gemini.generate(prompt)
    return answer
