import logging
import pymupdf
import utils.text as text
import os

class Extractor:
    def __init__(self, arquivo: str):
        self.pdf = arquivo
        self.documento = self.carregardocumento()

    def carregardocumento(self):
        try:
            return pymupdf.open(self.pdf)
        except Exception as e:
            logging.error(f"Erro ao abrir PDF: {e}")
            return None

    def tamanhopdf(self):
        paginas = self.documento.page_count
        bytes_ = os.path.getsize(self.pdf)
        mb = bytes_ / (1024 ** 2)

        return 1 if mb > 20 or paginas > 50 else 0

    def extrairtexto(self):
        if self.documento is None:
            return ""

        texto = []
        for i in range(self.documento.page_count):
            try:
                texto.append(self.documento[i].get_text())
            except Exception as e:
                logging.warning(f"Falha ao ler página {i}: {e}")

        return "".join(texto)

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
        texto = self.extrairtexto()
        numpaginas = self.contarpaginas(self.documento)
        aux = text.Text(texto)
        textolimpo = aux.limpartexto()
        numpalavras = self.contarpalavras(textolimpo)
        textosemstop = aux.removerstopwords(textolimpo)
        vocabulariou = aux.vocabulariounico(textosemstop)
        vocabulario10 = aux.maisfrequentes(textosemstop)
        peso = os.path.getsize(self.pdf)
        dadosfinais = self.organizar(numpaginas, numpalavras, vocabulariou, vocabulario10, peso)
        logging.info(dadosfinais)
        return dadosfinais

    def textoparallm(self):
        texto = self.extrairtexto()
        aux = text.Text(texto)
        textolimpo = aux.limpartexto()
        return textolimpo

    def fechardocumento(self):
        if self.documento is not None:
            try:
                self.documento.close()
            except Exception as e:
                logging.error(f"Erro ao fechar PDF: {e}")


