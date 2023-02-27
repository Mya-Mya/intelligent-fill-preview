from ifrontend import IFrontend
from filler import Filler
from normal_filler import NormalFiller
from intelligent_filler import IntelligentFiller
from typing import List
from pathlib import Path
from PIL import Image
from iftypes import Color
from threading import Thread

class Presenter:
    def __init__(self, intelligentfiller_model_path: Path) -> None:
        self.frontend: IFrontend = None
        self.normal_filler: Filler = NormalFiller()
        self.intelligentfiller_model_path = intelligentfiller_model_path
        self.intelligent_filler: Filler = None
        Thread(target=self.launch_intelligent_filler,name="Presenter#launch_intelligent_filler").start()

        self.filler_mode: str = "normal"
        self.fillcolor: Color = Color(0, 0, 0)
        self.diff:int = 0
        self.image_history: List[Image.Image] = []
    def launch_intelligent_filler(self):
        self.intelligent_filler = IntelligentFiller(self.intelligentfiller_model_path) # TAKES A LONG TIME !
    # Presenter -> Fontend Binding
    def set_frontend(self, fronetnd: IFrontend):
        self.frontend = fronetnd
        self.frontend.update_fillcolor(self.fillcolor)
    
    # Fill Color
    def on_open_fillcolor_press(self):
        self.frontend.ask_fillcolor()

    def on_fillcolor_specified(self, color: Color):
        self.fillcolor = color
        self.frontend.update_fillcolor(self.fillcolor)
    
    # Fill
    def on_image_click(self, x: int, y: int):
        if len(self.image_history) == 0:
            return
        old_image = self.image_history[len(self.image_history) - 1]
        filler:Filler = {
            "normal":self.normal_filler,
            "intelligent":self.intelligent_filler
        }[self.filler_mode]
        if filler is None:
            self.frontend.show_message("Maybe filler is still loading. Try later.")
            return
        new_image = filler.fill(
            image=old_image,
            x=x,
            y=y,
            color=self.fillcolor,
            diff=self.diff,
        )
        self.image_history.append(new_image)
        self.frontend.update_image(new_image)
    
    # Image File
    def on_open_imagefile_press(self):
        self.frontend.ask_opening_imagefile()

    def on_imagefile_specified(self, fp: Path):
        try:
            image = Image.open(fp)
            self.image_history.append(image)
            self.frontend.update_image(image)
        except:
            self.frontend.show_message("Failed to load image.")
    
    # Fill Mode
    def on_normal_filler_selected(self):
        self.filler_mode = "normal"

    def on_intelligent_filler_selected(self):
        self.filler_mode = "intelligent"
    
    # Diff
    def on_diff_selected(self,diff:int):
        self.diff = int(diff)
        self.frontend.update_diff(diff)

    # Undo
    def on_undo_press(self):
        if len(self.image_history) <= 1:
            return
        self.image_history.pop()
        image = self.image_history[len(self.image_history) - 1]
        self.frontend.update_image(image)
