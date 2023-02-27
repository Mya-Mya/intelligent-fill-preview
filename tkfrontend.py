from ifrontend import IFrontend
from presenter import Presenter
from iftypes import Color, convert_color_to_hexcolor
from PIL import Image
from pathlib import Path
from tkinter import (
    filedialog,
    messagebox,
    colorchooser,
    Tk,
    Frame,
    Button,
    IntVar,
    Radiobutton,
    Scale,
    BOTH,
    LEFT,
    RIGHT,
    HORIZONTAL,
)
from imagecanvas import ImageCanvas

class TKFrontend(Tk, IFrontend):
    def __init__(self) -> None:
        super().__init__()
        self.title("Intelligent Fill Preview")
        self.geometry("600x600")
        self.init_components()
        self.init_presenter()
        self.mainloop()

    def init_components(self)->None:
        # Image Canvas
        self.image_canvas = ImageCanvas(self, lambda x, y: self.on_click(x, y))
        self.image_canvas.pack(expand=True, fill=BOTH)

        # Menu Bar
        menubar = Frame(self)
        # Undo Button < Menu Bar
        self.undo_button = Button(
            menubar, text="Undo", command=lambda: self.presenter.on_undo_press()
        )
        self.undo_button.pack(side=LEFT)
        # Open Image Button < Menu Bar
        openimage_button = Button(
            menubar,
            text="Open",
            command=lambda: self.presenter.on_open_imagefile_press(),
        )
        openimage_button.pack(side=LEFT)
        # Fill Color Button < Menu Bar
        self.fillcolor_button = Button(
            menubar,
            text="",
            command=lambda: self.presenter.on_open_fillcolor_press(),
            width=10,
        )
        self.fillcolor_button.pack(side=LEFT)
        # Diff Scale < Menu Bar
        self.diff_scale = Scale(
            menubar,
            orient=HORIZONTAL,
            length=150,
            width=20,
            from_=0,
            to=30,
            resolution=1,
            tickinterval=5,
        )
        self.diff_scale.configure(
            command=lambda _: self.presenter.on_diff_selected(self.diff_scale.get())
        )
        self.diff_scale.pack(side=LEFT)
        # Filler Radio Buttons < Menu Bar
        _filler_choice = IntVar(self, 0)
        use_normalfiller_rb = Radiobutton(
            menubar,
            text="Normal",
            value=0,
            variable=_filler_choice,
            command=lambda: self.presenter.on_normal_filler_selected(),
        )
        use_intelligentfiller_rb = Radiobutton(
            menubar,
            text="Intelligent",
            value=1,
            variable=_filler_choice,
            command=lambda: self.presenter.on_intelligent_filler_selected(),
        )
        use_normalfiller_rb.pack(side=RIGHT)
        use_intelligentfiller_rb.pack(side=RIGHT)

        menubar.pack()
    
    def init_presenter(self)->None:
        self.presenter = Presenter(Path("./models/model1.h5"))
        self.presenter.set_frontend(self)

    def ask_opening_imagefile(self) -> None:
        fn = filedialog.askopenfilename(filetypes=[("Image", "*")])
        if fn is None or fn == "":
            return
        self.presenter.on_imagefile_specified(Path(fn))

    def update_image(self, image: Image.Image) -> None:
        self.image_canvas.set_image(image)

    def show_message(self, message: str) -> None:
        messagebox.showinfo("Intelligent Fill Preview", message=message)

    def ask_fillcolor(self) -> None:
        hexcolor = convert_color_to_hexcolor(self.presenter.fillcolor)
        res = colorchooser.askcolor(hexcolor, title="Fill Color")
        if res[0] is None:
            return
        color = Color(r=res[0][0], g=res[0][1], b=res[0][2])
        self.presenter.on_fillcolor_specified(color)

    def update_fillcolor(self, color: Color) -> None:
        hexcolor = convert_color_to_hexcolor(color)
        self.fillcolor_button.configure(bg=hexcolor)

    def update_diff(self, diff: int) -> None:
        self.diff_scale.set(diff)

    def on_click(self, x: int, y: int) -> None:
        self.presenter.on_image_click(x, y)
