"""Cadastro, consulta, alteração e ordenação de produtos."""


def cadastrar_produto(produtos, codigo, nome, categoria, preco, quantidade):
    """Adiciona um produto depois de validar todos os seus dados."""
    codigo = str(codigo).strip()
    nome = str(nome).strip()
    categoria = str(categoria).strip()

    if not codigo:
        return False, "O código não pode ficar vazio."
    if codigo in produtos:
        return False, "Já existe um produto com esse código."
    if not nome:
        return False, "O nome não pode ficar vazio."
    if not categoria:
        return False, "A categoria não pode ficar vazia."
    if not isinstance(preco, (int, float)) or isinstance(preco, bool) or preco <= 0:
        return False, "O preço deve ser um número maior que zero."
    if (
        not isinstance(quantidade, int)
        or isinstance(quantidade, bool)
        or quantidade < 0
    ):
        return False, "A quantidade deve ser um número inteiro não negativo."

    produtos[codigo] = {
        "codigo": codigo,
        "nome": nome,
        "categoria": categoria,
        "preco": float(preco),
        "quantidade": quantidade,
    }
    return True, "Produto cadastrado com sucesso."


def consultar_produto(produtos, codigo):
    """Retorna um produto pelo código ou None quando não for encontrado."""
    return produtos.get(str(codigo).strip())


def pesquisar_por_nome(produtos, texto):
    texto = str(texto).strip().casefold()
    return [produto for produto in produtos.values() if texto in produto["nome"].casefold()]


def pesquisar_por_categoria(produtos, categoria):
    categoria = str(categoria).strip().casefold()
    return [
        produto
        for produto in produtos.values()
        if categoria in produto["categoria"].casefold()
    ]


def listar_produtos(produtos):
    """Retorna os produtos em uma lista, sem modificar o dicionário original."""
    return list(produtos.values())


def atualizar_produto(produtos, codigo, nome=None, categoria=None, preco=None):
    produto = consultar_produto(produtos, codigo)
    if produto is None:
        return False, "Produto não encontrado."

    nome_novo = produto["nome"]
    categoria_nova = produto["categoria"]
    preco_novo = produto["preco"]

    if nome is not None:
        nome = str(nome).strip()
        if not nome:
            return False, "O nome não pode ficar vazio."
        nome_novo = nome

    if categoria is not None:
        categoria = str(categoria).strip()
        if not categoria:
            return False, "A categoria não pode ficar vazia."
        categoria_nova = categoria

    if preco is not None:
        if (
            not isinstance(preco, (int, float))
            or isinstance(preco, bool)
            or preco <= 0
        ):
            return False, "O preço deve ser um número maior que zero."
        preco_novo = float(preco)

    produto["nome"] = nome_novo
    produto["categoria"] = categoria_nova
    produto["preco"] = preco_novo

    return True, "Produto atualizado com sucesso."


def remover_produto(produtos, codigo, confirmacao):
    codigo = str(codigo).strip()
    if codigo not in produtos:
        return False, "Produto não encontrado."
    if str(confirmacao).strip().casefold() not in ("s", "sim"):
        return False, "Remoção cancelada."
    del produtos[codigo]
    return True, "Produto removido com sucesso."


def ordenar_produtos(produtos, criterio, reverso=False):
    """Ordena uma cópia da lista para não alterar o armazenamento original."""
    chaves = {
        "nome": lambda produto: produto["nome"].casefold(),
        "preco": lambda produto: produto["preco"],
        "quantidade": lambda produto: produto["quantidade"],
    }
    if criterio not in chaves:
        return []
    return sorted(produtos.values(), key=chaves[criterio], reverse=reverso)


def listar_categorias(produtos):
    """Retorna categorias únicas em ordem alfabética."""
    return sorted({produto["categoria"] for produto in produtos.values()}, key=str.casefold)
