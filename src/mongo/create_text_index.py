from src.mongo.mongo_connection import providencias

providencias.create_index(
    [("texto", "text")]
)

print("Indice creado correctamente")