import sqlite3


def conectar():
    return sqlite3.connect("data/job_hunter.db")


def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vagas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            empresa TEXT NOT NULL,
            local TEXT,
            modelo TEXT,
            compatibilidade INTEGER,
            link TEXT
        )
    """)

    conexao.commit()
    conexao.close()


def adicionar_coluna_habilidades():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("PRAGMA table_info(vagas)")

    colunas = [
        coluna[1]
        for coluna in cursor.fetchall()
    ]

    if "habilidades" not in colunas:

        cursor.execute("""
            ALTER TABLE vagas
            ADD COLUMN habilidades TEXT
        """)

    conexao.commit()
    conexao.close()


def adicionar_colunas_analise():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("PRAGMA table_info(vagas)")

    colunas = [
        coluna[1]
        for coluna in cursor.fetchall()
    ]

    if "habilidades_encontradas" not in colunas:

        cursor.execute("""
            ALTER TABLE vagas
            ADD COLUMN habilidades_encontradas TEXT
        """)

    if "habilidades_faltantes" not in colunas:

        cursor.execute("""
            ALTER TABLE vagas
            ADD COLUMN habilidades_faltantes TEXT
        """)

    conexao.commit()
    conexao.close()


def buscar_vagas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            titulo,
            empresa,
            local,
            modelo,
            habilidades,
            compatibilidade,
            habilidades_encontradas,
            habilidades_faltantes,
            link
        FROM vagas
    """)

    resultados = cursor.fetchall()

    conexao.close()

    vagas = []

    for vaga in resultados:

        vagas.append({
            "id": vaga[0],
            "titulo": vaga[1],
            "empresa": vaga[2],
            "local": vaga[3],
            "modelo": vaga[4],
            "habilidades": vaga[5],
            "compatibilidade": vaga[6],
            "habilidades_encontradas": vaga[7],
            "habilidades_faltantes": vaga[8],
            "link": vaga[9]
        })

    return vagas


def adicionar_vaga(
    titulo,
    empresa,
    local,
    modelo,
    habilidades,
    compatibilidade,
    habilidades_encontradas,
    habilidades_faltantes,
    link
):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO vagas (
            titulo,
            empresa,
            local,
            modelo,
            habilidades,
            compatibilidade,
            habilidades_encontradas,
            habilidades_faltantes,
            link
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        titulo,
        empresa,
        local,
        modelo,
        habilidades,
        compatibilidade,
        habilidades_encontradas,
        habilidades_faltantes,
        link
    ))

    conexao.commit()
    conexao.close()


def criar_tabela_perfil():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS perfil (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            formacao TEXT,
            habilidades TEXT,
            experiencia TEXT,
            objetivo TEXT
        )
    """)

    conexao.commit()
    conexao.close()


def buscar_perfil():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            formacao,
            habilidades,
            experiencia,
            objetivo
        FROM perfil
        LIMIT 1
    """)

    resultado = cursor.fetchone()

    conexao.close()

    if resultado is None:
        return None

    return {
        "id": resultado[0],
        "nome": resultado[1],
        "formacao": resultado[2],
        "habilidades": resultado[3],
        "experiencia": resultado[4],
        "objetivo": resultado[5]
    }


def salvar_perfil(
    nome,
    formacao,
    habilidades,
    experiencia,
    objetivo
):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id FROM perfil LIMIT 1")

    perfil_existente = cursor.fetchone()

    if perfil_existente:

        cursor.execute("""
            UPDATE perfil
            SET
                nome = ?,
                formacao = ?,
                habilidades = ?,
                experiencia = ?,
                objetivo = ?
            WHERE id = ?
        """, (
            nome,
            formacao,
            habilidades,
            experiencia,
            objetivo,
            perfil_existente[0]
        ))

    else:

        cursor.execute("""
            INSERT INTO perfil (
                nome,
                formacao,
                habilidades,
                experiencia,
                objetivo
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            nome,
            formacao,
            habilidades,
            experiencia,
            objetivo
        ))

    conexao.commit()
    conexao.close()
