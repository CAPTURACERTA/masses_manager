from data.db_manager import DbManager
from typing import Literal
from sqlite3 import Row


class App:
    def __init__(self, dbm: DbManager):
        self.dbm = dbm

    # PRODUCT

    def try_add_product(
        self,
        name: str,
        p_type: str,
        production_price: str,
        sale_price: str,
        min_stock: str,
        current_stock: str
    ) -> dict[
        Literal[
            "name", "type", "production_price", "sale_price", "min_stock", "current_stock"
        ], str
    ]:
        """Returns a dict with errors assigned to each field"""
        error_messages = {
            "name": "", "type": "", "production_price": "",
            "sale_price": "", "min_stock": "", "current_stock": ""
        }

        error_messages["name"] = self._validate_name("produtos", name, can_empty=False)
        error_messages["type"] = "Obrigatório" if not p_type else ""
        
        prod_price_val, error_messages["production_price"] = self._validate_and_convert_num(production_price, is_float=True, can_empty=False)
        sale_price_val, error_messages["sale_price"] = self._validate_and_convert_num(sale_price, is_float=True, can_empty=False)
        min_stock_val, error_messages["min_stock"] = self._validate_and_convert_num(min_stock, is_float=False, can_empty=False)
        curr_stock_val, error_messages["current_stock"] = self._validate_and_convert_num(current_stock, is_float=False, can_empty=False)

        if any(error_messages.values()):
            return error_messages 

        self.dbm.add_product(
            name,
            p_type,
            prod_price_val, 
            sale_price_val,
            min_stock_val,
            curr_stock_val
        )

        return error_messages 

    def try_update_product(
        self,
        p_id: int,
        name: str,
        p_type: str,
        production_price: str,
        sale_price: str,
        min_stock: str,
        current_stock: str
    ) -> dict[
        Literal[
            "name", "type", "production_price", "sale_price", "min_stock", "current_stock"
        ], str
    ]:
        """Returns a dict with errors assigned to each field"""
        error_messages = {
            "name": "", "type": "", "production_price": "",
            "sale_price": "", "min_stock": "", "current_stock": ""
        }

        error_messages["name"] = self._validate_name("produtos", name, instance_id=p_id)
        
        prod_price_val, error_messages["production_price"] = self._validate_and_convert_num(production_price, is_float=True)
        sale_price_val, error_messages["sale_price"] = self._validate_and_convert_num(sale_price, is_float=True)
        min_stock_val, error_messages["min_stock"] = self._validate_and_convert_num(min_stock, is_float=False)
        curr_stock_val, error_messages["current_stock"] = self._validate_and_convert_num(current_stock, is_float=False)

        if any(error_messages.values()):
            return error_messages 
        
        self.dbm.update_product(
            int(p_id),
            name=name,
            p_type=p_type,
            production_price=prod_price_val,
            sell_price=sale_price_val,
            min_stock=min_stock_val,
            current_stock=curr_stock_val
        )

        return error_messages

    def get_product_info(
            self,
            product_info_or_row: int | Row,
            column: Literal[
            "nome", "tipo", "preco_producao", "preco_venda",
            "estoque_min", "estoque_atual", "ativo", "all"
        ]
    ):
        return self.dbm.get_product_info(product_info_or_row, column)

    # VALIDATIONS

    def _validate_and_convert_num(
        self, value: str, is_float: bool, can_empty = True
    ) -> tuple[float | int | None, str]:
        """
        Try to convert and validate the number. 
        \nTuple: (Value converted, Error message)
        """
        if not can_empty and not value:
            return None, "Obrigatório"
        elif can_empty and not value:
            return None, ""
        
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
        can_empty = True
    ):
        if existing_product := self.dbm.get_by_name("produtos", name):
            if table == "produtos": get_func = self.dbm.get_product_info
            else: ...

            if instance_id and instance_id != get_func(existing_product, "id_produto"):
                return "Nome existente"      
                
        elif not can_empty and not name: return "Obrigatório"
        return ""

    # SEARCHS

    def search_product(self, term: str = None):
        if not term: return self.dbm.get_by_table("produtos")
        else: return self.dbm.get_by_text("produtos", term)