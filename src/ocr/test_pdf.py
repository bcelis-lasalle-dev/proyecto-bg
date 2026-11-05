import fitz

pdf_path = "data/a001-15.pdf"

documento = fitz.open(pdf_path)

texto = ""

for pagina in documento:
    texto += pagina.get_text()

print("Cantidad de caracteres:", len(texto))
print()
print(texto[:1000])