from tkinter import *
from PIL import Image, ImageTk
from cat import Cat


class Character:
    def __init__(self):
        self.x, self.y = 0, 0
        self.width, self.height = 100, 100
        self.dir_x, self.dir_y = 1, 1
        self.window = Tk()
        self.current_character = Cat()
        self.image = ImageTk.PhotoImage(self.current_character.current_image)
        self.label = Label(self.window, image=self.image, bg='white')
        self.init_self_window()

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
        # 라벨을 윈도우에 추가.
        self.label.pack(fill=BOTH, expand=True)

    def update_label(self):
        self.current_character.update()
        self.current_character.cut()
        if self.dir_x == -1:
            self.current_character.current_image = self.current_character.current_image.transpose(Image.FLIP_LEFT_RIGHT)
        self.image = ImageTk.PhotoImage(self.current_character.current_image)
        self.label.configure(image=self.image)
        self.window.after(10, self.update_label)