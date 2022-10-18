from PIL import Image
import cv2
import numpy as np


def fill_image(
    image: Image.Image, x: int, y: int, r: int, g: int, b: int, diff: int
) -> Image.Image:
    before_image_np = np.asarray(image)
    image_cv2 = cv2.cvtColor(before_image_np, cv2.COLOR_RGB2BGR)
    cv2.floodFill(
        image_cv2,
        None,
        (x, y),
        (b, g, r),
        loDiff=(diff, diff, diff),
        upDiff=(diff, diff, diff),
    )
    after_image_np = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)
    after_image: Image.Image = Image.fromarray(after_image_np)
    return after_image


def replace_changed_region(
    dst: Image.Image, before: Image.Image, after: Image.Image
) -> Image.Image:
    """
    Extract the changed parts from `after` compared to `before`. Then override them to `dst`.
    """

    before = before.convert("RGB")
    after = after.convert("RGB")
    b = np.asarray(before)
    a = np.asarray(after)
    delta = a - b
    changed = np.any(delta, axis=2)
    mask = Image.fromarray(changed).convert("L")
    dst = dst.convert("RGB")
    replaced = Image.composite(after,dst,mask)
    return replaced