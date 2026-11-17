from database.conexao import conectar
from datetime import date

def cadastrar_meta(id_usuario, nome, objetivo):
    conexao = conectar()
    conexao.execute(
        "INSERT INTO metas (id_usuario, nome, valor_objetivo) VALUES (?, ?, ?)",
        (id_usuario, nome, objetivo)
    )
    conexao.commit()
    conexao.close()

def listar_metas(id_usuario):
    conexao = conectar()
    metas = conexao.execute(
        "SELECT * FROM metas WHERE id_usuario = ? ORDER BY nome", (id_usuario,)
    ).fetchall()
    resultado = []
    for meta in metas:
        total = conexao.execute(
            "SELECT COALESCE(SUM(valor), 0) FROM aportes_meta WHERE id_meta = ?",
            (meta["id_meta"],)
        ).fetchone()[0]
        resultado.append((meta, total))
    conexao.close()
    return resultado

def adicionar_aporte(id_meta, valor, descricao):
    conexao = conectar()
    conexao.execute("""
        INSERT INTO aportes_meta (id_meta, valor, data, descricao)
        VALUES (?, ?, ?, ?)
    """, (id_meta, valor, date.today().isoformat(), descricao))
    conexao.commit()
    conexao.close()
