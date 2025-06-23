from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def notify_base():
    return {"message": "Notify endpoint (To be implemented)"}