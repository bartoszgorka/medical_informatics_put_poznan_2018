import os
import cv2
import numpy as np
from matplotlib import pyplot as plt


class Reader:
    pictures_path = 'Files/pictures'
    mask_path = 'Files/masks'
    expert_result_path = 'Files/expert_results'
    picture_ext = '.jpg'
    details_ext = '.tif'

    def __init__(self, file_name):
        self.file_name = file_name

    def read_picture(self):
        path = os.path.join(self.pictures_path, self.file_name) + self.picture_ext
        return cv2.imread(path)

    def read_expert_mask(self):
        path = os.path.join(self.expert_result_path, self.file_name) + self.details_ext
        return cv2.imread(path)

    def read_mask(self):
        path = os.path.join(self.mask_path, self.file_name) + '_mask' + self.details_ext
        return cv2.imread(path)


class Recognition:
    def __init__(self, picture, mask, expert_mask):
        self.picture = picture.copy()
        self.mask = mask.copy()
        self.expert_mask = expert_mask.copy()

    def cut_green_channel_with_contrast(self):
        img = np.int16(self.picture)
        img[:, :, 0] = 0
        img[:, :, 2] = 0

        contrast = 15
        brightness = 50
        img = img * (contrast / 127 + 1) - contrast + brightness
        img = np.clip(img, 0, 255)
        img = np.uint8(img)

        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def make_recognition(self):
        gray = self.cut_green_channel_with_contrast()
        canny_edges = cv2.Canny(gray, 150, 255, apertureSize=5, L2gradient=True)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        dilate = cv2.dilate(canny_edges, kernel)

        median = cv2.medianBlur(dilate, 5)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        dilate = cv2.dilate(median, kernel)
        return dilate


def main():
    file_name = '01_h'
    reader = Reader(file_name)

    original_image = reader.read_picture()
    mask = reader.read_mask()
    expert_mask = reader.read_expert_mask()

    recognition = Recognition(original_image, mask, expert_mask)
    edges = recognition.make_recognition()
    plt.imshow(edges, cmap='gray')
    plt.show()


if __name__ == "__main__":
    main()

# DONE LIST
# * Read image [DONE]
# * Read expert mask [DONE]
# * Select only green channel from image [DONE]
# * Dilatation [DONE]
# * MedianBlur [DONE]

# TODO LIST
# * Frangi filter to prepare continuous edges
# * Prepare binary response (0/1 - vessel or not) as own mask
# * Save result as picture
# * Compare own mask with expert mask and calculate statistics
# * Machine Learning with SciKit

# OPTIONAL
# * Cut image from channel - use mask to reduce extra edges around the eye