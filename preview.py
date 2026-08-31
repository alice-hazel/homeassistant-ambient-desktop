import cv2
import cv2.typing
from image_utils import Colours

def preview(image: cv2.typing.MatLike, preview_height: int=400) -> None:
    """
    Display the given image using OpenCV's imshow. 
    The image will be resized to fit the given preview_height for consistency when viewing differently sized images.

    Args:
        image: The OpenCV MatLike image to display
        preview_height: The height in px to scale the image to
    """
    height, width, _ = image.shape
    image = cv2.resize(image, (round(width * (preview_height / height)), preview_height), interpolation=cv2.INTER_NEAREST)

    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def preview_colours(image: cv2.typing.MatLike, colours: Colours, preview_size: int = 20) -> None:
    """
    Draw a palette of colours over an image and preview it on screen

    Args:
        image: The OpenCV MatLike image to preview
        colours: An array of (B,G,R) colours to draw over the image
        preview_size: The size in px of the colour swatches to be overlaid
    """
    height, width, _ = image.shape
    size = min(width, height) // preview_size

    for index, colour in enumerate(colours):
        cv2.rectangle(image, (index * size, 0), ((index + 1) * size, size), colour.tolist(), -1)

    preview(image)