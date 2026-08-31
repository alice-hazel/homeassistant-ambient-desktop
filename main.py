import cv2
import cv2.typing as cv2t
from image_utils import Colour, convert
from processor import MMCQ_Filter, hsv_filter
from time import sleep
from dotenv import load_dotenv
from os import getenv
import numpy as np
from outputter.hass import push_colour

SAMPLES = 16
UPDATE_DELAY = 1
CAM_INDEX = 0


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

    # Try to open the video capture device
    dev = cv2.VideoCapture(CAM_INDEX)
    if not dev.isOpened():
        print(f"Unable to open video capture device (with index {CAM_INDEX})")
        exit(1)

    # Set up the filter pipeline
    mmcq_filter = MMCQ_Filter()
    mmcq_filter.preprocess_colours = hsv_filter

    try:
        while True:
            ret, img = dev.read()
            if not ret:
                print("Unable to obtain frame from video capture device")
                exit(1)

            colours = mmcq_filter.process_image(img, SAMPLES)
            
            if len(colours) < 1:
                print("No colours found")
                sleep(UPDATE_DELAY)
                continue

            colours = hsv_filter(colours)
            colour = colours[0]
            colours = boost_colours(np.array([colour], np.uint8))
            colours = convert(*colours, flag=cv2.COLOR_BGR2RGB)
            rgb_colour = colours[0]

            push_colour(rgb_colour, HASS_ENDPOINT, HASS_ENTITY, HASS_TOKEN)

            sleep(UPDATE_DELAY)
        

    finally:
        dev.release()
