# -*- coding: utf-8 -*-
import cocos
from cocos.sprite import Sprite
from pyaudio import PyAudio, paInt16
import struct
from ppx import PPX
from block import Block


class VoiceGame(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(VoiceGame, self).__init__(255, 255, 255, 255, 800, 600)
        # init voice
        self.NUM_SAMPLES = 1000
        par = {"image":"black.png"}
        self.voicebar = Sprite(**par)
        self.voicebar.position = 20, 450
        self.voicebar.scale_y = 0.1
        self.voicebar.image_anchor = 0, 0
        self.add(self.voicebar)
        self.label = cocos.text.RichLabel('3 LIVES',
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center',
                                 color=(255, 0, 0, 255))

        self.label.position = 330, 400

        self.add(self.label)

        self.ppx = PPX()
        self.add(self.ppx)

        # layer order according the layer added order
        self.floor = cocos.cocosnode.CocosNode()
        self.add(self.floor)
        pos = 0, 100
        self.maxx=0
        for i in range(30):
            b = Block(pos)
            self.floor.add(b)
            pos = b.x + b.width, b.height
            if i == 29:
                self.maxx = b.x

        # open sound input
        pa = PyAudio()
        sampling_rate = int(pa.get_device_info_by_index(0)['defaultSampleRate'])
        self.stream = pa.open(format=paInt16, channels=1, rate=sampling_rate, input=True,
                              frames_per_buffer=self.NUM_SAMPLES)

        self.schedule(self.update)
    # prevent ppx is collided by block

    def collide(self):
        px = self.ppx.x - self.floor.x
        if px > self.maxx:
            label = cocos.text.RichLabel('CONGRATULATION!!!',
                                             font_name='Times New Roman',
                                             font_size=32,
                                             anchor_x='center', anchor_y='center',
                                             color=(255, 0, 0, 255))
            label.position = 330, 400
            self.setlabel(label)
            for b in self.floor.get_children():
                if b.x <= px + self.ppx.width * 0.8 and px + self.ppx.width * 0.2 <= b.x + b.width:
                    if self.ppx.y < b.height:
                        if b._change:
                            if self.ppx.y > b.last_y-30:
                                self.ppx.y = b.height
                            b._change = False
                        else:
                            self.ppx.land(b.height)
                        break
        else:
            for b in self.floor.get_children():
                if b.x <= px + self.ppx.width * 0.8 and px + self.ppx.width * 0.2 <= b.x + b.width:
                    if self.ppx.y < b.height:
                        if b._change:
                            if self.ppx.y > b.last_y-30:
                                self.ppx.y = b.height
                            b._change = False
                        else:
                            self.ppx.land(b.height)
                        break

    def update(self, dt):
        # 读入NUM_SAMPLES个取样
        string_audio_data = self.stream.read(self.NUM_SAMPLES)
        k = max(struct.unpack('1000h', string_audio_data))
        # print k
        self.voicebar.scale_x = k / 10000.0
        if k > 2000:
            self.floor.x -= min((k / 20.0), 250) * dt
        if k > 6000:
            self.floor.x -= min((k / 20.0), 250) * dt
            self.ppx.jump((k - 6000) / 1000.0)
        self.collide()

    def reset(self):
        self.floor.x = 0

    def setlabel(self, nlabel):
        self.remove(self.label)
        self.label = nlabel
        self.add(self.label)

cocos.director.director.init(caption="Let's Go! PiPiXia!")
cocos.director.director.run(cocos.scene.Scene(VoiceGame()))

