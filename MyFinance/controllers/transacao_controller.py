from database.conexao import conectar
from controllers.conta_controller import calcular_saldo
from models.transacao import Transacao

def registrar_transacao(id_conta, id_categoria, tipo, descricao, valor, data):
    if tipo == "despesa" and valor > calcular_saldo(id_conta):
        return False, "Saldo insuficiente para registrar essa despesa."

    conexao = conectar()
    conexao.execute("""
        INSERT INTO transacoes
        (id_conta, id_categoria, tipo, descricao, valor, data)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_conta, id_categoria, tipo, descricao, valor, data))
    conexao.commit()
    conexao.close()
    return True, "Movimentacao registrada com sucesso."

def listar_transacoes(id_conta, limite=20):
    conexao = conectar()
    transacoes = conexao.execute("""
        SELECT t.*, c.nome AS categoria
        FROM transacoes t
        JOIN categorias c ON t.id_categoria = c.id_categoria
        WHERE t.id_conta = ?
        ORDER BY t.data DESC, t.id_transacao DESC
        LIMIT ?
    """, (id_conta, limite)).fetchall()
    conexao.close()
    return transacoes

def totais_conta(id_conta):
    conexao = conectar()
    receitas = conexao.execute(
        "SELECT COALESCE(SUM(valor), 0) FROM transacoes WHERE id_conta = ? AND tipo = 'receita'",
        (id_conta,)
    ).fetchone()[0]
    despesas = conexao.execute(
        "SELECT COALESCE(SUM(valor), 0) FROM transacoes WHERE id_conta = ? AND tipo = 'despesa'",
        (id_conta,)
    ).fetchone()[0]
    conexao.close()
    return receitas, despesas

def totais_por_categoria(id_conta, tipo):
    conexao = conectar()
    dados = conexao.execute("""
        SELECT c.nome, SUM(t.valor) AS total
        FROM transacoes t
        JOIN categorias c ON t.id_categoria = c.id_categoria
        WHERE t.id_conta = ? AND t.tipo = ?
        GROUP BY c.nome
        ORDER BY total DESC
    """, (id_conta, tipo)).fetchall()
    conexao.close()
    return dados
