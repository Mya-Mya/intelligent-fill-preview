from abc import ABC, abstractmethod
from PIL.Image import Image


class Filler(ABC):
    @abstractmethod
    def fill(image: Image, x: int, y: int, r: int, g: int, b: int, diff: int) -> Image:
        pass
