const filtroCompatibilidade = document.getElementById(
    "filtro-compatibilidade"
);

const filtroModelo = document.getElementById(
    "filtro-modelo"
);

const vagas = document.querySelectorAll(".job-card");
const nenhumaVaga = document.getElementById("nenhuma-vaga");


function aplicarFiltros() {

    const minimo = Number(
        filtroCompatibilidade.value
    );

    const modeloSelecionado = filtroModelo.value;

    let vagasVisiveis = 0;


    vagas.forEach(function (vaga) {

        const compatibilidade = Number(
            vaga.dataset.compatibilidade
        );

        const modelo = vaga
            .querySelector(".location")
            .textContent
            .split("•")[1]
            ?.trim()
            .toLowerCase();


        const correspondeCompatibilidade =
            compatibilidade >= minimo;


        const correspondeModelo =
            modeloSelecionado === "todos" ||
            modelo === modeloSelecionado;


        if (
            correspondeCompatibilidade &&
            correspondeModelo
        ) {

            vaga.style.display = "";
            vagasVisiveis++;

        } else {

            vaga.style.display = "none";

        }

    });


    if (nenhumaVaga) {

        if (vagasVisiveis === 0) {
            nenhumaVaga.style.display = "block";
        } else {
            nenhumaVaga.style.display = "none";
        }

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
