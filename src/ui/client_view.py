import flet as ft
from application.app import App
from ui.base_view import BaseView, FieldDict
from data.table_classes import ClientColumns
from typing import get_args


class ClientView(BaseView):
    def __init__(self, app: App):

        self.search_bar = self.create_text_field(
            label="Buscar clientes",
            icon=ft.Icons.SEARCH,
            on_change=lambda e: self.update_lv()
        )

        self.add_fields = self._build_add_fields()
        self.update_fields = self._build_update_fields()

        search_layout = self._create_container_display(self.search_bar)
        add_layout = self._build_add_tab_layout()       
        update_layout = self._build_update_tab_layout()

        lv_headers = get_args(ClientColumns)[:-1]

        super().__init__(
            app,
            search_layout=search_layout,
            lv_headers=lv_headers,
            add_layout=add_layout,
            update_layout=update_layout
        )

    def get_raw_base_items_list(self):
        raw_base_items_list = []
        rows = self.app.search_client(self.search_bar.value)

        for row in rows:
            info = self.app.get_client_info(row)
            raw_base_items_list.append(
                {
                    "values":info,
                    "display_values":[
                        info["id_cliente"],
                        info["nome"],
                        info["contato"],
                    ],
                    "on_left_click": self.on_item_left_click
                }
            )
        
        return raw_base_items_list
    
    def add_action(self):
        error_messages = self.app.try_add_client(
            **self.get_field_data(self.add_fields)
        )
        self.db_action_error_handling(
            error_messages, self.add_fields, "Cliente salvo com sucesso"
        )

    def update_action(self):
        error_messages = self.app.try_update_client(
            **self.get_field_data(self.update_fields)
        )
        self.db_action_error_handling(
            error_messages, self.update_fields, "Cliente alterado com sucesso"
        )

    def _item_left_clicked(self, cliked):
        if cliked:
            self.tabs.selected_index=1
            for key, value in self.clicked_item.values.items():
                if key in self.update_fields:
                    self.update_fields[key].value = value
        else:
            self.clear_fields(self.update_fields, update=False)

    # BUILDERS

    def _build_add_fields(self) -> FieldDict:
        fields = {
            "nome": self.create_text_field(label="nome"),
            "contato": self.create_text_field(label="contato")
        }
        # Configura eventos em lote
        for field in fields.values():
            field.on_change = self.clear_error_field
            field.on_submit = lambda e: self.add_action() 
        return fields
    
    def _build_update_fields(self) -> FieldDict:
        fields = {
            "id_cliente": self.create_text_field(hint_text="id", disabled=True, expand=1),
            "nome": self.create_text_field(label="nome", expand=10),
            "contato": self.create_text_field(label="contato", expand=10)
        }
        for field in fields.values():
            field.on_change = self.clear_error_field
            field.on_submit = lambda e: self.update_action()
        return fields
    
    def _build_add_tab_layout(self):
        return self._create_container_display(
            self._create_column_layout(
                ft.Row(controls=list(self.add_fields.values())),
                ft.Row(
                    controls=[
                        self._create_main_button(
                            "Adicionar", ft.Icons.ADD, lambda e: self.add_action()
                        ),
                        self._create_rubber_button(
                            on_click=lambda e: self.clear_fields(self.add_fields)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        )

    def _build_update_tab_layout(self):
        return self._create_container_display(
            self._create_column_layout(
                ft.Row(controls=list(self.update_fields.values())),
                ft.Row(
                    controls=[
                        self._create_main_button(
                            "Atualizar", ft.Icons.UPDATE, lambda e: self.update_action()
                        ),
                        self._create_rubber_button(
                            on_click=lambda e: self.on_item_left_click(self.clicked_item)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        )