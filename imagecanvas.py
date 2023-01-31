from tkinter import Canvas
from PIL import Image, ImageTk
from typing import Callable

_imagetk_list = []


class ImageCanvas(Canvas):
    def __init__(self, master, on_image_click: Callable[[int, int], None]):
        super().__init__(master)
        self.on_image_click = on_image_click
        self.image = None
        self.image_component_id = None
        self.canvas_w = None
        self.canvas_h = None
        self.display_image_w = None
        self.display_image_h = None
        self.ratio = None
        self.bind("<Button-1>", self.on_click)
        self.bind("<Configure>", self.on_configure)

    def set_image(self, image: Image.Image):
        self.image = image
        self.show_image(self.image)
        self.update_image_size()

    def show_image(self, resized_image: Image.Image):
        if self.image_component_id:
            self.delete(self.image_component_id)
        imagetk = ImageTk.PhotoImage(resized_image)
        _imagetk_list.append(imagetk)
        self.image_component_id = self.create_image(
            resized_image.width / 2, resized_image.height / 2, image=imagetk
        )

    def update_image_size(self):
        if self.image and self.canvas_w and self.canvas_h:
            self.ratio = min(
                float(self.canvas_w) / float(self.image.width),
                float(self.canvas_h) / float(self.image.height),
            )
            self.display_image_w = int(self.image.width * self.ratio)
            self.display_image_h = int(self.image.height * self.ratio)
            resized_image = self.image.copy().resize(
                (self.display_image_w, self.display_image_h)
            )
            self.show_image(resized_image)

    def on_configure(self, e):
        self.canvas_w = e.width
        self.canvas_h = e.height
        self.update_image_size()

    def on_click(self, e):
        if self.display_image_w is None or self.display_image_h is None:
            return
        x_rate = e.x / self.display_image_w
        y_rate = e.y / self.display_image_h
        if (0 <= x_rate <= 1) and (0 <= y_rate <= 1):
            x = int(self.image.width * x_rate)
            y = int(self.image.height * y_rate)
            self.on_image_click(x, y)
