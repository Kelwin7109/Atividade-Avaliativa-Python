"""Ponto de entrada do Sistema de Gestão de Estoque."""

import armazenamento
import movimentacoes
import produtos
import relatorios


def titulo(texto):
    print(f"\n{'=' * 58}\n  {texto}\n{'=' * 58}")


def ler_preco(mensagem):
    try:
        texto = input(mensagem).strip().replace(",", ".")
        valor = float(texto)
        if valor <= 0:
            print("O preço deve ser maior que zero.")
            return None
        return valor
    except ValueError:
        print("Digite um preço válido, como 12,50.")
        return None


def ler_quantidade(mensagem, permitir_zero=True):
    try:
        valor = int(input(mensagem).strip())
        minimo = 0 if permitir_zero else 1
        if valor < minimo:
            print(f"Digite um número inteiro maior ou igual a {minimo}.")
            return None
        return valor
    except ValueError:
        print("Digite uma quantidade inteira válida.")
        return None


def mostrar_produto(produto):
    if produto is None:
        print("Produto não encontrado.")
    else:
        relatorios.exibir_produto(produto)


def cadastrar(produtos_estoque):
    titulo("CADASTRO DE PRODUTO")
    codigo = input("Código: ")
    nome = input("Nome: ")
    categoria = input("Categoria: ")
    preco = ler_preco("Preço unitário: ")
    quantidade = ler_quantidade("Quantidade: ")
    if preco is None or quantidade is None:
        return False
    sucesso, mensagem = produtos.cadastrar_produto(
        produtos_estoque, codigo, nome, categoria, preco, quantidade
    )
    print(mensagem)
    return sucesso


def atualizar(produtos_estoque):
    codigo = input("Código do produto: ")
    produto = produtos.consultar_produto(produtos_estoque, codigo)
    if produto is None:
        print("Produto não encontrado.")
        return False

    print("Deixe um campo vazio para manter o valor atual.")
    nome = input(f'Nome [{produto["nome"]}]: ').strip() or None
    categoria = input(f'Categoria [{produto["categoria"]}]: ').strip() or None
    texto_preco = input(f'Preço [{produto["preco"]:.2f}]: ').strip()
    preco = None
    if texto_preco:
        try:
            preco = float(texto_preco.replace(",", "."))
        except ValueError:
            print("Preço inválido.")
            return False

    sucesso, mensagem = produtos.atualizar_produto(
        produtos_estoque, codigo, nome, categoria, preco
    )
    print(mensagem)
    return sucesso


def registrar_movimentacao(produtos_estoque, historico, tipo):
    codigo = input("Código do produto: ")
    quantidade = ler_quantidade("Quantidade: ", permitir_zero=False)
    if quantidade is None:
        return False
    sucesso, mensagem = movimentacoes.registrar_movimentacao(
        produtos_estoque, historico, codigo, tipo, quantidade
    )
    print(mensagem)
    return sucesso


def exibir_menu():
    print(
        f"\n{'=' * 58}\n"
        "             SISTEMA DE GESTÃO DE ESTOQUE\n"
        f"{'=' * 58}\n"
        "  PRODUTOS\n"
        "  [1] Cadastrar       [2] Consultar       [3] Pesquisar nome\n"
        "  [4] Pesquisar categoria  [5] Atualizar  [6] Remover\n"
        f"{'-' * 58}\n"
        "  ESTOQUE E CONSULTAS\n"
        "  [7] Registrar entrada    [8] Registrar saída\n"
        "  [9] Listar produtos      [10] Relatórios\n"
        "  [11] Histórico           [12] Ordenar produtos\n"
        "  [13] Listar categorias\n"
        f"{'-' * 58}\n"
        "  [0] Encerrar\n"
        f"{'=' * 58}"
    )


def executar():
    produtos_estoque, historico = armazenamento.carregar_dados()
    limite_minimo = 5

    while True:
        exibir_menu()
        opcao = input("\n  Escolha uma opção: ").strip()
        alterou_dados = False

        if opcao == "1":
            alterou_dados = cadastrar(produtos_estoque)
        elif opcao == "2":
            mostrar_produto(produtos.consultar_produto(produtos_estoque, input("Código: ")))
        elif opcao == "3":
            encontrados = produtos.pesquisar_por_nome(
                produtos_estoque, input("Nome ou parte do nome: ")
            )
            relatorios.exibir_lista_produtos(encontrados, "Pesquisa por nome")
        elif opcao == "4":
            encontrados = produtos.pesquisar_por_categoria(
                produtos_estoque, input("Categoria ou parte da categoria: ")
            )
            relatorios.exibir_lista_produtos(encontrados, "Pesquisa por categoria")
        elif opcao == "5":
            alterou_dados = atualizar(produtos_estoque)
        elif opcao == "6":
            codigo = input("Código do produto: ")
            confirmacao = input("Confirma a exclusão? (s/n): ")
            alterou_dados, mensagem = produtos.remover_produto(
                produtos_estoque, codigo, confirmacao
            )
            print(mensagem)
        elif opcao == "7":
            alterou_dados = registrar_movimentacao(
                produtos_estoque, historico, "entrada"
            )
        elif opcao == "8":
            alterou_dados = registrar_movimentacao(
                produtos_estoque, historico, "saida"
            )
        elif opcao == "9":
            relatorios.exibir_lista_produtos(
                produtos.listar_produtos(produtos_estoque), "Todos os produtos"
            )
        elif opcao == "10":
            limite_minimo = relatorios.exibir_relatorios(
                produtos_estoque, historico, limite_minimo
            )
        elif opcao == "11":
            relatorios.exibir_historico(
                movimentacoes.historico_movimentacoes(historico)
            )
        elif opcao == "12":
            print("1. Nome  2. Preço  3. Quantidade")
            escolha = input("Critério: ").strip()
            criterios = {"1": "nome", "2": "preco", "3": "quantidade"}
            criterio = criterios.get(escolha)
            if criterio is None:
                print("Critério inválido.")
            else:
                reverso = input("Ordem inversa? (s/n): ").strip().casefold() in (
                    "s",
                    "sim",
                )
                relatorios.exibir_lista_produtos(
                    produtos.ordenar_produtos(produtos_estoque, criterio, reverso),
                    f"Produtos ordenados por {criterio}",
                )
        elif opcao == "13":
            categorias = produtos.listar_categorias(produtos_estoque)
            print("\n--- Categorias ---")
            if categorias:
                for categoria in categorias:
                    print(categoria)
            else:
                print("Nenhuma categoria cadastrada.")
        elif opcao in ("0", "14"):
            armazenamento.salvar_dados(produtos_estoque, historico)
            print("Dados salvos. Sistema encerrado.")
            break
        else:
            print("Opção inválida.")

        if alterou_dados:
            armazenamento.salvar_dados(produtos_estoque, historico)


if __name__ == "__main__":
    executar()
