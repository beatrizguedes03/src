import pymupdf
import utils.text as text
import os

class Extractor:
    def __init__(self, arquivo):
        self.pdf = arquivo

    @staticmethod
    def carregardocumento(arquivo):
        try:
            documento = pymupdf.open(arquivo)
        except Exception as e:
            print(f"Erro ao abrir o PDF: {e}")
            return None
        return documento

    @staticmethod
    def extrairtexto(documento):
        texto = ""
        for i, pagina in enumerate(documento):
            try:
                texto += pagina.get_text()
            except Exception as e:
                print(f"Não foi possível ler a página {i}: {e}")
                continue
        return texto

    @staticmethod
    def contarpaginas(documento):
        paginas = documento.page_count
        return paginas

    @staticmethod
    def contarpalavras(texto: str):
        if not texto.strip():
            print(0)
        return len(texto.split())

    @staticmethod
    def organizar(npg, npa, vu, vd, p):
        dicionario = {
            'Numero de Paginas': npg,
            'Numero de Palavras': npa,
            'Palavras Unicas no Texto': vu,
            '10 Palavras Mais Frequentes no Texto': vd,
            'Peso do Documento (em bytes)': p,
        }
        return dicionario

    def saida(self):
        documento = self.carregardocumento(self.pdf)
        texto = self.extrairtexto(documento)
        numpaginas = self.contarpaginas(documento)
        aux = text.Text(texto)
        textolimpo = aux.limpartexto()
        numpalavras = self.contarpalavras(textolimpo)
        textosemstop = aux.removerstopwords(textolimpo)
        vocabulariou = aux.vocabulariounico(textosemstop)
        vocabulario10 = aux.maisfrequentes(textosemstop)
        peso = os.path.getsize(self.pdf)
        dadosfinais = self.organizar(numpaginas, numpalavras, vocabulariou, vocabulario10, peso)
        print(dadosfinais)
        documento.close()


