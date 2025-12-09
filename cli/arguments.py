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
        resumo.add_argument('-o', '--saida', help='Salvar resumo em arquivo')

        relatorio = subparsers.add_parser('relatorio', help='Relatorio completo com todos os Dados Unificados')
        relatorio.add_argument('arquivo_entrada')
        relatorio.add_argument('-o', '--saidar', help='Salvar relatorio em arquivo')

        return parser

    def principal(self):
        parser = self.argumentos()
        args = parser.parse_args()

        if args.comando == "info":
            logging.info("Iniciando análise do PDF...")
            documento = extractor.Extractor(args.arquivo_entrada)
            analise = documento.saida()
            print(analise)

        elif args.comando == "imagens":
            print("Extraindo imagens...")
            documento = images.Images(args.arquivo_entrada)
            documento.principal()

        elif args.comando == "resumo":
            print("Gerando resumo...")
            extrator = extractor.Extractor(args.arquivo_entrada)
            texto = extrator.saidallm()
            summarizer = summarize.Summarize(texto)
            resumo = summarizer.gerarresumo()
            if args.saida:
                summarizer.salvarresumo(resumo, args.saida)

        elif args.comando == "relatorio":
            print("Gerando relatorio...")
            extrator = extractor.Extractor(args.arquivo_entrada)
            analise = extrator.saida()
            texto = extrator.saidallm()

            aux_imagens = images.Images(args.arquivo_entrada)
            fotos = aux_imagens.principal()

            summarizer = summarize.Summarize(texto)
            resumo = summarizer.gerarresumo()

            relatoriofinal = {
                'estatisticas': analise,
                'resumo': resumo,
                'diretorioimagens': fotos
            }

            if args.saidar:
                summarizer.salvarrelatorio(relatoriofinal, args.saidar)

            print("Relatório gerado com sucesso.")


        else:
            parser.print_help()

