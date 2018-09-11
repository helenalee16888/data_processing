#  encoding=utf8
#make string 'l0' or 'l1' Exist only in each line
#e.g.   make line'T1_F7_2_00001.wav	I'll be back(l0) in half(l1) an(l1) hour.' to lines:
#'T1_F7_2_00001.wav	I'll be back(l0) in half an hour.'
#'T1_F7_2_00001.wav	I'll be back in half(l1) an hour.'
#'T1_F7_2_00001.wav	I'll be back in half an(l1) hour.'
#string 'l0' or 'l1' here is actually Label
import pandas as pd
import numpy as np
import re
import copy

def location_and_extract(regex,string):
    pattern = re.compile(regex)
    match = re.search(pattern, string)
    if match is not None:
        m=match.group(0)
    else:
        m = None
    return m


origin=pd.read_csv("native_gridtext_all.csv",delimiter="\t",header=None,encoding="utf-8")
print(len(origin)) 


l0=[]
l1=[]
new = pd.DataFrame()
for i in range(len(origin)):
    if origin.iat[i,0] is np.nan :
        continue
    count_l0 = origin.iat[i, 1].count('l0') 
    count_l1 = origin.iat[i, 1].count('l1')  
    if (count_l0 + count_l1) == 0:  #if sum of l0 and l1 is 0 then delete this line 
        continue
    else:
        l0.append(count_l0)
        l1.append(count_l1)
        origin.iat[i, 0] = location_and_extract("(?<=audio\/).*", origin.iat[i, 0]) 
        origin.iat[i, 1] = re.sub('\(b0\)|\(b1\)|\(b2\)|\(l2\)', '',origin.iat[i, 1])  # delete other labels except l0 l1


        m = re.finditer('\(l0\)', origin.iat[i, 1])
        n = re.finditer('\(l1\)', origin.iat[i, 1])
        index_list = []
        for o in m:  # iterator failed after used once???
            index_list.append(list(o.span())[0])
        for p in n:
            index_list.append(list(p.span())[0])
        index_list = sorted(index_list)  # this step is easy for later 'insert'
        #print(index_list)

        m = re.finditer('\(l0\)', origin.iat[i, 1])
        n = re.finditer('\(l1\)', origin.iat[i, 1])
        #print(origin.iat[i, 1])
        temp = re.sub('\(l0\)|\(l1\)', '', origin.iat[i, 1])  # delete all the l0 l1 before inserting

        for q in m:
            s_list = list(temp)
            index = list(q.span())[0]
            s_list.insert(index - (4 * index_list.index(index)), q.group(0))
            s = ''.join(s_list)
            origin.iat[i, 1] = s
            new = new.append(origin.ix[i], ignore_index=True)
            #print(origin.ix[i])
        for r in n:
            s_list = list(temp)
            index = list(r.span())[0]
            s_list.insert(index - (4 * index_list.index(index)), r.group(0))
            s = ''.join(s_list)
            origin.iat[i, 1] = s
            new = new.append(origin.ix[i], ignore_index=True)
            #print(origin.ix[i])


print(sum(l0))
print(sum(l1))
print(len(new),len(l0),len(l1)) 

new.to_csv ("native_liaison_l0l1.csv", sep='\t',index=False,header=None,encoding="utf-8")
