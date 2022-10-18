from abc import ABC,abstractmethod
from PIL import Image
class IFrontend(ABC):
    @abstractmethod
    def show_image(self,image:Image.Image):
        pass