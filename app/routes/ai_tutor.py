from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
import google.generativeai as genai
import os, time
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/ai", tags=["Slash AI"])

# -------------------------------------------------
# 🔐 Gemini API Setup
# -------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

genai.configure(api_key=GEMINI_API_KEY)

# Gemini 2.5 Models
PREFERRED_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-2.5-flash-lite"

def get_model():
    try:
        return genai.GenerativeModel(PREFERRED_MODEL)
    except:
        return genai.GenerativeModel(FALLBACK_MODEL)


# -------------------------------------------------
# 🧠 Standard Tutor Endpoint
# -------------------------------------------------
@router.post("/tutor")
async def ai_tutor(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return {"response": "⚠️ Empty prompt."}

    model = get_model()

    try:
        result = model.generate(
            prompt,
            temperature=0.6,
            max_output_tokens=350
        )

        return {"response": result.text}

    except Exception as e:
        print("Gemini error:", e)
        return JSONResponse({"response": f"⚠️ Error: {e}"}, status_code=500)


# -------------------------------------------------
# ⚡ Streaming Tutor Endpoint (Gemini 2.5 Correct)
# -------------------------------------------------
@router.post("/tutor/stream")
async def ai_tutor_stream(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return StreamingResponse(iter(["⚠️ Empty prompt"]), media_type="text/plain")

    model = get_model()

    def stream_response():
        try:
            # NEW correct API for Gemini 2.5 streaming:
            for chunk in model.generate(
                prompt,
                stream=True,
                temperature=0.7
            ):
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            yield f"[Error] {e}"

    return StreamingResponse(stream_response(), media_type="text/plain")
