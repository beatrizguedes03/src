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
                "Você é um assistente especialista em resumos. Resuma o texto abaixo em 1 parágrafo, em Português (PT-BR), sem inventar informações.\n"
                "<|im_end|>\n"
                "<|im_start|>user\n"
                f"{texto}\n"
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
        pasta = "resumos"
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, self.nome)  # junta pasta + nome do arquivo
        try:
            with open(caminho, "w", encoding="utf-8") as file:
                file.write(resumo)
            logging.info(f"Resumo salvo com sucesso em {caminho}.")

        except Exception as e:
            logging.error(f"Falha ao salvar resumo: {e}")

    def salvarrelatorio(self, relatorio):
        pasta = "relatorios"
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, self.nome)
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write("## Estatísticas\n")
                f.write(str(relatorio['estatisticas']) + "\n\n")
                f.write("## Resumo\n")
                f.write(relatorio['resumo'] + "\n\n")
                f.write("## Imagens\n")
                f.write(str(relatorio['diretorioimagens']))
            logging.info(f"Relatório salvo em {caminho}")
        except Exception as e:
            logging.error(f"Falha ao salvar relatorio: {e}")
