import argparse
from pdf.extractor import saida

def argumentos():
    parser = argparse.ArgumentParser(description='Ferramenta CLI para PDFs')
    subparsers = parser.add_subparsers(dest='comando')

    info = subparsers.add_parser('info', help='Mostra estatísticas do PDF')
    info.add_argument('arquivo_entrada')

    imagens = subparsers.add_parser('imagens', help='Extrai imagens')
    imagens.add_argument('arquivo_entrada')

    resumo = subparsers.add_parser('resumo', help='Gera resumo com LLM local')
    resumo.add_argument('arquivo_entrada')
    resumo.add_argument('-o', '--saida', help='Salvar resumo em arquivo')

    return parser

def principal():
    parser = argumentos()
    args = parser.parse_args()

    if args.comando == "info":
        print("Rodando análise do PDF...")
        principal()

    elif args.comando == "imagens":
        print("Extraindo imagens...")


    elif args.comando == "resumo":
        print("Gerando resumo...")


    else:
        parser.print_help()

