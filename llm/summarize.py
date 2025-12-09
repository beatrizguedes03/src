from llm.model import Model
import os

class Summarize:
    def __init__(self, texto):
        self.texto = texto

    def gerarresumo(self):
        aux = Model()
        tokenizer, model = aux.carregarmodelo()

        tamanhochunk = 2000
        chunks = [self.texto[i:i + tamanhochunk] for i in range(0, len(self.texto), tamanhochunk)]

        resumos = []

        for chunk in chunks:
            prompt = (
                f"""### Texto:
                {chunk}

                ### Instrução:
                Resuma o texto acima.

                ### Regras:
                1. Use apenas texto, sem hashtags ou símbolos extras.
                2. Responda em apenas 1 parágrafo.
                3. Não invente informações.
                4. Português do Brasil.
                5. Não comece com saudações.

                ### Resposta:"""
            )

            resumo = aux.gerarsaida(model, tokenizer, prompt)
            resumos.append(resumo)

        texto_final = "\n".join(resumos)

        prompt_final = (
            f"""### Texto:
                {texto_final}

                ### Instrução:
                Resuma o texto acima.

                ### Regras:
                1. Use apenas texto, sem hashtags ou símbolos extras.
                2. Responda em apenas 1 parágrafo.
                3. Não invente informações.
                4. Português do Brasil.
                5. Não comece com saudações.

                ### Resposta:"""
        )

        resposta = aux.gerarsaida(model, tokenizer, prompt_final)

        print(resposta)
        return resposta

    def salvarresumo(self, resumo, nome):
        pasta = "resumos"
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, nome)  # junta pasta + nome do arquivo
        try:
            with open(caminho, "w", encoding="utf-8") as file:
                file.write(resumo)
            print(f"Resumo salvo com sucesso em {caminho}.")

        except Exception as e:
            print(f"Falha ao salvar o resumo: {e}")

    def salvarrelatorio(self, relatorio, nome):
        pasta = "relatorios"
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, nome)
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write("## Estatísticas\n")
                f.write(str(relatorio['estatisticas']) + "\n\n")
                f.write("## Resumo\n")
                f.write(relatorio['resumo'] + "\n\n")
                f.write("## Imagens\n")
                f.write(str(relatorio['diretorioimagens']))
            print(f"Relatório salvo em {caminho}")
        except Exception as e:
            print(f"Falha ao salvar o relatorio: {e}")
