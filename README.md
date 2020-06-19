# PythonProblemSolver
A Python question searcher application written in Python3 using Flask. Powered by Kaggle database [stackoverflow/pythonquestions](https://www.kaggle.com/stackoverflow/pythonquestions).

## System Prerequesties

- System & OS that could run Flask server
- At least 16 gig of RAM to generate wordbag and BM25 index.

## Init Server

Please create a `data` folder and place the above data in it. Then, start Flask engine, access [`http://[ip]:[port]/init`](http://127.0.0.1:2345/init) via web browser (or equivalent tools). Wait for cache to generate. During generating data, nothing will be shown and the browser will show as loading, and when the process is done, server will return the total run time.

After all's done, you can directly go to [`http://[ip]:[port]`](http://127.0.0.1:2345) and use the provided GUI.

It might take 10 minutes to init server at the first time, and after cache is generated, it will take less than 1 minute to load cache from disk. Each query would cost approx. 10 seconds.

## Screenshot

![Main Page](image/main.png)

