import numpy as np
import cv2
import cv2.typing
from image_utils import Colour, Colours, hsv_filter, mean_colour, from_file
from math import floor, sqrt


def quantize_image(image: cv2.typing.MatLike, samples: int) -> Colours:
    """
    MMCQ implementation to extract dominant colours from an image

    Args:
        image: An OpenCV MatLike image to extract colours from
        samples: The number of colours to extract - must be a power of 2

    Returns:
        An array of colours (B,G,R) chosen from the image
    """
    arr = np.array(image, dtype=np.uint8)
    height, width, _ = arr.shape
    pixels = arr.reshape(height*width, 3)
    # slim selected colours down by getting rid of boring pixels
    pixels = hsv_filter(pixels)

    if len(pixels) < 1:
        return np.array([])

    iters = floor(sqrt(samples))
    return split_colourspace(pixels, iters)
    

def split_colourspace(colours: Colours, depth: int) -> Colours:
    """
    Recursive MMCQ algorithm:
    1. Choose the colour channel with the highest range of values
    2. Sort the colours by that channel
    3. Split the colours into two groups at the median value
    4. Repeat for both groups until number of desired samples is achieved
    5. For each group, average the colours to get the final colour result

    https://modern-colorthief.readthedocs.io/en/stable/mmcq.html

    Args
        colours: The array of colours to divide up
        depth: The number of times to split the colourspace into two

    Returns:
        The result of the MMCQ algorithm - i.e. The averaged colour (BGR) of each group
    """

    # Calculate the max-min of each colour channel
    channel_ranges = [
        np.max(colours[:, 0]) - np.min(colours[:,0]),
        np.max(colours[:, 1]) - np.min(colours[:,1]),
        np.max(colours[:, 2]) - np.min(colours[:,2]),
    ]
    # Work out which channel has the highest variance (range)
    varyest_channel = np.argmax(channel_ranges)
    
    sorted_channel = np.argsort(colours[:, varyest_channel])
    centerpoint = len(sorted_channel) // 2

    # Split the sorted channel values by the median (centerpoint)
    #  And get the pixel values by the corresponding indexes
    part1 = colours[sorted_channel[:centerpoint]]
    part2 = colours[sorted_channel[centerpoint:]]

    next_depth = depth - 1
    if next_depth == 0:
        return np.vstack((mean_colour(part1), mean_colour(part2)))

    return np.concatenate((split_colourspace(part1, next_depth), split_colourspace(part2, next_depth)))

if __name__ == "__main__":
    from preview import preview_colours, preview

    # preview(from_camera())

    # img = from_camera()
    img = from_file("samples/1.png")
    if img is None:
        exit()

    colours = quantize_image(img, 16)
    colours = hsv_filter(colours)

    # print(colours)
    preview_colours(img, colours)
