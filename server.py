from flask import Flask, request, render_template
from pqsclasses import *
from pqsconfig import *
from urllib.parse import quote, unquote
from pqsalgorithm import *
from pqsutil import *
import heapq

app = Flask(__name__, template_folder="web")
config = Config()
kb = KnowledgeBase()


@app.route("/view/question/<id>", methods=['GET'])
def load_question(id=0):
    if not kb.ready:
        return "not ready!"
    id = int(id)
    app.logger.debug(id)
    return get_question(id)


@app.route("/view/answer/<id>", methods=['GET'])
def load_answer(id=0):
    if not kb.ready:
        return "not ready!"
    id = int(id)
    app.logger.debug(id)
    return get_answer(id)


@app.route("/", methods=['GET', 'POST'])
def query():
    if not kb.ready:
        print(load())
    ttime = time.time()
    if request.method == 'POST':
        key = request.form['query']
    else:
        return render_template("index.html")
    dkey = unquote(key).strip().lower().split(" ")
    qscores = pqsutil.query(dkey, kb.qbm25)
    ascores = pqsutil.query(dkey, kb.abm25)
    qresult = heapq.nlargest(100, range(len(qscores)), qscores.__getitem__)
    aresult = heapq.nlargest(3, range(len(ascores)), ascores.__getitem__)
    print("{:.2f} done query, reading from data...".format(time.time() - ttime))
    tabs = [{"href": "directans", "name": "Directly Related Answers"}]
    contents = [{"href": "directans", "tabs": [], "item": []}]
    for a in aresult:
        contents[0]["tabs"].append({"href": "da{}".format(a), "name": "Answer #{}".format(a)})
        contents[0]["item"].append({"href": "da{}".format(a), "text": get_answer(a)[5]})
    cnt = 0
    for q in qresult:
        text = get_question(q)
        qid = text[0]
        if qid not in kb.ameta.keys():
            continue
        cnt += 1
        if cnt == 4:
            break
        tabs.append({"href": "q{}".format(q), "name": "Question #{}".format(q)})
        content = {"href": "q{}".format(q), "tabs": [], "item": []}
        content["tabs"].append({"href": "qt{}".format(q), "name": "Question Text"})
        text = "<h3>{}</h3>{}".format(text[4], text[5])
        content["item"].append({"href": "qt{}".format(q), "text": text})
        x = [ansmeta[0] for ansmeta in sorted(kb.ameta[qid], key=lambda x: x[2])]
        if len(x) > 3:
            x = x[:3]
        for xx in x:
            content["tabs"].append({"href": "a{}".format(xx), "name": "Answer #{}".format(xx)})
            content["item"].append({"href": "a{}".format(xx), "text": get_answer(xx)[5]})
        contents.append(content)
    return render_template("index.html", tabs=tabs, contents=contents, lbl=key,
                           ttime="{:.2f}".format(time.time() - ttime))


@app.route("/init", methods=['GET'])
def init():
    ttime = time.time()
    kb.set_questions("data/Questions.csv", "cache/1", False)
    print("[{:.2f}] questions loaded".format(time.time() - ttime))
    kb.dump_questions('cache/kb_q')
    kb.set_answers("data/Answers.csv", "cache/1", False)
    print("[{:.2f}] answers loaded".format(time.time() - ttime))
    kb.dump_answers('cache/kb_a')
    
    return "finished. time: {:.2f} seconds.".format(time.time() - ttime)


@app.route("/load", methods=['GET'])
def load():
    ttime = time.time()
    kb.load('cache/kb_q', 'cache/kb_a')
    return "finished. time: {:.2f} seconds.".format(time.time() - ttime)


if __name__ == '__main__':
    app.run(port=2345, debug=True)
