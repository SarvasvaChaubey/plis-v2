from fastapi import APIRouter
from app.services.traffic_service import add_incident, calculate_impact
from app.models.schema import IncidentRequest, IncidentResponse
from app.services.gemma_service import generate_incident_reasoning

router = APIRouter()

@router.post("/report-incident", response_model=IncidentResponse)
def report_incident(data: IncidentRequest):

    incident = add_incident(data.location, data.severity)

    delay, routes, suggestion = calculate_impact(data.severity)

    # 🔥 FIXED GEMMA CALL (pass dict)
    ai_output = generate_incident_reasoning({
        "location": data.location,
        "severity": data.severity
    })

    return {
        "incident_detected": True,
        "location": incident["location"],
        "severity": incident["severity"],
        "delay_impact": delay,
        "affected_routes": routes,
        "ai_suggestion": suggestion,
        "ai_reasoning": ai_output["gemma_incident_analysis"]  # ✅ FIX
    }