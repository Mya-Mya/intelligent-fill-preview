from abc import ABC, abstractmethod
from iftypes import Color
from PIL import Image


class IFrontend(ABC):
    @abstractmethod
    def ask_opening_imagefile(self) -> None:
        pass

    @abstractmethod
    def update_image(self, image: Image.Image) -> None:
        pass

    @abstractmethod
    def show_message(self, message: str) -> None:
        pass

    @abstractmethod
    def ask_fillcolor(
        self,
    ) -> None:
        pass

    @abstractmethod
    def update_fillcolor(self, color: Color) -> None:
        pass

    @abstractmethod
    def update_diff(self,diff:int)->None:
        pass