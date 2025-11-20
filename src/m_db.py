import sqlite3
from typing import Literal


class MemoryMassesDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")

        self.schema = {
            # products and clients
            "produtos": [
                "id_produto INTEGER PRIMARY KEY AUTOINCREMENT",
                "nome TEXT UNIQUE NOT NULL",
                "tipo TEXT NOT NULL",
                "preco_producao REAL NOT NULL",
                "preco_venda REAL NOT NULL",
                "estoque_min INTEGER NOT NULL",
                "estoque_atual INTEGER NOT NULL",
            ],
            "clientes": [
                "id_cliente INTEGER PRIMARY KEY AUTOINCREMENT",
                "nome TEXT NOT NULL",
                "contato TEXT",
            ],
            # transactions related
            "transacoes": [
                "id_transacao INTEGER PRIMARY KEY AUTOINCREMENT",
                "id_cliente INTEGER",
                "data TEXT NOT NULL",
                'tipo TEXT NOT NULL CHECK(tipo IN ("P","V"))',  # Pedido(P), Venda(V)
                'estado TEXT NOT NULL CHECK(estado IN ("aberto","fechado","cancelado"))',
                "valor_total REAL NOT NULL",
                "valor_aberto REAL NOT NULL",
                "criado_em DEFAULT (datetime('now'))",
                "atualizado_em DEFAULT (datetime('now'))",
                "FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente)",
            ],
            "itens_transacao": [
                "id_item INTEGER PRIMARY KEY AUTOINCREMENT",
                "id_transacao INTEGER NOT NULL",
                "id_produto INTEGER NOT NULL",
                "quantidade INTEGER NOT NULL",
                "valor_unitario REAL NOT NULL",
                "criado_em DEFAULT (datetime('now'))",
                "atualizado_em DEFAULT (datetime('now'))",
                "FOREIGN KEY(id_transacao) REFERENCES transacoes(id_transacao)",
                "FOREIGN KEY(id_produto) REFERENCES produtos(id_produto)",
            ],
            "pagamentos": [
                "id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT",
                "id_transacao INTEGER NOT NULL",
                "data TEXT NOT NULL",
                "valor REAL NOT NULL",
                "criado_em DEFAULT (datetime('now'))",
                "atualizado_em DEFAULT (datetime('now'))",
                "FOREIGN KEY(id_transacao) REFERENCES transacoes(id_transacao)",
            ],
            # irrelevante por agora, mas já deixando aqui
            "producoes": [
                "id_producao INTEGER PRIMARY KEY AUTOINCREMENT",
                "id_produto INTEGER NOT NULL",
                "data TEXT NOT NULL",
                "quantidade INTEGER NOT NULL",
                "FOREIGN KEY(id_produto) REFERENCES produtos(id_produto)",
            ],
        }
        self._create_db()

    # INIT ↑

    def _create_db(self):
        with self.conn:
            self.conn.execute("PRAGMA foreign_keys = ON")
            self.conn.row_factory = sqlite3.Row

            for table, columns in self.schema.items():
                self.conn.execute(
                    f"CREATE TABLE IF NOT EXISTS {table} ({','.join(columns)})"
                )

    # --- ↑ CREATE ↑ --- #
    # --- ↓ DB MANIPULATION METHODS ↓ --- #
    # --- ↓ ADD/REGISTER ↓ --- #

    def add_product(
        self,
        db_cursor: sqlite3.Cursor,
        name: str,
        p_type: str,
        production_price: float,
        sell_price: float,
        min_stock: int,
        current_stock: int = 0,
    ):
        db_cursor.execute(
            """
            INSERT INTO produtos (
                nome,
                tipo,
                preco_producao,
                preco_venda,
                estoque_min,
                estoque_atual
            )
            VALUES (
                :name,
                :p_type,
                :production_price,
                :sell_price,
                :min_stock,
                :current_stock
            )
            """,
            {
                "name": name,
                "p_type": p_type,
                "production_price": production_price,
                "sell_price": sell_price,
                "min_stock": min_stock,
                "current_stock": current_stock,
            },
        )
        return db_cursor.lastrowid

    def add_client(self, db_cursor: sqlite3.Cursor, name: str, contact: str = None):
        db_cursor.execute(
            """
            INSERT INTO clientes (nome, contato)
            VALUES (:name, :contact)
            """,
            {"name": name, "contact": contact},
        )
        return db_cursor.lastrowid

    def register_transaction(
        self,
        db_cursor: sqlite3.Cursor,
        client_id: int,
        date: str,
        t_type: Literal["P", "V"],
        status: Literal["aberto", "fechado", "cancelado"],
        total_value: float,
        open_value: float,
    ):
        db_cursor.execute(
            """
            INSERT INTO transacoes
            (
            id_cliente,
            data,
            tipo,
            estado,
            valor_total,
            valor_aberto
            )
            VALUES (
            :client_id,
            :date,
            :t_type,
            :status,
            :total_value,
            :open_value
            )
            """,
            {
                "client_id": client_id,
                "date": date,
                "t_type": t_type,
                "status": status,
                "total_value": total_value,
                "open_value": open_value
            }
        )
        return db_cursor.lastrowid

    def register_transaction_items(
        self,
        db_cursor: sqlite3.Cursor,
        transaction_id: int,
        product_id: int,
        product_amount: int,
        product_unit_value: float,
    ):
        db_cursor.execute(
            """
            INSERT INTO itens_transacao
            (
            id_transacao,
            id_produto,
            quantidade,
            valor_unitario
            )
            VALUES (
            :transaction_id,
            :product_id,
            :product_amount,
            :product_unit_value
            )
            """, 
            {
                "transaction_id": transaction_id,
                "product_id": product_id,
                "product_amount": product_amount,
                "product_unit_value": product_unit_value,
            }
        )
        return db_cursor.lastrowid

    def register_payment(
        self,
        db_cursor: sqlite3.Cursor,
        transaction_id: int,
        date: str,
        value: float,
    ):
        db_cursor.execute(
            """
            INSERT INTO pagamentos
            (
            id_transacao,
            data,
            valor
            )
            VALUES (
            :transaction_id,
            :date,
            :value
            )
            """,
            {
            "transaction_id": transaction_id,
            "date": date,
            "value": value,
            }
        )
        return db_cursor.lastrowid

    def register_production(
        self,
        db_cursor: sqlite3.Cursor,
        product_id: int,
        date: str,
        amount: int,
    ):
        db_cursor.execute(
            """
            INSERT INTO producoes
            (
            id_produto , data, quantidade
            )
            VALUES (
            :product_id, :date, :amount
            )
            """,
            {
                "product_id": product_id,
                "date": date,
                "amount": amount,
            }
        )
        return db_cursor.lastrowid
    
    # --- ↑ ADD/REGISTER ↑ --- #
    # --- ↓ UPDATE ↓ --- #
 
    def update_product(
        self,
        db_cursor: sqlite3.Cursor,
        product_id: int,
        name: str,
        p_type: str,
        production_price: float,
        sell_price: float,
        min_stock: int,
        current_stock: int = 0,
    ):
        db_cursor.execute(
            """
            UPDATE produtos
            SET 
                nome = :name,
                tipo = :p_type,
                preco_producao = :production_price,
                preco_venda = :sell_price,
                estoque_min = :min_stock,
                estoque_atual = :current_stock
            WHERE id_produto = :product_id
            """, 
            {
                "name": name,
                "p_type": p_type,
                "production_price": production_price,
                "sell_price": sell_price,
                "min_stock": min_stock,
                "current_stock": current_stock,
                "product_id": product_id,
            }
        )

    def update_client(self, db_cursor: sqlite3.Cursor,
                      client_id: int,  name: str, contact: str = None):
        db_cursor.execute(
            """
            UPDATE clientes
            SET nome = :name, contato = :contact
            WHERE id_cliente = :client_id
            """,
            {
                "name": name,
                "contact": contact,
                "client_id": client_id,
            }
        )

    def update_transaction(
        self,
        db_cursor: sqlite3.Cursor,
        transaction_id: int,
        client_id: int,
        date: str,
        t_type: Literal["P", "V"],
        status: Literal["aberto", "fechado", "cancelado"],
        total_value: float,
        open_value: float,
    ):
        db_cursor.execute(
            """
            UPDATE transacoes
            SET 
                id_cliente = :client_id,
                data = :date,
                tipo = :t_type,
                estado = :status,
                valor_total = :total_value,
                valor_aberto = :open_value  
            WHERE id_transacao = :transaction_id
            """,
            {
                "transaction_id": transaction_id, 
                "client_id": client_id, 
                "date": date, 
                "t_type": t_type, 
                "status": status, 
                "total_value": total_value, 
                "open_value": open_value, 
            }
        )

    def update_transaction_items(
        self,
        db_cursor: sqlite3.Cursor,
        transaction_item_id: int,
        transaction_id: int,
        product_id: int,
        product_amount: int,
        product_unit_value: float,
    ):
        db_cursor.execute(
            """
            UPDATE itens_transacao
            SET
                id_transacao = :transaction_id,
                id_produto = :product_id,
                quantidade = :product_amount,
                valor_unitario = :product_unit_value
            WHERE id_item = :transaction_item_id
            """,
            {
                "transaction_id": transaction_id,
                "product_id": product_id,
                "product_amount": product_amount,
                "product_unit_value": product_unit_value,
                "transaction_item_id": transaction_item_id,
            }
        )

    def update_payment(
        self,
        db_cursor: sqlite3.Cursor,
        payment_id: int,
        transaction_id: int,
        date: str,
        value: float,
    ):
        db_cursor.execute(
            """
            UPDATE pagamentos
            SET
                id_transacao = :transaction_id,
                data = :date,
                valor = :value
            WHERE id_pagamento = :payment_id
            """,
            {
                "transaction_id": transaction_id,
                "date": date,
                "value": value,
                "payment_id": payment_id,
            }
        )
        
    def update_production(
        self,
        db_cursor: sqlite3.Cursor,
        production_id: int,
        product_id: int,
        date: str,
        amount: int,
    ):
        db_cursor.execute(
            """
            UPDATE producoes
            SET
                id_produto = :product_id,
                data = :date,
                quantidade = :amount
            WHERE id_producao = :production_id
            """,
            {
                "product_id": product_id,
                "date": date,
                "amount": amount,
                "production_id": production_id,
            }
        )

    # --- ↑ UPDATE ↑ --- #
    # --- ↓ GET_METHODS ↓ --- #

    def get_all_products(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM produtos")
            return cursor.fetchall()
        
    def get_all_clients(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            return cursor.fetchall()
        
    def get_all_transactions(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM transacoes")
            return cursor.fetchall()
        
    def get_all_transaction_items(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM itens_transacao")
            return cursor.fetchall()
        
    def get_all_payments(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM pagamentos")
            return cursor.fetchall()