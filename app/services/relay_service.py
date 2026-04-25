# 🔁 Relay State (demo)
relay_state = {
    "enabled": False,
    "current_driver": "A",
    "route": None,
    "package": None
}


def start_relay(route, package):
    relay_state["enabled"] = True
    relay_state["current_driver"] = "A"
    relay_state["route"] = route
    relay_state["package"] = package

    return relay_state


def get_relay_status():
    return relay_state


def complete_handover(next_driver):
    relay_state["current_driver"] = next_driver
    return relay_state