# main.py
import os
import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.applications import Starlette

# Load routes
from app.routes import ai_tutor, stats
from app.routes.practice import router as practice_router

# Load global Socket.IO server
from app.sockets.sio_server import sio


# ============================================================
# 🔥 UNIVERSAL CORS (WORKS WITH WEBSOCKETS + FASTAPI)
# ============================================================

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

allowed_origins = [
    FRONTEND_URL,
    "http://localhost:3000",
    "https://localhost:3000",
    "https://slashcoder-frontend.vercel.app",
    "https://*.vercel.app",      # allow ALL Vercel previews
    "*",                         # allow all domains for safety
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=86400,
    )
]


# ============================================================
# 🔵 FASTAPI APP (HTTP ROUTES ONLY)
# ============================================================

fastapi_app = FastAPI(title="SlashCoder Backend")

# Attach routers
fastapi_app.include_router(ai_tutor.router)
fastapi_app.include_router(stats.router)
fastapi_app.include_router(practice_router)

@fastapi_app.get("/")
async def home():
    return {"message": "SlashCoder backend LIVE on Railway"}


# ============================================================
# 🟣 SOCKET.IO ASGI APP (WEBSOCKETS ONLY)
# ============================================================

socket_app = socketio.ASGIApp(
    sio,
    other_asgi_app=fastapi_app,
    socketio_path="/socket.io"
)


# ============================================================
# 🟩 GLOBAL STARLETTE WRAPPER (APPLY CORS TO EVERYTHING)
# ============================================================

app = Starlette(middleware=middleware)
app.mount("/", socket_app)
