from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.mongo.mongo_connection import (
    providencias,
    similitudes
)


def obtener_documentos():

    return list(
        providencias.find(
            {
                "texto": {
                    "$exists": True,
                    "$ne": ""
                }
            },
            {
                "_id": 0,
                "nombre": 1,
                "texto": 1
            }
        )
    )


def obtener_nivel(score):

    if score >= 0.8:
        return "ALTA"

    elif score >= 0.5:
        return "MEDIA"

    return "BAJA"


def calcular_similitudes():

    documentos = obtener_documentos()

    print(f"Documentos encontrados: {len(documentos)}")

    nombres = []

    textos = []

    for doc in documentos:

        nombres.append(doc["nombre"])

        textos.append(doc["texto"])

    vectorizer = TfidfVectorizer()

    matriz_tfidf = vectorizer.fit_transform(
        textos
    )

    matriz_similitud = cosine_similarity(
        matriz_tfidf
    )

    return nombres, matriz_similitud


def guardar_similitudes():

    print("Limpiando colección similitudes...")

    similitudes.delete_many({})

    nombres, matriz = calcular_similitudes()

    total_relaciones = 0

    for i in range(len(nombres)):

        for j in range(i + 1, len(nombres)):

            score = float(
                matriz[i][j]
            )

            documento = {

                "documento_1": nombres[i],

                "documento_2": nombres[j],

                "similitud": round(
                    score,
                    4
                ),

                "nivel": obtener_nivel(
                    score
                )
            }

            similitudes.insert_one(
                documento
            )

            total_relaciones += 1

    print(
        f"Similitudes guardadas: {total_relaciones}"
    )