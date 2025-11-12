from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from qa import answer_question
from msg_client import fetch_messages

app = FastAPI(title="Member QA Service")

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/ask")
def ask(q: str = Query(..., description="Natural-language question")):
    try:
        messages = fetch_messages()
        ans = answer_question(q, messages)
        return JSONResponse({"answer": ans})
    except Exception as e:
        import traceback
        traceback.print_exc()   # 👈 shows full error in terminal
        return JSONResponse({"answer": f"Sorry, something went wrong: {e}"}, status_code=500)
