from tkinter import *


class Cat:
    def __init__(self):
        self.frame = 0
        self.action = 0
        self.frame_num = 9
        self.frame_len = 32
        self.action_len = 32
        self.image = PhotoImage(file=r'C:\Programming\SL_project1\resource\cat _sprite_sheet.png')