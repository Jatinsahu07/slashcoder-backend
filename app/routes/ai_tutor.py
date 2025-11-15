from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
import google.generativeai as genai
import os

router = APIRouter(prefix="/ai", tags=["Slash AI"], dependencies=[])

# ------------------------------
# Gemini Setup
# ------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ Missing GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

PREFERRED_MODEL = "gemini-1.5-flash-latest"
FALLBACK_MODEL = "gemini-1.0-pro"


def load_model():
    try:
        return genai.GenerativeModel(PREFERRED_MODEL)
    except:
        return genai.GenerativeModel(FALLBACK_MODEL)


# ------------------------------
# Normal Response
# ------------------------------
@router.post("/tutor")
async def ai_tutor(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return {"response": "⚠️ Empty prompt."}

    model = load_model()

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 350,
            }
        )

        # Gemini returns candidates
        if not response.candidates:
            return {"response": "⚠️ Gemini returned no response."}

        parts = response.candidates[0].content.parts

        text = ""
        for p in parts:
            if hasattr(p, "text"):
                text += p.text

        if not text:
            return {"response": "⚠️ Gemini returned empty content."}

        return {"response": text}

    except Exception as e:
        print("Gemini Error:", e)
        return JSONResponse({"response": f"⚠️ Error: {e}"}, status_code=500)


# ------------------------------
# Streaming Response
# ------------------------------
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
                prompt,
                stream=True,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 350,
                }
            )

            for chunk in response:
                if chunk.candidates:
                    for part in chunk.candidates[0].content.parts:
                        if hasattr(part, "text"):
                            yield part.text

        except Exception as e:
            yield f"[Error] {e}"

    return StreamingResponse(generate_stream(), media_type="text/plain")
