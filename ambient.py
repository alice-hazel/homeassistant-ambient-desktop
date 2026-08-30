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
    """
    return cv2.imread(path, cv2.IMREAD_COLOR_BGR)


def preview(image: cv2.typing.MatLike, preview_height: int=400) -> None:
    """
    Display the given image using imshow
    """
    height, width, _ = image.shape
    image = cv2.resize(image, (round(width * (preview_height / height)), preview_height), interpolation=cv2.INTER_NEAREST)

    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def preview_colours(image: cv2.typing.MatLike, colours: Colours, preview_size: int = 20) -> None:
    """
    Draw a palette of colours over an image and display it on screen
    """
    height, width, _ = image.shape
    size = min(width, height) // preview_size

    for index, colour in enumerate(colours):
        cv2.rectangle(image, (index * size, 0), ((index + 1) * size, size), colour.tolist(), -1)

    preview(image)


def quantize_image(image: cv2.typing.MatLike, samples: int) -> Colours:
    """
    """
    arr = np.array(image, dtype=np.uint8)
    height, width, _ = arr.shape
    pixels = arr.reshape(height*width, 3)
    # slim selected colours down by getting rid of boring pixels
    pixels = build_bgr_palette(pixels)

    if len(pixels) < 1:
        return np.array([])

    iters = floor(sqrt(samples))
    return split_colourspace(pixels, iters)
    

def split_colourspace(colours: Colours, depth: int) -> Colours:
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

def mean_colour(colours: Colours) -> Colour:
    return np.mean(colours, axis=0).astype(np.uint8)

def convert(*colours: Colours, flag: cv2.ColorConversionCodes) -> Colours:
    """
    Convert colours between two colourspaces according to the given flag
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


# Note: hsv in opencv is from 0-255, not as a %
def build_bgr_palette(colours: Colours, min_value: int = 50, min_saturation: int = 80) -> Colours:
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


if __name__ == "__main__":
    # preview(from_camera())

    # img = from_camera()
    img = from_file("samples/1.png")
    if not img:
        exit()

    colours = quantize_image(img, 16)
    colours = build_bgr_palette(colours)

    # print(colours)
    preview_colours(img, colours)
