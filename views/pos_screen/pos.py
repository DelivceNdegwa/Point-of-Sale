
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

    def __update_current_total(self):
        total = 0.0
        for product in self.current_cart:
            total += product["product_price"]
        self.current_total = total

    def on_current_cart(self, inst, cart):
        self.ids.gl_receipt.clear_widgets()
        self.ids.gl_products.clear_widgets()
        for item in cart:
            self._add_product(item)
            self.add_receipt_item(item)

    def add_product(self, inst):
        data = {
            "product_name": inst.product_name,
            "product_code": inst.product_code,
            "product_price": inst.product_price,
            "product_quantity": 1
        }
        self.current_cart.append(data)
        self.__update_current_total()

    def _add_product(self, product: dict):
        products_grid = self.ids.gl_products
        pt = ProductTile()
        pt.product_code = product.get("product_code", "")
        pt.product_name = product.get("product_name", "")
        pt.product_quantity = product.get("product_quantity", 0)
        pt.product_price = product.get("product_price", 0)
        pt.quantity_callback = self.quantity_control
        pt.product_remove = self.delete_product_from_cart
        products_grid.add_widget(pt)

    def add_receipt_item(self, item: dict) -> None:
        receiptItem = ReceiptItem()
        receiptItem.product_name = item["product_name"]
        receiptItem.product_quantity = item["product_quantity"]
        receiptItem.product_price = item["product_price"]
        
        self.ids.gl_receipt.add_widget(receiptItem)

    def delete_product_from_cart(self, tile):
        tgt = None
        temp = list(self.current_cart)
        for i, product in enumerate(temp):
            if product["product_code"] == tile.product_code:
                tgt = i
                break
        self.current_cart.pop(i)
        self.__update_current_total()


    def quantity_control(self, tile, increasing: bool=False):
        _product_id = tile.product_code
        _quantity = int(tile.product_quantity)
        _price = float(tile.product_price)
        single_product_price = round(_price / _quantity if _quantity > 0 else 0, 2)

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

        tmp = list(self.current_cart)
        tgt = None
        for i, product in enumerate(tmp):
            if product["product_code"] == _product_id:
                tgt = i
                break

        data["product_quantity"] = _quantity
        data["product_price"] = single_product_price * _quantity

        self.current_cart.pop(i)
        self.current_cart.insert(i, data)
        self.__update_current_total()


class ProductTile(BoxLayout):
    product_code = StringProperty("")
    product_name = StringProperty("")
    product_quantity = NumericProperty(0)
    product_price = NumericProperty(0)
    quantity_callback = ObjectProperty(allownone=True)
    product_remove = ObjectProperty(allownone=True)
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
