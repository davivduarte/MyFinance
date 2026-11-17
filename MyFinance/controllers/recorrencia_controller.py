from database.conexao import conectar
from controllers.transacao_controller import registrar_transacao
from datetime import date

def cadastrar_recorrencia(id_conta, id_categoria, tipo, descricao, valor, dia):
    conexao = conectar()
    conexao.execute("""
        INSERT INTO recorrencias
        (id_conta, id_categoria, tipo, descricao, valor, dia_vencimento)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_conta, id_categoria, tipo, descricao, valor, dia))
    conexao.commit()
    conexao.close()

def listar_recorrencias(id_conta):
    conexao = conectar()
    dados = conexao.execute("""
        SELECT r.*, c.nome AS categoria
        FROM recorrencias r
        JOIN categorias c ON r.id_categoria = c.id_categoria
        WHERE r.id_conta = ? AND r.ativa = 1
        ORDER BY r.dia_vencimento
    """, (id_conta,)).fetchall()
    conexao.close()
    return dados

def lancar_recorrencia(id_recorrencia, mes, ano):
    conexao = conectar()
    recorrencia = conexao.execute(
        "SELECT * FROM recorrencias WHERE id_recorrencia = ? AND ativa = 1",
        (id_recorrencia,)
    ).fetchone()

    if recorrencia is None:
        conexao.close()
        return False, "Recorrencia nao encontrada."

    existente = conexao.execute("""
        SELECT id_lancamento FROM recorrencias_lancadas
        WHERE id_recorrencia = ? AND mes = ? AND ano = ?
    """, (id_recorrencia, mes, ano)).fetchone()

    if existente:
        conexao.close()
        return False, "Essa recorrencia ja foi lancada nesse mes."

    dia = min(recorrencia["dia_vencimento"], 28)
    data = date(ano, mes, dia).isoformat()
    conexao.close()

    sucesso, mensagem = registrar_transacao(
        recorrencia["id_conta"], recorrencia["id_categoria"],
        recorrencia["tipo"], recorrencia["descricao"],
        recorrencia["valor"], data
    )
    if not sucesso:
        return sucesso, mensagem

    conexao = conectar()
    transacao = conexao.execute(
        "SELECT MAX(id_transacao) AS id FROM transacoes WHERE id_conta = ?",
        (recorrencia["id_conta"],)
    ).fetchone()["id"]
    conexao.execute("""
        INSERT INTO recorrencias_lancadas
        (id_recorrencia, mes, ano, id_transacao)
        VALUES (?, ?, ?, ?)
    """, (id_recorrencia, mes, ano, transacao))
    conexao.commit()
    conexao.close()
    return True, "Lancamento recorrente registrado."

