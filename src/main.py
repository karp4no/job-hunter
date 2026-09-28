from flask import Flask, render_template, request, redirect, url_for

from database import (
    criar_tabela,
    adicionar_coluna_habilidades,
    adicionar_colunas_analise,
    criar_tabela_perfil,
    buscar_vagas,
    adicionar_vaga as inserir_vaga,
    vaga_existe,
    buscar_perfil,
    salvar_perfil,
    adicionar_coluna_status,
    atualizar_status_vaga
)

from compatibilidade import analisar_compatibilidade
from busca_vagas import buscar_vagas_automaticas as executar_busca_vagas


app = Flask(__name__)


criar_tabela()
adicionar_coluna_habilidades()
adicionar_colunas_analise()
criar_tabela_perfil()
adicionar_coluna_status()


@app.route("/")
def home():

    vagas = buscar_vagas()

    total_vagas = len(vagas)

    vagas_compativeis = len(
        [
            vaga
            for vaga in vagas
            if vaga["compatibilidade"] >= 80
        ]
    )

    vagas_revisar = len(
        [
            vaga
            for vaga in vagas
            if vaga["compatibilidade"] < 80
        ]
    )

    status_contagem = {
        "Nova": 0,
        "Candidatura enviada": 0,
        "Entrevista": 0,
        "Recusada": 0,
        "Contratado": 0
    }

    for vaga in vagas:

        status = vaga.get("status", "Nova")

        if status in status_contagem:
            status_contagem[status] += 1

    return render_template(
        "index.html",
        total_vagas=total_vagas,
        vagas_compativeis=vagas_compativeis,
        vagas_revisar=vagas_revisar,
        status_contagem=status_contagem,
        vagas=vagas
    )


@app.route("/buscar-vagas")
def buscar_vagas_automaticamente():

    perfil = buscar_perfil()

    if not perfil or not perfil["habilidades"]:

        return redirect(
            url_for(
                "home",
                aviso=(
                    "Cadastre suas habilidades em "
                    "Configurações antes de buscar vagas."
                )
            )
        )

    try:

        vagas_encontradas = executar_busca_vagas(
            perfil["habilidades"]
        )

        novas = 0

        for vaga in vagas_encontradas:

            if not vaga["link"]:
                continue

            if vaga_existe(vaga["link"]):
                continue

            inserir_vaga(
                vaga["titulo"],
                vaga["empresa"],
                vaga["local"],
                vaga["modelo"],
                vaga["habilidades"],
                vaga["compatibilidade"],
                vaga["habilidades_encontradas"],
                vaga["habilidades_faltantes"],
                vaga["link"]
            )

            novas += 1

        return redirect(
            url_for(
                "home",
                aviso=(
                    f"Busca concluída: "
                    f"{novas} novas vagas adicionadas."
                )
            )
        )

    except Exception as erro:

        print(
            f"Erro na busca automática: {erro}"
        )

        return redirect(
            url_for(
                "home",
                aviso=(
                    "Não foi possível buscar vagas agora. "
                    "Tente novamente mais tarde."
                )
            )
        )


@app.route(
    "/adicionar-vaga",
    methods=["GET", "POST"]
)
def adicionar_vaga():

    if request.method == "POST":

        titulo = request.form["titulo"]
        empresa = request.form["empresa"]
        local = request.form["local"]
        modelo = request.form["modelo"]
        habilidades = request.form["habilidades"]
        link = request.form["link"]

        perfil = buscar_perfil()

        if perfil:

            analise = analisar_compatibilidade(
                perfil["habilidades"],
                habilidades
            )

            compatibilidade = analise["porcentagem"]

            habilidades_encontradas = ", ".join(
                analise["encontradas"]
            )

            habilidades_faltantes = ", ".join(
                analise["faltantes"]
            )

        else:

            compatibilidade = 0
            habilidades_encontradas = ""
            habilidades_faltantes = ""

        inserir_vaga(
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

        return redirect("/")

    return render_template(
        "adicionar_vaga.html"
    )


@app.route(
    "/configuracoes",
    methods=["GET", "POST"]
)
def configuracoes():

    if request.method == "POST":

        nome = request.form["nome"]
        formacao = request.form["formacao"]
        habilidades = request.form["habilidades"]
        experiencia = request.form["experiencia"]
        objetivo = request.form["objetivo"]

        salvar_perfil(
            nome,
            formacao,
            habilidades,
            experiencia,
            objetivo
        )

        return redirect(
            "/configuracoes"
        )

    perfil = buscar_perfil()

    return render_template(
        "configuracoes.html",
        perfil=perfil
    )




@app.route("/vaga/<int:vaga_id>/status", methods=["POST"])
def alterar_status_vaga(vaga_id):

    status = request.form["status"]

    status_validos = [
        "Nova",
        "Candidatura enviada",
        "Entrevista",
        "Recusada",
        "Contratado"
    ]

    if status in status_validos:
        atualizar_status_vaga(vaga_id, status)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
