# -*- coding: utf-8 -*
# split audio file

import re
import json
import struct
#import pydub
#import ffmpeg
#from pydub import AudioSegment

file=open("result-201806251735.log","r")
csvfile=open('dec_split.csv','w')
for line in file.readlines():
    result_json=json.loads(line)
    dec_path=result_json['debug_info']['user_data']['filename']#get filename
    dec=re.search('data\/(.+)',dec_path)
    dec=dec.group(1)

    snt_list=result_json['result']['snt']
    end = []
    start = []
    text_list=[]
    score=[]
    count=0
    for i in range(len(snt_list)):
        end.append(snt_list[i]['end'])
        start.append(snt_list[i]['start'])
        text_list.append(snt_list[i]['text'].encode('utf-8'))
        score.append(snt_list[i]['score'].encode('utf-8'))
        count+=1#count sentences
        #the following is spliting and storing
        complete_dec = open('./data/'+dec,'rb')#add path
        data = complete_dec.read()
        complete_dec.close()
        start_time = start[i] * 10 * 16
        if (i<len(snt_list)-1):
            stop_time = snt_list[i+1]['start'] * 10 * 16
        else:
            stop_time = end[i] * 10 * 16 + 15 * 16

        name = re.search('(.+)\.dec', dec)
        name = name.group(1)
        pcm_name = name + '-' + str(i+1)+'.pcm'
        pcmf = open('./chap_pcm/'+pcm_name, 'wb+')
        pcmf.write(data[2*start_time:2*stop_time])#here '*2' is due to start/stop time measured with byte,while audio file sampled with two bytes
        pcmf.close()

        #写表格
        csvfile.write('{}\t{}\t{}\n'.format(pcm_name,text_list[i],score[i]))
    #print count,end,start,text_list,score

csvfile.close()
file.close()