from tkinter import *
from PIL import ImageTk
from cat import Cat


class Character():
    def __init__(self):
        self.x, self.y = 0, 0
        self.width, self.height = 100, 100
        self.window = Tk()
        self.current_character = Cat()
        self.image = ImageTk.PhotoImage(self.current_character.current_image)
        self.init_self_window()

    def setting_self_window(self):
        pass

    def add_label(self):
        label = Label(self.window, image=self.image, bg='white')
        label.pack(fill=BOTH, expand=True)

    def init_self_window(self):
        # 윈도우 크기와 위치 설정.
        self.window.geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')
        # 윈도우 크기 조정 금지.
        self.window.resizable(False, False)
        # 윈도우 프레임 제거.
        self.window.overrideredirect(1)
        # 윈도우가 항상 가장 위에 있도록, 그리고 배경을 투명하게 설정
        self.window.attributes("-topmost", True, '-transparentcolor', 'white')
        # 종료키 설정.
        self.window.bind('<Escape>', lambda e: self.window.quit())
        self.add_label()