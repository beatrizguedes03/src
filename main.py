import cli.arguments as args
import logging


class Main:
    def __init__(self):
        aux = args.Arguments()
        aux.principal()

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    logging.getLogger("transformers").setLevel(logging.ERROR)
    logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)
    Main()