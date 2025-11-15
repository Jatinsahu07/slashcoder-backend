from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
import google.generativeai as genai
import os

router = APIRouter(prefix="/ai", tags=["Slash AI"], dependencies=[])

# -------------------------------------------------
# Gemini Setup
# -------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ Missing GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"         # works for chat
FALLBACK_MODEL = "gemini-1.5-flash"     # guaranteed working

def load_model():
    try:
        return genai.GenerativeModel(MODEL_NAME)
    except:
        return genai.GenerativeModel(FALLBACK_MODEL)

# -------------------------------------------------
# ✨ Normal (non-streaming) Response
# -------------------------------------------------
@router.post("/tutor")
async def ai_tutor(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return {"response": "⚠️ Empty prompt."}

    model = load_model()

    try:
        response = model.generate_content(
            [prompt],   # <<< IMPORTANT FOR GEMINI 2.x
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 350,
            }
        )

        # Gemini 2.x returns "candidates[0].content.parts"
        if not response.candidates:
            return {"response": "⚠️ Gemini returned no response."}

        parts = response.candidates[0].content.parts
        if not parts:
            return {"response": "⚠️ Gemini returned empty content."}

        text = parts[0].text if hasattr(parts[0], "text") else ""

        if not text:
            return {"response": "⚠️ Gemini returned no text content."}

        return {"response": text}

    except Exception as e:
        print("Gemini error:", e)
        return JSONResponse({"response": f"⚠️ Error: {e}"}, status_code=500)

# -------------------------------------------------
# ⚡ Streaming Response
# -------------------------------------------------
@router.post("/tutor/stream")
async def ai_tutor_stream(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return StreamingResponse(iter(["⚠️ Empty prompt"]), media_type="text/plain")

    model = load_model()

    def generate_stream():
        try:
            response = model.generate_content(
                [prompt], 
                stream=True,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 350,
                }
            )

            for chunk in response:
                if chunk.candidates:
                    parts = chunk.candidates[0].content.parts
                    for p in parts:
                        if hasattr(p, "text"):
                            yield p.text

        except Exception as e:
            yield f"[Error] {e}"

    return StreamingResponse(generate_stream(), media_type="text/plain")
