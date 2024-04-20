from PIL import Image
import time
import random


# cat action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


def change_Idle(e):
    return e[0] == 'Change_Idle'


def change_grooming(e):
    return e[0] == 'Change_Grooming'


class Grooming:
    @staticmethod
    def enter(cat, e):
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
        if time.time() - cat.start_time > 6.0:
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
            Idle: {change_Idle:Idle, change_grooming:Grooming},
            Grooming: {change_Idle:Idle, change_grooming:Grooming}
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
        num = random.randint(1, 2)
        if num == 1:
            self.state_machine.handle_event(('Change_Idle', 0))
        elif num == 2:
            self.state_machine.handle_event(('Change_Grooming', 0))