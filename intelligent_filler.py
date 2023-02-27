from filler import Filler
from normal_filler import NormalFiller
from PIL.Image import Image, fromarray, composite
from pathlib import Path
from numpy import ones, ndarray, asarray, cast, int32, any
from hashlib import sha1
from iftypes import Color


def replace_changed_region(dst: Image, before: Image, after: Image) -> Image:
    """
    Extract the changed parts from `after` compared to `before`. Then override them to `dst`.
    response = `dst` + `after` * (`after` != `before`)
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


class IntelligentFiller(Filler):
    def __init__(self, model_path: Path) -> None:
        super().__init__()
        from tensorflow import keras # TAKES A LONG TIME !
        self.model = keras.models.load_model(model_path)
        self.normal_filler = NormalFiller()
        self.line_closed_image_cache = {}

    def close_line(self, image: Image) -> Image:
        image_hash = sha1(image.tobytes())
        if image_hash in self.line_closed_image_cache:
            return self.line_closed_image_cache[image_hash]

        width = image.width
        height = image.height
        input_image_mono = image.convert("L").point(
            lambda x: int(x > 200) * 255, mode="1"
        )
        input_image_np: ndarray = ones((height, width)) * input_image_mono
        model_input = input_image_np.reshape(1, height, width, 1)
        model_output = self.model(model_input)
        output_height, output_width = model_output.shape[1:3]
        model_output_np = asarray(model_output).reshape(output_height, output_width)
        line_closed_image_np = cast[int32](model_output_np * 255.0)
        line_closed_image = fromarray(line_closed_image_np)

        self.line_closed_image_cache[image_hash] = line_closed_image
        return line_closed_image

    def fill(
        self, image: Image, x: int, y: int, color:Color, diff: int
    ) -> Image:
        line_closed_image = self.close_line(image)

        # Fill Line Closed Image
        filled_lined_closed_image = self.normal_filler.fill(
            line_closed_image, x, y, color, diff
        )

        # Create Response
        response = replace_changed_region(
            image, line_closed_image, filled_lined_closed_image
        )
        return response
