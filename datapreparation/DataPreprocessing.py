import cv2
import re
import math
import natsort

import distutils.errors
import os.path
from distutils.dir_util import copy_tree
import yaml

import glob
import pandas as pd
import collections
from random import *
import shutil
import matplotlib.pyplot as plt
import os


class FrameExtraction:
    def __init__(self, ext_vidpath, save_imgpath, ext_imgpath, save_vidpath):
        self.ext_vidpath = ext_vidpath
        self.save_imgpath = save_imgpath
        self.ext_imgpath = ext_imgpath
        self.save_vidpath = save_vidpath

    def video_to_frame(self):
        vidcap = cv2.VideoCapture(self.ext_vidpath)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        fps_int = round(fps)
        print("fps: %s" % (fps))
        count = 0
        while (vidcap.isOpened()):
            fps = vidcap.get(cv2.CAP_PROP_FPS)
            count_zero = str(count).zfill(5)
            ret, image = vidcap.read()
            # 이미지 사이즈 960x540으로 변경
            # image = cv2.resize(image, (960, 540))
            if count == math.floor(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)/fps_int):
                break
            else:
                if (int(vidcap.get(1)) % fps_int == 0):
                    print('Saved frame number : ' + str(int(vidcap.get(1))))
                    # 추출된 이미지가 저장되는 경로
                    cv2.imwrite(self.save_imgpath + "/%s.png" % count_zero, image)
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

    @classmethod
    def txt_revised(cls, file_list):
        file_list = natsort.natsorted(file_list)
        for file in file_list:
            open_file = open(file, 'r')
            read_file = open_file.read()
            regex = re.compile(',')
            read_file = regex.sub('   ', read_file)

            write_file = open(file, 'w')
            write_file.write(read_file)

            print(file + " is revised")
        return

class Foldering:
    def __init__(self, my_dir, case_name, train_dir, val_dir):
        self.my_dir = my_dir
        self.case_name = case_name
        self.train_dir = train_dir
        self.val_dir = val_dir

    def foldering(self):
        dst_train = self.my_dir + "Case/%s/train" % (self.case_name)
        dst_val = self.my_dir + "Case/%s/val" % (self.case_name)

        if os.path.exists(self.my_dir + "Case/" + self.case_name):
            print("%s 폴더가 이미 존재합니다. case_name을 변경하거나 기존 폴더(%s)를 삭제해 주세요." % (self.case_name, self.case_name))

        else:
            for i in range(len(self.train_dir)):
                try:
                    copy_tree(self.my_dir + "Dataset/%s/img/" % (self.train_dir[i]), dst_train + "/img/")
                    copy_tree(self.my_dir + "Dataset/%s/txt/" % (self.train_dir[i]), dst_train + "/txt/")
                except distutils.errors.DistutilsError:
                    print("%s의 input train list에 %s이 존재하지 않습니다. 제외하고 업로드합니다." % (self.case_name, self.train_dir[i]))

            for j in range(len(self.val_dir)):
                try:
                    copy_tree(self.my_dir + "Dataset/%s/img/" % (self.val_dir[j]), dst_val + "/img/")
                    copy_tree(self.my_dir + "Dataset/%s/txt/" % (self.val_dir[j]), dst_val + "/txt/")
                except distutils.errors.DistutilsError:
                    print("%s의 input val list에 %s이 존재하지 않습니다. 제외하고 업로드합니다." % (self.case_name, self.val_dir[i]))

            data = {
                'train': "%sCase/%s/train" % (self.my_dir, self.case_name),
                'val': "%sCase/%s/train" % (self.my_dir, self.case_name),
                'nc': 11,
                'names': "[\"drill_jumbo\", \"gunpowder_carrier\", \"work platform\", \"breaker\", \"excavator\", \"payloader\", \"dump_truck\","
                         "\"sprayer\", \"h_beam_holder\", \"mixer_truck\", \"mortar_trolley_truck\"]"
            }
            file = open("%sCase/%s/%s.yaml" % (self.my_dir, self.case_name, self.case_name), "w")
            yaml.dump(data, file)
            file.close()

            print("%s 업로드 완료" % (self.case_name))
        return

class Foldering_Random:
    def __init__(self, case_name, threshold, txt_path):
        self.case_name = case_name
        self.threshold = threshold
        self.txt_path = txt_path

        self.filepath = "./Case/%s/train/labels/*.txt"%(case_name)
        self.file_list = glob.glob(self.filepath)

        Foldering_Random.make_merge_txt(self)
        self.df = Foldering_Random.origin_df(self)

    # create dataframe
    def origin_df(self):
        Foldering_Random.make_merge_txt(self)
        filename_list = list()
        labelcount_list = list()
        for filename in sorted(self.file_list):
            with open(filename) as file:
                filename_list.append(filename)
                labelcount_list.append(len(file.readlines()))

        counted_filename_list = list()
        for i in range(len(labelcount_list)):
            for j in range(labelcount_list[i]):
                counted_filename_list.append(filename_list[i])

        colnames = ['label', 'x_center', 'y_center', 'width', 'height']
        data = pd.read_csv(self.txt_path, sep="   ", engine='python', encoding="cp949", names=colnames)
        data["filename"] = counted_filename_list

        label_count = list()
        for filename in data["filename"]:
            label_count.append(len(Foldering_Random.label_dict(filename)))
        data["labelcount"] = label_count
        return data

    # case folder, threshold를 받아 새로운 folder생성
    def Random_df(self):
        global dict

        new_case_name = self.case_name + "_" + str(self.threshold)

        cls_list = list(range(11))
        zero_list = [0 for i in range(11)]
        dict_count = dict(zip(cls_list, zero_list))

        other_list = list()
        df_Random = pd.DataFrame()
        for cls in range(0, 11):
            if dict_count[cls] >= self.threshold:
                pass

            else:
                con = (self.df.label == cls)
                if len(self.df[con]) >= self.threshold:
                    df_0 = self.df[con].sample(self.threshold)
                    for k in range(self.threshold):
                        other_list.append(cls)
                else:
                    df_0 = self.df[con].sample(len(self.df[con]))
                    for k in range(len(self.df[con])):
                        other_list.append(cls)

                labelcount_list = list()
                for i in df_0.index:
                    labelcount_list.append(
                        len(self.df[self.df.filename == self.df.at[i, "filename"]]))
                df_0["labelcount"] = labelcount_list
                df_Random = df_Random.append(df_0)

                con2 = (df_0.labelcount > 1)
                df_0_2 = df_0[con2]

                for i in df_0_2.index:
                    filename = df_0_2.at[i, "filename"]
                    con3 = (self.df.filename == filename) & (self.df.label != cls)

                    df_other = self.df[con3]
                    for j in df_other.index:
                        cls_0 = df_other.at[j, "label"]
                        if dict_count[cls_0] >= self.threshold:
                            pass
                        else:
                            if len(df_other[con]) == 0:
                                pass
                            elif random() < (self.threshold - dict_count[cls_0]) / len(
                                    df_other[con]):
                                other_list.append(df_other.at[j, "label"])
                                df_Random = df_Random.append(df_other.loc[[j]])

            dict_count = collections.Counter(other_list)

        filename_list = list(set(list(df_Random["filename"])))
        os.mkdir("./%s/" % (new_case_name))
        for i in range(len(filename_list)):
            src = filename_list[i]
            dst = "./%s/"%(new_case_name)
            shutil.copy(src, dst)

        return df_Random

    # save histogram by dataframe
    def save_plot(self, df, figpath):
        label_list = list(range(11))
        count_list = list()
        for i in label_list:
            count_list.append(list(df['label']).count(i))
        plot_df = pd.DataFrame({'label': label_list, 'count': count_list})
        plot_df.plot.bar(x='label', y='count', rot=0)
        plt.axhline(y=self.threshold, color='r', linewidth=1)
        plt.savefig(figpath)
        return

    # create merge txt
    def make_merge_txt(self):
        with open(self.txt_path, 'w') as outfile:
            for filename in sorted(self.file_list):
                with open(filename) as file:
                    outfile.write(file.read())
        return

    # filename에 해당하는 label list
    @classmethod
    def label_dict(cls, filename):
        f = open(filename, 'r')
        label_list = list()
        while True:
            line = f.readline()
            if not line: break
            label_list.append(line.split("   ")[0])
        f.close()
        return label_list