import os
import pymupdf
import pytesseract

from pdf2image import convert_from_path

# Configuración Tesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

POPPLER_PATH = r"C:\poppler\poppler-26.09.0\Library\bin"


def obtener_tipo(nombre_archivo):

    nombre = nombre_archivo.upper()

    if nombre.startswith("SU"):
        return "Sentencia de Unificacion"

    if nombre.startswith("T"):
        return "Tutela"

    if nombre.startswith("C"):
        return "Constitucionalidad"

    if nombre.startswith("A"):
        return "Auto"

    return "Desconocido"


def obtener_anio(nombre_archivo):

    nombre = nombre_archivo.replace(".pdf", "")

    anio_corto = nombre.split("-")[-1]

    if len(anio_corto) == 2:
        return 2000 + int(anio_corto)

    return None


def extraer_texto_ocr(pdf_path):

    paginas = convert_from_path(
        pdf_path,
        poppler_path=POPPLER_PATH
    )

    texto = ""

    for pagina in paginas:

        texto += pytesseract.image_to_string(
            pagina,
            lang="spa"
        )

    return texto


def extraer_pdf(pdf_path):

    documento = pymupdf.open(pdf_path)

    nombre_archivo = os.path.basename(pdf_path)

    nombre = nombre_archivo.replace(".pdf", "")

    paginas = len(documento)

    texto = ""

    for pagina in documento:
        texto += pagina.get_text()

    # Si el PDF no tiene texto, usar OCR
    if len(texto.strip()) < 100:
        texto = extraer_texto_ocr(pdf_path)

    return {
        "nombre": nombre,
        "tipo": obtener_tipo(nombre),
        "anio": obtener_anio(nombre),
        "paginas": paginas,
        "texto": texto
    }