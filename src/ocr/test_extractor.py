from pdf_extractor import extraer_pdf

resultado = extraer_pdf(
    "data/a001-15.pdf"
)

print("Nombre:", resultado["nombre"])
print("Tipo:", resultado["tipo"])
print("Año:", resultado["anio"])
print("Paginas:", resultado["paginas"])

print("\nPrimeros 1000 caracteres:\n")
print(resultado["texto"][:1000])