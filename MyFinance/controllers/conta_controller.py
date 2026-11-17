from database.conexao import conectar
from models.conta import Conta

def listar_contas(id_usuario, incluir_inativas=False):
    conexao = conectar()
    if incluir_inativas:
        contas = conexao.execute(
            "SELECT * FROM contas WHERE id_usuario = ? ORDER BY banco",
            (id_usuario,)
        ).fetchall()
    else:
        contas = conexao.execute(
            "SELECT * FROM contas WHERE id_usuario = ? AND ativa = 1 ORDER BY banco",
            (id_usuario,)
        ).fetchall()

    resultado = []
    for conta in contas:
        saldo = calcular_saldo(conta["id_conta"])
        resultado.append(Conta(conta["id_conta"], conta["banco"], conta["tipo"], saldo))
    conexao.close()
    return resultado

def calcular_saldo(id_conta):
    conexao = conectar()
    conta = conexao.execute(
        "SELECT saldo_inicial FROM contas WHERE id_conta = ?", (id_conta,)
    ).fetchone()
    if conta is None:
        conexao.close()
        return 0

    receitas = conexao.execute(
        "SELECT COALESCE(SUM(valor), 0) AS total FROM transacoes WHERE id_conta = ? AND tipo = 'receita'",
        (id_conta,)
    ).fetchone()["total"]
    despesas = conexao.execute(
        "SELECT COALESCE(SUM(valor), 0) AS total FROM transacoes WHERE id_conta = ? AND tipo = 'despesa'",
        (id_conta,)
    ).fetchone()["total"]
    saidas = conexao.execute(
        "SELECT COALESCE(SUM(valor), 0) AS total FROM transferencias WHERE conta_origem = ?",
        (id_conta,)
    ).fetchone()["total"]
    entradas = conexao.execute(
        "SELECT COALESCE(SUM(valor), 0) AS total FROM transferencias WHERE conta_destino = ?",
        (id_conta,)
    ).fetchone()["total"]

    saldo = conta["saldo_inicial"] + receitas - despesas - saidas + entradas
    conexao.close()
    return round(saldo, 2)

def cadastrar_conta(id_usuario, banco, tipo, saldo_inicial):
    conexao = conectar()
    conexao.execute(
        "INSERT INTO contas (id_usuario, banco, tipo, saldo_inicial) VALUES (?, ?, ?, ?)",
        (id_usuario, banco, tipo, saldo_inicial)
    )
    conexao.commit()
    conexao.close()

def buscar_conta(id_conta, id_usuario):
    conexao = conectar()
    conta = conexao.execute(
        "SELECT * FROM contas WHERE id_conta = ? AND id_usuario = ? AND ativa = 1",
        (id_conta, id_usuario)
    ).fetchone()
    conexao.close()
    return conta

def desativar_conta(id_conta, id_usuario):
    conexao = conectar()
    conta = conexao.execute(
        "SELECT id_conta FROM contas WHERE id_conta = ? AND id_usuario = ?",
        (id_conta, id_usuario)
    ).fetchone()
    if conta is None:
        conexao.close()
        return False
    conexao.execute("UPDATE contas SET ativa = 0 WHERE id_conta = ?", (id_conta,))
    conexao.commit()
    conexao.close()
    return True

def totais_gerais(id_usuario):
    conexao = conectar()
    contas = conexao.execute(
        "SELECT id_conta, saldo_inicial FROM contas WHERE id_usuario = ? AND ativa = 1",
        (id_usuario,)
    ).fetchall()
    conexao.close()

    patrimonio = 0
    for conta in contas:
        patrimonio += calcular_saldo(conta["id_conta"])
    return round(patrimonio, 2)
