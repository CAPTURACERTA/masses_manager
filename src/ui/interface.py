import flet as ft
from application.app import App
from ui.product_view import ProductView
from ui.client_view import ClientView


class UI(ft.Column):
    def __init__(self, app: App):
        super().__init__()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.app = app
        self.expand = True

        # VIEWS
        self.product_view = ProductView(self.app)
        self.client_view = ClientView(self.app)

        # TABS
        self.tabs = ft.Tabs(
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

        # FINAL LAYOUT
        self.controls = [
            ft.Container(
                content=self.tabs,
                width=1000,
                expand=True
            )
        ]


    def start(self,):
        self.product_view.update_lv()
        self.client_view.update_lv()
