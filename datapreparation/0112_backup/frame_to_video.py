import cv2
import numpy as np
import glob
import os
import pandas as pd
import natsort

path = "/home/obayashi/data/cctv_video/test_data/cycle6/"

file_list = os.listdir(path)
file_list_py = [file for file in file_list if file.endswith('.jpg')]
file_list_py = natsort.natsorted(file_list_py)

img_array = []
#for filename in glob.glob('/home/obayashi/data/first_video/test/cut_frame/*.png'):

for filename in file_list_py:
    img = cv2.imread(path + filename)
    height, width, layers = img.shape
    size = (width, height)
    img_array.append(img)
print("creating video strart!")
out = cv2.VideoWriter('/home/obayashi/data/cctv_video/test_data/cycle6.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 10, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()