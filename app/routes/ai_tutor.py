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

MODEL = "gemini-1.5-flash"

def load_model():
    return genai.GenerativeModel(MODEL)

# Normal Response
@router.post("/tutor")
async def ai_tutor(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()
    
    if not prompt:
        return {"response": "⚠️ Prompt is empty."}

    model = load_model()

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 300
            }
        )

        if response.text:
            return {"response": response.text}

        return {"response": "⚠️ Gemini returned empty content."}

    except Exception as e:
        print("Gemini Error:", e)
        return JSONResponse(
            {"response": f"⚠️ Error: {e}"}, status_code=500
        )

# Streaming Response
@router.post("/tutor/stream")
async def ai_tutor_stream(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return StreamingResponse(iter(["⚠️ Empty prompt"]), media_type="text/plain")

    model = load_model()

    def stream_output():
        try:
            response = model.generate_content(
                prompt,
                stream=True,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 300
                }
            )

            for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            yield f"[Error] {e}"

    return StreamingResponse(stream_output(), media_type="text/plain")
