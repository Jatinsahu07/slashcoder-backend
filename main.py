# main.py
import os
import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import Firebase init (must be imported first)
from app.utils.firebase_init import db

# Import routes
from app.routes import ai_tutor, stats
from app.routes.practice import router as practice_router

# Import Socket.IO shared server
from app.sockets.sio_server import sio


# ---------------------------------------------------------
# Create FastAPI app (ONLY for HTTP routes)
# ---------------------------------------------------------
fastapi_app = FastAPI(title="SlashCoder Backend")

# CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:3000",
        "https://slashcoder-frontend.vercel.app",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
fastapi_app.include_router(ai_tutor.router)
fastapi_app.include_router(stats.router)
fastapi_app.include_router(practice_router)


@fastapi_app.get("/")
async def home():
    return {"message": "SlashCoder backend LIVE on Railway!"}


# ---------------------------------------------------------
# Create Socket.IO ASGI app
# ---------------------------------------------------------
socket_app = socketio.ASGIApp(
    sio,
    other_asgi_app=fastapi_app,
    socketio_path="/socket.io"
)

# ---------------------------------------------------------
# The ASGI app exported to Uvicorn/Railway:
# ---------------------------------------------------------
app = socket_app
