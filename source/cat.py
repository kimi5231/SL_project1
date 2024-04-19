from PIL import Image

class StateMachine:
    def __init__(self, cat):
        self.player = cat
        # self.cur_state =
        self.table = {

        }

    def start(self):
        self.cur_state.enter(self.player, ('START', 0))

    def draw(self):
        self.cur_state.draw(self.player)

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True
        return False



class Cat:
    def __init__(self):
        self.frame, self.action = 0, 0
        self.frame_num = 9
        self.frame_len = 100
        self.action_len = 100
        self.image = Image.open(r'C:\Programming\SL_project1\resource\cat_sprite_sheet.png')
        self.current_image = self.image.crop((self.frame, self.action, self.frame + self.frame_len, self.action + self.action_len))
        self.statemachine = StateMachine(self)
        self.state_machine.start()

    def draw(self):
        self.state_machine.draw()
        # draw_rectangle(*self.get_bb())

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))