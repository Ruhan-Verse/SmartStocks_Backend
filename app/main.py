from fastapi import FastAPI
from app.routes import chat, stocks, news, notify
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="StockBot Backend")

# Register routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chatbot"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["Stocks"])
app.include_router(news.router, prefix="/api/news", tags=["News"])
app.include_router(notify.router, prefix="/api/notify", tags=["Notifications"])
app.include_router(chat.router, prefix="/chat", tags=["Chatbot"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "StockBot backend is running 🚀"}
