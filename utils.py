from PIL.Image import fromarray, composite, Image
from numpy import asarray, any


def replace_changed_region(dst: Image, before: Image, after: Image) -> Image:
    """
    Extract the changed parts from `after` compared to `before`. Then override them to `dst`.
    """

    before = before.convert("RGB")
    after = after.convert("RGB")
    b = asarray(before)
    a = asarray(after)
    delta = a - b
    changed = any(delta, axis=2)
    mask = fromarray(changed).convert("L")
    dst = dst.convert("RGB")
    replaced = composite(after, dst, mask)
    return replaced
