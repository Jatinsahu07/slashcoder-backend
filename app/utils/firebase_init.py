import firebase_admin
from firebase_admin import credentials, auth, firestore
import os, json

# Load service account JSON from Fly secret
FIREBASE_KEY = os.getenv("FIREBASE_KEY")

if not FIREBASE_KEY:
    raise Exception("Missing FIREBASE_KEY in environment variables.")

# Convert secret string → dict
service_account_info = json.loads(FIREBASE_KEY)

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Exported auth
firebase_auth = auth
