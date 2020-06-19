from pqsalgorithm import *
import pickle
import pqsutil


class KnowledgeBase(metaclass=Singleton):
    def __init__(self):
        print("init kb")
        self.qmeta = {}
        self.qbm25 = None
        self.ameta = {}
        self.abm25 = None
        self.__r1 = False
        self.__r2 = False
        self.ready = False

    def set_questions(self, questions_location, cache_location, use_cache):
        questions, self.qmeta = pqsutil.create_corpus(questions_location, cache_location, "questions",
                                                                      use_cache)
        self.qbm25 = BM25(questions)
        self.__r1 = True
        self.ready = self.__r1 and self.__r2
        del questions

    def set_answers(self, answers_location, cache_location, use_cache):
        answers, self.ameta = pqsutil.create_corpus(answers_location, cache_location, "answers",
                                                                  use_cache)
        self.abm25 = BM25(answers)
        self.__r2 = True
        self.ready = self.__r1 and self.__r2
        del answers

    def dump_questions(self, file, remove=True):
        fw = open(file, 'wb')
        pickle.dump([self.qmeta, self.qbm25], fw)
        if remove:
            del self.qmeta
            del self.qbm25
            self.__r2=False
            self.ready=False

    def dump_answers(self, file, remove=True):
        fw = open(file, 'wb')
        pickle.dump([self.ameta, self.abm25], fw)
        if remove:
            del self.ameta
            del self.abm25
            self.__r1=False
            self.ready=False


    def load(self, qfile, afile):
        with open(qfile, 'rb') as qr:
            self.qmeta, self.qbm25 = pickle.load(qr)
        with open(afile, 'rb') as ar:
            self.ameta, self.abm25 = pickle.load(ar)
        self.ready = True
