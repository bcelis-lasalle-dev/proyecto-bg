from mongo_connection import providencias
print("Iniciando prueba Mongo...")
documento = {
    "nombre": "C-313-14",
    "tipo": "Constitucionalidad",
    "anio": 2014,
    "paginas": 10
}

resultado = providencias.insert_one(documento)

print("Documento insertado:", resultado.inserted_id)
print("Finalizó la prueba")