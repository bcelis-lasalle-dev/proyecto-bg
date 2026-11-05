import sys
import os

sys.path.append(
    os.path.abspath(".")
)

import streamlit as st

from src.mongo.mongo_connection import (
    providencias,
    similitudes
)

from src.neo4j.graph_service import (
    obtener_relaciones
)

from src.neo4j.graph_visualizer import (
    generar_grafo
)

# ==================================
# CONFIGURACIÓN
# ==================================

st.set_page_config(
    page_title="Sistema Inteligente de Consulta de Providencias",
    layout="wide"
)

# ==================================
# ENCABEZADO
# ==================================

st.title(
    "Sistema Inteligente de Consulta de Providencias"
)

st.markdown(
    """
    ### Proyecto Big Data

    OCR + MongoDB Atlas + Neo4j Aura + TF-IDF + Similitud Coseno
    """
)

# ==================================
# MÉTRICAS
# ==================================

total_providencias = providencias.count_documents({})

total_relaciones = similitudes.count_documents({})

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Providencias procesadas",
        total_providencias
    )

with col2:

    st.metric(
        "Relaciones de similitud",
        total_relaciones
    )

st.info(
    """
    Funcionalidades disponibles:

    ✅ Buscar providencias por nombre

    ✅ Filtrar por tipo

    ✅ Buscar palabras o frases

    ✅ Consultar similitudes

    ✅ Visualizar grafo de relaciones
    """
)

# ==================================
# BUSCAR POR NOMBRE
# ==================================

st.divider()

st.header(
    "Buscar providencia por nombre"
)

nombre = st.text_input(
    "Nombre de la providencia"
)

if nombre:

    documento = providencias.find_one(
        {
            "nombre": nombre.lower()
        }
    )

    if documento:

        st.success(
            "Providencia encontrada"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Nombre:** {documento['nombre']}"
            )

            st.write(
                f"**Tipo:** {documento['tipo']}"
            )

        with col2:

            st.write(
                f"**Año:** {documento['anio']}"
            )

            st.write(
                f"**Páginas:** {documento['paginas']}"
            )

        st.text_area(
            "Texto",
            documento["texto"][:5000],
            height=300
        )

    else:

        st.warning(
            "Providencia no encontrada"
        )

# ==================================
# FILTRO POR TIPO
# ==================================

st.divider()

st.header(
    "Filtrar por tipo"
)

tipo = st.selectbox(
    "Seleccione un tipo",
    [
        "Todos",
        "Auto",
        "Tutela",
        "Constitucionalidad",
        "Sentencia de Unificacion"
    ]
)

if tipo != "Todos":

    documentos = providencias.find(
        {
            "tipo": tipo
        }
    )

    contador = 0

    for doc in documentos:

        contador += 1

        st.write(
            f"• {doc['nombre']} ({doc['anio']})"
        )

    st.success(
        f"Resultados encontrados: {contador}"
    )

# ==================================
# BÚSQUEDA POR TEXTO
# ==================================

st.divider()

st.header(
    "Buscar palabras o frases"
)

consulta = st.text_input(
    "Ingrese palabras o frases"
)

if consulta:

    resultados = providencias.find(
        {
            "$text": {
                "$search": consulta
            }
        }
    )

    resultados_lista = list(
        resultados
    )

    st.success(
        f"Documentos encontrados: {len(resultados_lista)}"
    )

    for doc in resultados_lista:

        with st.expander(
            doc["nombre"]
        ):

            st.write(
                f"Tipo: {doc['tipo']}"
            )

            st.write(
                f"Año: {doc['anio']}"
            )

            st.write(
                f"Páginas: {doc['paginas']}"
            )

            st.write(
                doc["texto"][:1000]
            )

# ==================================
# GRAFO NEO4J
# ==================================

st.divider()

st.header(
    "Visualización de relaciones"
)

nombre_grafo = st.text_input(
    "Providencia para analizar",
    key="grafo"
)

score_minimo = st.slider(
    "Similitud mínima",
    0.0,
    1.0,
    0.8
)

if nombre_grafo:

    relaciones = obtener_relaciones(
        nombre_grafo.lower(),
        score_minimo
    )

    st.success(
        f"Relaciones encontradas: {len(relaciones)}"
    )

    relaciones = sorted(
        relaciones,
        key=lambda x: x["score"],
        reverse=True
    )

    top_relaciones = relaciones[:10]

    st.subheader(
        "Top 10 relaciones más similares"
    )

    for rel in top_relaciones:

        st.write(
            f"{rel['origen']} → "
            f"{rel['destino']} | "
            f"Score: {rel['score']:.4f} | "
            f"Nivel: {rel['nivel']}"
        )

    if relaciones:

        archivo_html = generar_grafo(
            nombre_grafo.lower(),
            score_minimo
        )

        with open(
            archivo_html,
            "r",
            encoding="utf-8"
        ) as f:

            html = f.read()

        st.components.v1.html(
            html,
            height=750,
            scrolling=True
        )

# ==================================
# FOOTER
# ==================================

st.divider()

st.caption(
    """
    Proyecto académico desarrollado con:

    Python | Tesseract OCR | MongoDB Atlas |
    Neo4j Aura | Scikit-Learn |
    Streamlit | PyVis
    """
)