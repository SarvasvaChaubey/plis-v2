from fastapi import APIRouter
from app.services.relay_service import get_relay_status, start_relay

router = APIRouter()


# 🚛 START RELAY
@router.post("/start-relay")
def start(data: dict):

    relay = start_relay(
        route=data.get("route"),
        package=data.get("package")
    )

    return {
        "message": "Relay mode activated",
        "relay": relay
    }


# 📡 GET CURRENT STATUS
@router.get("/relay-status")
def status():
    return get_relay_status()