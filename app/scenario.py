"""Scenario classifier extracted from the original planner; synthetic input only."""
def _rain_scenario(rain_chance: int) -> str:
    """Classifica a previsão em três cenários para o planner."""
    if rain_chance < 25:
        return "sol"
    if rain_chance < 65:
        return "incerto"
    return "chuva"
