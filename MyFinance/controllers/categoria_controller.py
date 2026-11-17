from database.conexao import conectar

def listar_categorias(id_usuario, tipo=None):
    conexao = conectar()
    if tipo:
        categorias = conexao.execute(
            "SELECT * FROM categorias WHERE id_usuario = ? AND tipo = ? ORDER BY nome",
            (id_usuario, tipo)
        ).fetchall()
    else:
        categorias = conexao.execute(
            "SELECT * FROM categorias WHERE id_usuario = ? ORDER BY tipo, nome",
            (id_usuario,)
        ).fetchall()
    conexao.close()
    return categorias

def cadastrar_categoria(id_usuario, nome, tipo):
    conexao = conectar()
    try:
        conexao.execute(
            "INSERT INTO categorias (nome, tipo, id_usuario) VALUES (?, ?, ?)",
            (nome, tipo, id_usuario)
        )
        conexao.commit()
        resultado = True
    except Exception:
        resultado = False
    conexao.close()
    return resultado

def criar_categorias_padrao(id_usuario):
    padrao = [
        ("Salario", "receita"), ("Renda extra", "receita"),
        ("Alimentacao", "despesa"), ("Moradia", "despesa"),
        ("Transporte", "despesa"), ("Saude", "despesa"),
        ("Lazer", "despesa"), ("Educacao", "despesa"),
        ("Outros", "despesa")
    ]
    for nome, tipo in padrao:
        cadastrar_categoria(id_usuario, nome, tipo)
