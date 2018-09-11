# -*- coding: UTF-8 -*-
#the file is for getting all the filenames after a appointed time in a appointed path
import re
import os
import time
import datetime

def location_and_extract(regex,string):
    pattern = re.compile(regex)
    match = re.search(pattern, string).group(0)
    return match

def transTime(assignTime):
    """
    @summary:change appointed time into Long
    @param assignTime:appointed time    e.g.'2016-12-3 10:30'
    @return: timeLong 
    """
    timeList = assignTime.replace(' ', '-').replace(':', '-').split('-')
    timeList = map(int, timeList)  # [2016, 12, 3, 10, 30]
    timeStr = datetime.datetime(*timeList)  # 2016-12-03 10:30:00
    timeLong = time.mktime(timeStr.timetuple())  # 1480732200.0
    return timeLong


def getChangedFiles(assignPath, assignTime):
    """
    @summary: get appointed time and get changed filenames 
    @param assignPath: appointed path
    @param assignTime: appointed time
    """
    dec_filename=[]
    for root, dirs, files in os.walk(assignPath):
        for file in files:
            f = os.path.join(root, file)
            mtime = os.path.getmtime(f)
            if os.path.splitext(f)[1] in ('.dec') and mtime > transTime(assignTime):
                #print(f, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime)))#这里输出的f是字符串格式
                filename=location_and_extract("(?<=dec/).*",f)
                dec_filename.append(filename)
    return dec_filename

if __name__ == '__main__':
    assignTime = '2018-7-22 23:05:30'  # appointed time
    currentPath = os.getcwd()  # get current path
    #assignPath = os.path.dirname(currentPath) 
    DEC_filename=getChangedFiles(currentPath, assignTime)#get filenames
    print(DEC_filename[300])
    file = open('dec_filename0821.txt','w+')
    file.write(repr(DEC_filename))
    file.close()