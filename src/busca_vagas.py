import json
import re
import urllib.request

from compatibilidade import EQUIVALENCIAS, normalizar_habilidade


API_URL = "https://remotive.com/api/remote-jobs"


def limpar_html(texto):
    texto = re.sub(r"<[^>]+>", " ", texto or "")
    return re.sub(r"\s+", " ", texto).strip()


def habilidade_aparece(texto, habilidade):

    aliases = EQUIVALENCIAS.get(
        habilidade,
        [habilidade]
    )

    texto = texto.lower()

    for alias in aliases:

        padrao = (
            r"(?<![a-z0-9])"
            + re.escape(alias.lower())
            + r"(?![a-z0-9])"
        )

        if re.search(padrao, texto):
            return True

    return False


def buscar_vagas_automaticas(habilidades_perfil):

    habilidades = [
        normalizar_habilidade(habilidade)
        for habilidade in habilidades_perfil.split(",")
        if habilidade.strip()
    ]

    habilidades = list(dict.fromkeys(habilidades))

    if not habilidades:
        return []

    requisicao = urllib.request.Request(
        API_URL + "?limit=100",
        headers={
            "User-Agent": "JobHunter/1.0",
            "Accept": "application/json"
        }
    )

    with urllib.request.urlopen(
        requisicao,
        timeout=30
    ) as resposta:

        dados = json.loads(
            resposta.read().decode("utf-8")
        )

    vagas = []

    for vaga in dados.get("jobs", []):

        texto = " ".join([
            vaga.get("title", ""),
            vaga.get("description", ""),
            vaga.get("category", "")
        ])

        texto = limpar_html(texto)

        encontradas = [
            habilidade
            for habilidade in habilidades
            if habilidade_aparece(texto, habilidade)
        ]

        if not encontradas:
            continue

        faltantes = [
            habilidade
            for habilidade in habilidades
            if habilidade not in encontradas
        ]

        compatibilidade = round(
            (len(encontradas) / len(habilidades)) * 100
        )

        vagas.append({
            "titulo": vaga.get(
                "title",
                "Vaga sem título"
            ),

            "empresa": vaga.get(
                "company_name",
                "Empresa não informada"
            ),

            "local": vaga.get(
                "candidate_required_location",
                "Remoto"
            ),

            "modelo": "Remoto",

            "habilidades": ", ".join(
                encontradas
            ),

            "compatibilidade": compatibilidade,

            "habilidades_encontradas": ", ".join(
                encontradas
            ),

            "habilidades_faltantes": ", ".join(
                faltantes
            ),

            "link": vaga.get(
                "url",
                ""
            )
        })

    vagas.sort(
        key=lambda vaga: vaga["compatibilidade"],
        reverse=True
    )

    return vagas
