import os
import json
import firebase_admin
from firebase_admin import credentials, auth, firestore

# ------------------------------------
# Load Firebase Admin Credentials
# ------------------------------------
FIREBASE_KEY = os.getenv("FIREBASE_KEY")

if not FIREBASE_KEY:
    raise Exception("❌ Missing FIREBASE_KEY environment variable. "
                    "Add it in Railway → Variables.")

try:
    # Railway stores JSON in a single-line env var → convert to dict
    service_account_info = json.loads(FIREBASE_KEY)
except json.JSONDecodeError as e:
    raise Exception("❌ FIREBASE_KEY is not valid JSON. "
                    "Make sure it's pasted as one line.") from e

# ------------------------------------
# Initialize Firebase
# ------------------------------------
if not firebase_admin._apps:  # prevents re-initialization
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)

# ------------------------------------
# Firestore + Auth
# ------------------------------------
db = firestore.client()
firebase_auth = auth
