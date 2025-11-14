from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio

from app.sockets.sio_server import sio
from app.routes import ai_tutor
from app.routes import stats
from app.routes.practice import router as practice_router

app = FastAPI(title="SlashCoder Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTERS
app.include_router(ai_tutor.router)
app.include_router(stats.router)
app.include_router(practice_router)

@app.get("/")
async def home():
    return {"message": "SlashCoder backend OK"}

# IMPORTANT FIX:
socket_app = socketio.ASGIApp(
    sio,
    other_asgi_app=app,
    socketio_path="/socket.io"
)

# MOUNT AT /ws (final socket path = /ws/socket.io)
app.mount("/ws", socket_app)
