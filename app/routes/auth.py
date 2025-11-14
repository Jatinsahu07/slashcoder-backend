# slashcoder-backend/app/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from app.utils.firebase_init import firebase_auth, db  # ✅ Make sure this file exists and initializes Firebase

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
    Create a new user using Firebase Admin SDK.
    """
    try:
        user_record = firebase_auth.create_user(
            email=user.email,
            password=user.password
        )

        # Create Firestore doc
        db.collection("users").document(user_record.uid).set({
            "email": user.email,
            "wins": 0,
            "losses": 0,
        })

        return {"message": "User created", "uid": user_record.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------
# Verify Token Dependency
# -------------------------------
async def verify_token(request: Request):
    header = request.headers.get("Authorization")
    if not header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    id_token = header.strip()
    try:
        decoded = firebase_auth.verify_id_token(id_token)
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# -------------------------------
# Token Verification Endpoint
# -------------------------------
@router.get("/verify")
def verify(decoded=Depends(verify_token)):
    return {"verified": True, "uid": decoded.get("uid"), "email": decoded.get("email")}
