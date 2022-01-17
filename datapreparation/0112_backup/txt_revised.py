import os
import re
import natsort

#경로 수정하기

file_list = os.listdir('/home/obayashi/data/cctv_video/test_data/orginal/labels/2021-08-27_12-00-00/')
os.chdir('/home/obayashi/data/cctv_video/test_data/orginal/labels/2021-08-27_12-00-00/')
file_list = natsort.natsorted(file_list)

for file in file_list:
    open_file = open(file, 'r')
    read_file = open_file.read()
    regex = re.compile(',')
    read_file = regex.sub('   ', read_file)

    write_file = open(file, 'w')
    write_file.write(read_file)

    print(file + " is revised")
    
    
    '''
    original 0, 0.3, 0,2, 0.4, 0.3
    changed 0  0.3  0.2  0.4  0.3