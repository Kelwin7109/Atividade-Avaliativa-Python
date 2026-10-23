"""Registro de entradas e saídas do estoque."""

from datetime import datetime


def registrar_movimentacao(produtos, movimentacoes, codigo, tipo, quantidade):
    """Atualiza o estoque e registra a movimentação somente se ela for válida."""
    codigo = str(codigo).strip()
    produto = produtos.get(codigo)

    if produto is None:
        return False, "Produto não encontrado."
    if tipo not in ("entrada", "saida"):
        return False, "Tipo de movimentação inválido."
    if (
        not isinstance(quantidade, int)
        or isinstance(quantidade, bool)
        or quantidade <= 0
    ):
        return False, "A quantidade deve ser um número inteiro maior que zero."
    if tipo == "saida" and quantidade > produto["quantidade"]:
        return False, "A saída não pode ser maior que o estoque disponível."

    if tipo == "entrada":
        produto["quantidade"] += quantidade
    else:
        produto["quantidade"] -= quantidade

    movimentacoes.append(
        {
            "tipo": tipo,
            "codigo": codigo,
            "nome": produto["nome"],
            "quantidade": quantidade,
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
    )

    if produto["quantidade"] == 0:
        mensagem = "Movimentação registrada. Atenção: o produto ficou sem estoque."
    else:
        mensagem = "Movimentação registrada com sucesso."
    return True, mensagem


def historico_movimentacoes(movimentacoes):
    """Retorna uma cópia do histórico."""
    return list(movimentacoes)
