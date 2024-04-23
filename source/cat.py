from tkinter import *
from image_window import ImageWindow
from notepad import Notepad
from PIL import Image
import time
import random
import ctypes
import os
import pygame
import pyautogui


# cat action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


# 화면의 너비와 높이
user32 = ctypes.windll.user32
SW = user32.GetSystemMetrics(0)
SH = user32.GetSystemMetrics(1)


def change_Idle(e):
    return e[0] == 'Change_Idle'


def change_grooming(e):
    return e[0] == 'Change_Grooming'


def change_move_right_down(e):
    return e[0] == 'Change_Move_Right_Down'


def change_move_right_up(e):
    return e[0] == 'Change_Move_Right_Up'


def change_move_left_down(e):
    return e[0] == 'Change_Move_Left_Down'


def change_move_left_up(e):
    return e[0] == 'Change_Move_Left_Up'


def move_left(e):
    return e[0] == 'Move_Left'


def bring_image(e):
    return e[0] == 'Bring_Image'


def open_notepad(e):
    return e[0] == 'Open_Notepad'


def run_to_mouse(e):
    return e[0] == 'Run_To_Mouse'


def run_away_with_mouse(e):
    return e[0] == 'Run_Away_With_Mouse'


def raise_cat(e):
    return e[0] == 'Raise_Cat'


def run_away(e):
    return e[0] == 'Run_Away'


class RunAway:
    @staticmethod
    def enter(cat, e):
        cat.speed = 5
        cat.dir_x *= -1
        cat.dir_y *= -1
        cat.frame, cat.action = 0, 5
        cat.frame_num = 8
        cat.current_time = time.time()
        cat.start_time = time.time()

    @staticmethod
    def exit(cat, e):
        pass

    @staticmethod
    def do(cat):
        cat.x += cat.dir_x * cat.speed
        cat.y += cat.dir_y * cat.speed
        cat.calculate_frame()
        if time.time() - cat.start_time > 5.0:
            cat.select_next_state()
        elif SW < cat.x + 150 or 0 > cat.x - 150 or SH < cat.y + 150 or 0 > cat.y - 150:
            cat.select_next_state()

    @staticmethod
    def cut(cat):
        cat.current_image = cat.image.crop((int(cat.frame) * cat.frame_len,
                                            cat.action * cat.action_len,
                                            int(cat.frame) * cat.frame_len + cat.frame_len,
                                            cat.action * cat.action_len + cat.action_len))


class RaiseCat:
    @staticmethod
    def enter(cat, e):
        cat.frame, cat.action = 0, 1
        cat.frame_num = 4
        cat.current_time = time.time()
        cat.start_time = time.time()
        cat.mx, cat.my = pyautogui.position()

    @staticmethod
    def exit(cat, e):
        pass

    @staticmethod
    def do(cat):
        x, y = pyautogui.position()
        cat.x += x - cat.mx
        cat.y += y - cat.my
        cat.mx, cat.my = x, y
        cat.calculate_frame()
        if time.time() - cat.start_time > 5.0:
            cat.state_machine.handle_event(('Run_Away', 0))

    @staticmethod
    def cut(cat):
        cat.current_image = cat.image.crop((int(cat.frame) * cat.frame_len,
                                            cat.action * cat.action_len,
                                            int(cat.frame) * cat.frame_len + cat.frame_len,
                                            cat.action * cat.action_len + cat.action_len))


class RunAwayWithMouse:
    @staticmethod
    def enter(cat, e):
        cat.speed = 10
        cat.dir_x *= -1
        cat.dir_y *= -1
        cat.frame, cat.action = 0, 5
        cat.frame_num = 8
        cat.current_time = time.time()
        cat.start_time = time.time()

    @staticmethod
    def exit(cat, e):
        pass

    @staticmethod
    def do(cat):
        cat.x += cat.dir_x * cat.speed
        cat.y += cat.dir_y * cat.speed
        cat.calculate_frame()
        pyautogui.moveTo(cat.x + 50, cat.y + 50)
        if time.time() - cat.start_time > 5.0:
            cat.select_next_state()
        elif SW < cat.x + 150 or 0 > cat.x - 150 or SH < cat.y + 150 or 0 > cat.y - 150:
            cat.select_next_state()

    @staticmethod
    def cut(cat):
        cat.current_image = cat.image.crop((int(cat.frame) * cat.frame_len,
                                            cat.action * cat.action_len,
                                            int(cat.frame) * cat.frame_len + cat.frame_len,
                                            cat.action * cat.action_len + cat.action_len))


class RunToMouse:
    @staticmethod
    def enter(cat, e):
        cat.speed = 5
        cat.frame, cat.action = 0, 5
        cat.frame_num = 8
        cat.current_time = time.time()
        cat.start_time = time.time()

    @staticmethod
    def exit(cat, e):
        pass

    @staticmethod
    def do(cat):
        x, y = pyautogui.position()
        if cat.x < x:
            cat.dir_x = 1
        else:
            cat.dir_x = -1
        if cat.y < y:
            cat.dir_y = 1
        else:
            cat.dir_y = -1
        cat.x += cat.dir_x * cat.speed
        cat.y += cat.dir_y * cat.speed
        cat.calculate_frame()
        if x + 10 > cat.x > x - 10 and y + 10 > cat.y > y - 10:
            pyautogui.moveTo(cat.x + 50, cat.y + 50)
            cat.state_machine.handle_event(('Run_Away_With_Mouse', 0))
        elif time.time() - cat.start_time > 10.0:
            cat.select_next_state()

    @staticmethod
    def cut(cat):
        cat.current_image = cat.image.crop((int(cat.frame) * cat.frame_len,
                                            cat.action * cat.action_len,
                                            int(cat.frame) * cat.frame_len + cat.frame_len,
                                            cat.action * cat.action_len + cat.action_len))


class OpenNotepad:
    @staticmethod
    def enter(cat, e):
        cat.speed = 0
        cat.frame, cat.action = 0, 8
        cat.frame_num = 8
        cat.current_time = time.time()
        cat.notepad = Notepad(cat.x, cat.y, cat.dir_x)
        cat.notepad.get_text()

    @staticmethod
    def exit(cat, e):
        pass

    @staticmethod
    def do(cat):
        cat.calculate_frame()
        cat.notepad.write_text()
        if cat.notepad.text_index == cat.notepad.text_len-1:
            cat.select_next_state()
        else:
            cat.notepad.text_index += 1

    @staticmethod
    def cut(cat):
        cat.current_image = cat.image.crop((int(cat.frame) * cat.frame_len,
                                            cat.action * cat.action_len,
                                            int(cat.frame) * cat.frame_len + cat.frame_len,
                                            cat.action * cat.action_len + cat.action_len))


class BringImage:
    @staticmethod
    def enter(cat, e):
        cat.speed = 1
        cat.dir_x, cat.dir_y = -1, 0
        cat.frame, cat.action = 0, 4
        cat.frame_num = 8
        cat.current_time = time.time()
        cat.image_window = ImageWindow('Look at me!!!')
        cat.image_window.window.protocol("WM_DELETE_WINDOW", cat.close_image_window)
        cat.image_window.window.geometry(f'300x300+{cat.x - 270}+{cat.y}')

    @staticmethod
    def exit(cat, e):
        pass

    @staticmethod
    def do(cat):
        cat.x += cat.speed
        cat.y += cat.dir_y * cat.speed
        cat.calculate_frame()
        cat.image_window.window.geometry(f'300x300+{cat.x - 270}+{cat.y}')
        if cat.x == 300:
            cat.image_window.window.overrideredirect(0)
            cat.select_next_state()

    @staticmethod
    def cut(cat):
        cat.current_image = cat.image.crop((int(cat.frame) * cat.frame_len,
                                            cat.action * cat.action_len,
                                            int(cat.frame) * cat.frame_len + cat.frame_len,
                                            cat.action * cat.action_len + cat.action_len))


class MoveLeft:
    @staticmethod
    def enter(cat, e):
        cat.speed = 1
        cat.dir_x, cat.dir_y = -1, 0
        cat.frame, cat.action = 0, 4
        cat.frame_num = 8
        cat.current_time = time.time()

    @staticmethod
    def exit(cat, e):
        pass

    @staticmethod
    def do(cat):
        cat.x += cat.dir_x * cat.speed
        cat.y += cat.dir_y * cat.speed
        cat.calculate_frame()
        if 0 > cat.x + 150:
            cat.state_machine.handle_event(('Bring_Image', 0))

    @staticmethod
    def cut(cat):
        cat.current_image = cat.image.crop((int(cat.frame) * cat.frame_len,
                                            cat.action * cat.action_len,
                                            int(cat.frame) * cat.frame_len + cat.frame_len,
                                            cat.action * cat.action_len + cat.action_len))


class MoveLeftUp:
    @staticmethod
    def enter(cat, e):
        cat.speed = 1
        cat.dir_x, cat.dir_y = -1, -1
        cat.frame, cat.action = 0, 4
        cat.frame_num = 8
        cat.current_time = time.time()
        cat.start_time = time.time()

    @staticmethod
    def exit(cat, e):
        pass

    @staticmethod
    def do(cat):
        cat.x += cat.dir_x * cat.speed
        cat.y += cat.dir_y * cat.speed
        cat.calculate_frame()
        cat.check_time_over()
        if 0 > cat.x - 150 or 0 > cat.y - 150:
            cat.select_next_state()

    @staticmethod
    def cut(cat):
        cat.current_image = cat.image.crop((int(cat.frame) * cat.frame_len,
                                            cat.action * cat.action_len,
                                            int(cat.frame) * cat.frame_len + cat.frame_len,
                                            cat.action * cat.action_len + cat.action_len))


class MoveLeftDown:
    @staticmethod
    def enter(cat, e):
        cat.speed = 1
        cat.dir_x, cat.dir_y = -1, 1
        cat.frame, cat.action = 0, 4
        cat.frame_num = 8
        cat.current_time = time.time()
        cat.start_time = time.time()

    @staticmethod
    def exit(cat, e):
        pass

    @staticmethod
    def do(cat):
        cat.x += cat.dir_x * cat.speed
        cat.y += cat.dir_y * cat.speed
        cat.calculate_frame()
        cat.check_time_over()
        if 0 > cat.x - 150 or SH < cat.y + 150:
            cat.select_next_state()

    @staticmethod
    def cut(cat):
        cat.current_image = cat.image.crop((int(cat.frame) * cat.frame_len,
                                            cat.action * cat.action_len,
                                            int(cat.frame) * cat.frame_len + cat.frame_len,
                                            cat.action * cat.action_len + cat.action_len))


class MoveRightUp:
    @staticmethod
    def enter(cat, e):
        cat.speed = 1
        cat.dir_x, cat.dir_y = 1, -1
        cat.frame, cat.action = 0, 4
        cat.frame_num = 8
        cat.current_time = time.time()
        cat.start_time = time.time()

    @staticmethod
    def exit(cat, e):
        pass

    @staticmethod
    def do(cat):
        cat.x += cat.dir_x * cat.speed
        cat.y += cat.dir_y * cat.speed
        cat.calculate_frame()
        cat.check_time_over()
        if SW < cat.x + 150 or 0 > cat.y - 150:
            cat.select_next_state()

    @staticmethod
    def cut(cat):
        cat.current_image = cat.image.crop((int(cat.frame) * cat.frame_len,
                                            cat.action * cat.action_len,
                                            int(cat.frame) * cat.frame_len + cat.frame_len,
                                            cat.action * cat.action_len + cat.action_len))


class MoveRightDown:
    @staticmethod
    def enter(cat, e):
        cat.speed = 1
        cat.dir_x, cat.dir_y = 1, 1
        cat.frame, cat.action = 0, 4
        cat.frame_num = 8
        cat.current_time = time.time()
        cat.start_time = time.time()

    @staticmethod
    def exit(cat, e):
        pass

    @staticmethod
    def do(cat):
        cat.x += cat.dir_x * cat.speed
        cat.y += cat.dir_y * cat.speed
        cat.calculate_frame()
        cat.check_time_over()
        if SW < cat.x + 150 or SH < cat.y + 150:
            cat.select_next_state()

    @staticmethod
    def cut(cat):
        cat.current_image = cat.image.crop((int(cat.frame) * cat.frame_len,
                                            cat.action * cat.action_len,
                                            int(cat.frame) * cat.frame_len + cat.frame_len,
                                            cat.action * cat.action_len + cat.action_len))


class Grooming:
    @staticmethod
    def enter(cat, e):
        cat.speed = 0
        cat.frame, cat.action = 0, 2
        cat.frame_num = 4
        cat.current_time = time.time()
        cat.start_time = time.time()

    @staticmethod
    def exit(cat, e):
        pass

    @staticmethod
    def do(cat):
        cat.calculate_frame()
        if int(cat.frame) == 3:
            cat.frame = 0
            if cat.action == 2:
                cat.action = 3
            else:
                cat.action = 2
        cat.check_time_over()

    @staticmethod
    def cut(cat):
        cat.current_image = cat.image.crop((int(cat.frame) * cat.frame_len,
                                            cat.action * cat.action_len,
                                            int(cat.frame) * cat.frame_len + cat.frame_len,
                                            cat.action * cat.action_len + cat.action_len))


class Idle:
    @staticmethod
    def enter(cat, e): # Idle 상태로 들어갈 때 할 것
        cat.speed = 0
        cat.frame, cat.action = 0, 0
        cat.frame_num = 4
        cat.current_time = time.time()
        cat.start_time = time.time()

    @staticmethod
    def exit(cat, e): # Idle 상태에서 나올 때 할 것
        pass

    @staticmethod
    def do(cat): # Idle 상태인 동안 할 것
        cat.calculate_frame()
        cat.check_time_over()

    @staticmethod
    def cut(cat): # cat 이미지 지정
        cat.current_image = cat.image.crop((int(cat.frame) * cat.frame_len,
                                            cat.action * cat.action_len,
                                            int(cat.frame) * cat.frame_len + cat.frame_len,
                                            cat.action * cat.action_len + cat.action_len))


class StateMachine:
    def __init__(self, cat):
        self.cat = cat
        self.cur_state = Idle
        self.table = {
            Idle: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp, move_left:MoveLeft, open_notepad:OpenNotepad, run_to_mouse:RunToMouse, raise_cat:RaiseCat},
            Grooming: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp, move_left:MoveLeft, open_notepad:OpenNotepad, run_to_mouse:RunToMouse, raise_cat:RaiseCat},
            MoveRightDown: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp, move_left:MoveLeft, open_notepad:OpenNotepad, run_to_mouse:RunToMouse, raise_cat:RaiseCat},
            MoveRightUp: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp, move_left:MoveLeft, open_notepad:OpenNotepad, run_to_mouse:RunToMouse, raise_cat:RaiseCat},
            MoveLeftDown: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp, move_left:MoveLeft, open_notepad:OpenNotepad, run_to_mouse:RunToMouse, raise_cat:RaiseCat},
            MoveLeftUp: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp, move_left:MoveLeft, open_notepad:OpenNotepad, run_to_mouse:RunToMouse, raise_cat:RaiseCat},
            MoveLeft: {bring_image:BringImage},
            BringImage: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp},
            OpenNotepad: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp},
            RunToMouse: {change_Idle: Idle, change_grooming: Grooming, change_move_right_down: MoveRightDown, change_move_right_up: MoveRightUp, change_move_left_down: MoveLeftDown, change_move_left_up: MoveLeftUp, run_away_with_mouse: RunAwayWithMouse},
            RunAwayWithMouse: {change_Idle: Idle, change_grooming: Grooming, change_move_right_down: MoveRightDown, change_move_right_up: MoveRightUp, change_move_left_down: MoveLeftDown, change_move_left_up: MoveLeftUp},
            RaiseCat: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp, run_away:RunAway},
            RunAway: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp},
        }

    def start(self):
        self.cur_state.enter(self.cat, ('START', 0))

    def cut(self):
        self.cur_state.cut(self.cat)

    def update(self):
        self.cur_state.do(self.cat)

    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.cat, e)
                self.cur_state = next_state
                self.cur_state.enter(self.cat, e)
                return True
        return False


class Cat:
    def __init__(self):
        self.speed = 0
        self.x, self.y = 50, 50
        self.dir_x, self.dir_y = 1, 1
        self.frame, self.action = 0, 0
        self.frame_len = 100
        self.action_len = 100
        self.frame_num = 4
        self.image = Image.open(r'..\resource\cat_sprite_sheet.png')
        self.current_image = self.image.crop((self.frame, self.action, self.frame_len, self.action_len))
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.image_window = None
        self.obstructive = time.time()

    def cut(self):
        self.state_machine.cut()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def calculate_frame(self):
        self.frame_time = time.time() - self.current_time
        self.current_time += self.frame_time
        self.frame = ((self.frame + self.frame_num * ACTION_PER_TIME * self.frame_time) % self.frame_num)

    def select_next_state(self):
        num = random.randint(1, 6)
        if num == 1:
            self.state_machine.handle_event(('Change_Idle', 0))
        elif num == 2:
            self.state_machine.handle_event(('Change_Grooming', 0))
        elif num == 3 and SW > self.x + 150 and SH > self.y + 150:
            self.state_machine.handle_event(('Change_Move_Right_Down', 0))
        elif num == 4 and SW > self.x + 150 and 0 < self.y - 150:
            self.state_machine.handle_event(('Change_Move_Right_Up', 0))
        elif num == 5 and 0 < self.x - 150 and SH > self.y + 150:
            self.state_machine.handle_event(('Change_Move_Left_Down', 0))
        elif num == 6 and 0 < self.x - 150 and 0 < self.y - 150:
            self.state_machine.handle_event(('Change_Move_Left_Up', 0))

    def select_obstructive_behavior(self):
        num = random.randint(1, 2)
        self.obstructive = time.time()
        if num == 1:
            self.state_machine.handle_event(('Move_Left', 0))
        elif num == 2:
            self.state_machine.handle_event(('Open_Notepad', 0))

    def check_time_over(self):
        if time.time() - self.start_time > 3.0:
            self.select_next_state()
        elif time.time() - self.obstructive > 60.0:
            self.select_obstructive_behavior()

    def click(self, event=None):
        sounds = None
        for root, subfolders, files in os.walk(r'..\resource\sound'):
            sounds = files
        path = '..\\resource\sound\\' + sounds[random.randint(0, len(sounds) - 1)]
        pygame.mixer.init()  # 초기화
        sound = pygame.mixer.Sound(path)
        sound.play()
        self.state_machine.handle_event(('Raise_Cat', 0))

    def close_image_window(self):
        self.image_window.window.destroy()
        self.state_machine.handle_event(('Run_To_Mouse', 0))

    def click_down(self, event=None):
        if self.state_machine.cur_state != RunAway:
            self.select_next_state()