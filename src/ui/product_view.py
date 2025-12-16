import flet as ft
from application.app import App
from ui.base_view import BaseView, BaseItem
from data.table_classes import ProductColumns
from typing import get_args


class ProductView(BaseView):
    def __init__(self, app: App):

        add_fields = {
            "nome": BaseView.create_text_field(label="nome"),
            "tipo": BaseView.create_text_field(label="tipo"),
            "preco_producao": BaseView.create_text_field(label="preço produção"),
            "preco_venda": BaseView.create_text_field(label="preço venda"),
            "estoque_min": BaseView.create_text_field(label="estoque mínimo"),
            "estoque_atual": BaseView.create_text_field(label="estoque atual"),
        }
        add_layout = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        add_fields["nome"],
                        add_fields["tipo"],
                    ]
                ),
                ft.Row(
                    controls=[
                        add_fields["preco_producao"],
                        add_fields["preco_venda"],
                        add_fields["estoque_min"],
                        add_fields["estoque_atual"],
                    ]
                ),
            ]
        )

        update_fields = {
            "id_produto": BaseView.create_text_field(
                hint_text="id", disabled=True, expand=1
            ),
            "nome": BaseView.create_text_field(label="nome", expand=10),
            "tipo": BaseView.create_text_field(label="tipo", expand=10),
            "preco_producao": BaseView.create_text_field(label="preço produção"),
            "preco_venda": BaseView.create_text_field(label="preço venda"),
            "estoque_min": BaseView.create_text_field(label="estoque mínimo"),
            "estoque_atual": BaseView.create_text_field(label="estoque atual"),
        }
        update_layout = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        update_fields["id_produto"],
                        update_fields["nome"],
                        update_fields["tipo"],
                    ]
                ),
                ft.Row(
                    controls=[
                        update_fields["preco_producao"],
                        update_fields["preco_venda"],
                        update_fields["estoque_min"],
                        update_fields["estoque_atual"],
                    ]
                ),
            ]
        )

        super().__init__(
            app,
            search_bar_label="Buscar produtos",
            lv_header_labels=(
                "id",
                "nome",
                "tipo",
                "produção",
                "venda",
                "vol. min",
                "vol. atual",
            ),
            add_fields=add_fields,
            add_column_layout=add_layout,
            update_fields=update_fields,
            update_column_layout=update_layout,
            db_table_columns=get_args(ProductColumns),
        )

    def update_list_view(self, update=True):
        rows = self.app.search_product(self.search_bar.value)

        self.lv.controls.clear()

        for row in rows:
            values = self.app.get_product_info(row)
            display_values = [
                values["id_produto"],
                values["nome"],
                values["tipo"],
                f"R$ {values["preco_producao"]}",
                f"R$ {values["preco_venda"]}",
                values["estoque_min"],
                values["estoque_atual"],
            ]
            self.lv.controls.append(
                BaseItem(values, display_values, self.on_item_click)
            )

        if self.clicked_item:
            self.on_item_click(self.clicked_item, update=False)
        if update:
            self.update()

    def add_action(self):
        error_messages = self.app.try_add_product(
            **self.get_field_data(self.add_fields)
        )

        has_errors = False
        for field_key, msg in error_messages.items():
            self.add_fields[field_key].error_text = msg if msg else None
            if msg:
                has_errors = True

        if not has_errors:
            self.clear_fields(self.add_fields, update=False)
            self.update_list_view(update=False)
            self.page.snack_bar.content.value = "Produto salvo com sucesso!"
            self.page.snack_bar.bgcolor = ft.Colors.GREEN
            self.page.snack_bar.open = True
            self.page.overlay.append(self.page.snack_bar)

        self.page.update()

    def update_action(self):
        error_messages = self.app.try_update_product(
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
            self.page.snack_bar.content.value = "Produto alterado com sucesso!"
            self.page.snack_bar.bgcolor = ft.Colors.GREEN
            self.page.snack_bar.open = True
            self.page.overlay.append(self.page.snack_bar)

        self.page.update()
