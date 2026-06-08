from pydantic import BaseModel
from typing import Optional, List, Any

class SummaryRequest(BaseModel):
    text: str


class LineMatch(BaseModel):
    line: str
    match: Optional[str]
    span: Optional[List[int]]


class SummaryResponse(BaseModel):
    results: List[LineMatch]