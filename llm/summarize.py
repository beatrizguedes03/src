import logging
from llm.model import Model
import os

class Summarize:
    def __init__(self, texto, nome):
        self.texto = texto
        self.nome = nome

    def mapreducesummarizer(self, texto, model, tokenizer, limite=2000):
        aux = Model()

        if len(texto) <= limite:
            prompt = (
                "<|im_start|>system\n"
                "Você é um assistente útil.\n"
                "<|im_end|>\n"
                "<|im_start|>user\n"
                f"Resuma este texto em apenas 1 parágrafo curto: {texto}\n"
                "<|im_end|>\n"
                "<|im_start|>assistant"
            )
            return aux.gerarsaida(model, tokenizer, prompt)

        chunks = [texto[i:i + limite] for i in range(0, len(texto), limite)]
        resumos = []

        for chunk in chunks:
            prompt = (
                "<|im_start|>system\n"
                "Você é um assistente útil.\n"
                "<|im_end|>\n"
                "<|im_start|>user\n"
                f"Resuma este trecho: {chunk}\n"
                "<|im_end|>\n"
                "<|im_start|>assistant"
            )
            resumos.append(aux.gerarsaida(model, tokenizer, prompt))

        texto_reduzido = " ".join(resumos)
        return self.mapreducesummarizer(texto_reduzido, model, tokenizer, limite)


    def gerarresumo(self):
        logging.info("Gerando resumo...")
        aux = Model()
        tokenizer, model = aux.carregarmodelo()
        resumo = self.mapreducesummarizer(self.texto, model, tokenizer)
        logging.info(resumo)
        logging.info("Resumo Gerado. ")
        return resumo

    def salvarresumo(self, resumo):
        caminho = self.nome
        pasta = os.path.dirname(caminho)
        if pasta:
            os.makedirs(pasta, exist_ok=True)
        else:
            pasta = "resumos"
            os.makedirs(pasta, exist_ok=True)
            caminho = os.path.join(pasta, os.path.basename(caminho))
        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write(resumo)
            logging.info(f"Resumo salvo com sucesso em {caminho}.")
        except Exception as e:
            logging.error(f"Falha ao salvar resumo: {e}")

    def salvarrelatorio(self, relatorio):
        caminho = self.nome
        pasta = os.path.dirname(caminho)
        if pasta:
            os.makedirs(pasta, exist_ok=True)
        else:
            pasta = "relatorios"
            os.makedirs(pasta, exist_ok=True)
            caminho = os.path.join(pasta, os.path.basename(caminho))
        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write("## Estatísticas\n")
                arquivo.write(str(relatorio['estatisticas']) + "\n\n")
                arquivo.write("## Resumo\n")
                arquivo.write(relatorio['resumo'] + "\n\n")
                arquivo.write("## Imagens\n")
                arquivo.write(str(relatorio['diretorioimagens']))
            logging.info(f"Relatório salvo em {caminho}")
        except Exception as e:
            logging.error(f"Falha ao salvar relatorio: {e}")
