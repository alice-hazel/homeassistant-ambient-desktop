import requests

def push_colour(colour: Colour, ha_endpoint: str, ha_entity: str, ha_token: str) -> None:
    """
    Set the Home Assistant entity to a specific colour

    The state of the entity will be set to a space separated string of the RGB values - e.g. `"255 100 0"`.

    The entity will receive attributes for each colour channel set to the corresponding values - e.g. `{"r": 255, "g": 100, "b": 0}`.

    Args:
        colour: An (R,G,B) colour to send to Home Assistant
    """
    r, g, b = colour.tolist()

    url = f"{ha_endpoint}/states/{ha_entity}"
    result = requests.post(
        url, 
        headers={"Authorization": f"Bearer {ha_token}"},
        json={
            "state": f"{r} {g} {b}",
            "attributes": {
                "r": r,
                "g": g,
                "b": b
            }
        }
    )
    print(f"HTTP {result.status_code} | RGB {r} {g} {b}")
    result.raise_for_status()
