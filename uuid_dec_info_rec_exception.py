#coding=utf-8
#this scirpt is for extracting three columns 'uuid dec info rec' and collect abnormal datas 
import re
import copy

file_name = 'agent-dispatch.log'
file = open(file_name, 'r',encoding='UTF-8')

###extrac audio filenames and save in a list 'DEC_filename'
DEC_filename=[]
with open('dec_filename.txt', "r") as dec_filename:
    for line in dec_filename:
        DEC_filename=re.findall("(?<=\')[^\,].+?(?=\')", line)

def location_and_extract(regex,string):
    pattern = re.compile(regex)
    match = re.search(pattern, string)
    if match is not None:
        m=match.group(0)
    else:
        m = None
    return m

UUID_test={}#datas
UUID_exception={}#abnormal datas
for eachline in file:
    new_uuid=[]
    new_uuid = location_and_extract("(?<=uuid\[).+?(?=\])", eachline)
    if new_uuid == "00000000000000000000000000000000":
        continue
    if new_uuid not in UUID_test:
        UUID_test[new_uuid] = [None, None, None]
        for each_dec in DEC_filename:
            if new_uuid == location_and_extract("(?<=\-).+?(?=\-)", each_dec):
                if UUID_test[new_uuid][0] == None:
                    UUID_test[new_uuid][0] = each_dec
                else:                                     
                    print(new_uuid, "异常:dec大于1个")
                    if new_uuid not in UUID_exception:
                        UUID_exception[new_uuid]=[]
                        UUID_exception[new_uuid]=copy.deepcopy(UUID_test[new_uuid])
                    UUID_exception[new_uuid].append(each_dec)


    idx = location_and_extract("(?<=idx\[).+?(?=\])",eachline)
    if idx == '1':
        info_body=location_and_extract("(?<=info_body\[).+?(?=\]WebServer)",eachline)
        if UUID_test[new_uuid][1]==None:
            UUID_test[new_uuid][1] = info_body
        else:  
            print(new_uuid, "异常:idx[1]大于1个")
            if new_uuid not in UUID_exception:
                UUID_exception[new_uuid] = []
                UUID_exception[new_uuid]=copy.deepcopy(UUID_test[new_uuid])
            UUID_exception[new_uuid].append(info_body)  
    elif '-' in idx:
        rec_body = location_and_extract("(?<=rec_body\[).+?(?=\], stop_flag)", eachline)
        if UUID_test[new_uuid][2]==None:
            UUID_test[new_uuid][2] = rec_body
        else:  # 异常处理
            print(new_uuid, "异常:idx[-]大于1个")
            if new_uuid not in UUID_exception:
                UUID_exception[new_uuid] = []
                UUID_exception[new_uuid]=copy.deepcopy(UUID_test[new_uuid])
            UUID_exception[new_uuid].append(info_body)  

file.close()


#save normal datas
i=0
with open('uuid_dec_info_rec_1.csv', "w",encoding='utf-8') as csvfile:
    for k, v in UUID_test.items():
        if (None in v) and (k not in UUID_exception): # 有缺的数据也加入异常字典
                UUID_exception[k] = []
                UUID_exception[k]=copy.deepcopy(UUID_test[k])
        if (None not in v) and (k not in UUID_exception):
        #if k not in UUID_exception:
            #csvfile.write('{}\t{}\t{}\t{}\n'.format(k, v[0], v[1], v[2]))
            csvfile.write('{}\t'.format(k))
            csvfile.write('\t'.join('%s' % i for i in v) + '\n')
            i+=1
    csvfile.close()
print("正常数据个数",i)

#save abnormal datas
j=0
with open('uuid_dec_info_rec_exception.csv', "w",encoding='utf-8') as csvfile:
    for k, v in UUID_exception.items():
        #csvfile.write('{}\t{}\n'.format(k, v))
        csvfile.write('{}\t'.format(k))
        csvfile.write('\t'.join('%s' % i for i in v) + '\n')
        j+=1
    csvfile.close()
print("异常数据个数",j)
