# In-memory storage for incidents

incidents = []

def add_incident(location: str, severity: str):
    incident = {
        "location": location,
        "severity": severity
    }
    incidents.append(incident)
    return incident


def calculate_impact(severity: str):
    # Simple demo logic (can upgrade later)
    if severity == "high":
        return "+45 min", ["A", "C"], "Avoid Route A and C, take Route B"
    elif severity == "medium":
        return "+25 min", ["B"], "Delay expected on Route B"
    else:
        return "+10 min", [], "Minor impact, continue on current route"


def get_incidents():
    return incidents