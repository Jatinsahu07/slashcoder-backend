# slashcoder-backend/app/routes/sync_user.py
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["User Sync"])

@router.get("/sync-user")
async def sync_user():
    return {"ok": True}
