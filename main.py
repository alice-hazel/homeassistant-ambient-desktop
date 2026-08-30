import cv2
import ambient
import requests
from time import sleep
from dotenv import load_dotenv
from os import getenv

SAMPLES = 16
UPDATE_DELAY = 1
CAM_INDEX = 0

load_dotenv()
HASS_TOKEN = getenv("HASS_TOKEN")
HASS_API = getenv("HASS_ENDPOINT")
ENTITY = getenv("HASS_ENTITY")


def from_camera(index=0):
    dev = cv2.VideoCapture(index)

    if not dev.isOpened():
        raise Exception("Unable to connect")

    ret, frame = dev.read()

    if not ret:
        raise Exception("No frame received")

    return frame

def push_colour(colour):
    r, g, b = colour

    url = f"{HASS_API}/states/{ENTITY}"
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


def screen_to_ha(index):
    img = from_camera(index)
    
    colours = ambient.quantize_image(img, SAMPLES)
    colours = ambient.build_bgr_palette(colours)

    if len(colours) < 1:
        return

    hsv = ambient.convert(colours[0], flag=cv2.COLOR_BGR2HSV)
    # boost ~~saturation~~ and value for prettiness
    # hsv = (hsv[0], hsv[1], 255)
    hsv = (hsv[0], 255, 255)
    colour = ambient.convert(hsv, flag=cv2.COLOR_HSV2RGB)

    colour = [int(c) for c in colour]

    push_colour(colour)

if __name__ == "__main__":
    while True:
        screen_to_ha(CAM_INDEX)
        sleep(UPDATE_DELAY)
