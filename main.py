from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import os

# Import Firebase (ensures initialization)
from app.utils.firebase_init import db

# Import routes
from app.sockets.sio_server import sio
from app.routes import ai_tutor, stats
from app.routes.practice import router as practice_router

# ------------------------------------
# FastAPI application
# ------------------------------------
app = FastAPI(title="SlashCoder Backend")

# ------------------------------------
# CORS — Support Vercel + Localhost + Railway Preview Domains
# ------------------------------------
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

ALLOWED_ORIGINS = [
    FRONTEND_URL,
    "http://localhost:3000",
    "https://slashcoder-frontend.vercel.app",
    # Optional wildcard for Vercel preview deployments:
    "https://*.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------
# Normal API Routes
# ------------------------------------
app.include_router(ai_tutor.router)      # Slash AI
app.include_router(stats.router)         # User stats
app.include_router(practice_router)      # Practice problems

@app.get("/")
async def home():
    return {"message": "SlashCoder backend LIVE on Railway!"}

# ------------------------------------
# FIXED: Socket.IO ASGI bridge
# ------------------------------------
# ❗ IMPORTANT FIX:
# Remove other_asgi_app=app (was causing routing conflicts)
# Mount ASGIApp cleanly at /ws
# ------------------------------------
socket_app = socketio.ASGIApp(
    sio,
    socketio_path="/socket.io"   # Frontend connects using /ws/socket.io
)

# Mount the websocket server at /ws (final URL = /ws/socket.io/)
app.mount("/ws", socket_app)

# ------------------------------------
# END OF FILE — Everything working now
# ------------------------------------
