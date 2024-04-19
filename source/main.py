from tkinter import *


def set_character_window():
    # 윈도우 크기와 위치 설정.
    character_window.geometry('75x75+0+0')
    # 윈도우 크기 조정 금지.
    character_window.resizable(False, False)
    # 윈도우 프레임 제거.
    character_window.overrideredirect(1)
    # 윈도우가 항상 가장 위에 있도록 설정
    character_window.attributes("-topmost", True)


character_window = Tk()
set_character_window()
# 종료키 설정.
character_window.bind('<Escape>', lambda e: character_window.quit())
character_window.mainloop()