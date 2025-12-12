from data.table_classes import ProductInfo


def main():
    keys = [
                "nome", "tipo", "preco_producao",
                "preco_venda", "estoque_min", "estoque_atual", "ativo",
                "all"
            ]
    info = ProductInfo()

    for i, key in enumerate(keys):
        info[key] = i
    
    print(info)


if __name__ == "__main__":
    main()
