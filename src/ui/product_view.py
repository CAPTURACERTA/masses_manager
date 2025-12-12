import flet as ft
from application.app import App
from data.table_classes import ProductInfo
from typing import Callable, Literal



class ProductItem(ft.Container):
    def __init__(
        self,
        p_id: str,
        name: str,
        p_type: str,
        production_price: str,
        sale_price: str,
        min_stock: str,
        current_stock: str,
        on_click: Callable[[ft.Container], None],
    ):
        super().__init__()
        self.fields_values = {
            "id":p_id,
            "name":name,
            "type":p_type,
            "production_price":production_price,
            "sale_price":sale_price,
            "min_stock":min_stock,
            "current_stock":current_stock,
        }

        # CONTAINER CONFGS
        self.content=ft.Row(
            [
                ft.Text(
                    p_id, size=16, weight=ft.FontWeight.BOLD, expand=1,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    name, size=16, expand=1, text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    p_type, size=16, expand=1, text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"R$ {float(production_price):.2f}", size=16, expand=1, text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"R$ {float(sale_price):.2f}", size=16, expand=1, text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    min_stock, size=16, expand=1, text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    current_stock, size=16, expand=1, text_align=ft.TextAlign.CENTER,
                ),
            ],
            expand=True
        )
        self.padding=10
        self.border_radius=8
        self.ink=True
        self.on_click=lambda e: on_click(self)


    @classmethod
    def create(
        cls, product_info: ProductInfo, on_click: Callable[[ft.Container], None]
    ):
        return cls(
            product_info["id_produto"],
            product_info["nome"],
            product_info["tipo"],
            product_info["preco_producao"],
            product_info["preco_venda"],
            product_info["estoque_min"],
            product_info["estoque_atual"],
            on_click,
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
            on_click= lambda e: self.update_product()
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
        
    
    def update_lv(self, update = True):
        content = self.app.search_product(self.search_bar.value)

        self.lv.controls.clear()

        for row in content:
            row_info = self.app.get_product_info(row, "all")
            self.lv.controls.append(
                ProductItem.create(row_info, self.on_product_click)
            )

        if self.clicked: self.on_product_click(self.clicked, update=False)
        if update: self.update()

    def add_product(self):
        error_messages = self.app.try_add_product(
            self.add_fields["name"].value,
            self.add_fields["type"].value,
            self.add_fields["production_price"].value,
            self.add_fields["sale_price"].value,
            self.add_fields["min_stock"].value,
            self.add_fields["current_stock"].value
        )

        has_errors = False
        for field_key, msg in error_messages.items():
            self.add_fields[field_key].error_text = msg if msg else None
            if msg:
                has_errors = True

        if not has_errors:
            self.clear_fields(self.add_fields ,update=False)
            self.update_lv(update=False)
            self.page.snack_bar.content.value = "Produto salvo com sucesso!"
            self.page.snack_bar.bgcolor = ft.Colors.GREEN
            self.page.snack_bar.open = True
            self.page.overlay.append(self.page.snack_bar)
            
        self.page.update()

    def update_product(self):
        error_messages = self.app.try_update_product(
            self.update_fields["id"].value,
            self.update_fields["name"].value,
            self.update_fields["type"].value,
            self.update_fields["production_price"].value,
            self.update_fields["sale_price"].value,
            self.update_fields["min_stock"].value,
            self.update_fields["current_stock"].value
        )

        has_errors = False
        for field_key, msg in error_messages.items():
            self.update_fields[field_key].error_text = msg if msg else None
            if msg:
                has_errors = True

        if not has_errors:
            self.on_product_click(self.clicked, update=False)
            self.update_lv(update=False)
            self.page.snack_bar.content.value = "Produto alterado com sucesso!"
            self.page.snack_bar.bgcolor = ft.Colors.GREEN
            self.page.snack_bar.open = True
            self.page.overlay.append(self.page.snack_bar)
            
        self.page.update()

    def on_product_click(self, target: ProductItem, update = True):
        if self.clicked: self.clicked.bgcolor = None
        self.clicked = target if self.clicked != target else None
        if self.clicked:
            self.clicked.bgcolor = ft.Colors.BLUE_GREY_400
            self.tabs.selected_index = 1


        if self.clicked:
            for field_key, msg in target.fields_values.items():
                self.update_fields[field_key].value = msg
        else:
            self.clear_fields(self.update_fields, update=False)

        if update: self.update()

    def clear_fields(self, fields: dict[str, ft.TextField], update = True):
        for field in fields.values():
            field.value = None
            field.error_text = None

        if update: self.update()

    def clear_error_field(self, e: ft.ControlEvent):
        if e.control.error_text:
            e.control.error_text = None
            e.control.update()

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
            disabled=disabled,
            on_change=self.clear_error_field
        )