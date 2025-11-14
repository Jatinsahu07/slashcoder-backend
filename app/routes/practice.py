# slashcoder-backend/app/routes/practice.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import datetime

# Your curated practice problems
from app.data.practice_problems import PRACTICE_PROBLEMS

# Reuse Judge0 + Firestore from matchmaking
from app.sockets.matchmaking import (
    judge_run,
    compare_output,
    db,
    firestore
)

router = APIRouter(prefix="/api/practice", tags=["Practice"])


XP_MAP = {
    "Very Easy": 10,
    "Easy": 15,
    "Medium": 20
}


# ------------------- DATA MODELS -------------------
class RunPayload(BaseModel):
    language: str
    code: str
    stdin: str = ""


class SubmitPayload(BaseModel):
    uid: str
    pid: str
    language: str
    code: str


# ------------------- GET PROBLEMS -------------------
@router.get("/problems")
async def get_problems():
    """
    Returns all practice problems with metadata.
    """
    output = []

    for diff, problems in PRACTICE_PROBLEMS.items():
        for p in problems:
            output.append({
                "id": p["id"],
                "title": p["title"],
                "description": p["description"],
                "description_full": p.get("description_full", p["description"]),
                "input": p.get("input", ""),
                "output": p.get("output", ""),
                "example": p.get("example", ""),
                "constraints": p.get("constraints", ""),
                "explanation": p.get("explanation", ""),
                "difficulty": diff
            })

    return output


# ------------------- RUN (CUSTOM INPUT ONLY) -------------------
@router.post("/run")
async def run_code(payload: RunPayload):
    """
    Runs the user's code ONCE with custom input.
    Does NOT evaluate hidden tests.
    """

    try:
        result = await judge_run(
            payload.language,
            payload.code,
            payload.stdin or ""
        )

        return {
            "mode": "custom",
            "stdout": result or ""
        }

    except Exception as e:
        return {
            "mode": "custom",
            "error": str(e)
        }


# ------------------- SUBMIT (HIDDEN TESTS + XP) -------------------
@router.post("/submit")
async def submit_code(payload: SubmitPayload):
    """
    Runs all hidden tests + awards XP if solved.
    """

    # 1. Locate problem
    problem = None
    difficulty = None

    for diff, arr in PRACTICE_PROBLEMS.items():
        for p in arr:
            if p["id"] == payload.pid:
                problem = p
                difficulty = diff
                break
        if problem:
            break

    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # 2. Fetch tests
    tests = problem.get("tests", [])
    if not tests:
        raise HTTPException(status_code=400, detail="No testcases found for this problem")

    # 3. Execute hidden tests
    results = []
    passed = 0

    for idx, t in enumerate(tests):
        test_input = t.get("input", "")
        expected = str(t.get("output", "")).strip()

        try:
            raw = await judge_run(payload.language, payload.code, test_input)
            got = (raw or "").strip()
        except Exception as e:
            got = f"[error] {e}"

        ok = compare_output(got, expected)

        if ok:
            passed += 1

        results.append({
            "index": idx + 1,
            "input": test_input,
            "expected": expected,
            "got": got,
            "passed": ok
        })

    total = len(tests)

    # 4. XP calculation
    xp_gain = 0
    completed = passed == total

    if completed:
        xp_gain = XP_MAP.get(difficulty, 10)

        # Firestore update atomic
        user_ref = db.collection("users").document(payload.uid)
        user_ref.set({
            "xp": firestore.Increment(xp_gain),
            "practiceCompleted": firestore.ArrayUnion([payload.pid]),
            "updatedAt": datetime.datetime.utcnow()
        }, merge=True)

    # 5. Return final response
    return {
        "passed": passed,
        "total": total,
        "xp_gain": xp_gain,
        "completed": completed,
        "results": results
    }
