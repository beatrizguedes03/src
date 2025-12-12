import re
import unicodedata
from collections import Counter
import nltk
from nltk.corpus import stopwords

class Text:
    def __init__(self, texto):
        self.texto = texto
        self.textolimpo = self.limpartexto()
        self.textosemstops = self.removerstopwords()

    def limpartexto(self):
        limpando = self.texto.lower()

        limpando = limpando.replace(u'\xa0', ' ')

        limpando = re.sub(r"\\[a-zA-Z]+{.*?}", "", limpando)
        limpando = re.sub(r"\\[a-zA-Z]+\b", "", limpando)

        limpando = unicodedata.normalize('NFKD', limpando)
        limpando = limpando.encode("ascii", "ignore").decode("utf-8")

        limpando = limpando.replace("-\n", "")
        limpando = re.sub(r"[\n\t]+", " ", limpando)

        limpando = re.sub(r"[^a-z0-9 ]+", " ", limpando)
        limpando = re.sub(r"\s+", " ", limpando).strip()

        textolimpo = re.findall(r"\b\w+\b", limpando)
        textolimpo = [p for p in textolimpo if len(p) > 1]

        return textolimpo

    def removerstopwords(self):
        nltk.download('stopwords', quiet=True)
        stop = set(stopwords.words('portuguese'))

        if isinstance(self.textolimpo, str):
            self.textolimpo = self.textolimpo.split()

        return [palavra for palavra in self.textolimpo if palavra not in stop]

    def vocabulariounico(self):
        return len(set(self.textosemstops))

    def maisfrequentes(self):
        contagem = Counter(self.textosemstops)
        top10 = contagem.most_common(10)

        palavras = [palavra for palavra, frequencia in top10]

        return palavras









