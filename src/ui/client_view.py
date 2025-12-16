import flet as ft
from application.app import App
from ui.base_view import BaseItem, BaseView
from data.table_classes import ClientColumns
from typing import get_args


class ClientView(BaseView):
    def __init__(self, app: App):

        add_fields = {
            "nome": BaseView.create_text_field("nome"),
            "contato": BaseView.create_text_field("contato"),
        }
        add_fields_layout = ft.Column(
            controls=[ft.Row(controls=[add_fields["nome"], add_fields["contato"]])]
        )

        update_fields = {
            "id_cliente": BaseView.create_text_field(
                hint_text="id", disabled=True, expand=1
            ),
            "nome": BaseView.create_text_field("nome", expand=10),
            "contato": BaseView.create_text_field("contato", expand=10),
        }
        update_fields_layout = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        update_fields["id_cliente"],
                        update_fields["nome"],
                        update_fields["contato"],
                    ]
                )
            ]
        )

        super().__init__(
            app,
            search_bar_label="Buscar cliente",
            lv_header_labels=("id", "nome", "contato"),
            add_fields=add_fields,
            add_column_layout=add_fields_layout,
            update_fields=update_fields,
            update_column_layout=update_fields_layout,
            db_table_columns=get_args(ClientColumns),
        )

    def update_list_view(self, update=True):
        rows = self.app.search_client(self.search_bar.value)

        self.lv.controls.clear()

        for row in rows:
            values = self.app.get_client_info(row)
            display_values = [
                values["id_cliente"],
                values["nome"],
                values["contato"],
            ]
            self.lv.controls.append(
                BaseItem(values, display_values, self.on_item_click)
            )

        if self.clicked_item:
            self.on_item_click(self.clicked_item, update=False)
        if update:
            self.update()

    def add_action(self):
        error_messages = self.app.try_add_client(**self.get_field_data(self.add_fields))

        has_errors = False
        for field_key, msg in error_messages.items():
            self.add_fields[field_key].error_text = msg if msg else None
            if msg:
                has_errors = True

        if not has_errors:
            self.clear_fields(self.add_fields, update=False)
            self.update_list_view(update=False)
            self.page.snack_bar.content.value = "Cliente salvo com sucesso!"
            self.page.snack_bar.bgcolor = ft.Colors.GREEN
            self.page.snack_bar.open = True
            self.page.overlay.append(self.page.snack_bar)

        self.page.update()

    def update_action(self):
        error_messages = self.app.try_update_client(
            **self.get_field_data(self.update_fields)
        )

        has_errors = False
        for field_key, msg in error_messages.items():
            self.update_fields[field_key].error_text = msg if msg else None
            if msg:
                has_errors = True

        if not has_errors:
            self.on_item_click(self.clicked_item, update=False)
            self.update_list_view(update=False)
            self.page.snack_bar.content.value = "Cliente alterado com sucesso!"
            self.page.snack_bar.bgcolor = ft.Colors.GREEN
            self.page.snack_bar.open = True
            self.page.overlay.append(self.page.snack_bar)

        self.page.update()
