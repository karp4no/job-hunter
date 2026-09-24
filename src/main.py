from flask import Flask, render_template, request, redirect

from database import (
    criar_tabela,
    adicionar_coluna_habilidades,
    adicionar_colunas_analise,
    criar_tabela_perfil,
    buscar_vagas,
    adicionar_vaga as inserir_vaga,
    buscar_perfil,
    salvar_perfil
)
from compatibilidade import analisar_compatibilidade


app = Flask(__name__)


criar_tabela()
adicionar_coluna_habilidades()
adicionar_colunas_analise()
criar_tabela_perfil()


@app.route("/")
def home():

    vagas = buscar_vagas()

    total_vagas = len(vagas)

    vagas_compativeis = len(
        [vaga for vaga in vagas if vaga["compatibilidade"] >= 80]
    )

    vagas_revisar = len(
        [vaga for vaga in vagas if vaga["compatibilidade"] < 80]
    )

    return render_template(
        "index.html",
        total_vagas=total_vagas,
        vagas_compativeis=vagas_compativeis,
        vagas_revisar=vagas_revisar,
        vagas=vagas
    )


@app.route("/adicionar-vaga", methods=["GET", "POST"])
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

    return render_template("adicionar_vaga.html")
@app.route("/configuracoes", methods=["GET", "POST"])
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

        return redirect("/configuracoes")

    perfil = buscar_perfil()

    return render_template(
        "configuracoes.html",
        perfil=perfil
    )


if __name__ == "__main__":
    app.run(debug=True)
