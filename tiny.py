from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen


class MainScreen(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))

class TinyApp(MDApp):


    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "700"
    
    
    

app = TinyApp()
app.run()
