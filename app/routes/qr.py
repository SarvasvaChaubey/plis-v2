from fastapi import APIRouter
from pydantic import BaseModel
from app.services.qr_service import generate_qr, verify_qr
from app.services.relay_service import complete_handover  # 🔥 NEW

router = APIRouter()

# 🔐 TEMP OTP STORE (demo purpose)
otp_store = {}


# 🔥 NEW: Dynamic QR Request Model
class QRRequest(BaseModel):
    driver_from: str
    driver_to: str
    package: str
    route: str


# 📦 Generate QR (UPDATED)
@router.post("/generate-qr")
def create_qr(data: QRRequest):

    payload = generate_qr(
        driver_from=data.driver_from,
        driver_to=data.driver_to,
        package=data.package,
        route=data.route
    )

    return {
        "qr_payload": payload
    }


# 🔍 Verify QR + SEND OTP
@router.post("/verify-qr")
def check_qr(data: dict):

    result = verify_qr(data)

    if result["status"] != "valid":
        return {
            "status": "failed",
            "gemma_verification": result["reason"]
        }

    # 🔥 Generate OTP for both drivers
    otp_store["A"] = "1234"
    otp_store["B"] = "5678"

    return {
        "status": "otp_required",
        "message": "OTP sent to both drivers (A & B)"
    }


# 🔐 OTP VERIFY + FINAL AI DECISION + RELAY SHIFT
@router.post("/verify-otp")
def verify_otp(data: dict):

    otp_a = data.get("otp_a")
    otp_b = data.get("otp_b")

    if otp_store.get("A") == otp_a and otp_store.get("B") == otp_b:

        # 🔥 RELAY SHIFT (A → B)
        relay = complete_handover("B")

        return {
            "status": "verified",
            "current_driver": relay["current_driver"],  # 🔥 NEW FIELD
            "gemma_verification": "Valid transfer. Driver B is authorized. Package matches assigned route. No anomaly detected."
        }

    return {
        "status": "failed",
        "gemma_verification": "OTP verification failed. Possible unauthorized attempt."
    }