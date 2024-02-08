from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.properties import ColorProperty, ListProperty, ObjectProperty
from kivy.core.window import Window

from kivy.metrics import dp, sp

Builder.load_string("""
<FlatField>:
    padding: [dp(6), (self.height - self.line_height)/2]
""")
class FlatField(TextInput):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.background_normal = ""
        self.background_active = ""
        self.background_disabled = ""
        self.background_color = [0,0,0,0]
        self.write_tab = False

class TextField(FlatField):
    bcolor = ColorProperty([0,0,0,1])
    main_color = ColorProperty([1,1,1,1])
    radius = ListProperty([1])
    def __init__(self, **kw):
        super().__init__(**kw)

        with self.canvas.before:
            self.border_color = Color(rgba=self.bcolor)
            self.border_draw = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
            self.back_color = Color(rgba=self.main_color)
            self.back_draw = RoundedRectangle(
                pos=[self.pos[0]+1.5, self.pos[1]+1.5], 
                size=[self.size[0]-3, self.size[1]-3], 
                radius=self.radius
                )

        self.bind(size=self.update)
        self.bind(pos=self.update)

    def on_main_color(self, inst, value):
        self.back_color.rgba = value

    def on_bcolor(self, inst, value):
        self.border_color.rgba = value

    def update(self, *args):
        self.border_draw.pos = self.pos
        self.border_draw.size = self.size

        self.back_draw.pos=[self.pos[0]+1.5, self.pos[1]+1.5] 
        self.back_draw.size=[self.size[0]-3, self.size[1]-3]

    def on_radius(self, *args): 
        self.back_draw.radius=self.radius
        self.border_draw.radius=self.radius

class OutlineTextField(FlatField):
    bcolor = ColorProperty([0,0,0,1])
    main_color = ColorProperty([1,1,1,1])
    radius = ListProperty([1])
    def __init__(self, **kw):
        super().__init__(**kw)

        with self.canvas.before:
            self.border_color = Color(rgba=self.bcolor)
            self.border_draw = Line(
                width=dp(1.5),
                rounded_rectangle=[self.pos[0], self.pos[1], self.size[0], self.size[1], self.radius[0]]
            )
            # self.border_draw = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
            # self.back_color = Color(rgba=self.main_color)
            # self.back_draw = RoundedRectangle(
            #     pos=[self.pos[0]+1.5, self.pos[1]+1.5], 
            #     size=[self.size[0]-3, self.size[1]-3], 
            #     radius=self.radius
            #     )

        self.bind(size=self.update)
        self.bind(pos=self.update)

    def on_main_color(self, inst, value):
        self.back_color.rgba = value

    def on_bcolor(self, inst, value):
        self.border_color.rgba = value

    def update(self, *args):
        self.border_draw.rounded_rectangle=[self.pos[0], self.pos[1], self.size[0], self.size[1], self.radius[0]]

    def on_radius(self, *args): 
        self.border_draw.rounded_rectangle=[self.pos[0], self.pos[1], self.size[0], self.size[1], self.radius[0]]


class SearchBar(FlatField):
    suggestion_results = ListProperty(['Product 01', 'Product 02', 'Product 03'])
    suggestion_widget = ObjectProperty(allownone=True)
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mutiline = False
        self.dropdown = None

    def on_text(self, inst, text: str):
        try:
            if self.dropdown:
                self.dropdown.dismiss()
                self.dropdown = None
            
            # Show current suggestions
            self.show_suggestions(text)
        except Exception as e:
            print(e)

    def open_dropdown(self, *args):
        if self.dropdown:
            self.dropdown.open(self)

    def keyboard_on_key_down(self, window, key_code, text, modifier):
        if self.dropdown:
            self.dropdown.dismiss()
            self.dropdown = None
        else:
            super().keyboard_on_key_down(window, key_code, text, modifier)

    def show_suggestions(self, suggestion: str):
        try:
            self.dropdown = DropDown()
            self.dropdown.autowidth = False
            self.dropdown.size_hint_x = None
            self.dropdown.width = Window.width*.4
            
            for result in self.suggestion_results:
                btn = Button()
                if self.suggestion_widget:
                    btn = self.suggestion_widget()
                btn.text = result
                btn.size_hint_y = None
                btn.height = dp(54)
                self.dropdown.add_widget(btn)

            if len(self.suggestion_results) > 0:
                self.dropdown.open(self)
        except Exception as e:
            print(e)