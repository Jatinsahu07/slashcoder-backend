from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/ai", tags=["Slash AI"], dependencies=[])

# ---------------------------------------------
# Gemini API Setup
# ---------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment")

genai.configure(api_key=GEMINI_API_KEY)

# Gemini 2.5 Models
PREFERRED_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-2.5-flash-lite"


def get_model():
    try:
        return genai.GenerativeModel(PREFERRED_MODEL)
    except:
        return genai.GenerativeModel(FALLBACK_MODEL)

# ---------------------------------------------
# ✨ FIXED: Normal Tutor Endpoint
# ---------------------------------------------
@router.post("/tutor")
async def ai_tutor(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return {"response": "⚠️ Empty prompt."}

    model = get_model()

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 350,
            }
        )

        # Gemini 2.5: extract text safely
        if response.parts:
            text = "".join([p.text for p in response.parts if hasattr(p, "text")])
        else:
            text = "⚠️ No content returned from Gemini."

        return {"response": text}

    except Exception as e:
        print("Gemini error:", e)
        return JSONResponse({"response": f"⚠️ Error: {e}"}, status_code=500)


# ---------------------------------------------
# ✨ FIXED: Streaming Endpoint
# ---------------------------------------------
@router.post("/tutor/stream")
async def ai_tutor_stream(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return StreamingResponse(iter(["⚠️ Empty prompt"]), media_type="text/plain")

    model = get_model()

    def stream_data():
        try:
            for chunk in model.generate_content(
                prompt,
                stream=True,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 350
                }
            ):
                if chunk.parts:
                    for p in chunk.parts:
                        if hasattr(p, "text"):
                            yield p.text
        except Exception as e:
            yield f"[Error] {e}"

    return StreamingResponse(stream_data(), media_type="text/plain")
