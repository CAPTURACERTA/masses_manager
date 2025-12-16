from typing import TypedDict, TypeAlias, Literal


class Item(TypedDict):
    item_id: int
    item_amount: int
    unit_value: float


TableColumn: TypeAlias = str
DataBaseTables: TypeAlias = Literal[
    "produtos", "clientes", "transacoes",
    "itens_transacao", "pagamentos", "producoes"
]
ProductColumns: TypeAlias = Literal[
    "id_produto", "nome", "tipo", "preco_producao",
    "preco_venda", "estoque_min", "estoque_atual", "ativo",
]
ClientColumns: TypeAlias = Literal[
    "id_cliente", "nome", "contato", "ativo",
]

class ProductInfo(TypedDict):
    id_produto: int
    nome: str
    tipo: str
    preco_producao: float
    preco_venda: float
    estoque_min: int
    estoque_atual: int
    ativo: int

class ClientInfo(TypedDict):
    id_cliente: int
    nome: str
    contato: str
    ativo: int