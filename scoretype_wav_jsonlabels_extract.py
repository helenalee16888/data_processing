# -*- coding: UTF-8 -*-
# this scirpt is for extracting three columns 'scoretype wav jsonlabels'
# here more lines show how to processing datas multiple threads
import sys, os
import threading
import json
import re

reload(sys) 
sys.setdefaultencoding('utf8')

dest_path = "data/"

def threadFunc(lines):
    global mutex
    threadName = threading.currentThread().getName()
    print("start " + threadName)
    for line in lines:
        line=line.strip()
        items = line.split("\t")
        if len(items) < 4:
            continue
        try:
            rec_json=json.loads(items[2])
        except Exception as e:
            continue 
        if "word" in rec_json["result"]:
            if "fluency" in rec_json["result"]:
                scoretype="eng_snt"
            else:
                scoretype="eng_wrd"
        elif "snt" in rec_json["result"]:
            scoretype="eng_chp"
        wav=items[1]    
        if scoretype=="eng_wrd":
            wordlist=rec_json["result"]["word"]
            text=wordlist[0]["word"]
        elif scoretype=="eng_snt":
            wordlist=rec_json["result"]["word"]
            word_in_snt=[]
            for j in range(len(wordlist)):
                word_in_snt.append(wordlist[j]["word"])
            text=' '.join(word_in_snt)
        elif scoretype=="eng_chp":
            sntlist=rec_json["result"]["snt"]
            snt_in_chp=[]
            for jj in range(len(sntlist)):
                snt_in_chp.append(sntlist[jj]["text"])
            text='. '.join(snt_in_chp)
        #text=json.dumps(text,ensure_ascii=False).decode('utf8')
        if "***" in text:
            text=text.replace('***','')
        if "\n" in text:
            text=text.replace('\n','')
        if "\r" in text:
            text=text.replace('\r','')
        mutex.acquire()
        with open('scoretype_wav_jsonlabels_0723_test.csv', "a") as csvfile:
            csvfile.write('{0}\t{1}\t{2}\n'.format(scoretype,wav,text))
            # mutex is necessary when write a file
        mutex.release()
        audio_filename = wav
        audio_path = "speech@10.142.65.95:/search/speech/speech_assessment/sa-dispatch/data/dec/" + audio_filename
        cmd = "rsync -avu %s %s" % (audio_path, dest_path)  # copy audio file from audio_path to dest_path
        print(cmd)
        os.system(cmd)
    print("finish " + threadName)


def mutithread_process(zipLists):
    global totalZipFile, mutex
    # create mutex
    mutex = threading.Lock()
    # define threads
    threads = []
    # create thread object
    for x in range(0, len(zipLists)):
        threads.append(threading.Thread(target=threadFunc, args=(zipLists[x],)))
    # start all the threads
    for t in threads:
        t.start()
    # main thread wait for all the sub thread to finish
    for t in threads:
        t.join()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python pred_split.py input_file thread_num")  
        sys.exit(1)

    path = os.path.abspath(sys.argv[1])
    thread_num = int(sys.argv[2])
    file = open(path, 'r')
    print("path=%s, thread_num=%d" % (path, thread_num))
    lines = file.readlines()
    file.close()
    start_line = 0  
    line_num = len(lines) - start_line
    N = int(line_num / thread_num) + 1
    if line_num % thread_num == 0:
        N = line_num / thread_num
    zipLists = [lines[i:i + N] for i in range(start_line, len(lines), N)]
    print("N=%d, zipLists.size=%d" % (N, len(zipLists)))
    if thread_num > len(zipLists):
        thread_num = len(zipLists)
	#have problem with this part (delete output file before writing if it exist)
	'''
	pwd=os.getcwd()
	if os.path.exists('pwd/dec_chap.csv'):
		os.remove('pwd/dec_chap.csv')
	else:
		print('not exist')
	'''
    mutithread_process(zipLists)
