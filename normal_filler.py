from filler import Filler
from PIL.Image import Image, fromarray
from cv2 import floodFill, cvtColor, COLOR_RGB2BGR, COLOR_BGR2RGB
from numpy import asarray
from iftypes import Color


class NormalFiller(Filler):
    def fill(self, image: Image, x: int, y: int, color: Color, diff: int) -> Image:
        image = image.convert("RGB")
        before_image_np = asarray(image)
        image_cv2 = cvtColor(before_image_np, COLOR_RGB2BGR)
        floodFill(
            image_cv2,
            None,
            (x, y),
            (color.b, color.g, color.r),
            loDiff=(diff, diff, diff),
            upDiff=(diff, diff, diff),
        )
        after_image_np = cvtColor(image_cv2, COLOR_BGR2RGB)
        after_image = fromarray(after_image_np)
        return after_image
