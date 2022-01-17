import os
#경로 수정하기
label_list= os.listdir("labels")
image_list= os.listdir("images")

file_name=[]
for file in label_list:
    name = file.split('.')[0]
    name = name +".jpg"
    file_name.append(name)

sub_list = [x for x in image_list if x not in file_name]

os.chdir("images")
for sub_file in sub_list:
    os.remove(sub_file)
    print(sub_file + " is removed")