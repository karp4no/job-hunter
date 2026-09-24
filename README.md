# Job Hunter

Sistema pessoal para agilizar o processo de busca, análise, organização e acompanhamento de oportunidades de emprego.

## Objetivo

O Job Hunter está sendo desenvolvido como uma ferramenta pessoal para reduzir o trabalho manual durante a busca por emprego.

A ideia é evoluir o sistema para que ele consiga:

- buscar oportunidades de emprego;
- organizar as vagas encontradas;
- analisar a compatibilidade entre meu perfil e os requisitos das vagas;
- facilitar a filtragem das oportunidades;
- armazenar informações das vagas e do meu perfil;
- acompanhar o processo de candidatura;
- evitar o trabalho repetitivo durante a busca;
- futuramente automatizar partes do processo de busca e candidatura.

## Funcionalidades atuais

- Dashboard com resumo das vagas cadastradas;
- Cadastro manual de vagas;
- Armazenamento das vagas em banco de dados SQLite;
- Cadastro de perfil profissional;
- Armazenamento das informações do perfil;
- Análise de compatibilidade entre habilidades do perfil e da vaga;
- Identificação de habilidades encontradas;
- Identificação de habilidades faltantes;
- Exibição do percentual de compatibilidade;
- Armazenamento do link da vaga;
- Acesso às configurações do perfil.

## Tecnologias

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Jinja2

## Estrutura

```text
job-hunter/
├── data/
│   └── job_hunter.db
├── src/
│   ├── main.py
│   ├── database.py
│   ├── compatibilidade.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── adicionar_vaga.html
│   │   └── configuracoes.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── script.js
├── .gitignore
└── README.md
