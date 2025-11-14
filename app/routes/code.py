from fastapi import APIRouter, HTTPException
import requests

router = APIRouter(prefix="/code", tags=["Code Execution"])

JUDGE0_URL = "https://api.judge0.com/submissions/?base64_encoded=false&wait=true"

@router.post("/run")
def run_code(payload: dict):
    """
    Execute code via Judge0 API.
    """
    try:
        res = requests.post(JUDGE0_URL, json=payload)
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
