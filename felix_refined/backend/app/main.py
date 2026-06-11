from fastapi import  FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.diagnosis import router as diagnosis_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adjust if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diagnosis_router, prefix="/api")