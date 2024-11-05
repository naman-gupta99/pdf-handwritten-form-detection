from image_matcher.image_matcher import ImageMatcher
import numpy as np
import cv2
from PIL import Image

class SSIMatcher(ImageMatcher):
    def __init__(self, threshold=0.82):
        self.threshold = threshold
    
    def match(self, image1: Image, image2: Image) -> bool:
        """
        Compares two images to determine if they are identical.

        Args:
            img1 (PIL.Image): First image.
            img2 (PIL.Image): Second image.
            threshold (float): Similarity threshold between 0 and 1.

        Returns:
            bool: True if images are similar above the threshold, False otherwise.
        """
        # Convert images to grayscale
        img1_gray = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2GRAY)
        img2_gray = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2GRAY)

        # Resize images to the same size
        if img1_gray.shape != img2_gray.shape:
            return False

        # Compute Structural Similarity Index (SSI)
        score, _ = cv2.quality.QualitySSIM_compute(img1_gray, img2_gray)
        print(score)
        return score[0] >= self.threshold
