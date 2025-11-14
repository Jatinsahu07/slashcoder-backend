# app/sockets/sio_server.py
# -------------------------------------------------------
# Slashcoder Unified Socket.IO Server
# Chatrooms + Matchmaking share the SAME `sio` instance
# -------------------------------------------------------

from app.sockets.matchmaking import sio  # ← import the single Socket.IO server


# -------------------------------------------------------
# 🔹 Chatroom: Join Room
# -------------------------------------------------------
@sio.event
async def join_room(sid, data):
    """
    Join a socket.io chatroom
    data example:
    {
        "roomId": "python-room",
        "username": "Jatin"
    }
    """

    room = data.get("roomId")
    username = data.get("username", "Anonymous")

    if not room:
        print(f"[join_room] ERROR: missing roomId (sid={sid})")
        return

    # Join the room
    await sio.enter_room(sid, room)
    print(f"[CHAT] {username} joined room {room}")

    # Notify everyone in that room
    await sio.emit(
        "system_message",
        {
            "roomId": room,
            "msg": f"{username} joined the room"
        },
        room=room
    )


# -------------------------------------------------------
# 🔹 Chatroom: Send Message
# -------------------------------------------------------
@sio.event
async def send_message(sid, data):
    """
    Broadcast a user message to the room
    data example:
    {
        "roomId": "python-room",
        "text": "Hello everyone!",
        "senderName": "Jatin"
    }
    """

    room = data.get("roomId")
    text = data.get("text")
    sender = data.get("senderName", "Anonymous")

    # Validation
    if not room:
        print(f"[send_message] ERROR: missing roomId (sid={sid})")
        return
    if not text:
        print(f"[send_message] ERROR: empty message (sid={sid})")
        return

    print(f"[CHAT][{room}] {sender}: {text}")

    # Broadcast message to room
    await sio.emit(
        "receive_message",
        {
            "roomId": room,
            "text": text,
            "senderName": sender
        },
        room=room
    )


# -------------------------------------------------------
# 🔹 OPTIONAL: User disconnected from chat (not required)
# -------------------------------------------------------
@sio.event
async def disconnect(sid):
    print(f"[CHAT] socket disconnected: {sid}")
