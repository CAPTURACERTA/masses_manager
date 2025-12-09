import flet as ft
from sqlite3 import Row
from application.app import App
from typing import Callable, Literal



class ProductItem(ft.Container):
    def __init__(
        self,
        p_id:int,
        name: str,
        p_type: str,
        production_price: float,
        sale_price: float,
        min_stock: int,
        current_stock: int,
        on_click: Callable[[ft.Container], None],
    ):
        super().__init__()
        self.p_id = p_id
        self.name = name
        self.p_type = p_type
        self.production_price = production_price
        self.sale_price = sale_price
        self.min_stock = min_stock
        self.current_stock = current_stock

        # CONTAINER CONFGS
        self.content=ft.Row(
            [
                ft.Text(
                    self.p_id, size=16, weight=ft.FontWeight.BOLD, expand=1,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    self.name, size=16, expand=1, text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    self.p_type, size=16, expand=1, text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"R$ {self.production_price}", size=16, expand=1, text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"R$ {self.sale_price}", size=16, expand=1, text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    self.min_stock, size=16, expand=1, text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    self.current_stock, size=16, expand=1, text_align=ft.TextAlign.CENTER,
                ),
            ],
            expand=True
        )
        self.padding=10
        self.border_radius=8
        self.ink=True
        self.on_click=lambda e: on_click(self)


    @classmethod
    def create(cls, product_row: Row, on_click: Callable[[ft.Container], None]):
        p_id, name, p_type, production_price, sale_price, min_stock, current_stock = product_row
        return cls(
            p_id, name, p_type, production_price, sale_price, min_stock, current_stock, on_click
        )



class ProducView(ft.Column):
    def __init__(self, app: App):
        super().__init__()

        self.app = app

        # SEARCH BAR
        self.search_bar = ft.TextField(
            label="Buscar produto",
            expand=True,
            icon=ft.Icons.SEARCH,
            on_change=lambda e: self.update_lv()
        )

        # SEARCH LIST VIEW 
        self.lv_header = ft.Row(
            [
                ft.Text(
                    "id", size=16, weight=ft.FontWeight.BOLD, expand=1,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "nome", size=16, weight=ft.FontWeight.BOLD, expand=1,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "tipo", size=16, weight=ft.FontWeight.BOLD, expand=1,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "produção", size=16, weight=ft.FontWeight.BOLD, expand=1,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "venda", size=16, weight=ft.FontWeight.BOLD, expand=1,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "vol. min", size=16, weight=ft.FontWeight.BOLD, expand=1,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "vol. atual", size=16, weight=ft.FontWeight.BOLD, expand=1,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],       
        )
        self.lv = ft.ListView(
            expand=True,
            spacing=5,
        )
        self.clicked: ft.Container = None

        # ADD SECTION 
        self.add_fields: dict[
            Literal[
            "name", "type", "production_price", "sale_price", "min_stock", "current_stock"
            ], ft.TextField
        ] = {
            "name": self._create_text_field(label="nome"),
            "type": self._create_text_field(label="tipo"),
            "production_price": self._create_text_field(label="preço produção"),
            "sale_price": self._create_text_field(label="preço venda"),
            "min_stock": self._create_text_field(label="estoque mínimo"),
            "current_stock": self._create_text_field(label="estoque atual"),
        }
        self.add_button = ft.ElevatedButton(
            "Adicionar",
            width=300,
            icon=ft.Icons.ADD,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE,
            on_click= lambda e: self.add_product()
        )
        self.add_rubber_button = ft.IconButton(
            icon=ft.Icons.CLEAR,
            tooltip="Desfazer",
            on_click=lambda e: self.clear_add_fields()
        )
        self.add_container = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [self.add_fields["name"], self.add_fields["type"],]
                    ),

                    ft.Row(
                        [
                            self.add_fields["production_price"],
                            self.add_fields["sale_price"],
                            self.add_fields["min_stock"],
                            self.add_fields["current_stock"]
                        ]
                    ),

                    ft.Row(
                        [self.add_button, self.add_rubber_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
            ),
            margin=ft.margin.only(top=5)
        )

        # UPDATE SECTION
        self.update_fields: dict[
            Literal[
                "id", "name", "type", "production_price", "sale_price", "min_stock", "current_stock"
            ], ft.TextField
        ] = {
            "id": self._create_text_field(hint_text="id", disabled=True, expand=1),
            "name": self._create_text_field(label="nome", expand=10),
            "type": self._create_text_field(label="tipo", expand=10),
            "production_price": self._create_text_field(label="preço produção"),
            "sale_price": self._create_text_field(label="preço venda"),
            "min_stock": self._create_text_field(label="estoque mínimo"),
            "current_stock": self._create_text_field(label="estoque atual"),
        }
        self.update_button = ft.ElevatedButton(
            "Aualizar",
            width=300,
            icon=ft.Icons.REFRESH,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE,
        )
        self.update_rubber_button = ft.IconButton(
            icon=ft.Icons.CLEAR,
            tooltip="Desfazer",
            on_click=lambda e: self.on_product_click(self.clicked)
        )
        self.update_container = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            self.update_fields["id"],
                            self.update_fields["name"],
                            self.update_fields["type"],
                        ]
                    ),

                    ft.Row(
                        [
                            self.update_fields["production_price"],
                            self.update_fields["sale_price"],
                            self.update_fields["min_stock"],
                            self.update_fields["current_stock"],
                        ]
                    ),

                    ft.Row(
                        [self.update_button, self.update_rubber_button],
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
                    content=self.update_container,
                )
            ]
        )

        # FINAL LAYOUT
        self.controls = [
                # search bar
                ft.Container(
                    content=ft.Row([self.search_bar]),
                    margin=ft.margin.only(top=10),
                ),

                # lv container
                ft.Container(
                    content=ft.Column(
                        [
                            self.lv_header,

                            ft.Container(
                                content=self.lv,
                                expand=True,
                                padding=0
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
        
    
    def update_lv(self):
        content = self.app.search_product(self.search_bar.value)

        self.lv.controls.clear()

        for row in content:
            self.lv.controls.append(
                ProductItem.create(row, self.on_product_click)
            )

        if self.clicked: self.on_product_click(self.clicked)
        else: self.update()

    def add_product(self):
        error_messages = self.app.try_add_product(
            self.add_fields["name"].value,
            self.add_fields["type"].value,
            self.add_fields["production_price"].value,
            self.add_fields["sale_price"].value,
            self.add_fields["min_stock"].value,
            self.add_fields["current_stock"].value
        )

        for field, msg in error_messages.items():
            self.add_fields[field].error_text = msg

        self.update_lv()

    def on_product_click(self, target: ProductItem):
        if self.clicked: self.clicked.bgcolor = None
        self.clicked = target if self.clicked != target else None
        if self.clicked:
            self.clicked.bgcolor = ft.Colors.RED_200
            self.tabs.selected_index = 1


        self.update_fields["id"].value = target.p_id if self.clicked else ""
        self.update_fields["name"].value = target.name if self.clicked else ""
        self.update_fields["type"].value = target.p_type if self.clicked else ""
        self.update_fields["production_price"].value = target.production_price if self.clicked else ""
        self.update_fields["sale_price"].value = target.sale_price if self.clicked else ""
        self.update_fields["min_stock"].value = target.min_stock if self.clicked else ""
        self.update_fields["current_stock"].value = target.current_stock if self.clicked else ""

        if not self.clicked:
            for field in self.update_fields.values():
                field.error_text = ""

        self.update()

    def clear_add_fields(self):
        for field in self.add_fields.values():
            field.value = ""
            field.error_text = ""

        self.update()

    # HELPERS

    def _create_text_field(
            self,
            label="",
            hint_text="",
            expand=True,
            disabled=False,
    ):
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            expand=expand,
            height=40,
            disabled=disabled
        )