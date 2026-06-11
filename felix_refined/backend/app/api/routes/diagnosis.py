from fastapi import APIRouter
from app.services.matcher import process_lines

router = APIRouter()

@router.post("/process-diagnoses")
def process_diagnoses(payload: dict):
    return {
        "results": process_lines(payload.get("lines", []))
    }