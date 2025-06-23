from fastapi import FastAPI
from app.routes import chat, stocks, news, notify

app = FastAPI(title="StockBot Backend")

# Register routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chatbot"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["Stocks"])
app.include_router(news.router, prefix="/api/news", tags=["News"])
app.include_router(notify.router, prefix="/api/notify", tags=["Notifications"])
app.include_router(chat.router, prefix="/chat", tags=["Chatbot"])

@app.get("/")
async def root():
    return {"status": "StockBot backend is running 🚀"}
