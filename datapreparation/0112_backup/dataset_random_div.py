import os
import numpy as np
from sklearn.model_selection import train_test_split
import shutil

#경로 수정하기
label_path = "E:/obayashi/test_0908/labels/"
image_path = "E:/obayashi/test_0908/images/"

label_list = os.listdir(label_path)
image_list = os.listdir(image_path)
#경로 수정하기
train_label_path = 'E:/obayashi/test_0908/train/labels/'
val_label_path = 'E:/obayashi/test_0908/val/labels/'
train_image_path = 'E:/obayashi/test_0908/train/images/'
val_image_path = 'E:/obayashi/test_0908/val/images/'

label_list_np = np.array(label_list)
#랜덤 비율 수정 가능 현재는 8:2
train_label, val_label = train_test_split(label_list_np, test_size=0.2)
train_image = []
val_image= []

for k in train_label:
    name = k.split('.')[0]
    name = name +".jpg"
    train_image.append(name)
for l in val_label:
    name = l.split('.')[0]
    name = name +".jpg"
    val_image.append(name)
print(train_image)
print(val_image)

for i in train_label:
    shutil.move(label_path + i, train_label_path + i)
    print("1success")

for j in val_label:
    shutil.move(label_path + j, val_label_path + j)
    print("2success")

for i in train_image:
    shutil.move(image_path + i, train_image_path + i)
    print("3success")

for j in val_image:
    shutil.move(image_path + j, val_image_path + j)
    print("4success")