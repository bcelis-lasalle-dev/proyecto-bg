import re
from unidecode import unidecode

#funcion para limpiar texto, eliminando caracteres especiales, acentos y convirtiendo a minusculas
def limpiar_texto(texto):

    texto = texto.lower()

    texto = unidecode(texto)

    texto = texto.replace("\n", " ")
    texto = texto.replace("\r", " ")
    texto = texto.replace("\t", " ")

    texto = re.sub(r"[^a-z0-9 ]", " ", texto)

    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()