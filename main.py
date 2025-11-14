from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio

from app.sockets.sio_server import sio
from app.routes import ai_tutor
from app.routes import stats
from app.routes.practice import router as practice_router

# FastAPI instance
app = FastAPI(title="SlashCoder Backend", root_path="/")

# CORS for Vercel + Localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend.vercel.app",  # <-- change this
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(ai_tutor.router)
app.include_router(stats.router)
app.include_router(practice_router)

@app.get("/")
async def home():
    return {"message": "SlashCoder backend OK"}

# Socket.IO
socket_app = socketio.ASGIApp(
    sio,
    other_asgi_app=app,
    socketio_path="/socket.io"
)

# Final WebSocket endpoint → /ws/socket.io
app.mount("/ws", socket_app)
