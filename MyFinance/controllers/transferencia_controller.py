from database.conexao import conectar
from controllers.conta_controller import calcular_saldo

def transferir(conta_origem, conta_destino, valor, descricao, data):
    if conta_origem == conta_destino:
        return False, "A conta de origem e destino devem ser diferentes."

    if valor > calcular_saldo(conta_origem):
        return False, "Saldo insuficiente na conta de origem."

    conexao = conectar()
    try:
        conexao.execute("BEGIN")
        conexao.execute("""
            INSERT INTO transferencias
            (conta_origem, conta_destino, valor, descricao, data)
            VALUES (?, ?, ?, ?, ?)
        """, (conta_origem, conta_destino, valor, descricao, data))
        conexao.commit()
        return True, "Transferencia realizada com sucesso."
    except Exception as erro:
        conexao.rollback()
        return False, "Nao foi possivel realizar a transferencia: {}".format(erro)
    finally:
        conexao.close()