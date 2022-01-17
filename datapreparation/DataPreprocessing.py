import cv2
import numpy as np
import glob
import os
import pandas as pd
import natsort

import distutils.errors
import os.path
from distutils.dir_util import copy_tree


class FrameExtraction:
    def __init__(self, ext_vidpath, save_imgpath, ext_imgpath, save_vidpath):
        self.ext_vidpath = ext_vidpath
        self.save_imgpath = save_imgpath
        self.ext_imgpath = ext_imgpath
        self.save_vidpath = save_vidpath

    def video_to_frame(self):
        vidcap = cv2.VideoCapture(self.ext_vidpath)
        count = 0
        while (vidcap.isOpened()):
            count_zero = str(count).zfill(5)
            ret, image = vidcap.read()
            # 이미지 사이즈 960x540으로 변경
            # image = cv2.resize(image, (960, 540))

            # 30프레임당 하나씩 이미지 추출
            if (int(vidcap.get(1)) % 30 == 0):
                print('Saved frame number : ' + str(int(vidcap.get(1))))
                # 추출된 이미지가 저장되는 경로
                cv2.imwrite(self.save_imgpath+"/%s.png" % count_zero, image)
                # print('Saved frame%s.png' % count)
                count += 1
            else:
              pass
        
        vidcap.release()
        return

    def frame_to_video(self):
        file_list = os.listdir(self.ext_imgpath)
        file_list_py = [file for file in file_list if file.endswith('.png')]
        file_list_py = natsort.natsorted(file_list_py)

        img_array = []
        size = (0, 0)
        # for filename in glob.glob('/home/obayashi/data/first_video/test/cut_frame/*.png'):
        
        for filename in file_list_py:
            img = cv2.imread(self.ext_imgpath + filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)
        print("creating video strart!")
        out = cv2.VideoWriter(self.save_vidpath, cv2.VideoWriter_fourcc(*'DIVX'), 10, size)

        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        return


class FormatRevision:
    def __init__(self, label_list, image_list):
        self.label_list = label_list
        self.image_list = image_list

    def file_filter(self):
        file_name = []
        for file in self.label_list:
            name = file.split('.')[0]
            name = name + ".jpg"
            file_name.append(name)

        sub_list = [x for x in self.image_list if x not in file_name]

        os.chdir("images")
        for sub_file in sub_list:
            os.remove(sub_file)
            print(sub_file + " is removed")
        return

class Foldering:
    def __init__(self, my_dir, case_name, train_dir, val_dir):
        self.my_dir = my_dir
        self.case_name = case_name
        self.train_dir = train_dir
        self.val_dir = val_dir

    def foldering(self):
        dst_train = self.my_dir+"Case/%s/train" % (self.case_name)
        dst_val = self.my_dir+"Case/%s/val" % (self.case_name)

        if os.path.exists(self.my_dir+"Case/" + self.case_name):
            print("%s 폴더가 이미 존재합니다. case_name을 변경하거나 기존 폴더(%s)를 삭제해 주세요." % (self.case_name, self.case_name))

        else:
            for i in range(len(self.train_dir)):
                try:
                    copy_tree(self.my_dir+"Dataset/%s/img/" % (self.train_dir[i]), dst_train + "/img/")
                    copy_tree(self.my_dir+"Dataset/%s/txt/" % (self.train_dir[i]), dst_train + "/txt/")
                except distutils.errors.DistutilsError:
                    print("%s의 input train list에 %s이 존재하지 않습니다. 제외하고 업로드합니다." % (self.case_name, self.train_dir[i]))

            for j in range(len(self.val_dir)):
                try:
                    copy_tree(self.my_dir+"Dataset/%s/img/" % (self.val_dir[j]), dst_val + "/img/")
                    copy_tree(self.my_dir+"Dataset/%s/txt/" % (self.val_dir[j]), dst_val + "/txt/")
                except distutils.errors.DistutilsError:
                    print("%s의 input val list에 %s이 존재하지 않습니다. 제외하고 업로드합니다." % (self.case_name, self.val_dir[i]))

            print("%s 업로드 완료" % (self.case_name))
        return