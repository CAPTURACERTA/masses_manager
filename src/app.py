import flet as ft
from db_manager import DbManager
from product_view import ProducView


class App(ft.Column):
    def __init__(self, dbm: DbManager):
        super().__init__()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.dbm = dbm

        self.product_view = ProducView({})

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

        self.controls = [
            ft.Container(
                content=self.tabs,
                width=1000
            )
        ]

    def start(self,):
        ...

    

    # VALIDAÇÕES

    def check_product_name(self,):
        ...