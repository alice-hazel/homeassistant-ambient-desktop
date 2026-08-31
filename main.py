import cv2
import cv2.typing as cv2t
from image_utils import Colour, convert
from processor import MMCQ_Filter, hsv_filter
import requests
from time import sleep
from dotenv import load_dotenv
from os import getenv
import numpy as np

SAMPLES = 16
UPDATE_DELAY = 1
CAM_INDEX = 0

def from_camera(index=0) -> cv2t.MatLike:
    """
    Pull a still image from a video capture device

    Args:
        index: The video capture device index - see OpenCV's VideoCapture method

    Returns:
        A frame from the capture device
    """
    dev = cv2.VideoCapture(index)

    if not dev.isOpened():
        raise Exception("Unable to connect")

    ret, frame = dev.read()

    if not ret:
        raise Exception("No frame received")

    return frame

def push_colour(colour: Colour) -> None:
    """
    Set the Home Assistant entity to a specific colour

    The state of the entity will be set to a space separated string of the RGB values - e.g. `"255 100 0"`.

    The entity will receive attributes for each colour channel set to the corresponding values - e.g. `{"r": 255, "g": 100, "b": 0}`.

    Args:
        colour: An (R,G,B) colour to send to Home Assistant
    """
    r, g, b = colour.tolist()

    url = f"{HASS_ENDPOINT}/states/{HASS_ENTITY}"
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


def boost_colours(colours: Colours) -> Colours:
    """
    Boosts the saturation and value channels

    Args:
        colours: The (B, G, R) colours to boost
    
    Returns:
        A new array with the modified colours (B, G, R)
    """

    hsv_colours = convert(colours[0], flag=cv2.COLOR_BGR2HSV)
    hsv_colour = hsv_colours[0]

    hsv_colour = np.array(
        (hsv_colour.item(0), 255, 255), 
        dtype=np.uint8
    )

    colours = convert(hsv_colour, flag=cv2.COLOR_HSV2BGR)
    return colours

if __name__ == "__main__":
    load_dotenv()
    HASS_TOKEN = getenv("HASS_TOKEN")
    HASS_ENTITY = getenv("HASS_ENTITY")
    HASS_ENDPOINT = getenv("HASS_ENDPOINT")

    mmcq_filter = MMCQ_Filter()
    mmcq_filter.preprocess_colours = hsv_filter

    while True:
        img = from_camera(CAM_INDEX)

        colours = mmcq_filter.process_image(img, SAMPLES)
        if len(colours) < 1:
            print("No colours found")
            exit()

        colour = colours[0]
        colours = boost_colours(np.array([colour], np.uint8))
        colours = convert(*colours, flag=cv2.COLOR_BGR2RGB)
        rgb_colour = colours[0]

        push_colour(rgb_colour)

        sleep(UPDATE_DELAY)
