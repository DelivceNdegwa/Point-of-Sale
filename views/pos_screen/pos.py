
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict

from kivy.clock import Clock, mainthread

from kivy.properties import StringProperty, ListProperty, ColorProperty, NumericProperty, ObjectProperty
from random import randint

Builder.load_file('views/pos_screen/pos.kv')
class Pos(BoxLayout):
    username = StringProperty("Delivce")
    role = "user"
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)    

    def render(self, _):
        for x in range(5):
            prod = {
                "product_name": f"Product {x}",
                "product_quantity": 1,
                "product_price": 200.00,
                "product_code": str(randint(1000000, 4000000))
            }
            self.add_product(prod)
    
    def add_product(self, product: dict):
        products_grid = self.ids.gl_products
        pt = ProductTile()
        pt.product_code = product.get("product_code", "")
        pt.product_name = product.get("product_name", "")
        pt.product_quantity = product.get("product_quantity", 0)
        pt.product_price = product.get("product_price", 0)
        pt.quantity_callback = self.quantity_control
        products_grid.add_widget(pt)
    
    def quantity_control(self, tile, increasing: bool=False):
        _quantity = int(tile.product_quantity)
        _price = float(tile.product_price)
        _single_product_price = round(_price/_quantity, 2)if(tile.product_quantity > 0) else 0
        if increasing:
            _quantity += 1
        else:
            _quantity -= 1
        
        if _quantity <= 0:
            _quantity = 0
    
        tile.product_quantity = _quantity
        tile.product_price = _single_product_price * _quantity


class ProductTile(BoxLayout):
    product_code = StringProperty("")
    product_name = StringProperty("")
    product_quantity = NumericProperty(0)
    product_price = NumericProperty(0)
    qty_callback = ObjectProperty(allownone=True)
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass
        