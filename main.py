import cv2
import cv2.typing as cv2t
import ambient
import requests
from time import sleep
from dotenv import load_dotenv
from os import getenv
import numpy as np

SAMPLES = 16
UPDATE_DELAY = 1
CAM_INDEX = 0

def from_camera(index=0) -> cv2t.MatLike:
    dev = cv2.VideoCapture(index)

    if not dev.isOpened():
        raise Exception("Unable to connect")

    ret, frame = dev.read()

    if not ret:
        raise Exception("No frame received")

    return frame

def push_colour(colour: ambient.Colour) -> None:
    r, g, b = colour.tolist()

    url = f"{HASS_ENDPOINT}/states/{HASS_ENTITY}"
    print(url)
    print(f"RGB {r} {g} {b}")
    return
    result = requests.post(
        url, 
        headers={"Authorization": f"Bearer {HASS_TOKEN}"},
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


def screen_to_ha(index: int) -> None:
    img = from_camera(index)
    
    colours = ambient.quantize_image(img, SAMPLES)
    colours = ambient.build_bgr_palette(colours)

    if len(colours) < 1:
        print("No colours found")
        return

    hsv_colours = ambient.convert(colours[0], flag=cv2.COLOR_BGR2HSV)
    hsv_colour = hsv_colours[0]

    hsv_colour = np.array(
        # boost saturation and value for prettiness
        (hsv_colour.item(0), 255, 255), 
        dtype=np.uint8
    )

    colours = ambient.convert(hsv_colour, flag=cv2.COLOR_HSV2RGB)
    # There is only one colour, but .convert returns a list of colours
    colour = colours[0]

    push_colour(colour)

if __name__ == "__main__":
    load_dotenv()
    HASS_TOKEN = getenv("HASS_TOKEN")
    HASS_ENTITY = getenv("HASS_ENTITY")
    HASS_ENDPOINT = getenv("HASS_ENDPOINT")

    while True:
        screen_to_ha(CAM_INDEX)
        sleep(UPDATE_DELAY)
