import flet as ft
from application.app import App
from ui.product_view import ProducView


class UI(ft.Column):
    def __init__(self, app: App):
        super().__init__()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.app = app

        # PRODUCT VIEW
        self.product_view = ProducView()

        # TABS
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Produtos",
                    icon=ft.Icons.INVENTORY_2, 
                    content=self.product_view,
                )
            ]
        )

        # FINAL LAYOUT
        self.controls = [
            ft.Container(
                content=self.tabs,
                width=1000
            )
        ]


    def start(self,):
        ...
