import argparse
import pdf.extractor as extractor
import pdf.images as images
import llm.summarize as summarize
import logging

class Arguments:
    @staticmethod
    def argumentos():
        parser = argparse.ArgumentParser(description='Ferramenta CLI para PDFs')
        subparsers = parser.add_subparsers(dest='comando')

        info = subparsers.add_parser('info', help='Mostra estatísticas do PDF')
        info.add_argument('arquivo_entrada')

        imagens = subparsers.add_parser('imagens', help='Extrai imagens')
        imagens.add_argument('arquivo_entrada')

        resumo = subparsers.add_parser('resumo', help='Gera resumo com LLM local')
        resumo.add_argument('arquivo_entrada')
        resumo.add_argument('-o', '--saida', help='Salvar resumo em arquivo .md ou .txt')

        relatorio = subparsers.add_parser('relatorio', help='Relatorio completo com todos os Dados Unificados')
        relatorio.add_argument('arquivo_entrada')
        relatorio.add_argument('-o', '--saidar', help='Salvar relatorio em arquivo .md ou .txt')

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
            logging.info("Iniciando analise do PDF...")
            documento.saida()
            logging.info("Analise Concluida. ")

        elif args.comando == "imagens":
            logging.info("Extraindo imagens...")
            fotos = images.Images(args.arquivo_entrada)
            fotos.principal()
            logging.info("Extraçao Concluida. ")

        elif args.comando == "resumo":
            logging.info("Gerando resumo...")
            texto = documento.textoparallm()
            summarizer = summarize.Summarize(texto)
            resumo = summarizer.gerarresumo()
            logging.info("Resumo Gerado. ")
            if args.saida:
                logging.info("Salvando Resumo...")
                if not args.saida.endswith(".txt") and not args.saida.endswith(".md"):
                    logging.error("Arquivo de Saida nao Suportado. ")
                    parser.print_help()
                    return
                summarizer.salvarresumo(resumo, args.saida)


        elif args.comando == "relatorio":
            logging.info("Gerando relatorio...")
            analise = documento.saida()
            texto = documento.textoparallm()
            aux = images.Images(args.arquivo_entrada)
            fotos = aux.principal()
            summarizer = summarize.Summarize(texto)
            resumo = summarizer.gerarresumo()

            relatoriofinal = {
                'estatisticas': analise,
                'resumo': resumo,
                'diretorioimagens': fotos
            }
            logging.info("Relatorio Gerado. ")

            if args.saidar:
                logging.info("Salvando Relatorio...")
                if not args.saidar.endswith(".txt") and not args.saidar.endswith(".md"):
                    logging.error("Arquivo de Saida nao Suportado. ")
                    parser.print_help()
                    return
                summarizer.salvarrelatorio(relatoriofinal, args.saidar)


        else:
            logging.error("Comando nao Reconhecido. ")
            parser.print_help()

        documento.fechardocumento()

