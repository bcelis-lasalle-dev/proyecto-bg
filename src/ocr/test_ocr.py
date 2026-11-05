from pdf2image import convert_from_path
import pytesseract

# Tesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Poppler
POPPLER_PATH = r"C:\poppler\poppler-26.09.0\Library\bin"

pdf_path = "data/a001-15.pdf"

print("Convirtiendo PDF a imágenes...")

paginas = convert_from_path(
    pdf_path,
    first_page=1,
    last_page=1,
    poppler_path=POPPLER_PATH
)

print("Ejecutando OCR...")

texto = pytesseract.image_to_string(
    paginas[0],
    lang="spa"
)

print("\nPrimeros 2000 caracteres:\n")
print(texto[:2000])