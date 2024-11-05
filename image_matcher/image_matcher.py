from image_matcher.ssi_matcher import SSIMatcher
from PIL import Image

class ImageMatcher:
    def match(self, image1: Image, image2: Image) -> bool:
        # Compare two images and return a similarity score
        pass

def get_image_matcher(matcher_type:str) -> ImageMatcher:
    if matcher_type == "ssim":
        return SSIMatcher()
    else:
        return ImageMatcher()
