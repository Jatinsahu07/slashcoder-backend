from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
import google.generativeai as genai
import os, time
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/ai", tags=["Slash AI"])

# -------------------------------------------------
# 🔐 Gemini Setup
# -------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

genai.configure(api_key=GEMINI_API_KEY)

PREFERRED_MODEL = "gemini-2.5-flash-lite"
FALLBACK_MODEL = "gemini-1.5-pro"


def get_model():
    """
    Return a ready-to-use GenerativeModel instance.
    """
    try:
        print(f"🔹 Using model: {PREFERRED_MODEL}")
        return genai.GenerativeModel(model_name=PREFERRED_MODEL)
    except Exception as e:
        print(f"⚠️ {PREFERRED_MODEL} unavailable → Falling back to {FALLBACK_MODEL}")
        print("Details:", e)
        return genai.GenerativeModel(model_name=FALLBACK_MODEL)


# -------------------------------------------------
# 🧠 Standard Tutor Endpoint (non-streaming)
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
             "temperature": 0.7,           # low = precise, less random
             "max_output_tokens": 150,     # ✨ limits the response length
             "top_p": 0.8,                 # balanced diversity
             "top_k": 20                   # focus on best words
             }

        )
        return {"response": getattr(result, "text", "No response.")}
    except Exception as e:
        print("Gemini error:", e)
        return JSONResponse({"response": f"⚠️ Error: {e}"}, status_code=500)


# -------------------------------------------------
# ⚡ Streaming Tutor Endpoint (auto-fallback)
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
            # ✅ If streaming method exists (newer SDK)
            if hasattr(model, "generate_content_stream"):
                for chunk in model.generate_content_stream(
                    prompt,
                    generation_config={"temperature": 0.7}
                ):
                    if getattr(chunk, "text", None):
                        yield chunk.text
            else:
                # ⚙️ Fallback: call once and yield in small pieces
                result = model.generate_content(
                    prompt,
                    generation_config={"temperature": 0.7}
                )
                text = getattr(result, "text", "Slash AI couldn't generate a reply.")
                for i in range(0, len(text), 40):
                    yield text[i : i + 40]
                    time.sleep(0.02)
        except Exception as e:
            yield f"[Error] {e}"

    return StreamingResponse(stream_response(), media_type="text/plain")
