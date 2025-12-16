from data.db_manager import DbManager
from data.table_classes import ProductColumns, ClientColumns
from typing import Literal, get_args
from sqlite3 import Row


class App:
    def __init__(self, dbm: DbManager):
        self.dbm = dbm

    # PRODUCT & CLIENT

    def try_add_product(self, **data):
        """Returns a dict with errors assigned to each field"""
        error_messages = {}
        for arg in get_args(ProductColumns)[1:-1]:
            error_messages[arg] = ""

        error_messages["nome"] = self._validate_name("produtos", data["nome"])
        error_messages["tipo"] = "Obrigatório" if not data["tipo"] else ""

        prod_price_val, error_messages["preco_producao"] = (
            self._validate_and_convert_num(data["preco_producao"], is_float=True)
        )
        sale_price_val, error_messages["preco_venda"] = self._validate_and_convert_num(
            data["preco_venda"], is_float=True
        )
        min_stock_val, error_messages["estoque_min"] = self._validate_and_convert_num(
            data["estoque_min"], is_float=False
        )
        curr_stock_val, error_messages["estoque_atual"] = (
            self._validate_and_convert_num(data["estoque_atual"], is_float=False)
        )

        if not any(error_messages.values()):
            self.dbm.add_product(
                str(data["nome"]),
                str(data["tipo"]),
                prod_price_val,
                sale_price_val,
                min_stock_val,
                curr_stock_val,
            )

        return error_messages

    def try_update_product(self, **data):
        """Returns a dict with errors assigned to each field"""
        error_messages = {}
        for arg in get_args(ProductColumns)[1:-1]:
            error_messages[arg] = ""

        error_messages["nome"] = self._validate_name(
            "produtos", data["nome"], instance_id=data["id_produto"]
        )

        prod_price_val, error_messages["preco_producao"] = (
            self._validate_and_convert_num(data["preco_producao"], is_float=True)
        )
        sale_price_val, error_messages["preco_venda"] = self._validate_and_convert_num(
            data["preco_venda"], is_float=True
        )
        min_stock_val, error_messages["estoque_min"] = self._validate_and_convert_num(
            data["estoque_min"], is_float=False
        )
        curr_stock_val, error_messages["estoque_atual"] = (
            self._validate_and_convert_num(data["estoque_atual"], is_float=False)
        )

        if not any(error_messages.values()):
            self.dbm.update_product(
                int(data["id_produto"]),
                str(data["nome"]),
                str(data["tipo"]),
                prod_price_val,
                sale_price_val,
                min_stock_val,
                curr_stock_val,
            )

        return error_messages

    def try_add_client(self, **data):
        """Returns a dict with errors assigned to each field"""
        error_messages = {}
        for arg in get_args(ClientColumns)[1:-1]:
            error_messages[arg] = ""

        error_messages["nome"] = self._validate_name("clientes", data["nome"])

        if not any(error_messages.values()):
            self.dbm.add_client(str(data["nome"]), str(data["contato"]))

        return error_messages

    def try_update_client(self, **data):
        """Returns a dict with errors assigned to each field"""
        error_messages = {}
        for arg in get_args(ClientColumns)[1:-1]:
            error_messages[arg] = ""

        error_messages["nome"] = self._validate_name(
            "clientes", data["nome"], instance_id=data["id_cliente"]
        )

        if not any(error_messages.values()):
            self.dbm.update_client(
                int(data["id_cliente"]), str(data["nome"]), str(data["contato"])
            )

        return error_messages

    def get_product_info(
        self, product_id_or_row: int | Row, column: ProductColumns = "all"
    ):
        return self.dbm.get_table_row_info("produtos", product_id_or_row, column)

    def get_client_info(
        self, client_id_or_row: int | Row, column: ClientColumns = "all"
    ):
        return self.dbm.get_table_row_info("clientes", client_id_or_row, column)

    # SEARCHS

    def search_product(self, term: str = None):
        if not term:
            return self.dbm.get_by_table("produtos")
        return self.dbm.get_by_text("produtos", term)

    def search_client(self, term: str = None):
        if not term:
            return self.dbm.get_by_table("clientes")
        return self.dbm.get_by_text("clientes", term)

    # VALIDATIONS

    def _validate_and_convert_num(
        self, value: str, is_float: bool
    ) -> tuple[float | int | None, str]:
        """
        Try to convert and validate the number.
        \nTuple: (Value converted, Error message)
        """
        if value == "":
            return None, "Obrigatório"

        if isinstance(value, (float, int)):
            return value, ""

        try:
            if is_float:
                num = float(value.replace(",", "."))
            else:
                num = int(value)

            if num < 0:
                return None, "Não pode ser negativo"

            return num, ""

        except ValueError:
            return None, "Deve ser um número válido"

    def _validate_name(
        self,
        table: Literal["produtos", "clientes"],
        name: str,
        instance_id: int = None,
    ):
        if existing_row := self.dbm.get_by_name(table, name):
            if instance_id and instance_id != self.dbm.get_table_row_info(
                table,
                existing_row,
                ("id_produto" if table == "produtos" else "id_cliente"),
            ):
                return "Nome existente"
        elif not name:
            return "Obrigatório"
        return ""
