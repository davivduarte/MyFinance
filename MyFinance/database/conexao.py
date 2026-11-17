import sqlite3

NOME_BANCO = "myfinance.db"

def conectar():
    conexao = sqlite3.connect(NOME_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas (
            id_conta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            banco TEXT NOT NULL,
            tipo TEXT NOT NULL,
            saldo_inicial REAL NOT NULL DEFAULT 0,
            ativa INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            id_usuario INTEGER NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
            UNIQUE(nome, tipo, id_usuario)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id_transacao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_conta INTEGER NOT NULL,
            id_categoria INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (id_conta) REFERENCES contas(id_conta),
            FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transferencias (
            id_transferencia INTEGER PRIMARY KEY AUTOINCREMENT,
            conta_origem INTEGER NOT NULL,
            conta_destino INTEGER NOT NULL,
            valor REAL NOT NULL,
            descricao TEXT,
            data TEXT NOT NULL,
            FOREIGN KEY (conta_origem) REFERENCES contas(id_conta),
            FOREIGN KEY (conta_destino) REFERENCES contas(id_conta)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recorrencias (
            id_recorrencia INTEGER PRIMARY KEY AUTOINCREMENT,
            id_conta INTEGER NOT NULL,
            id_categoria INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            dia_vencimento INTEGER NOT NULL,
            ativa INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (id_conta) REFERENCES contas(id_conta),
            FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recorrencias_lancadas (
            id_lancamento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_recorrencia INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            id_transacao INTEGER NOT NULL,
            FOREIGN KEY (id_recorrencia) REFERENCES recorrencias(id_recorrencia),
            FOREIGN KEY (id_transacao) REFERENCES transacoes(id_transacao),
            UNIQUE(id_recorrencia, mes, ano)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metas (
            id_meta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            nome TEXT NOT NULL,
            valor_objetivo REAL NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aportes_meta (
            id_aporte INTEGER PRIMARY KEY AUTOINCREMENT,
            id_meta INTEGER NOT NULL,
            valor REAL NOT NULL,
            data TEXT NOT NULL,
            descricao TEXT,
            FOREIGN KEY (id_meta) REFERENCES metas(id_meta)
        )
    """)

    conexao.commit()
    conexao.close()

def obter_usuario():
    conexao = conectar()
    usuario = conexao.execute("SELECT * FROM usuarios LIMIT 1").fetchone()

    if usuario is None:
        print("\nAinda nao existe um perfil cadastrado.")
        nome = input("Digite seu nome para criar o perfil: ").strip()
        while nome == "":
            nome = input("O nome nao pode ficar vazio. Digite novamente: ").strip()

        conexao.execute("INSERT INTO usuarios (nome) VALUES (?)", (nome,))
        conexao.commit()
        usuario = conexao.execute("SELECT * FROM usuarios LIMIT 1").fetchone()

    conexao.close()
    return dict(usuario)
