from database import MassesDatabase
from sqlite3 import Cursor
import exceptions
from typing import Literal, TypedDict
import datetime


class Item(TypedDict):
    item_id: int
    item_amount: int


class DbManager:
    def __init__(self, db: MassesDatabase):
        self.db = db


    def add_product(
        self,
        name: str,
        p_type: str,
        production_price: float,
        sale_price: float,
        min_stock: int,
        current_stock: int = 0,
    ):
        with self.db.get_connection() as conn:
            self.db.add_product(
                conn.cursor(),
                name,
                p_type,
                production_price,
                sale_price,
                min_stock,
                current_stock
            )

    def add_client(self, name: str, contact: str = None):
        with self.db.get_connection() as conn:
            self.db.add_client(conn.cursor(), name, contact)

    def register_transaction(
        self,
        client: str | int,
        t_type: Literal["P", "V"],
        items: list[Item],
        date: str = datetime.date.today(),
    ):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            errors = []
            errors.append(self._try_client(cursor, client))
            if t_type not in ["P", "V"]: errors.append(exceptions.TransactionTypeError)

            
        
    
    # ↓ HELPERS ↓ #

    def _check_existence(
        self,
        db_cursor: Cursor,
        table: Literal["produtos", "clientes", "transacoes",
                    "itens_transacao", "pagamentos", "producoes"],
        target: str | int,
    ):
        if isinstance(target, str) and table not in ["produtos", "clientes"]:
            return exceptions.UnsupportedSearchTypeError(
                f"tabela {table} não admite busca por texto"
            )

        if isinstance (target, int):
            found = self.db.get_by_id(db_cursor, table, target)
        else:
            found = self.db.get_by_text(db_cursor, table, target)
        return True if found else False
                
    def _try_client(self,db_cursor: Cursor ,client: str | int):
        found_client = self._check_existence(db_cursor,'clientes', client)
        if not found_client: found_client = exceptions.ClientError()
        elif found_client == True: found_client = None
        return found_client
    
    def _try_items(self, items: list[Item]):
        ...
    