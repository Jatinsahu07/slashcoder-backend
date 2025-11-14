from fastapi import APIRouter, HTTPException
from app.utils.firebase_init import db  # ensures Firestore is initialized

router = APIRouter(prefix="/profile", tags=["User Profile"])

@router.get("/{user_id}")
async def get_profile(user_id: str):
    """
    Fetch user profile data from Firestore using their UID.
    """
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    return user_doc.to_dict()
