from preview import preview_colours, preview
from processor import MMCQ_Filter, hsv_filter
from image_utils import from_file

if __name__ == "__main__":

    # preview(from_camera())

    # img = from_camera()
    img = from_file("samples/1.png")
    if img is None:
        exit()

    mmcq_filter = MMCQ_Filter()
    mmcq_filter.preprocess_colours = hsv_filter

    colours = mmcq_filter.process_image(img, 16)
    colours = hsv_filter(colours)

    # print(colours)
    preview_colours(img, colours)
