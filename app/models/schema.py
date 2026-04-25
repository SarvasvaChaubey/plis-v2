from pydantic import BaseModel, Field
from typing import Literal, List

class IncidentRequest(BaseModel):
    location: str = Field(..., min_length=2)
    severity: Literal["low", "medium", "high"]

class IncidentResponse(BaseModel):
    incident_detected: bool
    location: str
    severity: str
    delay_impact: str
    affected_routes: List[str]   # 🔥 better typing
    ai_suggestion: str
    ai_reasoning: str            # 🔥 ADDED