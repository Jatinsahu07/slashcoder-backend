import firebase_admin
from firebase_admin import credentials, auth, firestore
import os

# Define the path to the key
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIREBASE_KEY_PATH = os.path.join(BASE_DIR, "firebase_key.json")

print(f"🔍 Firebase key path: {FIREBASE_KEY_PATH}")
print(f"📂 Exists: {os.path.exists(FIREBASE_KEY_PATH)}")

# Initialize Firebase app (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)

# Initialize Firestore databasea
db = firestore.client()   # ✅ this line adds Firestore

# Export firebase auth and db
firebase_auth = auth
