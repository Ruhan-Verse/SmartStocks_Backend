from fastapi import APIRouter, Query
from app.services.fetchers.news_fallback import get_latest_news

router = APIRouter()

@router.get("/")
async def news_base():
    return {"message": "News endpoint (To be implemented)"}

@router.get("/company")
async def get_company_news(name: str = Query(..., description="Company name or keyword")):
    return await get_latest_news(name)