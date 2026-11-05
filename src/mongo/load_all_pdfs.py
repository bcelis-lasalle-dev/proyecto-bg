import os

from src.ocr.pdf_extractor import extraer_pdf
from src.utils.text_cleaner import limpiar_texto
from src.mongo.mongo_connection import providencias

PDF_FOLDER = "data"

for archivo in os.listdir(PDF_FOLDER):

    if not archivo.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(
        PDF_FOLDER,
        archivo
    )

    print(f"Procesando: {archivo}")

    documento = extraer_pdf(pdf_path)

    documento["texto"] = limpiar_texto(
        documento["texto"]
    )

    # VALIDAR SI YA EXISTE
    existente = providencias.find_one(
        {
            "nombre": documento["nombre"]
        }
    )

    if existente:
        print(f"{documento['nombre']} ya existe")
        continue

    resultado = providencias.insert_one(
        documento
    )

    print(
        f"Guardado correctamente: {resultado.inserted_id}"
    )

print("Proceso terminado")