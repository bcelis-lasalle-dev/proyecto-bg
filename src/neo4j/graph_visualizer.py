from pyvis.network import Network

from src.neo4j.graph_service import (
    obtener_relaciones
)


def generar_grafo(
    nombre,
    score_minimo=0.8
):

    relaciones = obtener_relaciones(
        nombre,
        score_minimo
    )

    net = Network(
        height="700px",
        width="100%",
        bgcolor="#ffffff",
        font_color="black"
    )

    net.add_node(
        nombre,
        label=nombre,
        color="red"
    )

    for rel in relaciones:

        net.add_node(
            rel["destino"],
            label=rel["destino"]
        )

        net.add_edge(
            rel["origen"],
            rel["destino"],
            title=f"{rel['score']:.4f}",
            label=f"{rel['score']:.2f}"
        )

    net.save_graph(
        "grafo.html"
    )

    return "grafo.html"