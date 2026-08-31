from image_utils import Colours, convert
import cv2
import numpy as np

def hsv_filter(colours: Colours, min_value: int = 50, min_saturation: int = 80) -> Colours:
    """
    Filter for vibrant colours based on the HSV channels
    
    Args:
        colours: The colours in (B,G,R) to filter through
        min_value: The minimum HSV value (from 0-255) of colours in the palette
        min_saturation: The minimum HSV saturation (from 0-255) of colours in the palette

    Returns:
        The colours in (B,G,R) meeting the value & saturation criteria, sorted by saturation (high->low)
    """
    # OpenCV will open images as BGR because gr
    # For most operations we dont care, but here we do, so reinterpret the colours
    if len(colours) < 1:
        return np.array([])

    colours = convert(*colours, flag=cv2.COLOR_BGR2HSV)
    
    #
    # Do the building
    #

    # Apply some min requirements for the colours we generate
    value_mask = colours[:, 2] > min_value
    # The mask has 2 dimensions, which I guess means we lose one dimension. Add it back
    colours = colours[value_mask]

    sat_mask = colours[:, 1] > min_saturation
    colours = colours[sat_mask]
   
    # Sort by saturation
    # -colours "flips" the number line, thus reversing the sort
    value_order = np.argsort(-colours[:, 2]).flatten()
    colours = colours[value_order]

    if len(colours) < 1:
        return np.array([])
    
    # Convert back to BGR
    return convert(*colours, flag=cv2.COLOR_HSV2BGR)
