import flet as ft
from application.app import App
from ui.base_view import BaseView, Calendar, ItemPicker, BaseItem
from data.table_classes import TransactionColumns
from typing import get_args


class ItemsListView(ft.Container):
    def __init__(self, lv: ft.ListView, app: App):
        super().__init__()

        self.lv = lv
        self.app = app
        self.product_picker = ItemPicker(app, "produtos")

        self.expand=True
        self.visible=False

        self.add_product_field = BaseView.create_text_field(
            hint_text="Procurar Produto",
            on_focus=lambda _: self.open_product_picker(self.add_product_field),
            icon=ft.Icons.SEARCH,
            expand=3
        )
        self.add_amount_field = BaseView.create_text_field(
            label="Quantidade",
            expand=3,
            on_change=lambda _: self.clear_error_field
        )

        self.content=ft.Stack(
            controls=[
                self._build_bg(),
                self._build_main_content()
            ],
            alignment=ft.alignment.center,
        )

    def open_product_picker(self, target_text_field):
        self.product_picker.page = self.page
        self.product_picker.appear(target_text_field)

    def appear(self):
        self.visible = True
        if self not in self.page.overlay:
            self.page.overlay.append(self)

        self.page.update()

    def disappear(self):
        self.visible = False
        self.page.overlay.remove(self)
        self.page.update()

    def add_item(self):
        error = False
        if not self.add_product_field.value:
            self.add_product_field.error_text = "Obrigatório"
            error = True
        if not self.add_amount_field.value:
            self.add_amount_field.error_text = "Obrigatório"
            error = True
        if not self.add_amount_field.value.isnumeric():
            self.add_amount_field.error_text = "Apenas números"
            error = True

        if not error:
            self.lv.controls.append(
                BaseItem(
                    {
                        "nome": self.add_product_field.value,
                        "quantidade": int(self.add_amount_field.value)
                    },
                    [self.add_product_field.value, self.add_amount_field.value],
                    self.on_left_click
                )
            )
            self.clear_fields(self.add_product_field, self.add_amount_field, update=False)

        self.update()

    def on_left_click(self, item: BaseItem):
        self.lv.controls.remove(item)
        self.lv.update()

    # HELPERS

    def clear_fields(self, *fields: ft.TextField, update=True):
        for field in fields:
            field.value = None
            field.error_text = None

        if update: self.update()

    def clear_error_field(self, e: ft.ControlEvent):
        if e.control.error_text:
            e.control.error_text = None
            e.control.update()

    # BUILDERS

    def _build_bg(self,):
        return ft.GestureDetector(
            on_tap=lambda _: self.disappear(),
            content=ft.Container(
                expand=True,
                bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            )
        )

    def _build_main_content(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=self.lv,
                        height=200,
                        border_radius=12,
                        bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    ),

                    ft.Row(
                        controls=[
                            self.add_product_field,
                            self.add_amount_field,
                        ]
                    ),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            BaseView._create_main_button(
                                "adicionar", ft.Icons.ADD, lambda _: self.add_item()
                            ),
                            BaseView._create_rubber_button(
                                ft.Colors.RED, "desfazer", lambda _: self.clear_fields(
                                    self.add_product_field, self.add_amount_field
                                )
                            )
                        ]
                    )
                    
                ],
                tight=True
            ),
            bgcolor=ft.Colors.WHITE,
            width=600,          
            padding=20,
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK54), 
        )

class TransactionView(BaseView):
    def __init__(self, app: App):

        self.client_picker = ItemPicker(app, "cliente")
        self.search_client_field = BaseView.create_text_field(
            hint_text="Procurar cliente",
            on_focus=lambda _: self.open_client_picker(self.search_client_field),
            expand=False,
            icon=ft.Icons.SEARCH
        )

        self.start_date = Calendar("INÍCIO")
        self.end_date = Calendar("FIM")

        self.add_fields = self._build_add_fields()

        self.items_list_lv = ft.ListView(
            expand=True,
            spacing=5,
        )
        self.items_view = ItemsListView(self.items_list_lv, app)

        super().__init__(
            app,
            search_layout=self._build_search_layout(),
            lv_headers=(
                "id_transacao", "cliente", "data", "tipo", "estado",
                "valor_total", "valor_aberto"
            ),
            add_layout=self._build_add_layout(),
            update_layout=ft.Container()
        )


    def get_raw_base_items_list(self):
        ...
    
    def add_action(self):
        ...

    def update_action(self):
        ...

    def _item_left_clicked(self, cliked):
        ...

    def open_client_picker(self, target_text_field):
        self.client_picker.page = self.page
        self.client_picker.appear(target_text_field)

    def open_items_view(self):
        self.items_view.page = self.page
        self.items_view.appear()

    # BUILDERS

    def _build_calendar_row(self):
        return ft.Row(
            controls=[
                ft.Text(value="De"),
                self.start_date,
                ft.Text(value="Até"),
                self.end_date
            ]
        )
    
    def _build_search_layout(self):
        return BaseView._create_container_display(
            ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            self.search_client_field,
                            self._create_rubber_button(
                                ft.Colors.RED,
                                "apagar",
                                lambda _: self.clear_fields(self.search_client_field)
                            ),
                        ]
                    ),

                    self._build_calendar_row()
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            )
        )
    
    def _build_add_fields(self):
        fields = {
            "cliente": BaseView.create_text_field(
                                hint_text="procurar cliente",
                                on_focus=lambda e: self.open_client_picker(
                                    self.add_fields["cliente"]
                                ),
                                icon=ft.Icons.SEARCH
                            ),
            "tipo": BaseView.create_text_field(
                label="tipo", hint_text="(P) pedido ou (V) venda "
            ),
            "pagamento": BaseView.create_text_field(label="pagamento"),
            "data": Calendar("Data da transação"),
        }
        for field in fields.values():
            if isinstance(field, ft.TextField):
                field.on_change = self.clear_error_field
                field.on_submit = lambda e: self.add_action() 
        return fields

    def _build_add_layout(self):
        return BaseView._create_container_display(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=list(self.add_fields.values())
                    ),
                    self._build_items_list_lv(),
                    ft.Row(
                        controls=[BaseView._create_main_button("adicionar", ft.Icons.ADD)],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            )
        )
    
    def _build_items_list_lv(self):
        header = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value="Lista de items",
                    size=16,
                    expand=1,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                )
            ]
        )
        return ft.Container(
            content=header,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=12,
            padding=10,
            on_click= lambda _: self.open_items_view()
        )