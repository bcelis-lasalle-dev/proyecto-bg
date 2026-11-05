from neo4j_connection import driver

with driver.session() as session:

    session.run(
        """
        MERGE (p:Providencia {
            nombre:'C-313-14',
            tipo:'Constitucionalidad',
            anio:2014,
            paginas:10
        })
        """
    )

print("Nodo creado correctamente")