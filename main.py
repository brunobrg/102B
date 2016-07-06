from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from game import PlayScreen

presentation = Builder.load_file("templates/main.kv")

class ScreenManagement(ScreenManager):
    pass

class MainScreen(Screen):
    pass

class MainApp(App):
    def build(self):
        return ScreenManagement()

if __name__ == "__main__":
    MainApp().run()
