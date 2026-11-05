from src.ocr.pdf_extractor import extraer_pdf
from src.utils.text_cleaner import limpiar_texto
from src.mongo.mongo_connection import providencias

pdf_path = "data/a001-15.pdf"

documento = extraer_pdf(pdf_path)

documento["texto"] = limpiar_texto(
    documento["texto"]
)

resultado = providencias.insert_one(
    documento
)

print("Documento insertado:")
print(resultado.inserted_id)