from image_utils import Colours
import cv2.typing
import numpy as np

class Processor:
    def mat_to_colours(self, image: cv2.typing.MatLike) -> Colours:
        arr = np.array(image, dtype=np.uint8)
        height, width, _ = arr.shape
        colours = arr.reshape(height*width, 3)

        return colours

    def process_image(self, image: cv2.typing.MatLike, samples: int) -> Colours:
        """
        Passes an image through extract_colours

        Args:
            image: An OpenCV MatLike image to sample colours from
            samples: The number of colours to sample
        
        Returns:
            An array of colours (B, G, R) samples from the image
        """
        colours = self.mat_to_colours(image)
    
        colours = self.preprocess_colours(colours)
        # Don't process an image where all the colours are filtered out
        if len(colours) < 1:
            return np.array([], np.uint8)

        return self.extract_colours(colours, samples)

    def preprocess_colours(self, colours: Colours) -> Colours:
        """
        Called during process_image to reduce the number of colours analysed by extract_colours

        Args:
            colours: An array of colours (B, G, R) to filter
        
        Returns:
            The resulting filtered array of colours (B, G, R) 
        """
        return colours

    def extract_colours(self, colours: Colours, samples: int) -> Colours:
        """
        Process a series of colours to extract dominant colours

        Args:
            colours: The (B, G, R) colours to analyse
            samples: The number of colours to extract from the image

        Returns:
            An array with the given number of samples pulled from the image. 
            Note: These colours may not actually exist in the source `colours` array.
        """
        pass
