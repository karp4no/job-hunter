const filtroCompatibilidade = document.getElementById(
    "filtro-compatibilidade"
);

const filtroModelo = document.getElementById(
    "filtro-modelo"
);

const filtroStatus = document.getElementById(
    "filtro-status"
);

const vagas = document.querySelectorAll(".job-card");
const nenhumaVaga = document.getElementById("nenhuma-vaga");


function aplicarFiltros() {

    const minimo = filtroCompatibilidade
        ? Number(filtroCompatibilidade.value)
        : 0;

    const modeloSelecionado = filtroModelo
        ? filtroModelo.value.toLowerCase()
        : "todos";

    const statusSelecionado = filtroStatus
        ? filtroStatus.value.toLowerCase()
        : "todos";

    let vagasVisiveis = 0;


    vagas.forEach(function (vaga) {

        const compatibilidade = Number(
            vaga.dataset.compatibilidade || 0
        );

        const modeloTexto = vaga
            .querySelector(".location")
            ?.textContent
            .split("•")[1]
            ?.trim()
            .toLowerCase() || "";

        const statusElement = vaga.querySelector(
            ".status-form select"
        );

        const status = statusElement
            ? statusElement.value.trim().toLowerCase()
            : "nova";


        const correspondeCompatibilidade =
            compatibilidade >= minimo;

        const correspondeModelo =
            modeloSelecionado === "todos" ||
            modeloTexto === modeloSelecionado;

        const correspondeStatus =
            statusSelecionado === "todos" ||
            status === statusSelecionado;


        if (
            correspondeCompatibilidade &&
            correspondeModelo &&
            correspondeStatus
        ) {

            vaga.style.display = "";
            vagasVisiveis++;

        } else {

            vaga.style.display = "none";

        }

    });


    if (nenhumaVaga) {

        nenhumaVaga.style.display =
            vagasVisiveis === 0
                ? "block"
                : "none";

    }

}


if (filtroCompatibilidade) {
    filtroCompatibilidade.addEventListener(
        "change",
        aplicarFiltros
    );
}


if (filtroModelo) {
    filtroModelo.addEventListener(
        "change",
        aplicarFiltros
    );
}


if (filtroStatus) {
    filtroStatus.addEventListener(
        "change",
        aplicarFiltros
    );
}


aplicarFiltros();
