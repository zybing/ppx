# -*- coding: utf-8 -*-
import math
import random
import cocos
# speed orientation is straight downward


class PPX(cocos.sprite.Sprite):
    def __init__(self):
        super(PPX, self).__init__('ppx.png')
        self.can_jump = True
        self.speed = 0
        self.image_anchor = 0, 0
        self.position = 100, 300
        self.schedule(self.update)
        self.lives = 3

    def jump(self, h):
        if self.can_jump:
            self.y += 1
            self.speed -= max(min(h, 12), 7)
            self.can_jump = False

    def land(self, y):
        if self.y > y - 30:
            self.can_jump = True
            self.speed = 0
            self.y = y

    def update(self, dt):
        self.speed += 10 * dt
        self.y -= self.speed
        if self.y < -80:
            self.reset()

    def reset(self):
        self.lives -= 1
        if self.lives == 0:
            self.parent.reset()
            self.lives = 3
            label = cocos.text.RichLabel(str(self.lives)+' LIVES',
                                         font_name='Times New Roman',
                                         font_size=32,
                                         anchor_x='center', anchor_y='center',
                                         color=(255, 0, 0, 255))

            label.position = 330, 400
            self.parent.setlabel(label)
        else:
            label = cocos.text.RichLabel(str(self.lives)+' LIVES',
                                         font_name='Times New Roman',
                                         font_size=32,
                                         anchor_x='center', anchor_y='center',
                                         color=(255, 0, 0, 255))

            label.position = 330, 400
            self.parent.setlabel(label)
        self.can_jump = False
        self.speed = 0
        self.position = 100, 300
