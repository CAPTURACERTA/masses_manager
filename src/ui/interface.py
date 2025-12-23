import flet as ft
from application.app import App
from ui.product_view import ProductView
from ui.client_view import ClientView


class UI(ft.Container):
    def __init__(self, app: App):
        super().__init__()

        self.app = app
        self.expand = True
        self.width=1000

        # VIEWS
        self.product_view = ProductView(self.app)
        self.client_view = ClientView(self.app)

        # TABS
        self.tabs = self._build_tabs()

        self.content=self.tabs
        
    def start(self,):
        self.product_view.update_lv()
        self.client_view.update_lv()

    # BUILDERS

    def _build_tabs(self):
        return ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Produtos",
                    icon=ft.Icons.INVENTORY_2,
                    content=self.product_view,
                ),
                ft.Tab(
                    text="Clientes",
                    icon=ft.Icons.PEOPLE,
                    content=self.client_view
                )
            ]
        )