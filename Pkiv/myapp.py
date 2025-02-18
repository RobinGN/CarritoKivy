from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Window.clearcolor = (1, 1, 1, 1)

        self.total_price = 0  
        self.cart_items = {}

        
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        
        self.header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        
        self.price_label = Label(
            text=f"Total: ${self.total_price}",
            font_size=22,
            bold=True,
            color='#FF0000'
        )
        self.header_layout.add_widget(self.price_label)

        
        self.checkout_button = Button(
            text="Proceed to Checkout",
            size_hint_x=None,
            width=250
        )
        self.checkout_button.bind(on_press=self.go_to_checkout)
        self.header_layout.add_widget(self.checkout_button)

        self.main_layout.add_widget(self.header_layout)

        
        self.main_layout.add_widget(Image(source="Amazon_logo.png", size_hint=(None, None), size=(200, 100)))

        scroll_view = ScrollView(size_hint=(1, 5))
        product_grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
        product_grid.bind(minimum_height=product_grid.setter('height'))

        self.products = [
            ("Audifonos XM4", "xm4s.jpg", 400),
            ("Nintendo Switch", "Nintendo-Switch.png", 300),
            ("iPhone X", "iphone.png", 200),
            ("Xbox Controller", "xboxcon.png", 60),
        ]

        for name, image, price in self.products:
            btn = Button(
                text=f"{name}\nPrice: ${price}",
                size_hint=(1, None),
                height=400,
                bold=True,
                background_normal=image,  
                background_down=image
            )
            btn.bind(on_press=lambda instance, p=price, n=name: self.add_to_cart(p, n))
            product_grid.add_widget(btn)

        scroll_view.add_widget(product_grid)
        self.main_layout.add_widget(scroll_view)

        self.add_widget(self.main_layout)

    def add_to_cart(self, price, name):
        self.total_price += price
        self.cart_items[name] = self.cart_items.get(name, 0) + 1
        self.price_label.text = f"Total: ${self.total_price}"

    def go_to_checkout(self, instance):
        checkout_screen = self.manager.get_screen('checkout')
        checkout_screen.update_cart(self.cart_items, self.total_price)

        self.total_price = 0
        self.cart_items = {}
        self.price_label.text = f"Total: ${self.total_price}"

        self.manager.current = 'checkout'


class CheckoutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.payment_status = Label(
            text="",
            font_size=20,
            bold=True,
            color='#008000'  
        )
        self.layout.add_widget(self.payment_status)

        self.cart_label = Label(font_size=18, color='#000000')
        self.layout.add_widget(self.cart_label)

        self.clear_cart_button = Button(text="Empty Cart", size_hint_y=None, height=50)
        self.clear_cart_button.bind(on_press=self.clear_cart)
        self.layout.add_widget(self.clear_cart_button)

        self.payment_button = Button(text="Make Payment", size_hint_y=None, height=50)
        self.payment_button.bind(on_press=self.make_payment)
        self.layout.add_widget(self.payment_button)

        self.add_widget(self.layout)

    def update_cart(self, items, total):
        self.payment_status.text = ""  
        if not items:
            self.cart_label.text = "Cart is empty!"
        else:
            item_list = "\n".join([f"{name} x{count}" for name, count in items.items()])
            self.cart_label.text = f"Items:\n{item_list}\nTotal: ${total}"

    def clear_cart(self, instance):
        self.payment_status.text = ""  
        self.manager.current = 'main'
        self.reset_cart()

    def make_payment(self, instance):
        self.payment_status.text = "Payment Done!"  
        self.reset_cart()

        from kivy.clock import Clock
        Clock.schedule_once(self.go_back_to_main, 1.5)

    def go_back_to_main(self, dt):
        self.manager.current = 'main'

    def reset_cart(self):
        main_screen = self.manager.get_screen('main')
        main_screen.total_price = 0
        main_screen.cart_items = {}
        main_screen.price_label.text = f"Total: ${main_screen.total_price}"
        self.cart_label.text = "Cart is empty!"

class ShoppingApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CheckoutScreen(name='checkout'))
        return sm

if __name__ == "__main__":
    ShoppingApp().run()
