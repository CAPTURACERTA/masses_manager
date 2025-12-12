from typing import TypedDict


class Item(TypedDict):
    item_id: int
    item_amount: int
    unit_value: float


class ProductInfo(TypedDict):
    id_produto: int
    nome: str
    tipo: str
    preco_producao: float
    preco_venda: float
    estoque_min: int
    estoque_atual: int
    ativo: int