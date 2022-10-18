from ifrontend import IFrontend
import utils
from PIL import Image
from typing import Literal

frontend: IFrontend = None
filling_mode: Literal["normal", "intelligent"] = "intelligent"
diff: int = 15

_image: Image.Image = None


def open_image_file(fn: str):
    try:
        _image = Image.open(fn)
        frontend.show_image(_image)
    except:
        pass


def fill(x: int, y: int, r: int, g: int, b: int):
    fill_impl = {"normal": _fill_normal_impl, "intelligent": _fill_intelligent_impl}[
        filling_mode
    ]
    fill_impl(x, y, r, g, b)
    frontend.show_image(_image)


def _fill_normal_impl(x: int, y: int, r: int, g: int, b: int) -> None:
    _image = utils.fill_image(image=_image, x=x, y=y, r=r, g=g, b=b, diff=diff)


def _fill_intelligent_impl(x: int, y: int, r: int, g: int, b: int) -> None:
    pass
