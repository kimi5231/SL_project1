from tkinter import *
from PIL import Image, ImageTk
import os
import random


class ImageWindow:
    def __init__(self, title):
        self.window = Toplevel()
        self.window.title(title)
        self.window.overrideredirect(1)
        self.get_window_image()
        Label(self.window, image=self.image).pack()

    def get_window_image(self):
        images = None
        for root, subfolders, files in os.walk(r'..\resource\image'):
            images = files
        path = '..\\resource\image\\' + images[random.randint(0, len(images) - 1)]
        image = Image.open(path)
        image = image.resize((300, 300))
        self.image = ImageTk.PhotoImage(image)