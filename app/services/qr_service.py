import time
import random
import string

# 🔐 Generate random token
def generate_nonce():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


# 📦 GENERATE QR PAYLOAD
def generate_qr(driver_from, driver_to, package, route):

    payload = {
        "driver_from": driver_from,
        "driver_to": driver_to,
        "package": package,
        "route": route,
        "timestamp": int(time.time()),
        "nonce": generate_nonce()
    }

    return payload


# ⏱ VERIFY QR (expiry + logic)
def verify_qr(payload):

    current_time = int(time.time())

    # 🔥 expiry check (3 sec)
    if current_time - payload["timestamp"] > 30:
        return {
            "status": "failed",
            "reason": "QR expired"
        }

    # ✅ basic validation
    if payload["driver_from"] and payload["driver_to"]:
        return {
            "status": "valid",
            "message": "QR is valid"
        }

    return {
        "status": "failed",
        "reason": "Invalid data"
    }