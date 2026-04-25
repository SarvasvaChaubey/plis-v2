from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal

from app.services.traffic_service import add_incident, incidents

router = APIRouter()


# ----------- REQUEST MODEL (INPUT SHOW IN SWAGGER) -----------
class SimulationRequest(BaseModel):
    location: str
    severity: Literal["low", "medium", "high"]


# 🎮 SIMULATE INCIDENT (DYNAMIC)
@router.post("/simulate/incident")
def simulate_incident(data: SimulationRequest):

    add_incident(data.location, data.severity)

    return {
        "message": "Simulated incident triggered",
        "location": data.location,
        "severity": data.severity
    }


# 🧹 CLEAR INCIDENTS
@router.post("/simulate/clear")
def clear_incidents():

    incidents.clear()

    return {
        "message": "All incidents cleared. System reset."
    }