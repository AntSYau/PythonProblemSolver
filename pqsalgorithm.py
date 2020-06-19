import math
import sys
import time
from pqsconfig import *

conf = Config()
# BM25 parameters.
try:
    PARAM_K1 = float(conf.get_value("bm25_k1"))
    PARAM_B = float(conf.get_value("bm25_b"))
    EPSILON = float(conf.get_value("bm25_epsilon"))
except ValueError:
    sys.stderr.write("no preset bm25 parameters. creating")
    PARAM_K1 = 1.5
    PARAM_B = 0.75
    EPSILON = 0.25
    conf.set_value("bm25_k1", 1.5)
    conf.set_value("bm25_b", 0.75)
    conf.set_value("bm25_epsilon", 0.25)


class BM25(object, metaclass=Singleton):  # inspired by gensim

    def __init__(self, corpus):
        ttime = time.time()
        self.corpus_size = len(corpus)
        self.avgdl = sum(map(lambda x: float(len(x)), corpus)) / self.corpus_size
        self.f = []
        self.df = {}
        self.idf = {}
        self.initialize(corpus)
        del self.df
        self.average_idf = sum(map(lambda k: float(self.idf[k]), self.idf.keys())) / len(self.idf.keys())
        print("BM25 init finished. Time cost: {:.2f}s.".format(time.time() - ttime))

    def initialize(self, corpus):
        for document in corpus:
            frequencies = {}
            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
            self.f.append(frequencies)

            for word, freq in frequencies.items():
                if word not in self.df:
                    self.df[word] = 0
                self.df[word] += 1

        for word, freq in self.df.items():
            self.idf[word] = math.log(self.corpus_size - freq + 0.5) - math.log(freq + 0.5)

    def get_score(self, document, index):
        score = 0
        for word in document:
            if word not in self.f[index]:
                continue
            idf = self.idf[word] if self.idf[word] >= 0 else EPSILON * self.average_idf
            delta = (idf * self.f[index][word] * (PARAM_K1 + 1)
                     / (self.f[index][word] + PARAM_K1 * (1 - PARAM_B + PARAM_B * self.corpus_size / self.avgdl)))
            score += delta
        return score

    def get_scores(self, document):
        print("querying from {} records".format(self.corpus_size))
        scores = [self.get_score(document, index) for index in range(self.corpus_size)]
        return scores
