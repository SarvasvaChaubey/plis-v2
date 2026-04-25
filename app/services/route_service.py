import random

# Dummy distance DB (expand later)
DISTANCE_DB = {
    ("Delhi", "Mumbai"): 1400,
    ("Delhi", "Jaipur"): 280,
    ("Jaipur", "Mumbai"): 1150,
    ("Delhi", "Lucknow"): 550,
    ("Lucknow", "Mumbai"): 1350,
}

def get_distance(source, destination):
    return DISTANCE_DB.get((source, destination), 1000)


def generate_routes(source, destination, rest_time=0):

    base_distance = get_distance(source, destination)

    routes = []

    route_types = ["fastest", "safest", "cheapest"]

    for r in route_types:

        distance = base_distance + random.randint(-50, 150)

        if r == "fastest":
            speed = random.randint(75, 90)
            delay_prob = random.randint(15, 30)

        elif r == "safest":
            speed = random.randint(55, 65)
            delay_prob = random.randint(5, 15)

        else:
            speed = random.randint(60, 70)
            delay_prob = random.randint(20, 35)

        hours = distance / speed

        # fatigue add
        hours += rest_time

        buffer = random.randint(15, 40)

        routes.append({
            "route": r,
            "distance": f"{distance} km",
            "eta": f"{round(hours,1)} hr ± {buffer} min",
            "delay": f"{delay_prob}%",
            "base_eta_hours": round(hours, 2)
        })

    return routes