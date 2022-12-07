import tkinter as tk
from tkinter import Tk, Frame, Canvas, Label, Button, filedialog
from PIL import ImageTk, Image

_imagetk_list = []


class MenuBar(Frame):
    def __init__(self, master):
        super().__init__(master)
        label = Label(self, text="Intelligent Fill Preview")
        label.grid(column=0, row=0)
        open_button = Button(self, text="Open File", command=self.on_open_button_press)
        open_button.grid(column=1, row=0)

    def on_open_button_press(self):
        fn = filedialog.askopenfilename(filetypes=[("Image", "*")])
        if fn is None or fn == "":
            return


class PictureCanvas(Canvas):
    def __init__(self, master):
        super().__init__(master)
        self.image = None
        self.image_component_id = None
        self.display_image_w = None
        self.display_image_h = None
        self.ratio = None
        self.bind("<Button-1>", self.on_click)
        self.bind("<Configure>", self.on_configure)

    def set_image(self, image: Image.Image):
        self.image = image
        self.show_image(self.image)

    def show_image(self, resized_image: Image.Image):
        if self.image_component_id:
            self.delete(self.image_component_id)
        imagetk = ImageTk.PhotoImage(resized_image)
        _imagetk_list.append(imagetk)
        self.image_component_id = self.create_image(
            resized_image.width / 2, resized_image.height / 2, image=imagetk
        )

    def change_image_size(self, width: int, height: int):
        if not self.image:
            return
        self.ratio = min(
            float(width) / float(self.image.width),
            float(height) / float(self.image.height),
        )
        print(self.ratio)
        self.display_image_w = int(self.image.width * self.ratio)
        self.display_image_h = int(self.image.height * self.ratio)
        resized_image = self.image.copy().resize(
            (self.display_image_w, self.display_image_h)
        )
        self.show_image(resized_image)

    def on_configure(self, e):
        canvas_width = e.width
        canvas_height = e.height
        self.change_image_size(canvas_width, canvas_height)

    def on_click(self, e):
        x = e.x / self.display_image_w
        y = e.y / self.display_image_h
        print(x, y)


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Intelligent Fill Preview")
        self.geometry("400x400")
        MenuBar(self).pack()
        picture_canvas = PictureCanvas(self)
        image: Image.Image = Image.open("sample/Original.png")
        picture_canvas.pack(expand=True, fil=tk.BOTH)
        picture_canvas.set_image(image)


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()
