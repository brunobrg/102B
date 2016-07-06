from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from game import PlayScreen
from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')
Config.set('graphics', 'resizable', 0)

presentation = Builder.load_file("templates/main.kv")

class ScreenManagement(ScreenManager):
    pass

class MainScreen(Screen):
    def __init__(self, **kwargs):
        return super(MainScreen, self).__init__(**kwargs)

    def startGame(self):
        app = App.get_running_app()
        app.root.current = 'play'

class MainApp(App):
    def build(self):
        global app
        app = self
        return ScreenManagement()

    def on_size(self, *args):
        pass

if __name__ == "__main__":
    MainApp().run()
