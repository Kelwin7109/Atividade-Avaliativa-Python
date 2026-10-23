"""Funções responsáveis por salvar e carregar os dados do sistema."""

import json
import os
import tempfile


NOME_ARQUIVO = "dados_estoque.json"


def carregar_dados(nome_arquivo=NOME_ARQUIVO):
    """Carrega produtos e movimentações. Retorna listas vazias se o arquivo não existir."""
    if not os.path.exists(nome_arquivo):
        return {}, []

    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        produtos = dados.get("produtos", {})
        movimentacoes = dados.get("movimentacoes", [])

        if not isinstance(produtos, dict) or not isinstance(movimentacoes, list):
            raise ValueError("formato interno inválido")

        return produtos, movimentacoes
    except (OSError, json.JSONDecodeError, ValueError) as erro:
        print(f"Erro ao carregar os dados: {erro}. Os dados atuais foram iniciados vazios.")
        return {}, []


def salvar_dados(produtos, movimentacoes, nome_arquivo=NOME_ARQUIVO):
    """Salva os dados com um arquivo temporário para reduzir o risco de perda."""
    dados = {"produtos": produtos, "movimentacoes": movimentacoes}
    pasta = os.path.dirname(os.path.abspath(nome_arquivo))
    arquivo_temporario = None

    try:
        os.makedirs(pasta, exist_ok=True)
        fd, arquivo_temporario = tempfile.mkstemp(
            prefix="dados_estoque_", suffix=".tmp", dir=pasta
        )
        with os.fdopen(fd, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        os.replace(arquivo_temporario, nome_arquivo)
        return True
    except (OSError, TypeError, ValueError) as erro:
        print(f"Erro ao salvar os dados: {erro}")
        if arquivo_temporario and os.path.exists(arquivo_temporario):
            os.remove(arquivo_temporario)
        return False
