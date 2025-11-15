# app/routes/ai_tutor.py
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
import google.generativeai as genai
import os

router = APIRouter(prefix="/ai", tags=["Slash AI"], dependencies=[])

# -------------------------------------------------
# 🔐 Gemini Setup
# -------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ Missing GEMINI_API_KEY environment variable")

genai.configure(api_key=GEMINI_API_KEY)

# Best stable free-tier models
PREFERRED_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-1.5-flash"

def model_loader():
    try:
        return genai.GenerativeModel(PREFERRED_MODEL)
    except:
        return genai.GenerativeModel(FALLBACK_MODEL)


# =================================================
# 🟩 NORMAL (NON-STREAMING) RESPONSE
# =================================================
@router.post("/tutor")
async def ai_tutor(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return {"response": "⚠️ Empty prompt."}

    model = model_loader()

    try:
        response = model.generate_content(
            [prompt],
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 512,
            }
        )

        # Make sure response exists
        if not hasattr(response, "candidates") or not response.candidates:
            return {"response": "⚠️ Gemini returned no response."}

        candidate = response.candidates[0]
        parts = candidate.content.parts if hasattr(candidate, "content") else []

        text = ""
        for part in parts:
            if hasattr(part, "text"):
                text += part.text

        if not text:
            return {"response": "⚠️ Gemini returned empty content."}

        return {"response": text}

    except Exception as e:
        print("Gemini Error:", e)
        return JSONResponse({"response": f"⚠️ Error: {e}"}, status_code=500)



# =================================================
# ⚡ STREAMING RESPONSE — FULLY FIXED
# =================================================
@router.post("/tutor/stream")
async def ai_tutor_stream(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return StreamingResponse(iter(["⚠️ Empty prompt"]), media_type="text/plain")

    model = model_loader()

    def generate_stream():
        try:
            response = model.generate_content(
                [prompt],
                stream=True,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 512,
                }
            )

            for chunk in response:

                # ---------------------------------------------
                # 🔥 SAFETY FIXES FOR GEMINI 2.5 STREAMING
                # ---------------------------------------------

                # 1) chunk has no candidates → skip
                if not hasattr(chunk, "candidates") or not chunk.candidates:
                    continue

                candidate = chunk.candidates[0]

                # 2) candidate has no content → skip safely
                if not hasattr(candidate, "content") or not candidate.content:
                    continue

                # 3) Text extraction from parts
                for part in candidate.content.parts:
                    if hasattr(part, "text") and part.text:
                        yield part.text

        except Exception as e:
            yield f"[Error] {e}"

    return StreamingResponse(generate_stream(), media_type="text/plain")
