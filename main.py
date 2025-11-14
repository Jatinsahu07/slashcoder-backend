from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import os

# Import Firebase (ensures initialization)
from app.core.firebase import db

# Import routes
from app.sockets.sio_server import sio
from app.routes import ai_tutor, stats
from app.routes.practice import router as practice_router

# ------------------------------------
# FastAPI instance
# ------------------------------------
app = FastAPI(title="SlashCoder Backend")

# ------------------------------------
# CORS for Railway + Vercel + Localhost
# ------------------------------------
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

ALLOWED_ORIGINS = [
    FRONTEND_URL,                                    # dynamic
    "http://localhost:3000",
    "https://slashcoder-frontend.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------
# API Routes
# ------------------------------------
app.include_router(ai_tutor.router)
app.include_router(stats.router)
app.include_router(practice_router)

@app.get("/")
async def home():
    return {"message": "SlashCoder backend LIVE on Railway!"}

# ------------------------------------
# Socket.IO ASGI bridge
# ------------------------------------
socket_app = socketio.ASGIApp(
    sio,
    other_asgi_app=app,
    socketio_path="/socket.io"
)

# WebSocket endpoint for frontend
app.mount("/ws", socket_app)
