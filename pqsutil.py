from pqsconfig import Config
from pqsalgorithm import *
import multiprocessing as mp
import csv
import json
import os, sys
import time
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import linecache

word_tokenizer = RegexpTokenizer('[A-Za-z]+')
conf = Config()
debug = False


def answers_process_row(row, i):
    id, _, _, parent, score, body = row
    bbody = body.lower()
    terms = word_tokenizer.tokenize(bbody)
    return [terms, parent, [i, id, score]]


def questions_process_row(row, i):
    id, _, _, score, title, body = row
    bbody = title.lower() + " " + body.lower()
    terms = word_tokenizer.tokenize(bbody)
    return [terms, id, [i, score]]


def create_corpus(file, output, mode, use_cache=True):
    ttime = time.time()
    corpus = []
    metadata = {}
    if use_cache and os.path.exists("{}_{}_corpus".format(output, mode)) and os.path.exists(
            "{}_{}_metadata".format(output, mode)):
        print("cache found")
        with open("{}_{}_corpus".format(output, mode), "r") as f:
            corpus = json.loads(f.read())
        with open("{}_{}_metadata".format(output, mode), "r") as f:
            metadata = json.loads(f.read())
        print("[{}] finished".format(time.time() - ttime))
        return corpus, metadata
    f = open(file, 'r', errors='ignore')
    reader = csv.reader(f)
    i = 0
    pool = mp.Pool(4)
    ps = []
    for row in reader:
        if i == 0:
            i += 1
            continue
        if mode == 'answers':
            x = pool.apply_async(answers_process_row, args=(row, i,))
        else:
            x = pool.apply_async(questions_process_row, args=(row, i,))
        ps.append(x)
        i += 1
        if debug:
            if i > 20000:
                break
    pool.close()
    pool.join()
    f.close()
    for i, pp in enumerate(ps):
        td, parent, value = pp.get()
        assert i + 1 == value[0]
        corpus.append(td)
        if parent not in metadata.keys():
            metadata[parent] = []
        metadata[parent].append(value)
    if use_cache:
        print("[{}] writing...".format(time.time() - ttime))
        with open("{}_{}_corpus".format(output, mode), "w") as f:
            f.write(json.dumps(corpus))
        with open("{}_{}_metadata".format(output, mode), "w") as f:
            f.write(json.dumps(metadata))
    print("done reading {}. time cost: {:.2f}".format(mode, time.time() - ttime))
    return corpus, metadata


def query(q: list, bm25: BM25):
    scores = bm25.get_scores(q)
    return scores


def get(line: int, string: str):
    line += 1
    file = math.floor(line / 20000)
    ret = []
    with open('data/{}/{}{:03d}.csv'.format(string, string, file), 'r', errors='ignore') as f:
        ff = csv.reader(f)
        line = line % 20000
        for i, x in enumerate(ff):
            if i == line:
                ret = x
                break
    return ret


def get_question(line):
    return get(line, 'Questions')


def get_answer(line):
    return get(line, 'Answers')


def chunk_file(string):
    if not os.path.exists(f'data/{string}'):
        os.makedirs(f'data/{string}')
    with open('data/{}.csv'.format(string), 'r', errors='ignore') as f:
        ff = csv.reader(f)
        cnt = 0
        r = open('data/{}/{}{:03d}.csv'.format(string, string, cnt), 'w', errors='ignore')
        fr = csv.writer(r)
        for i, x in enumerate(ff):
            fr.writerow(x)
            if i % 20000 == 19999:
                r.close()
                cnt += 1
                r = open('data/{}/{}{:03d}.csv'.format(string, string, cnt), 'w', errors='ignore')
                fr = csv.writer(r)
        del ff, fr
        r.close()
