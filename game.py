from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Canvas
from kivy.input.shape import ShapeRect
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.clock import Clock
from random import choice, random

presentation = Builder.load_file("templates/game.kv")
app = None

class PlayScreen(Screen):
    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)
        self.window = BoxLayout(orientation='vertical', size=(400,400), size_hint=(None, None))
        self.add_widget(self.window)
        self.background = GameBackground()
        self.window.add_widget(self.background)

    def startGame(self):
        self.background.startGame()

class GameBackground(FloatLayout):
    def __init__(self, **kwargs):
        super(GameBackground, self).__init__(**kwargs)
        self.matriz = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]]

    def startGame(self):
        for ix, iy, child in self.iterate():
            child.destroy()

        self.matriz = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]]
        self.adiciona_bloco()
        self.adiciona_bloco()

    def on_touch_up(self, touch):
        if(abs(abs(touch.ox - touch.x) - abs(touch.oy - touch.y)) > 50):
            if(abs(touch.ox - touch.x) > abs(touch.oy - touch.y)):
                self.adiciona_bloco()

        return super(GameBackground, self).on_touch_up(touch)

    def indice_para_posicao(self, ix, iy):
        return [
            self.x + (ix * 100),
            self.y + (iy * 100)]

    def iterate(self):
        for ix, iy in self.iterate_pos():
            child = self.matriz[ix][iy]
            if child:
                yield ix, iy, child

    def iterate_empty(self):
        for ix, iy in self.iterate_pos():
            child = self.matriz[ix][iy]
            if not child:
                yield ix, iy

    def iterate_pos(self):
        for ix in range(4):
            for iy in range(4):
                yield ix, iy

    def adiciona_bloco(self, *args):
        empty = list(self.iterate_empty())
        if not empty:
            return
        value = 2 if random() < .9 else 4
        ix, iy = choice(empty)
        self.adiciona_bloco_pos(ix, iy, value)

    def adiciona_bloco_pos(self, ix, iy, value):
        bloco = Bloco(value,
                pos=self.indice_para_posicao(ix, iy)
                )
        self.matriz[ix][iy] = bloco
        self.add_widget(bloco)

class Bloco(Scatter):
    def __init__(self, value, **kwargs):
        super(Bloco, self).__init__(**kwargs)
        self.size= (100,100)
        self.add_widget(Label(text=str(value)))

    def on_touch_move(self, touch):
        return True

    def on_touch_down(self, touch):
        return True

    def on_touch_up(self, touch):
        if(abs(abs(touch.ox - touch.x) - abs(touch.oy - touch.y)) > 50):
            if(abs(touch.ox - touch.x) > abs(touch.oy - touch.y)):
                if(touch.ox > touch.x):
                    self.swipeLeft()
                else:
                    self.swipeRight()
            else:
                if(touch.oy > touch.y):
                    self.swipeDown()
                else:
                    self.swipeUp()
        return super(Bloco, self).on_touch_up(touch)

    def swipeUp(self):
        if self.y < 300:
            Animation(pos=[self.x, self.y + 100], d=.1, t='out_quad').start(self)

    def swipeDown(self):
        if self.y > 0:
            Animation(pos=[self.x, self.y-100], d=.1, t='out_quad').start(self)

    def swipeLeft(self):
        if self.x > 0:
            Animation(pos=[self.x - 100, self.y], d=.1, t='out_quad').start(self)

    def swipeRight(self):
        if self.x < 300:
            Animation(pos= [self.x + 100, self.y], d=.1, t='out_quad').start(self)

    def destroy(self, *args):
        self.parent.remove_widget(self)
