from src.neo4j.neo4j_connection import driver


def obtener_relaciones(nombre, score_minimo):

    with driver.session() as session:

        result = session.run(
            """
            MATCH (p:Providencia {nombre:$nombre})
                  -[r:SIMILAR_A]->
                  (q:Providencia)

            WHERE r.score >= $score

            RETURN
                p.nombre AS origen,
                q.nombre AS destino,
                r.score AS score,
                r.nivel AS nivel
            """,
            nombre=nombre,
            score=score_minimo
        )

        datos = [
            record.data()
            for record in result
        ]

        print(datos)

        return datos