# app/routes/stats.py
from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from app.utils.firebase_init import db

router = APIRouter(prefix="/api", tags=["User Stats"])


@router.post("/update-stats")
async def update_stats(payload: dict):
    """
    Update user stats after a match.
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

    # -----------------------------------
    # WIN/LOSS/POINTS
    # -----------------------------------
    won = payload.get("won", False)
    win_inc = 1 if won else 0
    loss_inc = 0 if won else 1
    points_inc = 100 if won else 20

    # -----------------------------------
    # XP + LEVEL
    # -----------------------------------
    incoming_xp = int(payload.get("xp", 0))
    current_xp = int(user.get("xp", 0))
    new_xp = current_xp + incoming_xp

    new_level = 1 + new_xp // 100

    # -----------------------------------
    # Firestore update
    # -----------------------------------
    update_data = {
        "wins": firestore.Increment(win_inc),
        "losses": firestore.Increment(loss_inc),
        "totalPoints": firestore.Increment(points_inc),
        "xp": new_xp,        # XP stays a number (consistent)
        "level": new_level,  # Level separate field
    }

    if "badge" in payload:
        update_data["badge"] = payload["badge"]

    user_ref.set(update_data, merge=True)

    return {
        "ok": True,
        "wins_inc": win_inc,
        "losses_inc": loss_inc,
        "points_added": points_inc,
        "new_xp": new_xp,
        "new_level": new_level
    }

@router.get("/user-stats/{uid}")
async def get_user_stats(uid: str):
    """
    Return user's wins, losses, xp for dashboard & profile.
    Frontend calls this on every page load.
    """

    try:
        snap = db.collection("users").document(uid).get()
    except Exception as e:
        return {"error": f"Firestore error: {e}"}

    if not snap.exists:
        # return default zero stats
        return {
            "wins": 0,
            "losses": 0,
            "xp": 0,
            "level": 1
        }

    data = snap.to_dict()

    xp = int(data.get("xp", 0))
    level = 1 + xp // 100

    return {
        "wins": data.get("wins", 0),
        "losses": data.get("losses", 0),
        "xp": xp,
        "level": level
    }

