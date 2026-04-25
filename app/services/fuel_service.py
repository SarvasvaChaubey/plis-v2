def calculate_fuel(distance_km, mileage=15):
    """
    distance_km: total distance
    mileage: km per liter (default truck avg)
    """
    fuel_used = distance_km / mileage
    return round(fuel_used, 2)