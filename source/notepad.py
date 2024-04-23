import subprocess
import pyautogui
import time
import random


class Notepad:
    def __init__(self, x, y, dir_x):
        subprocess.Popen(["notepad.exe"])
        time.sleep(0.1)
        self.window = pyautogui.getWindowsWithTitle("제목 없음 - Windows 메모장")[0]
        self.window.resizeTo(500, 500)
        if dir_x == 1:
            self.window.moveTo(x+100, y)
        else:
            self.window.moveTo(x-550, y)

    def get_text(self):
        texts = []
        with open(r'..\resource\notepad.txt', 'r') as f:
            for l in f:
                texts.append(l)
        self.text = texts[random.randint(0, len(texts) - 1)]
        self.text_len = len(self.text)
        self.text_index = 0

    def write_text(self):
        self.window.activate()
        pyautogui.write(self.text[self.text_index])