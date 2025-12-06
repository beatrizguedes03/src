## CLI de processamento de PDF: Extração de Dados e Uso de LLM para Obter Descrição detalhada do Texto.

Olá, meu nome é Beatriz Guedes da Silva e esse é o meu trabalho de uma Interface de Linha de comando para o processo seletivo Assembly Digital Assistant para Trainee de LLM.

Os assuntos abordados nesse arquivo tratam de:

1 - Ferramentas utilizadas

2 - Como cada parte foi feita

3 - Como rodar o código

4 - O que eu espero que seja avaliado

## Ferramentas Utilizadas
- Python 3.13
- Ambiente de Desenvolvimento Integrado PyCharm
- Bibliotecas Python argparse, pymupdf, re, unicodedata e string

## Construção do Trabalho
Primeiramente foi criado o repositório, seguindo a base de arquivos enviada no enunciado do trabalho. Após isso foi criado as estuturas do arquivo main e arguments. É notável que a linguagem Python não precisa de funções como a linguagem Java precisa, por exemplo, mas essa modularização garante a segurança e integração dos códigos.

Primeiro foi criado a estrutura inicial do CLI, utilizando a biblioteca argparse. A estrutura contém as opções de obter os dados do pdf como número de páginas, número de palavras, 10 palavras mais repetidas, etc. opção de extração de imagens do pdf, resumo dado pela LLM e salvar o resumo do arquivo (este sendo opcional)

Após isso, foi criado os arquivos extractor.py e text.py, com o primeiro tendo as funções de extração de dados do pdf. A biblioteca escolhida foi o pymupdf, por ser a mais atualizada em relação a extração de características do pdf. As funções do arquivo extractor.py são:
- carregardocumento: carrega o documento para extração de informações;
- extrairtexto: extrai o texto bruto do pdf e guarda em uma variável Literal String
- contarpaginas: conta quantas páginas tem no pdf.
- contarpalavras: conta quantas palavras tem no PDF (seu funcionamento depende do arquivo text.py).

Como já citado, a função de contarpaginas precisa do arquivo text.py, que contém a função limpartexto. Ela passa o texto bruto extraído por um tratamento que consiste em:
- Transformar todas as letras em minúsculas;
- Separar os acentos das letras;
- Como os acentos não são caracteres ASCII, todos os acentos são removidos;
- Toda a pontuação foi removida;
- E qualquer coisa que não seja número, letra ou espaço é removida.
