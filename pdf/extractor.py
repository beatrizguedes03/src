import pymupdf
from utils.text import limpartexto

def carregardocumento(arquivo):
    documento = pymupdf.open(arquivo)
    return documento

def extrairtexto(documento):
    texto_total = []

    for pagina in documento:
        texto_total.append(pagina.get_text())

    return "\n".join(texto_total)

def contarpaginas(documento):
    paginas = documento.page_count
    print("Total de paginas: ", paginas)

def contarpalavras(texto: str) -> int:
    if not texto.strip():
        return 0
    print("Total de Palavras: ", len(texto.split()))

def saida(arquivo):
    documento = carregardocumento(arquivo)
    texto = extrairtexto(documento)
    contarpaginas(documento)
    textolimpo = limpartexto(texto)
    contarpalavras(textolimpo)
    documento.close()

