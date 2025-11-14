from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import datetime

# Import your curated problems with built-in tests
from app.data.practice_problems import PRACTICE_PROBLEMS

# Reuse ONLY judge + Firestore helpers from matchmaking
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
    Runs the user's code ONCE using custom input.
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

    # 1. FIND PROBLEM
    problem = None
    difficulty = "Easy"

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


    # 2. USE ONLY YOUR OWN TESTCASES (NO MATCHMAKING TESTS)
    tests = problem.get("tests", [])
    if not tests:
        raise HTTPException(status_code=400, detail="Problem has no testcases configured.")


    # 3. RUN TESTCASES
    results = []
    passed = 0

    for idx, t in enumerate(tests):
        test_input = t["input"]
        expected = t["output"]

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

    # 4. XP LOGIC
    xp_gain = 0
    completed = False

    if passed == total:
        completed = True
        xp_gain = XP_MAP.get(difficulty, 10)

        # update Firestore atomically
        user_ref = db.collection("users").document(payload.uid)
        user_ref.set({
            "xp": firestore.Increment(xp_gain),
            "practiceCompleted": firestore.ArrayUnion([payload.pid]),
            "updatedAt": datetime.datetime.utcnow()
        }, merge=True)


    # 5. RETURN FULL RESULT
    return {
        "passed": passed,
        "total": total,
        "xp_gain": xp_gain,
        "completed": completed,
        "results": results
    }
