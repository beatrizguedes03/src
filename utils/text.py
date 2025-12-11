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
        self.texto = self.texto.lower()
        self.texto = self.texto.replace(u'\xa0', ' ')
        self.texto = unicodedata.normalize('NFKD', self.texto)
        self.texto = self.texto.encode("ascii", "ignore").decode("utf-8")
        self.texto = self.texto.replace("\n", " ").replace("\t", " ")
        self.texto = re.sub(r"[^a-z0-9 ]+", " ", self.texto)
        self.texto = re.sub(r"\s+", " ", self.texto).strip()

        return self.texto

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









