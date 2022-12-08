import tkinter as tk
from tkinter import Tk, Frame, Canvas, Label, Button, filedialog, Entry
from PIL import ImageTk, Image
from intelligent_filler import IntelligentFiller
from pathlib import Path

filler = IntelligentFiller(Path("./models/model1.h5"))

_imagetk_list = []


class MenuBar(Frame):
    def __init__(self, master, set_image):
        super().__init__(master)
        self.set_image = set_image
        open_button = Button(self, text="Open File", command=self.on_open_button_press)
        open_button.grid(column=0, row=0)

        def validate_color_power(x):
            return 0 <= int(x) <= 255

        validate_color_power_command = self.register(validate_color_power)

        Label(self, text="R").grid(column=1, row=0)
        self.r_input = Entry(
            self, validate="key", validatecommand=(validate_color_power_command, "%P")
        )
        self.r_input.grid(column=1, row=1)
        Label(self, text="G").grid(column=2, row=0)
        self.g_input = Entry(
            self, validate="key", validatecommand=(validate_color_power_command, "%P")
        )
        self.g_input.grid(column=2, row=1)
        Label(self, text="B").grid(column=3, row=0)
        self.b_input = Entry(
            self, validate="key", validatecommand=(validate_color_power_command, "%P")
        )
        self.b_input.grid(column=3, row=1)

    def on_open_button_press(self):
        fn = filedialog.askopenfilename(filetypes=[("Image", "*")])
        if fn is None or fn == "":
            return
        image = Image.open(fn)
        self.set_image(image)

    def get_color(self) -> tuple:
        return (
            int(self.r_input.get() or 0),
            int(self.g_input.get() or 0),
            int(self.b_input.get() or 0),
        )


class PictureCanvas(Canvas):
    def __init__(self, master, fill_image):
        super().__init__(master)
        self.fill_image = fill_image
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
            print(self.ratio)
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
        x_rate = e.x / self.display_image_w
        y_rate = e.y / self.display_image_h
        if (0 <= x_rate <= 1) and (0 <= y_rate <= 1):
            x = int(self.image.width * x_rate)
            y = int(self.image.height * y_rate)
            self.fill_image(self.image, x, y)


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Intelligent Fill Preview")
        self.geometry("400x400")
        self.picture_canvas = PictureCanvas(self, self.fill_image)
        self.picture_canvas.pack(expand=True, fil=tk.BOTH)
        self.menu_bar = MenuBar(self, set_image=self.picture_canvas.set_image)
        self.menu_bar.pack()

    def fill_image(self, image, x, y):
        self.picture_canvas.set_image(
            filler.fill(image, x, y, *self.menu_bar.get_color(), 10)
        )


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()
