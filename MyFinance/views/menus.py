from database.conexao import conectar
from controllers.conta_controller import (
    listar_contas, cadastrar_conta, buscar_conta, desativar_conta,
    totais_gerais, calcular_saldo
)
from controllers.categoria_controller import (
    listar_categorias, cadastrar_categoria, criar_categorias_padrao
)
from controllers.transacao_controller import (
    registrar_transacao, listar_transacoes, totais_conta, totais_por_categoria
)
from controllers.transferencia_controller import transferir
from controllers.recorrencia_controller import (
    cadastrar_recorrencia, listar_recorrencias, lancar_recorrencia
)
from controllers.meta_controller import cadastrar_meta, listar_metas, adicionar_aporte
from utils import titulo, linha, pausar, ler_texto, ler_valor, ler_numero, ler_data, formatar_dinheiro

def nome_usuario(id_usuario):
    conexao = conectar()
    usuario = conexao.execute(
        "SELECT nome FROM usuarios WHERE id_usuario = ?", (id_usuario,)
    ).fetchone()
    conexao.close()
    return usuario["nome"]

def mostrar_contas(id_usuario):
    contas = listar_contas(id_usuario)
    if not contas:
        print("Nenhuma conta bancaria cadastrada.")
        return []
    for i, conta in enumerate(contas, 1):
        print("\n[{}] {}".format(i, conta.banco.upper()))
        print("    Tipo: {}".format(conta.tipo))
        print("    Saldo: {}".format(formatar_dinheiro(conta.saldo)))
    return contas

def cadastrar_banco(id_usuario):
    titulo("CADASTRAR NOVA CONTA")
    banco = ler_texto("Nome do banco/instituicao: ")
    print("\nTipo de conta:")
    print("[1] Conta corrente")
    print("[2] Conta poupanca")
    print("[3] Carteira (dinheiro em especie)")
    opcao = input("Escolha: ")
    tipos = {"1": "Conta corrente", "2": "Conta poupanca", "3": "Carteira"}
    while opcao not in tipos:
        opcao = input("Opcao invalida. Escolha: ")
    saldo = input("Saldo inicial (ex.: 1500,00): ").strip().replace(",", ".")
    try:
        saldo = float(saldo)
        if saldo < 0:
            print("O saldo inicial nao pode ser negativo.")
            return
    except ValueError:
        print("Valor invalido.")
        return
    cadastrar_conta(id_usuario, banco, tipos[opcao], round(saldo, 2))
    print("\nConta cadastrada com sucesso!")

def escolher_conta(id_usuario):
    contas = mostrar_contas(id_usuario)
    if not contas:
        return None
    escolha = ler_numero("\nSelecione o numero da conta: ")
    if escolha > len(contas):
        print("Conta nao encontrada.")
        return None
    return contas[escolha - 1]

def selecionar_categoria(id_usuario, tipo):
    categorias = listar_categorias(id_usuario, tipo)
    if not categorias:
        print("Nenhuma categoria cadastrada para esse tipo.")
        return None
    print("\nCategorias:")
    for i, categoria in enumerate(categorias, 1):
        print("[{}] {}".format(i, categoria["nome"]))
    print("[0] Cadastrar nova categoria")
    escolha = input("Escolha: ")
    if escolha == "0":
        nome = ler_texto("Nome da nova categoria: ")
        if cadastrar_categoria(id_usuario, nome, tipo):
            categorias = listar_categorias(id_usuario, tipo)
            for item in categorias:
                if item["nome"].lower() == nome.lower():
                    return item["id_categoria"]
        print("Nao foi possivel cadastrar. Talvez ja exista.")
        return None
    try:
        indice = int(escolha) - 1
        if indice < 0 or indice >= len(categorias):
            print("Opcao invalida.")
            return None
        return categorias[indice]["id_categoria"]
    except ValueError:
        print("Opcao invalida.")
        return None

def menu_transacao(id_conta, id_usuario, tipo):
    titulo("REGISTRAR " + tipo.upper())
    categoria = selecionar_categoria(id_usuario, tipo)
    if categoria is None:
        return
    descricao = ler_texto("Descricao: ")
    valor = ler_valor("Valor: R$ ")
    data = ler_data()
    sucesso, mensagem = registrar_transacao(
        id_conta, categoria, tipo, descricao, valor, data
    )
    print("\n" + mensagem)

def menu_categorias(id_usuario):
    while True:
        titulo("CATEGORIAS")
        categorias = listar_categorias(id_usuario)
        for categoria in categorias:
            print("[{}] {} ({})".format(
                categoria["id_categoria"], categoria["nome"], categoria["tipo"]
            ))
        print("\n[1] Nova categoria de receita")
        print("[2] Nova categoria de despesa")
        print("[0] Voltar")
        op = input("Escolha: ")
        if op == "1" or op == "2":
            tipo = "receita" if op == "1" else "despesa"
            nome = ler_texto("Nome: ")
            if cadastrar_categoria(id_usuario, nome, tipo):
                print("Categoria cadastrada.")
            else:
                print("Essa categoria ja existe.")
            pausar()
        elif op == "0":
            break
        else:
            print("Opcao invalida.")
            pausar()

def menu_historico(id_conta):
    titulo("HISTORICO DE MOVIMENTACOES")
    transacoes = listar_transacoes(id_conta)
    if not transacoes:
        print("Ainda nao existem movimentacoes.")
    else:
        for item in transacoes:
            sinal = "+" if item["tipo"] == "receita" else "-"
            print("{} | {} | {}{} | {}".format(
                item["data"], item["categoria"], sinal,
                formatar_dinheiro(item["valor"]), item["descricao"]
            ))
    pausar()

def menu_relatorio_conta(id_conta):
    titulo("RELATORIO DA CONTA")
    receitas, despesas = totais_conta(id_conta)
    saldo = calcular_saldo(id_conta)
    print("Total de receitas: {}".format(formatar_dinheiro(receitas)))
    print("Total de despesas: {}".format(formatar_dinheiro(despesas)))
    print("Saldo atual:       {}".format(formatar_dinheiro(saldo)))
    print("\nDespesas por categoria:")
    dados = totais_por_categoria(id_conta, "despesa")
    if not dados:
        print("Nenhuma despesa registrada.")
    for item in dados:
        print("- {}: {}".format(item["nome"], formatar_dinheiro(item["total"])))
    pausar()

def menu_recorrencias(id_conta, id_usuario):
    while True:
        titulo("RECEITAS FIXAS E GASTOS MENSAIS")
        itens = listar_recorrencias(id_conta)
        if not itens:
            print("Nenhuma recorrencia cadastrada.")
        else:
            for item in itens:
                print("[{}] {} | {} | {} | Dia {}".format(
                    item["id_recorrencia"], item["tipo"].upper(),
                    item["descricao"], formatar_dinheiro(item["valor"]),
                    item["dia_vencimento"]
                ))
        print("\n[1] Cadastrar receita fixa")
        print("[2] Cadastrar gasto mensal")
        print("[3] Registrar recorrencia deste mes")
        print("[0] Voltar")
        op = input("Escolha: ")
        if op in ("1", "2"):
            tipo = "receita" if op == "1" else "despesa"
            categoria = selecionar_categoria(id_usuario, tipo)
            if categoria is not None:
                descricao = ler_texto("Descricao: ")
                valor = ler_valor("Valor: R$ ")
                dia = ler_numero("Dia previsto (1 a 31): ")
                if dia > 31:
                    print("Dia invalido.")
                else:
                    cadastrar_recorrencia(id_conta, categoria, tipo, descricao, valor, dia)
                    print("Recorrencia cadastrada.")
            pausar()
        elif op == "3":
            if not itens:
                print("Cadastre uma recorrencia primeiro.")
            else:
                id_rec = ler_numero("Numero da recorrencia: ")
                mes = ler_numero("Mes (1 a 12): ")
                ano = ler_numero("Ano: ", 2000)
                if mes > 12:
                    print("Mes invalido.")
                else:
                    sucesso, mensagem = lancar_recorrencia(id_rec, mes, ano)
                    print(mensagem)
            pausar()
        elif op == "0":
            break
        else:
            print("Opcao invalida.")
            pausar()

def menu_metas(id_usuario):
    while True:
        titulo("METAS FINANCEIRAS")
        metas = listar_metas(id_usuario)
        if not metas:
            print("Nenhuma meta cadastrada.")
        for meta, total in metas:
            percentual = (total / meta["valor_objetivo"]) * 100
            if percentual > 100:
                percentual = 100
            print("\n[{}] {}".format(meta["id_meta"], meta["nome"]))
            print("Guardado: {} de {}".format(
                formatar_dinheiro(total), formatar_dinheiro(meta["valor_objetivo"])
            ))
            print("Progresso: {:.1f}%".format(percentual))
        print("\n[1] Criar meta")
        print("[2] Adicionar aporte")
        print("[0] Voltar")
        op = input("Escolha: ")
        if op == "1":
            nome = ler_texto("Nome da meta: ")
            valor = ler_valor("Valor desejado: R$ ")
            cadastrar_meta(id_usuario, nome, valor)
            print("Meta criada.")
            pausar()
        elif op == "2":
            id_meta = ler_numero("ID da meta: ")
            valor = ler_valor("Valor do aporte: R$ ")
            descricao = input("Descricao (opcional): ").strip()
            ids = [meta["id_meta"] for meta, total in metas]
            if id_meta in ids:
                adicionar_aporte(id_meta, valor, descricao)
                print("Aporte registrado.")
            else:
                print("Meta nao encontrada.")
            pausar()
        elif op == "0":
            break
        else:
            print("Opcao invalida.")
            pausar()

def menu_conta(conta, id_usuario):
    while True:
        saldo = calcular_saldo(conta.id_conta)
        titulo("MYFINANCE - " + conta.banco.upper())
        print("Tipo: {}".format(conta.tipo))
        print("Saldo atual: {}".format(formatar_dinheiro(saldo)))
        print("-" * 62)
        print("[1] Registrar receita")
        print("[2] Registrar despesa")
        print("[3] Receitas fixas e gastos mensais")
        print("[4] Historico de movimentacoes")
        print("[5] Categorias")
        print("[6] Relatorios desta conta")
        print("[7] Metas financeiras")
        print("[0] Voltar para a tela principal")
        op = input("\nEscolha uma opcao: ")
        if op == "1":
            menu_transacao(conta.id_conta, id_usuario, "receita")
            pausar()
        elif op == "2":
            menu_transacao(conta.id_conta, id_usuario, "despesa")
            pausar()
        elif op == "3":
            menu_recorrencias(conta.id_conta, id_usuario)
        elif op == "4":
            menu_historico(conta.id_conta)
        elif op == "5":
            menu_categorias(id_usuario)
        elif op == "6":
            menu_relatorio_conta(conta.id_conta)
        elif op == "7":
            menu_metas(id_usuario)
        elif op == "0":
            break
        else:
            print("Opcao invalida.")
            pausar()

def menu_transferencia(id_usuario):
    titulo("TRANSFERENCIA ENTRE CONTAS")
    contas = mostrar_contas(id_usuario)
    if len(contas) < 2:
        print("\nCadastre pelo menos duas contas para transferir.")
        pausar()
        return
    origem = ler_numero("\nNumero da conta de origem: ")
    destino = ler_numero("Numero da conta de destino: ")
    if origem > len(contas) or destino > len(contas) or origem == destino:
        print("Selecao invalida.")
        pausar()
        return
    valor = ler_valor("Valor da transferencia: R$ ")
    descricao = input("Descricao (opcional): ").strip()
    data = ler_data()
    sucesso, mensagem = transferir(
        contas[origem - 1].id_conta, contas[destino - 1].id_conta,
        valor, descricao, data
    )
    print("\n" + mensagem)
    pausar()

def menu_gerenciar_contas(id_usuario):
    while True:
        titulo("GERENCIAR CONTAS")
        contas = listar_contas(id_usuario)
        if not contas:
            print("Nenhuma conta ativa.")
        for i, conta in enumerate(contas, 1):
            print("[{}] {} - {}".format(i, conta.banco, conta.tipo))
        print("\n[1] Cadastrar nova conta")
        print("[2] Desativar conta")
        print("[0] Voltar")
        op = input("Escolha: ")
        if op == "1":
            cadastrar_banco(id_usuario)
            pausar()
        elif op == "2":
            if contas:
                indice = ler_numero("Numero da conta para desativar: ")
                if indice <= len(contas):
                    if desativar_conta(contas[indice - 1].id_conta, id_usuario):
                        print("Conta desativada. O historico foi preservado.")
                else:
                    print("Conta nao encontrada.")
            pausar()
        elif op == "0":
            break
        else:
            print("Opcao invalida.")
            pausar()

def relatorio_geral(id_usuario):
    titulo("RELATORIO FINANCEIRO GERAL")
    contas = listar_contas(id_usuario)
    total_receitas = 0
    total_despesas = 0
    for conta in contas:
        receitas, despesas = totais_conta(conta.id_conta)
        total_receitas += receitas
        total_despesas += despesas
    patrimonio = totais_gerais(id_usuario)
    print("Patrimonio atual:   {}".format(formatar_dinheiro(patrimonio)))
    print("Receitas registradas: {}".format(formatar_dinheiro(total_receitas)))
    print("Despesas registradas: {}".format(formatar_dinheiro(total_despesas)))
    print("\nObservacao: transferencias nao contam como receita ou despesa.")
    pausar()

def perfil(id_usuario):
    titulo("MEU PERFIL")
    print("Nome: {}".format(nome_usuario(id_usuario)))
    print("O MyFinance utiliza um perfil local neste computador.")
    pausar()

def menu_principal(usuario):
    id_usuario = usuario["id_usuario"]
    criar_categorias_padrao(id_usuario)

    while True:
        contas = listar_contas(id_usuario)
        titulo("MYFINANCE - VISAO GERAL")
        print("USUARIO: {}".format(usuario["nome"].upper()))
        print("\nPATRIMONIO TOTAL: {}".format(formatar_dinheiro(totais_gerais(id_usuario))))
        print("\nMINHAS CONTAS")
        linha()
        if not contas:
            print("Nenhuma conta cadastrada. Comece adicionando seu banco.")
        else:
            for i, conta in enumerate(contas, 1):
                receitas, despesas = totais_conta(conta.id_conta)
                print("\n[{}] {}".format(i, conta.banco.upper()))
                print("    {}".format(conta.tipo))
                print("    Saldo: {}".format(formatar_dinheiro(conta.saldo)))
                print("    Ganhos: {} | Despesas: {}".format(
                    formatar_dinheiro(receitas), formatar_dinheiro(despesas)
                ))
        linha()
        print("\n[1 a {}] Entrar em uma conta".format(len(contas)) if contas else "")
        print("[A] Adicionar banco")
        print("[T] Transferir entre contas")
        print("[G] Gerenciar minhas contas")
        print("[R] Relatorio financeiro geral")
        print("[C] Categorias")
        print("[M] Metas financeiras")
        print("[P] Meu perfil")
        print("[0] Sair")
        op = input("\nEscolha uma opcao: ").strip().upper()

        if op.isdigit() and op != "0":
            indice = int(op)
            if 1 <= indice <= len(contas):
                menu_conta(contas[indice - 1], id_usuario)
            else:
                print("Conta nao encontrada.")
                pausar()
        elif op == "A":
            cadastrar_banco(id_usuario)
            pausar()
        elif op == "T":
            menu_transferencia(id_usuario)
        elif op == "G":
            menu_gerenciar_contas(id_usuario)
        elif op == "R":
            relatorio_geral(id_usuario)
        elif op == "C":
            menu_categorias(id_usuario)
        elif op == "M":
            menu_metas(id_usuario)
        elif op == "P":
            perfil(id_usuario)
        elif op == "0":
            print("\nObrigado por utilizar o MyFinance!")
            break
        else:
            print("Opcao invalida.")
            pausar()
