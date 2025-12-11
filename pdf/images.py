import logging
import os

class Images:
    def __init__(self, documento, nome):
        self.pdf = documento
        self.nome = nome

    def acharimagens(self):
        imagens = []
        for numpagina, pagina in enumerate(self.pdf):
            for img in pagina.get_images(full=True):
                xref = img[0]
                imagens.append((numpagina, xref))
        return imagens

    def salvarimagens(self, imagens):
        caminhos = []
        pasta1 = "imagens"
        pasta2 = self.nome
        caminhopasta = os.path.join(pasta1, pasta2)
        os.makedirs(caminhopasta, exist_ok=True)

        for i, (numpagina, xref) in enumerate(imagens, start=1):
            try:
                info = self.pdf.extract_image(xref)
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
        logging.info("Extraindo imagens...")
        fotos = self.acharimagens()
        if not fotos:
            logging.info("O Arquivo nao possui imagens. ")
            return "Nao Possui. "
        caminhos = self.salvarimagens(fotos)
        logging.info("Extraçao Concluida. ")
        return caminhos



