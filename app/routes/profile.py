from fastapi import APIRouter, HTTPException
from app.utils.firebase_init import db  # Firestore ready

router = APIRouter(prefix="/profile", tags=["User Profile"])


@router.get("/{user_id}")
async def get_profile(user_id: str):
    """
    Fetch a user's profile from Firestore using UID.
    """

    try:
        user_doc = db.collection("users").document(user_id).get()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {e}")

    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    data = user_doc.to_dict()

    # Optional safety: never send password or auth info
    sensitive_fields = ["password", "hash", "token"]
    for key in sensitive_fields:
        data.pop(key, None)

    return data

