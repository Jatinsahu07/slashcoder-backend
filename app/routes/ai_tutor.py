from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
import google.generativeai as genai
import os

router = APIRouter(prefix="/ai", tags=["Slash AI"], dependencies=[])

# Gemini Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "models/chat-bison-001"
FALLBACK_MODEL = "models/text-bison-001"

def load_model():
    try:
        return genai.GenerativeModel(MODEL_NAME)
    except:
        return genai.GenerativeModel(FALLBACK_MODEL)

@router.post("/tutor")
async def ai_tutor(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return {"response": "⚠️ Empty prompt."}

    model = load_model()

    try:
        response = model.generate_content(prompt)

        if not response:
            return {"response": "⚠️ Empty response."}

        return {"response": response.text}

    except Exception as e:
        print("Gemini Error:", e)
        return JSONResponse({"response": f"⚠️ Error: {e}"}, status_code=500)

@router.post("/tutor/stream")
async def ai_tutor_stream(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return StreamingResponse(iter(["⚠️ Empty prompt"]), media_type="text/plain")

    model = load_model()

    def generate_stream():
        try:
            response = model.generate_content(prompt, stream=True)

            for chunk in response:
                if hasattr(chunk, "text") and chunk.text:
                    yield chunk.text

        except Exception as e:
            yield f"[Error] {e}"

    return StreamingResponse(generate_stream(), media_type="text/plain")
