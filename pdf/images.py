import logging
import os
import pdf.extractor as extractor

class Images:
    def __init__(self, documento):
        self.documento = documento

    @staticmethod
    def acharimagens(documento):
        imagens = []
        for numpagina, pagina in enumerate(documento):
            for img in pagina.get_images(full=True):
                xref = img[0]
                imagens.append((numpagina, xref))
        return imagens

    def salvarimagens(self, documento, imagens):
        caminhos = []
        pasta1 = "imagens"
        pasta2 = self.documento
        caminhopasta = os.path.join(pasta1, pasta2)
        os.makedirs(caminhopasta, exist_ok=True)

        for i, (numpagina, xref) in enumerate(imagens, start=1):
            try:
                info = documento.extract_image(xref)
                conteudo = info["image"]
                extensao = info["ext"]
                caminhofoto = os.path.join(caminhopasta, f"imagem{i}.{extensao}")

                with open(caminhofoto, "wb") as arquivo:
                    arquivo.write(conteudo)

                caminhos.append(caminhofoto)
                logging.info(f"Imagem {i} Salva em {caminhofoto}")

            except Exception as e:
                logging.error(f"Falha ao salvar imagem {i}: {e}")

        return caminhos

    def principal(self):
        aux = extractor.Extractor(self.documento)
        pdf = aux.carregardocumento()
        fotos = self.acharimagens(pdf)
        caminhos = self.salvarimagens(pdf, fotos)
        return caminhos



