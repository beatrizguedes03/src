import logging
import pymupdf
import utils.text as text
import os

class Extractor:
    def __init__(self, arquivo: str):
        self.pdf = arquivo
        self.documento = self.carregardocumento()
        self.texto = self.extrairtexto()
        self.peso = os.path.getsize(self.pdf)

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
        logging.info("Iniciando analise do PDF...")
        numpaginas = self.contarpaginas(self.documento)
        aux = text.Text(self.texto)
        textolimpo = aux.limpartexto()
        numpalavras = self.contarpalavras(textolimpo)
        vocabulariou = aux.vocabulariounico()
        vocabulario10 = aux.maisfrequentes()
        dadosfinais = self.organizar(numpaginas, numpalavras, vocabulariou, vocabulario10, self.peso)
        saidafinal = self.imprimirdicionario(dadosfinais)
        logging.info(saidafinal)
        logging.info("Analise Concluida. ")
        return saidafinal

    @staticmethod
    def imprimirdicionario(dados):
        linhas = []
        for categoria, valor in dados.items():
            linhas.append(f"{categoria}: {valor}")
        return "\n".join(linhas)

    def textoparallm(self):
        aux = text.Text(self.texto)
        textolimpo = aux.limpartexto()
        return textolimpo

    def fechardocumento(self):
        if self.documento is not None:
            try:
                self.documento.close()
            except Exception as e:
                logging.error(f"Erro ao fechar PDF: {e}")


