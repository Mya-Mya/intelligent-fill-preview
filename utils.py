from PIL import Image
import cv2
import numpy as np


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