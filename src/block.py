# -*- coding: utf-8 -*-
import random
import cocos
# 坐标以左下角为原点


class Block(cocos.sprite.Sprite):

    def __init__(self, pos):
        super(Block, self).__init__('black.png')
        self.image_anchor = 0, 0
        x, y = pos
        if x == 0:
            self.scale_x = 5
            self.scale_y = 1
        else:
            self.scale_x = 0.5 + random.random() * 1.5
            self.scale_y = min(max(y - 50 + random.random() * 100, 50), 300) / 100.0
            self.position = x + 70 + random.random() * 100, 0
        self.origin_x = self.scale_x
        self.origin_y = self.scale_y
        self.last_y = self.height
        self.time = 0
        self._change = False
        self.schedule(self.update)

    def update(self, dt):
        self.time += dt
        if self.time > 1:
            self.last_y = self.height
            self.scale_y = self.origin_y * max(0.5, random.random()*2)
            self.time = 0
            self._change = True


