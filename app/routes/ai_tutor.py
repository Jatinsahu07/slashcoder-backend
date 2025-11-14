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

# -------------------------------------------------
# 🚀 Gemini 2.5 Models (Latest & Supported)
# -------------------------------------------------
PREFERRED_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-2.5-flash-lite"


def get_model():
    """
    Always returns a valid generative model.
    Falls back automatically if preferred model is unavailable.
    """
    try:
        return genai.GenerativeModel(PREFERRED_MODEL)
    except Exception as e:
        print(f"⚠️ Preferred model failed: {e}")
        print(f"→ Falling back to {FALLBACK_MODEL}")
        return genai.GenerativeModel(FALLBACK_MODEL)


# -------------------------------------------------
# 🧠 Standard AI Tutor Endpoint
# -------------------------------------------------
@router.post("/tutor")
async def ai_tutor(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return {"response": "⚠️ Empty prompt."}

    model = get_model()

    try:
        result = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.6,
                "max_output_tokens": 250,
                "top_p": 0.9
            },
        )

        text = getattr(result, "text", None)
        if not text:
            text = "⚠️ No response."

        return {"response": text}

    except Exception as e:
        print("Gemini Error:", e)
        return JSONResponse({"response": f"⚠️ Error: {e}"}, status_code=500)


# -------------------------------------------------
# ⚡ Streaming Tutor Endpoint
# -------------------------------------------------
@router.post("/tutor/stream")
async def ai_tutor_stream(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return StreamingResponse(iter(["⚠️ Empty prompt"]), media_type="text/plain")

    model = get_model()

    def stream_response():
        """
        Streams tokens continuously from Gemini 2.5.
        """
        try:
            # New streaming method (works for 2.5 Flash)
            for chunk in model.generate_content_stream(
                prompt,
                generation_config={"temperature": 0.65},
            ):
                text = getattr(chunk, "text", None)

                # Some chunks may contain structured parts
                if not text and hasattr(chunk, "parts"):
                    try:
                        text = chunk.parts[0].text
                    except:
                        pass

                if text:
                    yield text

        except Exception as e:
            yield f"[Error] {e}"

    return StreamingResponse(stream_response(), media_type="text/plain")
