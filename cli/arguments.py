import argparse
import pdf.extractor as extractor
import pdf.images as images
import llm.summarize as summarize
import logging

class Arguments:
    @staticmethod
    def argumentos():
        parser = argparse.ArgumentParser(description='Ferramenta CLI para processamento de PDFs')

        subparsers = parser.add_subparsers(dest='comando', required=True)

        info = subparsers.add_parser('info', help='Mostra estatísticas do PDF')
        info.add_argument('arquivo_entrada', help='Caminho do arquivo PDF')

        imagens = subparsers.add_parser('imagens', help='Extrai todas as imagens do PDF')
        imagens.add_argument('arquivo_entrada', help='Caminho do arquivo PDF')

        resumo = subparsers.add_parser('resumo', help='Gera um resumo usando LLM local')
        resumo.add_argument('arquivo_entrada', help='Caminho do arquivo PDF')
        resumo.add_argument('-o', '--saida', help='Salvar resumo em .md ou .txt')

        relatorio = subparsers.add_parser('relatorio', help='Gera relatório completo (estatísticas + resumo)')
        relatorio.add_argument('arquivo_entrada', help='Caminho do arquivo PDF')
        relatorio.add_argument('-o', '--saida', help='Salvar relatório em .md ou .txt')

        return parser

    def principal(self):
        parser = self.argumentos()
        args = parser.parse_args()

        if not args.arquivo_entrada.endswith(".pdf"):
            logging.error("Arquivo de Entrada nao Suportado. ")
            parser.print_help()
            return

        documento = extractor.Extractor(args.arquivo_entrada)
        dados = documento.tamanhopdf()

        if dados == 1:
            logging.error("Tamanho do Arquivo nao Suportado. ")
            parser.print_help()
            return

        if args.comando == "info":
            documento.saida()

        elif args.comando == "imagens":
            aux = documento.carregardocumento()
            fotos = images.Images(aux, args.arquivo_entrada)
            temfotos = fotos.principal()
            if temfotos == "Nao Possui. ":
                return

        elif args.comando == "resumo":
            texto = documento.textoparallm()
            summarizer = summarize.Summarize(texto, args.saida)
            resumo = summarizer.gerarresumo()
            if args.saida:
                logging.info("Salvando Resumo...")
                if not args.saida.endswith(".txt") and not args.saida.endswith(".md"):
                    logging.error("Arquivo de Saida nao Suportado. ")
                    parser.print_help()
                    return
                summarizer.salvarresumo(resumo)

        elif args.comando == "relatorio":
            logging.info("Gerando relatorio...")
            analise = documento.saida()
            texto = documento.textoparallm()
            arquivo = documento.carregardocumento()
            aux = images.Images(arquivo, args.arquivo_entrada)
            fotos = aux.principal()
            summarizer = summarize.Summarize(texto, args.saida)
            resumo = summarizer.gerarresumo()
            relatoriofinal = {
                'estatisticas': analise,
                'resumo': resumo,
                'diretorioimagens': fotos
            }
            logging.info("Relatorio Gerado. ")
            if args.saida:
                logging.info("Salvando Relatorio...")
                if not args.saida.endswith(".txt") and not args.saida.endswith(".md"):
                    logging.error("Arquivo de Saida nao Suportado. ")
                    parser.print_help()
                    return
                summarizer.salvarrelatorio(relatoriofinal)

        else:
            logging.error("Comando nao Reconhecido. ")
            parser.print_help()

        documento.fechardocumento()

