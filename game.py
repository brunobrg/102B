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

presentation = Builder.load_file("templates/game.kv")
app = None

class PlayScreen(Screen):
    def __init__(self, **kwargs):
        return super(PlayScreen, self).__init__(**kwargs)

    def startGame(self):
        self.window = BoxLayout(orientation='vertical', size=(400,400), size_hint=(None, None))
        self.add_widget(self.window)
        self.background = GameBackground()
        self.window.add_widget(self.background)

        self.background.add_widget(Bloco(1))

class GameBackground(FloatLayout):
    def __init__(self, **kwargs):
        super(GameBackground, self).__init__(**kwargs)

class Bloco(Scatter):
    def __init__(self, value, **kwargs):
        super(Bloco, self).__init__(**kwargs)

        self.size= (100,100)

        with self.canvas:
            Color(1,1,1,1)
            Rectangle(pos=(self.x, self.y), size=(self.width, self.height))


        self.add_widget(Label(text=str(value), color=[0,0,0,1]))

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
