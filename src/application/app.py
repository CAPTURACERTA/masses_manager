from data.db_manager import DbManager
from typing import Literal


class App:
    def __init__(self, dbm: DbManager):
        self.dbm = dbm


    def try_add_product(
        self,
        name: str,
        p_type: str,
        production_price: float,
        sale_price: float,
        min_stock: int,
        current_stock: int
    ) -> dict[
        Literal[
            "name",
            "p_type",
            "production_price",
            "sale_price",
            "min_stock",
            "current_stock",
        ], str
    ]:
        error_messages = {
            "name": "",
            "type": "",
            "production_price": "",
            "sale_price": "",
            "min_stock": "",
            "current_stock": "",
        }

        error_messages["name"] = self._validate_name("produtos", name, False)
        error_messages["type"] = "Vazio" if not p_type else ""
        error_messages["production_price"] = self._validate_num(production_price)
        error_messages["sale_price"] = self._validate_num(sale_price)
        error_messages["min_stock"] = self._validate_num(min_stock)
        error_messages["current_stock"] = self._validate_num(current_stock)

        for error in error_messages.values():
            if error: break
        else:
            self.dbm.add_product(
                name,
                p_type,
                float(production_price),
                float(sale_price),
                int(min_stock),
                int(current_stock)
            )

        return error_messages

    def _validate_name(
        self,
        table: Literal["produtos", "clientes"],
        name: str,
        can_empty = True
    ):
        if self.dbm.get_by_name(table, name): return "Nome existente"
        elif not can_empty and not name: return "Vazio"
        else: return ""

    # error na checagem
    def _validate_num(self, num: float | str | int):
        if isinstance(num, str) and num.isnumeric():
            if float(num) < 0: return "Menor do que zero"
            else: return ""

        if isinstance(num, float) or isinstance(num, int):
            if num < 0: return "Menor do que zero"
            else: return ""

        if not isinstance(num, float) or not isinstance(num, int):
            return "Não é um número"
        else: return ""

    def search_product(self, term: str = None):
        if not term: return self.dbm.get_by_table("produtos")
        else: return self.dbm.get_by_text("produtos", term)