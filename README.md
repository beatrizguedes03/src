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
- Bibliotecas Python argparse, pymupdf, re, unicodedata, string, os, nltk

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

Continuando os trabalhos, o foco da vez agora era ajeitar a estrutura do código e terminar a parte analítica. Após pensar um pouco, notei que ainda faltava uma coisa para que a estrutura ficasse ótima: as classes. Para projetos envolvendo várias pastas e arquivos, ter classes em cada código facilita a sua chamada e implementação.

Após corrigir a estrutura dos arquivos já feitos, foi transformado em função estática todas as funções que podiam ser estáticas, para facilitar sua implementação.

Após isso foram feitas as funções para retirar stopwords utilizando a biblioteca nltk (permitida apenas para essa tarefa) e o resultado do tratamento vai para as funções que auxiliam a contar quantas palavras únicas tem e as 10 palavras mais frequentes do texto. Por fim, foi utilizado a biblioteca os para analisar o tamanho do arquivo em bytes. Os resultados foram reunidos em um dicionário e este dicionário é exposto ao usuário.

Partindo para as tarefas mais complexas da CLI, foi criado o arquivo images.py para extração das imagens do documento. Utilizando a função get_images a biblioteca os para salvar todas as imagens extraídas, foi criado com sucesso duas funções (acharimagens, salvarimagens) para o processamento. Entretando, é importante ressaltar que qualquer imagem posta no pdf que não tenha uma extensão de imagem (como em muitos adesivos do canva, por exemplo) não vai ser reconhecida como tal. Para isso, funções de processamento de imagens devem ser feitos (coisa que é bem difícil de fazer com bibliotecas padrão do Python. Não foi pesquisado bibliotecas para manipular pdf além das 3 citada no enunciado no desafio).

Após isso, vem a tarefa mais visada desse desafio: carregar uma llm para fazer o resumo textual do pdf. Para essa tarefa, deve ser notado diversos fatores:
- O hardware da autora desse relatório não tem GPU.
- O hardware da autora desse relatório é fraco para modelos multimodais;
- O Hardware da autora desse relatório não possui AVX.

Dado todos esses impedimentos, a solução para usar um modelo do Hugging Face foi utilizar o programa LM Studio para conseguir gerar um servidor local de uma llm. Foi escolhido a LLM qwen2.5-1.5b-instruct, por ser leve e ter suporte para Portugês-BR. Além disso, para deixar o modelo mais leve ainda, ele foi baaixado na extensão .gguf (formato binário utilizado para armazenar modelos de linguagem grandes (LLMs), É um formato otimizado, especialmente para carregar e salvar modelos rapidamente, tornando a inferência (geração de respostas pelo modelo) mais eficiente, inclusive em CPUs.)

Com estas configurações, foi montado o arquivo model.py com a função para criar o resumo, tudo que você precisa fazer é obter o endereço local passado pelo lm studio quando inicia o server e rodar o arquivo. O prompt é bem claro: "Segue o conteúdo extraído do PDF:\n\n{texto}\n\n" "Resuma isso em um parágrafo, em português do Brasil."

Após fazer as mudanças no arquivo arguments.py, temos mais duas tarefas finalizadas.

A tarefa de criar o arquivo summarize.py me mostrou que parte do desenvolvimento da tarefa estava errado. E é logo a parte mais crucial: o LLM. Ignorei que deveria ser utilizado um LLM local, porém sem nenhum programa externo. Logo, o lm studio não pode ser utilizado.

A solução foi utilizar uma SLM (pequeno modelo de linguagem), sendo escolhido o modelo qwen2.5-1.5b-instruct (puro) para esta tarefa. Sim, o código demora MUITO pra rodar, mas foi a única solução possível.

Além disso, pequenos modelos de linguagem podem alucinar com inputs muito grandes, então o input do pdf foi dividido em chunks de 2000 caracteres. O input agora passa a ser o texto tratado para evitar desperdício de caracteres.

A estrutura de model.py estava fazendo o trabalho de model.py e summarize.py. Para corrigir este erro, as funções carregarmodelo (para carregar a llm) e gerarsaida(para receber a saída dos chunks e da resposta final) ficaram em model.py. Já as funções de gerarresumo (onde tem o prompt que vai gerar o resumo) e salvarresumo (caso o usuario queira salvar o resumo) estão em summarize.py

## Resumo dos Commits
### Commit 1: 
- Estrutura base das pastas e arquivos;
- Arquivos main.py, arguments.py, extractor.py e text.py criados;
- Funções main.py criada;
- Funções arguments.py: argumentos e principal;
- Funções extractor.py: carregardocumento, extrairtexto, contarpaginas, contarpalavras e saida criados e desenvolvidos;
- Funções text.py: limpartexto criado e desenvolvido;

### Commit 2
- Alteração na estrutura dos códigos; Agora cada código é uma classe;
- Função main.py: __init__ criada e desenvolvida;
- Funções extractor.py: carregardocumento e extrairtexto aprimoradas para pdfs grandes. saida aprimorada para receber todas as operações, saida criada e desenvolvida;
- Funções text.py: removerstopwords, vocabulariounico e maisfrequentes criadas e desenvolvidas.

### Commit 3
- Alteração na função carregardocumento (extractor.py): o método não é mais estático;
- Desenvolvimento da função principal (arguments.py): para incluir as funções do arquivo model.py
- Arquivos images.py e model.py criados e desenvolvidos.