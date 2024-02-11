
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
    current_total = NumericProperty(0.0)
    current_cart = ListProperty([])
    role = "user"
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)    

    def render(self, _):
        pass

    def add_product(self, inst):
        data = {
            "product_name": inst.product_name,
            "product_code": inst.product_code,
            "product_price": inst.product_price,
            "product_quantity": 1
        }
        self.current_cart.append(data)

    def on_current_cart(self, inst, cart):
        self.ids.gl_receipt.clear_widgets()
        self.ids.gl_products.clear_widgets()
        for item in cart:
            self._add_product(item)
            self.add_receipt_item(item)

    def _add_product(self, product: dict):
        products_grid = self.ids.gl_products
        pt = ProductTile()
        pt.product_code = product.get("product_code", "")
        pt.product_name = product.get("product_name", "")
        pt.product_quantity = product.get("product_quantity", 0)
        pt.product_price = product.get("product_price", 0)
        pt.quantity_callback = self.quantity_control
        products_grid.add_widget(pt)

    def add_receipt_item(self, item: dict) -> None:
        receiptItem = ReceiptItem()
        receiptItem.product_name = item["product_name"]
        receiptItem.product_quantity = item["product_quantity"]
        receiptItem.product_price = item["product_price"]
        
        self.ids.gl_receipt.add_widget(receiptItem)
    
    def quantity_control(self, tile, increasing: bool=False):
        _quantity = int(tile.product_quantity)
        if increasing:
            _quantity += 1
        else:
            _quantity -= 1
        
        if _quantity <= 1:
            _quantity = 1
    
        data = {
            "product_name": tile.product_name,
            "product_code": tile.product_code,
            "product_price": tile.product_price,
            "product_quantity": 1
        }
        fetched_quantity = data.get("product_quantity")
        fetched_price = data.get("product_price")
        single_product_price = fetched_price/fetched_quantity if fetched_quantity > 0 else 0
        _product_id = data.get("product_code")

        tmp = list(self.current_cart)
        tgt = None
        for i, product in enumerate(tmp):
            if product["product_code"] == _product_id:
                tgt = i
                break

        data["product_quantity"] = _quantity
        data["product_price"] = _quantity * single_product_price

        self.current_cart.pop(i)
        self.current_cart.insert(i, data)


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


class ReceiptItem(BoxLayout):
    product_name = StringProperty("")
    product_quantity = NumericProperty(0)
    product_price = NumericProperty(0)
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass
