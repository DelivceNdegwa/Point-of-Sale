from random import randint
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.properties import ColorProperty, ListProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.core.window import Window

from kivy.metrics import dp, sp

Builder.load_string("""
<FlatField>:
    padding: [dp(6), (self.height - self.line_height)/2]


<SuggestionWidget>:
    size_hint_y: None
    height: dp(42)
    spacing: dp(8)
    padding: [dp(8), dp(4)]
    canvas.before:
        Color:
            rgba: app.color_secondary_bg
        Rectangle:
            pos: self.pos
            size: self.size
    Text:
        text:root.product_code
        color: app.color_primary_text
        font_size: app.fonts.size.h4
        font_name: app.fonts.body
        size_hint_x: .3

    Text:
        text:root.product_name
        color: app.color_primary_text
        font_size: app.fonts.size.h4
        font_name: app.fonts.body
        size_hint_x: .5

    Text:
        text:f"KES {round(root.product_price, 2)}"
        color: app.color_primary_text
        font_size: app.fonts.size.h4
        font_name: app.fonts.body
        size_hint_x: .2
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
    suggestion_results = ListProperty([])
    suggested_products = ListProperty([])
    suggestion_widget = ObjectProperty(allownone=True)
    callback = ObjectProperty(allownone=True)
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
        suggestions = self.get_suggestions(suggestion)
        self.suggestion_results = suggestions

        try:
            self.dropdown = DropDown()
            self.dropdown.autowidth = False
            self.dropdown.size_hint_x = None
            self.dropdown.width = Window.width*.4
            
            for result in self.suggestion_results:
                btn = SuggestionWidget()
                btn.product_name = result["product_name"]
                btn.product_code = result["product_code"]
                btn.product_price = result["product_price"]
                btn.size_hint_y = None
                btn.height = dp(54)
                btn.bind(on_release=self.suggest)
                self.dropdown.add_widget(btn)

            if len(self.suggestion_results) > 0:
                self.dropdown.open(self)
        except Exception as e:
            print(e)


    def suggest(self, inst):
        if self.callback:
            self.callback(inst)
        if self.dropdown:
            self.dropdown.dismiss()
            self.dropdown = None

    def get_suggestions(self, suggestion):
        products = self.suggested_products
        suggested_prods = [
            suggested_product for suggested_product in products
            if (suggestion.lower() in suggested_product.get("product_name").lower() or
                suggestion in str(suggested_product.get("product_price")) or
                suggestion in suggested_product.get("product_code"))
        ]
        return suggested_prods

class SuggestionWidget(ButtonBehavior, BoxLayout):
    product_code = StringProperty("")
    product_name = StringProperty("")
    product_price = NumericProperty(0)


class AmountTendered(FlatField):
    amount_total = NumericProperty(0)
    amount_tendered = NumericProperty(0)


    