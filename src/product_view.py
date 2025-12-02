import flet as ft
from typing import TypedDict


class ProductBorrowedFuncs(TypedDict):
    ...

class ProducView(ft.Column):
    def __init__(self, borrowed_funcs: ProductBorrowedFuncs):
        super().__init__()

        self.funcs = borrowed_funcs

        # SEARCH BAR
        self.search_bar = ft.TextField(
            label="Buscar produto",
            expand=True,
            icon=ft.Icons.SEARCH,
            on_change=...
        )

        # LIST VIEW 
        self.lv_header = ft.Row(
            [
                ft.Text("id", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("nome", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("tipo", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("preço produção", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("preço venda", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("estoque mínimo", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("estoque atual", size=16, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        self.lv = ft.ListView(
            expand=True,
            spacing=5,
            padding=10
        )

        # ADD 
        self.add_name_bar = ft.TextField(label="nome", expand=True, height=40)
        self.add_type_bar = ft.TextField(label="tipo", expand=True, height=40)
        self.add_production_price_bar = ft.TextField(label="preço produção", expand=True, height=40)
        self.add_sale_price_bar = ft.TextField(label="preço venda", expand=True, height=40)
        self.add_min_stock_bar = ft.TextField(label="estoque mínimo", expand=True, height=40)
        self.add_current_stock_bar = ft.TextField(label="estoque atual", expand=True, height=40)
        self.add_button = ft.ElevatedButton(
            "Adicionar",
            width=300,
            icon=ft.Icons.ADD,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE,
        )
        self.add_container = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [self.add_name_bar, self.add_type_bar,]
                    ),

                    ft.Row(
                        [
                            self.add_production_price_bar,
                            self.add_sale_price_bar,
                            self.add_min_stock_bar,
                            self.add_current_stock_bar,
                        ]
                    ),

                    ft.Row(
                        [self.add_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
            ),
            margin=ft.margin.only(top=5)
        )

        # TABS
        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="Adicionar",
                    icon=ft.Icons.ADD,
                    height=50,
                    content=self.add_container,
                ),

                ft.Tab(
                    text="Atualizar",
                    icon=ft.Icons.UPDATE,
                    height=50,
                    content=ft.Text("gugugaga"),
                )
            ]
        )

        # FINAL LAYOUT
        self.controls = [
                # search bar
                ft.Container(
                    content=ft.Row([self.search_bar]),
                    margin=ft.margin.only(top=5),
                ),

                # lv container
                ft.Container(
                    content=ft.Column(
                        [
                            self.lv_header,

                            ft.Container(
                                content=self.lv,
                                expand=True,
                            )
                        ],
                        height=300,
                    ),
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    border_radius=12,
                    padding=10,
                ),

                # tabs (add,change,...)
                self.tabs
            ]