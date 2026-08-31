from .processor import Processor
import numpy as np
import cv2
import cv2.typing
from image_utils import Colour, Colours, mean_colour, from_file
from math import floor, sqrt
from typing import override

class MMCQ_Filter(Processor):
    @override
    def extract_colours(self, colours: Colours, samples: int) -> Colours:
        """
        Returns:
            The result of the MMCQ algorithm - i.e. The averaged colour (BGR) of each group
        """
        iters = floor(sqrt(samples))

        return self._split_colourspace(colours, iters)

 
    def _split_colourspace(self, colours: Colours, depth: int) -> Colours:
        """
        Recursive MMCQ algorithm:
        1. Choose the colour channel with the highest range of values
        2. Sort the colours by that channel
        3. Split the colours into two groups at the median value
        4. Repeat for both groups until number of desired samples is achieved
        5. For each group, average the colours to get the final colour result

        https://modern-colorthief.readthedocs.io/en/stable/mmcq.html

        Args:
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

        return np.concatenate((self._split_colourspace(part1, next_depth), self._split_colourspace(part2, next_depth)))
