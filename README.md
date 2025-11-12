# ■ Member QA Service
A simple **FastAPI**-based Question Answering API that responds to natural-language questions
about members using data from a public API.
This project was built as part of an assignment to demonstrate end-to-end design, implementation, and
deployment of a natural-language interface over structured/unstructured data.
---

## ■ Live Demo
■ **Live URL:** https://assignment-qa-services.onrender.com
■ Health check: https://assignment-qa-services.onrender.com/healthz
---


## ■ Example Queries
| Question | Example Response |
|-----------|------------------|
| When is Layla planning her trip to London? | “Layla is planning the trip to London on 2025-03-15.” |
| How many cars does Vikram Desai have? | “Vikram Desai has 2 cars.” |
| What are Amira’s favorite restaurants? | “Amira’s favorite restaurants: Olive Garden, Chipotle.” |
*(Actual answers depend on the live data returned by the public API.)*
---


## ■ Problem Statement
> Build a small API service that accepts a natural-language question and responds with an answer
inferred from member messages.
The service uses the public messages endpoint:
https://november7-730026606190.europe-west1.run.app/messages
---
## ■■ How It Works
1. **Fetch Messages:** The service calls the public `/messages` endpoint to retrieve member data.
2. **Intent Detection:** Detects if the question is about trips, cars, or restaurants.
3. **Information Extraction:** Uses regex + `dateparser` to pull relevant info.
4. **Response Generation:** Returns a formatted, human-readable answer in JSON.
---

## ■ API Endpoints
### `GET /healthz`
Check if the API is running.
**Response:**
```json
{"ok": true}
```

### `GET /ask?q=`
Ask a natural-language question.
**Response:**
```json
{"answer": "..."}
```

---
## ■ Tech Stack
- Python 3.11
- FastAPI
- Uvicorn
- Requests
- Dateparser
- Render (Deployment)
---

## ■ Bonus 1: Design Notes
| Approach |                Description |                        Pros |                                   Cons |
|
| Rule-based (current) |    Regex + keyword search |            Fast, explainable |                       Limited flexibility |
| Semantic Search |         Embedding-based retrieval |         Better recall |                           Requires model hosting |
| RAG + LLM |               Retrieval + generation |            High accuracy |                           Slower, API cost |
---
## ■ Bonus 2: Data Insights
- Only 2 messages available from the public dataset.
- Some entries are plain strings instead of structured JSON.
- No clear trip or car information visible.
- The system handles both dict and string messages gracefully.
---
## ■ Project Structure
app.py — FastAPI app
qa.py — Intent detection & logic
msg_client.py — Fetch messages
requirements.txt — Dependencies
render.yaml — Deployment config
README.md — Documentation
---
## ■■ Run Locally
```bash
git clone https://github.com/YOUR_USERNAME/member-qa-service.git
cd member-qa-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```
---
## ■ Deployment Steps (Render)
1. Push to GitHub
2. Create new web service on Render
3. Environment: Python
4. Start Command:
uvicorn app:app --host 0.0.0.0 --port 10000
---
## ■ Author
**Bal Ram Reddy Tekmal**
GitHub: https://github.com/Balram15