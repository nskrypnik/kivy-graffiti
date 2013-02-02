import kivy
kivy.require('1.5.2') # replace with your current kivy version !

from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics.instructions import Canvas
from kivy.graphics import Color, Ellipse


class GraffitiBackground(StackLayout):
    """
        This class represents background for graffiti canvas.
        Graffiti widget should lay on this widget
    """
    pass

class Graffiti(Widget):
    """
        Main application widget - canvas where user can draw
    """
    def on_touch_move(self, touch):
        # Check if im really in graffiti canvas
        
        if touch.x > self.parent.pos[0] and \
            touch.x < (self.parent.pos[0] + self.parent.size[0]) and \
            touch.y > (self.parent.pos[1]) and \
            touch.y < (self.parent.pos[1] + self.parent.size[1]):
            
            with self.canvas:
                Color(1, 1, 0)
                d = 30.
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
    
    def on_touch_down(self, touch):
        """"""


class MainFrame(BoxLayout):
    pass


class GraffitiApp(App):

    def build(self):
        return MainFrame()


if __name__ == '__main__':
    GraffitiApp().run()
