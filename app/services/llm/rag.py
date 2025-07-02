# ✅ rag.py (Updated for Gemini 1.5 Pro)
import os
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv
from app.services.fetchers import sector
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro")

def is_aggregate_query(query: str) -> bool:
    query = query.lower()
    keywords = [
        "top performing", "top gainers", "top losers", "best tech stocks",
        "top 5", "top 10", "most active", "sector leaders", "highest growth",
        "sector performance", "ai companies","sector analysis", "technology sector",
        "healthcare sector", "energy sector", "renewable energy sector",
        "clean energy", "market trends", "industry trends", "dividend paying"
    ]
    return any(kw in query for kw in keywords)

def is_sector_theme_query(query: str) -> bool:
    keywords = ["renewable energy", "AI", "artificial intelligence", "EV", "semiconductors", "cloud computing", "biotech", "green energy", "cybersecurity"]
    return any(kw.lower() in query.lower() for kw in keywords)



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

    # ✅ Check for aggregate-style queries first
    if is_aggregate_query(query):
        try:
            sector_info = await sector.get_sector_performance()
            context_parts.append("\n📊 Sector Performance:")
            for item in sector_info:
                context_parts.append(f"- {item['sector']}: {item['change']}")
        except Exception as e:
            context_parts.append(f"\n📊 Sector data failed: {str(e)}")
        context_parts.append("\n📝 Note: This is sector-level analysis. For deeper insights, try specifying individual companies.")
        return "\n".join(context_parts)
    
    # 🌐 Thematic Sector (e.g., "Should I invest in renewable energy?")
    if is_sector_theme_query(query):
        try:
            thematic_news = await get_news_context(query)
        except Exception as e:
            thematic_news = f"❌ Failed to fetch sector news: {e}"
        
        try:
            thematic_sentiment = await get_sentiment_context(query)
        except Exception as e:
            thematic_sentiment = f"❌ Failed to fetch sentiment: {e}"

        context_parts.append(f"\n📰 Sector News Context:\n{thematic_news}")
        context_parts.append(f"\n🧠 Sentiment Summary:\n{thematic_sentiment}")
        context_parts.append("\n📝 Note: This analysis is based on news and sentiment for the sector/theme, not a single company.")
        return "\n".join(context_parts)


    # ✅ Proceed to extract individual stock symbol
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

1. Stock Overview
   - Show current price, daily high/low, and performance trend.  
   - Interpret if the price movement is bullish, bearish, or neutral.

2. News Context 
   - Summarize 3–5 of the most relevant headlines.  
   - Mention which are positive, neutral, or negative.

3. Sentiment Analysis
   - HuggingFace: % score and tone.  
   - Reddit: summarize sentiment of 2–3 top posts (quote titles if available).  
   - StockTwits (if available).

4. Data Conflicts & Observations 
   - Do stock price & sentiment contradict? Explain.  
   - Any red flags or data gaps?

5. Recommendation by Investor Type
   - Short-term trader: Give trade signal if technicals suggest action.  
   - Long-term investor: Analyze value, fundamentals, and future outlook.  
   - Options trader: Suggest strategy if volatility is high.

6. Risks to Watch
   - Any major regulatory, market, or competitive threats?

7. Conclusion & Tip
   - Final call based on evidence. Give a clear signal (Buy/Hold/Sell/Caution)  
   - Provide a smart investing tip or next step.

Do not hallucinate or make up data. If data is missing, explain clearly what is missing and how it would affect the answer.

If some data sources (like stock price, Reddit, GNews, StockTwits) are missing, DO NOT focus on that. Instead:

- Educate the user about the overall investment theme (e.g., Renewable Energy sector).
- Highlight sector trends using historical or policy-related information.
- List 3–5 relevant stocks or ETFs with a short description of their role in the sector.
- Provide risk vs reward for different types of investors (long-term, short-term, options).
- Offer a bottom-line recommendation: Is this a promising space to watch/invest in?
- Give a useful investor tip to close.
Stay confident and useful. If data is missing, acknowledge it in 1 line only — don’t dwell on it.
Answer:
"""

    answer = await gemini.generate(prompt)
    return answer
