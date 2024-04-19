from tkinter import *
from cat import Cat


class Character(Cat):
    def __init__(self):
        self.x, self.y = 0, 0
        self.width, self.height = 50, 50
        self.window = Tk()
        self.init_self_window()

    def init_self_window(self):
        # 윈도우 크기와 위치 설정.
        self.window.geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')
        # 윈도우 크기 조정 금지.
        self.window.resizable(False, False)
        # 윈도우 프레임 제거.
        self.window.overrideredirect(1)
        # 윈도우가 항상 가장 위에 있도록 설정
        self.window.attributes("-topmost", True)
        # 종료키 설정.
        self.window.bind('<Escape>', lambda e: self.window.quit())