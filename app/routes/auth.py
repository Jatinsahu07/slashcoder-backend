# slashcoder-backend/app/routes/auth.py

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from firebase_admin import firestore
from app.utils.firebase_init import firebase_auth, db

router = APIRouter(prefix="/auth", tags=["Authentication"])


# -------------------------------
# Models
# -------------------------------
class UserCredentials(BaseModel):
    email: str
    password: str


# -------------------------------
# Signup Route
# -------------------------------
@router.post("/signup")
def signup(user: UserCredentials):
    """
    Create a new Firebase user + initialize Firestore profile.
    """
    try:
        # Create account in Firebase Auth  
        user_record = firebase_auth.create_user(
            email=user.email,
            password=user.password
        )

        # Create Firestore user profile
        db.collection("users").document(user_record.uid).set({
            "email": user.email,
            "wins": 0,
            "losses": 0,
            "xp": 0,                                 # required for matchmaking
            "createdAt": firestore.SERVER_TIMESTAMP,
        })

        return {"message": "User created", "uid": user_record.uid}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------
# Verify Token Dependency
# -------------------------------
async def verify_token(request: Request):
    """
    Extract Bearer token from Authorization header and verify it.
    Frontend must send:  Authorization: Bearer <idToken>
    """
    header = request.headers.get("Authorization")

    if not header or not header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    # Extract only the token
    id_token = header.replace("Bearer ", "").strip()

    try:
        decoded = firebase_auth.verify_id_token(id_token)
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# -------------------------------
# Token Verification Endpoint
# -------------------------------
@router.get("/verify")
def verify(decoded = Depends(verify_token)):
    """
    Verifies token and returns the user info.
    """
    return {
        "verified": True,
        "uid": decoded.get("uid"),
        "email": decoded.get("email")
    }
