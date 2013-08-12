import kivy
kivy.require('1.5.2') # replace with your current kivy version !

from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.bubble import Bubble 
from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics.instructions import Canvas
from kivy.graphics import Color, Ellipse, Line, Point
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
#from colorpicker import ColorPicker
from kivy.uix.colorpicker import ColorPicker

DEFAULT_BRUSH_WIDTH = 10.
DEFAULT_BRUSH_COLOR = (1, 1, 0, 1)

APP_CONTEXT = {}


class ColorPickerContainer(Bubble):
    
    def __init__(self, *args, **kw):
        picked_callback = kw.get('picker_callback') 
        super(ColorPickerContainer, self).__init__(*args, **kw)
        brush = APP_CONTEXT.get('brush')
        self.color_picker = ColorPicker()
        if brush:
            self.color_picker.color = brush.color
        self.color_picker.bind(color=picked_callback)
        self.add_widget(self.color_picker)


class ColorPickerButton(Button):
        
    def change_color(self, color):
        with self.canvas.after:
            Color(*color)
            d = self.height*0.8
            pos = (self.x + self.width / 2. - d / 2., self.y + 0.1*self.height)
            Ellipse(pos=pos, size=(d, d))


class Brush(object):
    
    def __init__(self, color=DEFAULT_BRUSH_COLOR, width=DEFAULT_BRUSH_WIDTH):
        self.color = color
        self.width = width
        
    def change_width(self, slider, value):
        self.width = value
        slider.label.text = "Thickness: %.2f" % value


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
    
    def __init__(self, *args, **kw):
        super(Graffiti, self).__init__(*args, **kw)
        self.brush = Brush()
        APP_CONTEXT['brush'] = self.brush 
        
    def avoid_collation(func):
        def wrapper(self, touch):
            if self.collide_point(touch.x, touch.y) and not len(touch.grab_list):
                func(self, touch)
        return wrapper
    
    @avoid_collation
    def on_touch_down(self, touch):
        with self.canvas:
            Color(*self.brush.color)
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.brush.width)
    
    @avoid_collation        
    def on_touch_move(self, touch):
        if touch.ud.get('line'):
            touch.ud['line'].points += (touch.x, touch.y)
                
    @avoid_collation
    def on_touch_up(self, touch):
        with self.canvas:
            Color(*self.brush.color)
            d = self.brush.width * 2
            Ellipse(pos=(touch.x - d/2., touch.y-d/2.), size=(d, d))

class MainFrame(FloatLayout):
    """ MainFrame class """
    
    def __init__(self, *args, **kw):
        
        super(MainFrame, self).__init__(*args, **kw)
        self.choose_color_btn.bind(on_press=self.show_color_picker)
        self.thickness_slider.value = DEFAULT_BRUSH_WIDTH
        self.slider_label.text = "Thickness: %s" % DEFAULT_BRUSH_WIDTH
        self.thickness_slider.bind(value=self.graffiti_canvas.brush.change_width)
        # trick to draw circle on choose_color_btn
        Clock.schedule_once(lambda dt: self.choose_color_btn.change_color(DEFAULT_BRUSH_COLOR), 0.5)
        
    def picker_callback(self, inst, color):
        self.graffiti_canvas.brush.color = color
        self.choose_color_btn.change_color(color)
        
    def show_color_picker(self, btn):
        if not hasattr(self, 'color_picker_bubble'):
            self.color_picker_bubble = ColorPickerContainer(picker_callback=self.picker_callback)
            # set color picker bubble position
            inner_x = self.choose_color_btn.pos[0] + self.choose_color_btn.width/2 
            inner_y = self.choose_color_btn.pos[1] + self.choose_color_btn.height
            bubble_x = inner_x - self.color_picker_bubble.size[0]/2
            # else one trick for getting good size of widget
            self.color_picker_bubble.pos = [bubble_x, inner_y]
            self.add_widget(self.color_picker_bubble)
        else:
            color = self.color_picker_bubble.color_picker.color
            #self.graffiti_canvas.brush.color = color
            #self.choose_color_btn.change_color(color)
            self.remove_widget(self.color_picker_bubble)
            del self.color_picker_bubble
            

class GraffitiApp(App):

    def build(self):
        # load color picker kivy file
        #Builder.load_file('colorpicker.kv')
        return MainFrame()


if __name__ == '__main__':
    GraffitiApp().run()
