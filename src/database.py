import sqlite3


class MassesDatabase:
    def __init__(self, path: str):
        self.path = path

        self.schema = {
            'produtos':[
                'id_produto INTEGER PRIMARY KEY AUTOINCREMENT',
                'nome TEXT UNIQUE NOT NULL',
                'tipo TEXT NOT NULL',
                'preco_producao REAL NOT NULL',
                'preco_venda REAL NOT NULL',
                'estoque_min INTEGER NOT NULL',
                'estoque_atual INTEGER'
            ],
            'clientes':[
                'id_cliente INTEGER PRIMARY KEY AUTOINCREMENT',
                'nome TEXT NOT NULL',
                'contato TEXT'
            ],
            'producoes':[
                'id_producao INTEGER PRIMARY KEY AUTOINCREMENT',
                'id_produto INTEGER NOT NULL',
                'dt_producao TEXT NOT NULL',
                'quantidade INTEGER NOT NULL',
                'FOREIGN KEY(id_produto) REFERENCES produtos(id_produto)'
            ],
            'vendas':[
                'id_venda INTEGER PRIMARY KEY AUTOINCREMENT',
                'id_cliente INTEGER NOT NULL',
                'dt_venda TEXT NOT NULL',
                'valor_total REAL NOT NULL',
                'valor_aberto REAL',
                'FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente)'
            ],
            'itens_vendas':[
                'id_item_venda INTEGER PRIMARY KEY AUTOINCREMENT',
                'id_venda INTEGER NOT NULL',
                'id_produto INTEGER NOT NULL',
                'qnt_produto INTEGER NOT NULL',
                'FOREIGN KEY(id_venda) REFERENCES vendas(id_venda)',
                'FOREIGN KEY(id_produto) REFERENCES produtos(id_produto)'
            ],
            'pagamentos':[
                'id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT',
                'id_venda INTEGER NOT NULL',
                'dt_pagamento TEXT NOT NULL',
                'valor_recebido REAL NOT NULL',
                'FOREIGN KEY(id_venda) REFERENCES vendas(id_venda)'
            ]
        }
        self._create_db()

    def _get_connection(self):
        """Retorna uma conexão com o banco, sempre ativando as FK."""
        conn = sqlite3.connect(self.path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def _create_db(self):
        with self._get_connection() as conn:
            for table, columns in self.schema.items():
                conn.execute(f"CREATE TABLE IF NOT EXISTS {table} ({','.join(columns)})")