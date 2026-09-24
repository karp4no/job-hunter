EQUIVALENCIAS = {
    "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "python": ["python", "python3"],
    "git": ["git", "github", "gitlab"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "react": ["react", "reactjs"],
    "node": ["node", "nodejs"],
}


def normalizar_habilidade(habilidade):
    habilidade = habilidade.strip().lower()

    for principal, equivalentes in EQUIVALENCIAS.items():

        if habilidade in equivalentes:
            return principal

    return habilidade


def analisar_compatibilidade(habilidades_perfil, habilidades_vaga):

    perfil = [
        normalizar_habilidade(habilidade)
        for habilidade in habilidades_perfil.split(",")
        if habilidade.strip()
    ]

    vaga = [
        normalizar_habilidade(habilidade)
        for habilidade in habilidades_vaga.split(",")
        if habilidade.strip()
    ]

    if not vaga:
        return {
            "porcentagem": 0,
            "encontradas": [],
            "faltantes": []
        }

    encontradas = []
    faltantes = []

    for habilidade in vaga:

        if habilidade in perfil:

            if habilidade not in encontradas:
                encontradas.append(habilidade)

        else:

            if habilidade not in faltantes:
                faltantes.append(habilidade)

    porcentagem = round(
        (len(encontradas) / len(vaga)) * 100
    )

    return {
        "porcentagem": porcentagem,
        "encontradas": encontradas,
        "faltantes": faltantes
    }
