import random

def get_weather_for_routes(routes):

    weather_options = ["Clear", "Rain", "Storm"]

    weather_summary = []

    for route in routes:

        weather = random.choice(weather_options)

        # impact on delay
        if weather == "Rain":
            route["delay"] = str(min(100, int(route["delay"].replace("%","")) + 10)) + "%"

        elif weather == "Storm":
            route["delay"] = str(min(100, int(route["delay"].replace("%","")) + 20)) + "%"

        # attach weather info
        route["weather"] = weather

        weather_summary.append(f"{route['route']} → {weather}")

    return routes, ", ".join(weather_summary)