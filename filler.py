from abc import ABC, abstractmethod
from PIL.Image import Image
from iftypes import Color


class Filler(ABC):
    @abstractmethod
    def fill(image: Image, x: int, y: int, color:Color, diff: int) -> Image:
        pass
