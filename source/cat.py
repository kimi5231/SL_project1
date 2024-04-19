from PIL import Image


class Cat:
    def __init__(self):
        self.frame, self.action = 0, 0
        self.frame_num = 9
        self.frame_len = 100
        self.action_len = 100
        self.image = Image.open(r'C:\Programming\SL_project1\resource\cat_sprite_sheet.png')
        self.current_image = self.image.crop((self.frame, self.action, self.frame + self.frame_len, self.action + self.action_len))