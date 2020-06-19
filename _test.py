import server, time, pqsclasses, pqsutil

if __name__ == "__main__":
    ttime = time.time()
    kb = pqsclasses.KnowledgeBase()
    # kb.set_questions("data/Questions.csv", "cache/1", False)
    # print("[{:.2f}] questions loaded".format(time.time() - ttime))
    # kb.dump_questions('cache/kb_q')
    # kb.set_answers("data/Answers.csv", "cache/1", False)
    # print("[{:.2f}] answers loaded".format(time.time() - ttime))
    # kb.dump_answers('cache/kb_a')
    # print("finished. time: {:.2f} seconds.".format(time.time() - ttime))

    # print(pqsutil.get_question(19997))
    # print(pqsutil.get_question(39997))
    # print(pqsutil.get_answer(59997))

    # pqsutil.chunk_file('Questions')
    # print(time.time() - ttime)
    # pqsutil.chunk_file('Answers')

    print(time.time() - ttime)
    # kb.load('cache/kb_q','cache/kb_a')
