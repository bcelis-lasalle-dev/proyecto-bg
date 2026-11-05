from src.ocr.pdf_extractor import extraer_pdf
from src.utils.text_cleaner import limpiar_texto

resultado = extraer_pdf(
    "data/a001-15.pdf"
)

texto_limpio = limpiar_texto(
    resultado["texto"]
)

print("Longitud original:", len(resultado["texto"]))
print("Longitud limpia:", len(texto_limpio))

print("\nPrimeros 1000 caracteres:\n")
print(texto_limpio[:1000])