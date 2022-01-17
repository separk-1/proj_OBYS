import os
import pandas as pd
import natsort
#텍스트 파일 읽어서 dictionary 형태로 추출

###추후 수정 가능##
class_num=13
path = "/home/obayashi/Projects/proj_obayashi/runs/detect/exp4/labels/"
###
file_list = os.listdir(path)
vocab = {}
file_list_py = [file for file in file_list if file.endswith('.txt')]
file_list_py = natsort.natsorted(file_list_py)
#print(file_list_py)


for files in file_list_py:
  
  with open(path+files, "r") as result:
    lines = result.readlines()
    List = list()
    for voc in lines:
      #띄어쓰기 자율 수정
      List.append(int(voc.strip().split(' ')[0]))
    LList = [0]*class_num
    for j in List:
      LList[j]=1
    vocab[files.rstrip('.txt')] = LList
print(vocab)

#딕셔너리를 dataframe으로 변환
df = pd.DataFrame(vocab)
print(df)
df.to_csv('runs/detect/exp4/time.csv')

#for files in file_list_py:
#    with open(files, 'r') as result:
#        lines = result.readlines()
#        List = list()
#        for voc in lines:
#            #띄어쓰기 자율 수정
#            List.append(int(voc.strip().split(' ')[0]))
#        LList = [0]*class_num
#        for j in List:
#            LList[j]=1
#        vocab[files.rstrip('.txt')] = LList