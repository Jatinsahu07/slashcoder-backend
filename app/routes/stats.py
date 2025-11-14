# app/routes/stats.py
from fastapi import APIRouter, HTTPException
from google.cloud import firestore
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
    # Calculate win/loss & total points
    # -----------------------------------
    won = payload.get("won", False)

    win_inc = 1 if won else 0
    loss_inc = 0 if won else 1
    points_inc = 100 if won else 20

    # -----------------------------------
    # XP handling (supports both number or dict)
    # -----------------------------------
    incoming_xp = int(payload.get("xp", 0))

    existing_xp = user.get("xp", 0)

    # If xp is dict like { "xp": 100, "level": 2 }
    if isinstance(existing_xp, dict):
        current_xp = existing_xp.get("xp", 0)
    else:
        current_xp = existing_xp  # numeric XP

    new_xp_total = current_xp + incoming_xp
    new_level = 1 + new_xp_total // 100

    xp_struct = {
        "xp": new_xp_total,
        "level": new_level
    }

    # -----------------------------------
    # Update Firestore atomically
    # -----------------------------------
    update_data = {
        "wins": firestore.Increment(win_inc),
        "losses": firestore.Increment(loss_inc),
        "totalPoints": firestore.Increment(points_inc),
        "xp": xp_struct,  # fully overwrite XP object
    }

    # Only overwrite badge if passed by frontend
    if "badge" in payload:
        update_data["badge"] = payload["badge"]

    user_ref.set(update_data, merge=True)

    return {
        "ok": True,
        "wins_inc": win_inc,
        "losses_inc": loss_inc,
        "points_added": points_inc,
        "new_xp": xp_struct,
    }
