"""Cálculos e exibição dos relatórios do estoque."""


def valor_total_estoque(produtos):
    return sum(
        produto["preco"] * produto["quantidade"] for produto in produtos.values()
    )


def quantidade_total(produtos):
    return sum(produto["quantidade"] for produto in produtos.values())


def produtos_abaixo_do_limite(produtos, limite=5):
    return [
        produto for produto in produtos.values() if produto["quantidade"] < limite
    ]


def produtos_sem_estoque(produtos):
    return [produto for produto in produtos.values() if produto["quantidade"] == 0]


def agrupar_por_categoria(produtos):
    grupos = {}
    for produto in produtos.values():
        grupos.setdefault(produto["categoria"], []).append(produto)
    return grupos


def dinheiro(valor):
    """Formata valores no padrão monetário brasileiro."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def titulo(texto):
    print(f"\n{'-' * 72}\n  {texto.upper()}\n{'-' * 72}")


def exibir_produto(produto):
    valor = produto["preco"] * produto["quantidade"]
    codigo = str(produto["codigo"])
    nome = str(produto["nome"])
    categoria = str(produto["categoria"])
    print(
        f'  {codigo[:8]:<8}  {nome[:22]:<22}  {categoria[:14]:<14}  '
        f'{produto["quantidade"]:>5}  {dinheiro(produto["preco"]):>12}  '
        f'{dinheiro(valor):>12}'
    )


def exibir_lista_produtos(produtos, mensagem="Produtos"):
    titulo(mensagem)
    if not produtos:
        print("  Nenhum produto encontrado.")
        return
    print(f'  {"CÓDIGO":<8}  {"NOME":<22}  {"CATEGORIA":<14}  {"QTD.":>5}  {"PREÇO UNIT.":>12}  {"TOTAL":>12}')
    print(f'  {"-" * 91}')
    for produto in produtos:
        exibir_produto(produto)


def exibir_historico(movimentacoes):
    titulo("Histórico de movimentações")
    if not movimentacoes:
        print("  Nenhuma movimentação registrada.")
        return
    for movimento in movimentacoes:
        seta = "+" if movimento["tipo"] == "entrada" else "-"
        print(f'  {movimento["data_hora"]}  {movimento["tipo"].upper():<8} '
              f'{movimento["codigo"]:<8} {movimento["nome"]:<24} '
              f'{seta}{movimento["quantidade"]} un.')


def exibir_relatorios(produtos, movimentacoes, limite=5):
    while True:
        print(
            f"\n{'-' * 42}\n"
            "              RELATÓRIOS\n"
            f"{'-' * 42}\n"
            "  [1] Valor total do estoque\n"
            "  [2] Quantidade total de unidades\n"
            "  [3] Produtos abaixo do limite mínimo\n"
            "  [4] Produtos sem estoque\n"
            "  [5] Relatório geral\n"
            "  [6] Produtos por categoria\n"
            "  [7] Histórico de movimentações\n"
            "  [8] Alterar limite mínimo\n"
            "  [0] Voltar"
        )
        opcao = input("\n  Escolha uma opção: ").strip()

        if opcao == "1":
            print(f"Valor total do estoque: {dinheiro(valor_total_estoque(produtos))}")
        elif opcao == "2":
            print(f"Quantidade total: {quantidade_total(produtos)} unidade(s).")
        elif opcao == "3":
            exibir_lista_produtos(
                produtos_abaixo_do_limite(produtos, limite),
                f"Produtos abaixo de {limite} unidade(s)",
            )
        elif opcao == "4":
            exibir_lista_produtos(produtos_sem_estoque(produtos), "Produtos sem estoque")
        elif opcao == "5":
            exibir_lista_produtos(list(produtos.values()), "Relatório geral")
        elif opcao == "6":
            print("\n--- Produtos por categoria ---")
            grupos = agrupar_por_categoria(produtos)
            if not grupos:
                print("Nenhum produto cadastrado.")
            for categoria in sorted(grupos, key=str.casefold):
                print(f"\nCategoria: {categoria}")
                for produto in grupos[categoria]:
                    exibir_produto(produto)
        elif opcao == "7":
            exibir_historico(movimentacoes)
        elif opcao == "8":
            novo_limite = input_inteiro("Novo limite mínimo (0 ou maior): ", minimo=0)
            if novo_limite is not None:
                limite = novo_limite
                print(f"Limite atualizado para {limite} unidade(s).")
        elif opcao == "0":
            return limite
        else:
            print("Opção inválida.")


def input_inteiro(mensagem, minimo=None):
    try:
        valor = int(input(mensagem).strip())
        if minimo is not None and valor < minimo:
            print(f"Digite um número inteiro maior ou igual a {minimo}.")
            return None
        return valor
    except ValueError:
        print("Digite um número inteiro válido.")
        return None
