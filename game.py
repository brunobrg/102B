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
from kivy.properties import NumericProperty
from random import choice, random
from kivy.core.audio import SoundLoader
import imp
import os

PluginFolder = "./plugins"
MainModule = "__init__"


presentation = Builder.load_file("templates/game.kv")
app = None
sound_path = None

def getPlugins():
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = imp.find_module(MainModule, [location])
        plugins.append({"name": i, "info": info})
    return plugins

def loadPlugin(plugin):
    return imp.load_module(MainModule, *plugin["info"])

class PlayScreen(Screen):
    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)
        self.window = BoxLayout(orientation='vertical', size=(400,400), size_hint=(None, None))
        self.add_widget(self.window)
        self.background = GameBackground()
        self.window.add_widget(self.background)

    def startGame(self):
        global sound_path
        sound_path = 'sounds/alarm.ogg'
        for i in getPlugins():
            print("Carregando o Plugin: " + i["name"])
            plugin = loadPlugin(i)
            sound_path = plugin.run()
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
                self.swipe_horizontal(touch.ox < touch.x)
                return True
            else:
                self.swipe_vertical(touch.oy < touch.y)
                return True

        return super(GameBackground, self).on_touch_up(touch)

    # def on_touch_down(self, touch):
    #     self.adiciona_bloco()
    #     return True

    def swipe_horizontal(self, pra_direita):
        r = range(3, -1, -1) if pra_direita else range(4)
        matriz = self.matriz
        moveu = False

        for iy in range(4):
            # get all the cube for the current line
            blocos = []
            for ix in r:
                bloco = matriz[ix][iy]
                if bloco:
                    blocos.append(bloco)

            # combine them
            self.combinar(blocos)

            # update the grid
            for ix in r:
                bloco = blocos.pop(0) if blocos else None
                if matriz[ix][iy] != bloco:
                    moveu = True
                matriz[ix][iy] = bloco
                if not bloco:
                    continue
                pos = self.indice_para_posicao(ix, iy)
                if bloco.pos != pos:
                    bloco.move(pos)

        Clock.schedule_once(self.adiciona_bloco, .20)

    def swipe_vertical(self, pra_cima):
        r = range(3, -1, -1) if pra_cima else range(4)
        matriz = self.matriz
        moveu = False

        for ix in range(4):
            # get all the cube for the current line
            blocos = []
            for iy in r:
                bloco = matriz[ix][iy]
                if bloco:
                    blocos.append(bloco)

            # combine them
            self.combinar(blocos)

            # update the grid
            for iy in r:
                bloco = blocos.pop(0) if blocos else None
                if matriz[ix][iy] != bloco:
                    moveu = True
                matriz[ix][iy] = bloco
                if not bloco:
                    continue
                pos = self.indice_para_posicao(ix, iy)
                if bloco.pos != pos:
                    bloco.move(pos)

        Clock.schedule_once(self.adiciona_bloco, .20)

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
        bloco = Bloco(
                pos=self.indice_para_posicao(ix, iy),
                value = value
                )
        self.matriz[ix][iy] = bloco
        self.add_widget(bloco)

    def combinar(self, blocos):
        if len(blocos) <= 1:
            return blocos
        i = 0
        while i < len(blocos) - 1:
            bloco1 = blocos[i]
            bloco2 = blocos[i + 1]
            if bloco1.value == bloco2.value:
                bloco1.value *= 2
                bloco2.destroy()
                del blocos[i + 1]

                sound = SoundLoader.load(sound_path)
                if sound:
                    sound.play()
            i += 1

class Bloco(Scatter):
    value = NumericProperty(2)

    def __init__(self, **kwargs):
        super(Bloco, self).__init__(**kwargs)
        self.size= (100,100)

    def on_touch_down(self, touch):
        return True

    def on_touch_up(self, touch):
        return True

    def on_touch_move(self, touch):
        return True

    def move(self, pos):
            Animation(pos=pos, d=.1, t='out_quad').start(self)

    def destroy(self, *args):
        self.parent.remove_widget(self)
