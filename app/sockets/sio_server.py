# app/sockets/sio_server.py
# -------------------------------------------------------
# Slashcoder Unified Socket.IO Server
# - Uses the SINGLE sio instance from matchmaking.py
# - Adds only chatroom events here
# -------------------------------------------------------

from app.sockets.matchmaking import sio   # ← ONLY import sio (NO register function)


# -------------------------------------------------------
# CHATROOM EVENTS
# -------------------------------------------------------

@sio.event
async def join_room(sid, data):
    """
    data = { roomId, username }
    """
    room = data.get("roomId")
    username = data.get("username", "Anonymous")

    if not room:
        print(f"[join_room] Missing roomId from {sid}")
        return

    await sio.enter_room(sid, room)
    print(f"[CHAT] {username} joined {room}")

    await sio.emit(
        "system_message",
        {"msg": f"{username} joined {room}", "roomId": room},
        room=room
    )


@sio.event
async def send_message(sid, data):
    """
    data = { roomId, text, senderName }
    """
    room = data.get("roomId")
    text = data.get("text")
    sender = data.get("senderName", "Anonymous")

    if not room or not text:
        print(f"[send_message] Invalid msg from {sid}")
        return

    print(f"[CHAT][{room}] {sender}: {text}")

    await sio.emit(
        "receive_message",
        {
            "roomId": room,
            "text": text,
            "senderName": sender
        },
        room=room
    )
