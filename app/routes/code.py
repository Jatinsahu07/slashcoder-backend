from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/code", tags=["Code Execution"])

JUDGE0_URL = "https://api.judge0.com/submissions?base64_encoded=false&wait=true"


@router.post("/run")
async def run_code(payload: dict):
    """
    Execute code via Judge0 (non-blocking async).
    Payload example:
    {
        "source_code": "...",
        "language_id": 71,
        "stdin": "input..."
    }
    """
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(JUDGE0_URL, json=payload)

        if res.status_code != 201 and res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code,
                detail=res.text
            )

        return res.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Judge0 error: {e}")
