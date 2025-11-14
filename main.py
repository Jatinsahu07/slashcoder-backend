from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio

from app.sockets.sio_server import sio
from app.routes import ai_tutor
from app.routes import stats
from app.routes.practice import router as practice_router

# ------------------------------------
# FastAPI instance
# ------------------------------------
app = FastAPI(title="SlashCoder Backend")

# ------------------------------------
# CORS (FINAL for Vercel + Localhost)
# ------------------------------------
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://slashcoder-frontend.vercel.app",  # 🚀 your frontend domain
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
    return {"message": "SlashCoder backend OK"}

# ------------------------------------
# Socket.IO ASGI App
# ------------------------------------
socket_app = socketio.ASGIApp(
    sio,
    other_asgi_app=app,
    socketio_path="/socket.io"   # ✔ matches frontend
)

# FINAL WebSocket endpoint:
# wss://slashcoder-backend.onrender.com/ws/socket.io
app.mount("/ws", socket_app)
