from PIL import Image
import time
import random
import ctypes


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
        cat.frame_time = time.time() - cat.current_time
        cat.current_time += cat.frame_time
        cat.frame = ((cat.frame + cat.frame_num * ACTION_PER_TIME * cat.frame_time) % cat.frame_num)
        if time.time() - cat.start_time > 3.0:
             cat.select_next_state()
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
        cat.frame_time = time.time() - cat.current_time
        cat.current_time += cat.frame_time
        cat.frame = ((cat.frame + cat.frame_num * ACTION_PER_TIME * cat.frame_time) % cat.frame_num)
        if time.time() - cat.start_time > 3.0:
             cat.select_next_state()
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
        cat.frame_time = time.time() - cat.current_time
        cat.current_time += cat.frame_time
        cat.frame = ((cat.frame + cat.frame_num * ACTION_PER_TIME * cat.frame_time) % cat.frame_num)
        if time.time() - cat.start_time > 3.0:
             cat.select_next_state()
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
        cat.frame_time = time.time() - cat.current_time
        cat.current_time += cat.frame_time
        cat.frame = ((cat.frame + cat.frame_num * ACTION_PER_TIME * cat.frame_time) % cat.frame_num)
        if time.time() - cat.start_time > 3.0:
             cat.select_next_state()
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
        cat.frame_time = time.time() - cat.current_time
        cat.current_time += cat.frame_time
        cat.frame = ((cat.frame + cat.frame_num * ACTION_PER_TIME * cat.frame_time) % cat.frame_num)
        if int(cat.frame) == 3:
            cat.frame = 0
            if cat.action == 2:
                cat.action = 3
            else:
                cat.action = 2
        if time.time() - cat.start_time > 3.0:
             cat.select_next_state()

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
        cat.frame_time = time.time() - cat.current_time
        cat.current_time += cat.frame_time
        cat.frame = ((cat.frame + cat.frame_num * ACTION_PER_TIME * cat.frame_time) % cat.frame_num)
        if time.time() - cat.start_time > 3.0:
             cat.select_next_state()

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
            Idle: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp},
            Grooming: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp},
            MoveRightDown: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp},
            MoveRightUp: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp},
            MoveLeftDown: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp},
            MoveLeftUp: {change_Idle:Idle, change_grooming:Grooming, change_move_right_down:MoveRightDown, change_move_right_up:MoveRightUp, change_move_left_down:MoveLeftDown, change_move_left_up:MoveLeftUp},
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
        self.image = Image.open(r'C:\Programming\SL_project1\resource\cat_sprite_sheet.png')
        self.current_image = self.image.crop((self.frame, self.action, self.frame_len, self.action_len))
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def cut(self):
        self.state_machine.cut()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

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