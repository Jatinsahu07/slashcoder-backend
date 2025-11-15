# slashcoder-backend/app/routes/sync_user.py
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["User Sync"])

@router.post("/sync-user")
async def sync_user(payload: dict):
    return {"ok": True}

