from fastapi import  FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import get_db
from app.services.diagnosis_services import find_diagnoses_service
from app.services.string_matcher import find_best_matches

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adjust if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summaries/find-diagnoses")
def find_diagnoses(payload: dict, db=Depends(get_db)):
    text = payload.get("text", "")

    tree = find_diagnoses_service(db, text, find_best_matches)

    return {"results": tree}