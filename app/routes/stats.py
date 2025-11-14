# app/routes/stats.py
from fastapi import APIRouter, HTTPException
from app.utils.firebase_init import db

router = APIRouter(prefix="/api", tags=["User Stats"])

@router.post("/update-stats")
async def update_stats(payload: dict):
    """
    Update user stats after a match.
    Payload example:
    {
      "uid": "...",
      "won": true,
      "xp": 50,
      "badge": "Silver"
    }
    """
    uid = payload.get("uid")
    if not uid:
        raise HTTPException(status_code=400, detail="Missing uid")

    user_ref = db.collection("users").document(uid)
    snap = user_ref.get()

    if not snap.exists:
        raise HTTPException(status_code=404, detail="User not found")

    user = snap.to_dict()
    wins = user.get("wins", 0)
    losses = user.get("losses", 0)
    totalPoints = user.get("totalPoints", 0)

    if payload.get("won"):
        wins += 1
        totalPoints += 100  # 🏆 points per win
    else:
        losses += 1
        totalPoints += 20   # 🎯 participation points

    xp_obj = user.get("xp", {})
    xp_obj["xp"] = xp_obj.get("xp", 0) + payload.get("xp", 0)
    xp_obj["level"] = 1 + xp_obj["xp"] // 100

    user_ref.update({
        "wins": wins,
        "losses": losses,
        "totalPoints": totalPoints,
        "badge": payload.get("badge", user.get("badge", "Iron")),
        "xp": xp_obj,
    })
    return {"ok": True}
