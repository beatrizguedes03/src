import re
import unicodedata
from collections import Counter
import nltk
from nltk.corpus import stopwords

class Text:
    def __init__(self, texto):
        self.texto = texto

    def limpartexto(self):
        self.texto = self.texto.lower()
        self.texto = self.texto.replace(u'\xa0', ' ')
        self.texto = unicodedata.normalize('NFKD', self.texto)
        self.texto = self.texto.encode("ascii", "ignore").decode("utf-8")
        self.texto = self.texto.replace("\n", " ").replace("\t", " ")
        self.texto = re.sub(r"[^a-z0-9 ]+", " ", self.texto)
        self.texto = re.sub(r"\s+", " ", self.texto).strip()

        return self.texto

    def removerstopwords(self, texto):
        nltk.download('stopwords', quiet=True)
        stop = set(stopwords.words('portuguese'))

        if isinstance(texto, str):
            texto = texto.split()

        return [palavra for palavra in texto if palavra not in stop]

    def vocabulariounico(self, texto):
        return len(set(texto))

    def maisfrequentes(self, texto):
        contagem = Counter(texto)
        top10 = contagem.most_common(10)

        # só as palavras
        palavras = [palavra for palavra, frequencia in top10]

        return palavras









