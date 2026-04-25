from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import random

from app.services.route_service import generate_routes
from app.services.traffic_service import get_incidents
from app.services.gemma_service import generate_route_reasoning

router = APIRouter()


# ----------- REQUEST MODEL (VALIDATION) -----------
class RouteRequest(BaseModel):
    source: str = Field(..., min_length=2)
    destination: str = Field(..., min_length=2)
    rest_time: Optional[float] = 0


# ----------- HELPER: APPLY INCIDENT IMPACT -----------
def apply_incident_impact(routes):
    incidents = get_incidents()

    if not incidents:
        return routes, "No active incidents"

    latest = incidents[-1]
    severity = latest["severity"]

    if severity == "high":
        extra_min = 45
        affected = ["fastest", "cheapest"]
    elif severity == "medium":
        extra_min = 25
        affected = ["safest"]
    else:
        extra_min = 10
        affected = []

    updated_routes = []

    for r in routes:
        new_r = r.copy()

        if r["route"] in affected:
            base_hours = r["base_eta_hours"]
            new_hours = base_hours + (extra_min / 60)

            new_r["eta"] = f"{round(new_hours,1)} hr ± 30 min"
            new_r["incident_delay_added"] = f"+{extra_min} min"
        else:
            new_r["incident_delay_added"] = "+0 min"

        updated_routes.append(new_r)

    effect_msg = f"Incident at {latest['location']} impacting routes: {', '.join(affected) if affected else 'minor impact'}"

    return updated_routes, effect_msg


# ----------- MAIN API -----------
@router.post("/predict-route")
def predict_route(data: RouteRequest):

    source = data.source
    destination = data.destination
    rest_time = data.rest_time

    if source.lower() == destination.lower():
        raise HTTPException(status_code=400, detail="Source and destination cannot be same")

    # 1. Generate routes
    routes = generate_routes(source, destination, rest_time)

    # 2. Apply incident impact
    routes, incident_effect = apply_incident_impact(routes)

    # ---------------- FATIGUE ----------------
    if rest_time < 1:
        fatigue_status = "High Fatigue Risk"
    elif rest_time < 3:
        fatigue_status = "Moderate Fatigue"
    else:
        fatigue_status = "Low Fatigue"

    fatigue_output = {"status": fatigue_status}

    # ---------------- RELAY ----------------
    relay_status = "Not Required"
    relay_reason = ""
    relay_eta = ""
    relay_benefit = ""

    max_distance = max(int(r["distance"].split()[0]) for r in routes)
    max_delay = max(int(r["delay"].replace("%", "")) for r in routes)

    if max_distance > 1200 or fatigue_status == "High Fatigue Risk" or max_delay > 30:
        relay_status = "Recommended"
        relay_reason = "Long distance / fatigue / high delay"
        relay_eta = f"{round(min(r['base_eta_hours'] for r in routes) * 0.85,1)} hr"
        relay_benefit = "Faster delivery & reduced fatigue risk"

    relay_output = {
        "status": relay_status,
        "reason": relay_reason,
        "new_eta": relay_eta,
        "benefit": relay_benefit
    }

    # ---------------- LIVE SPEED ----------------
    live_speed_output = {
        "current_speed": f"{random.randint(50,80)} km/h",
        "expected_speed": "60 km/h",
        "status": random.choice([
            "Faster than expected",
            "On track",
            "Slower than expected"
        ]),
        "eta_change": random.choice(["-20 min", "+15 min", "+30 min"])
    }

    # ---------------- GEMMA REASONING ----------------
    best_route = min(routes, key=lambda x: x["base_eta_hours"])["route"]

    gemma_reason = generate_route_reasoning(
        incident_effect,
        best_route
    )

    # ---------------- FINAL RESPONSE ----------------
    return {
        "incident_effect": incident_effect,
        "gemma_reasoning": gemma_reason,  # 🔥 NEW
        "fatigue_analysis": fatigue_output,
        "relay_system": relay_output,
        "live_speed_analysis": live_speed_output,
        "routes": routes
    }