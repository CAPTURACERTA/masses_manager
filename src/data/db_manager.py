from data.database import MassesDatabase
from sqlite3 import Cursor
from typing import Literal, TypedDict
import datetime



class Item(TypedDict):
    item_id: int
    item_amount: int
    unit_value: float


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
        client_id: int,
        t_type: Literal["P", "V"],
        items: list[Item],
        date: str | datetime.date = None,
        payment: float = 0,
    ):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            total_value = self._get_total_value(items)
            open_value = total_value - payment
            status = "aberto" if open_value > 0 else "fechado"
            date = (date or datetime.date.today())

            transaction = self.db.register_transaction(
                cursor, client_id, date, t_type, status, total_value, open_value
            )
            self._register_transaction_items(cursor, transaction, items)
            
            if t_type == "V":
                self._subtract_product_current_stock(cursor, items)
            if payment and t_type == "V":
                self.db.register_payment(cursor, transaction, date, payment)

    def _register_transaction_items(
            self,
            db_cursor: Cursor,
            transaction_id: int,
            items: list[Item],
    ):
        for item in items:
            self.db.register_transaction_items(
                db_cursor, transaction_id, item["item_id"], item["item_amount"], item["unit_value"]
            )

    def register_payment(
            self,
            transaction_id: int,
            value: float,
            date: str | datetime.date = None
    ):
        if not date: date = datetime.date.today()
        with self.db.get_connection() as conn:
            self.db.register_payment(conn.cursor(), transaction_id, date, value)

    def register_production(
            self,
            product_id: int,
            amount: int,
            date: str | datetime.date = None
    ):
        if not date: date = datetime.date.today()
        with self.db.get_connection() as conn:
            self.db.register_production(conn.cursor(),product_id, date, amount)

    # ↑ ADDERS/REGISTERS ↑ #
    # ↓ UPDATERS ↓ #

    def _subtract_product_current_stock(self, db_cursor: Cursor, items: list[Item]):
        for item in items:
            current_stock = self.db.get_product_info(db_cursor, item["item_id"], "estoque_atual")
            new_current_stock = current_stock - item["item_amount"]

            self.update_product(item["item_id"], db_cursor, current_stock=new_current_stock)

    def update_product(
        self,
        product_id: int,
        db_cursor: Cursor = None,
        name: str = None,
        p_type: str = None,
        production_price: float = None,
        sell_price: float = None,
        min_stock: int = None,
        current_stock: int = None,
    ):
        conn = None
        if not db_cursor:
            conn = self.db.get_connection()
            db_cursor = conn.cursor()

        try:
            product = self.db.get_by_id(db_cursor, "produtos", product_id)
            self.db.update_product(
                db_cursor,
                product_id,
                (name or product["nome"]),
                (p_type or product["tipo"]),
                production_price if production_price is not None else product["preco_producao"],
                sell_price if sell_price is not None else product["preco_venda"],
                min_stock if min_stock is not None else product["estoque_min"],
                current_stock if current_stock is not None else product["estoque_atual"],
            )
        except Exception as e:
            if conn: conn.rollback()
            raise e
        else:
            if conn: conn.commit()
        finally:
            if conn: conn.close()
        
    # ↑ UPDATERS ↑ #
    # ↓ GETTERS  ↓ #

    def get_by_id(
        self,
        row_id: int,
        table: Literal["produtos", "clientes", "transacoes",
                       "itens_transacao", "pagamentos", "producoes"],
    ):
        with self.db.get_connection() as conn:
            return self.db.get_by_id(conn.cursor(), table, row_id)

    def get_by_text(
        self,
        table: Literal["produtos", "clientes"], 
        term: str,
    ):
        with self.db.get_connection() as conn:
            return self.db.get_by_text(conn.cursor(), table, term)
        
    def get_by_name(
        self,
        table: Literal["produtos", "clientes"], 
        name: str,
    ):
        with self.db.get_connection() as conn:
            return self.db.get_by_name(conn.cursor(), table, name)

    def get_by_table(
        self,
        table: Literal[
            "produtos","clientes","transacoes",
            "itens_transacao","pagamentos","producoes",
        ]
    ):
        with self.db.get_connection() as conn:
            return self.db.get_by_table(conn.cursor(), table)

    # ↓ HELPERS ↓ #

    def _get_total_value(self, items: list[Item]):
        total_value = 0
        
        for item in items:
            total_value += item["item_amount"] * item["unit_value"]

        return total_value
    