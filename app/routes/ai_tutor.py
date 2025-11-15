from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse
import google.generativeai as genai
import os

router = APIRouter(prefix="/ai", tags=["Slash AI"])

# -------------------------------------------------
# Gemini Setup
# -------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise Exception("Missing GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"        # ✔ Supported by your key
FALLBACK_NAME = "gemini-2.0-flash"     # ✔ Backup option


def load_model():
    try:
        return genai.GenerativeModel(MODEL_NAME)
    except:
        return genai.GenerativeModel(FALLBACK_NAME)


# -------------------------------------------------
# Non-streaming
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
            [prompt],   # IMPORTANT for 2.x models
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 500
            }
        )

        if not response.candidates:
            return {"response": "⚠️ Gemini returned no output."}

        parts = response.candidates[0].content.parts
        text = "".join(p.text for p in parts if hasattr(p, "text"))

        if not text:
            return {"response": "⚠️ Gemini returned empty text."}

        return {"response": text}

    except Exception as e:
        print("Gemini Error:", e)
        return JSONResponse({"response": f"⚠️ Error: {e}"}, status_code=500)


# -------------------------------------------------
# Streaming
# -------------------------------------------------
@router.post("/tutor/stream")
async def ai_tutor_stream(request: Request):

    data = await request.json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return StreamingResponse(iter(["⚠️ Empty prompt"]), media_type="text/plain")

    model = load_model()

    def stream():
        try:
            res = model.generate_content(
                [prompt],
                stream=True,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 500
                }
            )

            for chunk in res:
                if chunk.candidates:
                    for part in chunk.candidates[0].content.parts:
                        if hasattr(part, "text"):
                            yield part.text

        except Exception as e:
            yield f"[Error] {e}"

    return StreamingResponse(stream(), media_type="text/plain")
