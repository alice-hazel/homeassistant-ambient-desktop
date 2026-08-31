import cv2
import numpy as np
from math import sqrt, floor
import typing
import cv2.typing as cv2t
import numpy.typing as npt

type Colour = np.ndarray[tuple[int], np.dtype[np.uint8]]
type Colours = np.ndarray[tuple[int, int], np.dtype[np.uint8]]


def from_file(path: str) -> typing.Union[cv2t.MatLike | None]:
    """
    Read a file as an image

    Args:
        path: The file to open as a string
    
    Returns:
        The contents of the file as an OpenCV image
    """
    return cv2.imread(path, cv2.IMREAD_COLOR_BGR)


def mean_colour(colours: Colours) -> Colour:
    """
    Calculates the arithmatic mean of each colour channel to produce a single "average" colour.

    Args:
        colours: An array of colours to average

    Returns:
        The mean of the given colours in the same colour space as the input
    """
    return np.mean(colours, axis=0).astype(np.uint8)

def convert(*colours: Colours, flag: cv2.ColorConversionCodes) -> Colours:
    """
    Convert colours between two colourspaces according to the given flag

    Args:
        *colours: The colours to convert
        flag: An OpenCV ColorConversionCode denoting the which colourspaces to convert to/from

    Returns:
        An array of colours in the new colourspace
    """
    if len(colours) < 1:
        return np.array([])

    # Treat colours as a set of pixels in an image
    # Read ints as 8bit and then reshape (NColours, 3) to (1, NColours, 3)
    colour_array = np.array(colours, dtype=np.uint8)[np.newaxis, :, :3]
    colour_img = cv2.cvtColor(colour_array, flag)

    # Get the list of colours back
    new_colour_array = np.array(colour_img, dtype=np.uint8)
    new_colours = np.squeeze(new_colour_array, axis=0)

    return new_colours

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
