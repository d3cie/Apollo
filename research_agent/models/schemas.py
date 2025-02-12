from pydantic import BaseModel
from typing import List, Optional

class ResearchQuery(BaseModel):
    topic: str
    depth: Optional[int] = 2
    max_questions: Optional[int] = 5

class Question(BaseModel):
    text: str
    sub_questions: List['Question'] = []
    sources: List[dict] = []
    findings: Optional[str] = None

    class Config:
        from_attributes = True

class Source(BaseModel):
    title: str
    link: str
    snippet: Optional[str] = None
    extracted_content: Optional[str] = None
    analysis: Optional[dict] = None

class ResearchReport(BaseModel):
    topic: str
    main_questions: List[Question]
    summary: str
    detailed_analysis: str

    class Config:
        from_attributes = True 