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

# -------------------------------------------------
# Models (Free-tier compatible)
# -------------------------------------------------
PREFERRED_MODEL = "gemini-1.5-flash"   # Fast, reliable, works on free tier
FALLBACK_MODEL = "gemini-pro"          # Backup model


def load_model():
    """
    Load primary model, fallback if needed.
    """
    try:
        return genai.GenerativeModel(PREFERRED_MODEL)
    except Exception as e:
        print("❗ Primary model failed, using fallback:", e)
        return genai.GenerativeModel(FALLBACK_MODEL)


# -------------------------------------------------
# ✨ Normal (non-streaming) response
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
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 350,
            }
        )

        # Validate Gemini response
        if not response.candidates:
            return {"response": "⚠️ Gemini returned no response."}

        parts = response.candidates[0].content.parts
        if not parts:
            return {"response": "⚠️ Gemini returned empty content."}

        # Extract text
        text_output = ""
        for part in parts:
            if hasattr(part, "text"):
                text_output += part.text

        if not text_output.strip():
            return {"response": "⚠️ Gemini returned no text content."}

        return {"response": text_output}

    except Exception as e:
        print("Gemini Error:", e)
        return JSONResponse({"response": f"⚠️ Error: {e}"}, status_code=500)



# -------------------------------------------------
# ⚡ Streaming Response
# -------------------------------------------------
@router.post("/tutor/stream")
async def ai_tutor_stream(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return StreamingResponse(
            iter(["⚠️ Empty prompt"]), media_type="text/plain"
        )

    model = load_model()

    def stream_generator():
        try:
            stream = model.generate_content(
                prompt,
                stream=True,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 350,
                }
            )

            for chunk in stream:
                if chunk.candidates:
                    parts = chunk.candidates[0].content.parts
                    for p in parts:
                        if hasattr(p, "text"):
                            yield p.text

        except Exception as e:
            yield f"[Error] {e}"

    return StreamingResponse(stream_generator(), media_type="text/plain")
