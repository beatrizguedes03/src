### CLI para Processamento de PDFs com Suporte a LLM

Olá! meu nome é Beatriz Guedes da Silva e esse é o meu trabalho de uma Interface de Linha de Comando para o processo seletivo Assembly Digital Assistant para Trainee de LLM.

Os assuntos abordados nesse arquivo tratam de:
1. Funcionalidades implementadas
2. Como rodar o projeto
3. O que eu espero que seja avaliado
4. Observações

## Funcionalidades Implementadas
O CLI tem o objetivo de ler o PDF e extrair os seguintes dados do mesmo:
- Estatísticas do Arquivo:
	- Número de páginas;
	- Número de palavras;
	- Número de palavras únicas;
	- Top 10 palavras mais repetidas;
	- Peso em bytes.
- Salvar imagens do Arquivo;
- Gerar resumo do Arquivo feito por uma LLM (Grande Modelo de Linguagem) (Com opção de salvar em formato .txt ou .md);
- Gerar relatório do Arquivo contendo todos os dados já citados acima (Com opção de salvar em formato .txt ou .md)

## Como Rodar o Projeto
- Requisitos:
	- Python = 3.X;
	- Dependências: vide requirements.txt;
	- LLM utilizada: Qwen 2.5 - 0.5B

- Comandos:
	- Gerar Estatísticas:
	```python main.py info exemplo.pdf```
	- Extrair e Salvar Imagens:
	```python main.py imagens exemplo.pdf```
	- Gerar Resumo:
	```python main.py resumo exemplo.pdf```
	- Gerar Relatório
	```python main.py relatorio exemplo.pdf```
	- Gerar e Salvar Resumo:
	```python main.py resumo exemplo.pdf -o exemplo.txt``` ou ```python main.py resumo exemplo.pdf -o exemplo.md```
	- Gerar e Salvar Relatório:
	```python main.py relatorio exemplo.pdf -o exemplo.txt``` ou ```python main.py relatorio exemplo.pdf -o exemplo.md```

## O Que eu Gostaria Que Fosse Avaliado
Gostaria que a avaliação considerasse tanto a implementação do CLI quanto a arquitetura do código, clareza do fluxo, robustez dos tratamentos de exceção e uso da LLM dentro do pipeline. Também tenho interesse em receber feedback sobre boas práticas de organização, modularização e otimização para rodar modelos de linguagem.

## Observações
