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
