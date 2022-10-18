import tkinter as tk
from tkinter import Tk, Frame, Canvas, Label,Button,filedialog
from PIL import ImageTk, Image

_imagetk_list = []

class MenuBar(Frame):
    def __init__(self, master):
        super().__init__(master)
        label = Label(self,text="Intelligent Fill Preview")
        label.grid(column=0,row=0)
        open_button = Button(self,text="Open File",command=self.on_open_button_press)
        open_button.grid(column=1,row=0)
    
    def on_open_button_press(self):
        fn = filedialog.askopenfilename(filetypes=[("Image","*")])
        if fn is None or fn=="":
            return
        
        
class PictureCanvas(Canvas):
    def __init__(self, master):
        super().__init__(master)

    def set_image(self, image: Image.Image):
        imagetk = ImageTk.PhotoImage(image)
        _imagetk_list.append(imagetk)
        a = self.create_image(0,0, image=imagetk)
        print(a)


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Intelligent Fill Preview")
        self.geometry("400x400")
        MenuBar(self).pack()
        picture_canvas = PictureCanvas(self)
        image:Image.Image = Image.open("sample/sample1.png")
        picture_canvas.pack(expand=True, fil=tk.BOTH)
        picture_canvas.set_image(image)


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()