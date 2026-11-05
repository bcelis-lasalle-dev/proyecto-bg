from src.mongo.mongo_connection import (
    providencias,
    similitudes
)

from src.neo4j.neo4j_connection import (
    driver
)


def limpiar_grafo():

    with driver.session() as session:

        session.run(
            """
            MATCH (n)
            DETACH DELETE n
            """
        )

    print("Grafo limpiado")


def cargar_nodos():

    documentos = list(
        providencias.find(
            {},
            {
                "_id": 0
            }
        )
    )

    with driver.session() as session:

        for doc in documentos:

            session.run(
                """
                MERGE (p:Providencia {
                    nombre:$nombre
                })

                SET
                    p.tipo=$tipo,
                    p.anio=$anio,
                    p.paginas=$paginas
                """,
                nombre=doc["nombre"],
                tipo=doc["tipo"],
                anio=doc["anio"],
                paginas=doc["paginas"]
            )

    print(
        f"Nodos creados: {len(documentos)}"
    )


def cargar_relaciones():

    relaciones = list(
        similitudes.find(
            {},
            {
                "_id": 0
            }
        )
    )

    with driver.session() as session:

        for rel in relaciones:

            session.run(
                """
                MATCH (a:Providencia {
                    nombre:$doc1
                })

                MATCH (b:Providencia {
                    nombre:$doc2
                })

                MERGE (a)-[r:SIMILAR_A]->(b)

                SET
                    r.score=$score,
                    r.nivel=$nivel
                """,
                doc1=rel["documento_1"],
                doc2=rel["documento_2"],
                score=rel["similitud"],
                nivel=rel["nivel"]
            )

    print(
        f"Relaciones creadas: {len(relaciones)}"
    )


def cargar_grafo():

    limpiar_grafo()

    cargar_nodos()

    cargar_relaciones()

    print(
        "Carga completa"
    )