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

    @classmethod
    def video_to_frame(ext_vidpath, save_imgpath):
        vidcap = cv2.VideoCapture(ext_vidpath)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        fps_int = round(fps)
        print("fps: %s" % (fps))
        count = 0
        while (vidcap.isOpened()):
            fps = vidcap.get(cv2.CAP_PROP_FPS)
            count_zero = str(count).zfill(5)
            ret, image = vidcap.read()
            if count == math.floor(vidcap.get(cv2.CAP_PROP_FRAME_COUNT) / fps_int):
                break
            else:
                if (int(vidcap.get(1)) % fps_int == 0):
                    print('Saved frame number : ' + str(int(vidcap.get(1))))
                    cv2.imwrite(save_imgpath + "/%s.png" % count_zero, image)
                    # print('Saved frame%s.png' % count)
                    count += 1
                else:
                    pass

        vidcap.release()
        return
        
    @classmethod
    def frame_to_video(ext_imgpath, save_vidpath, fps=10):

        file_list = os.listdir(ext_imgpath)
        file_list_py = [file for file in file_list if file.endswith('.png')]
        file_list_py = natsort.natsorted(file_list_py)

        img_array = []
        size = (0, 0)

        for filename in file_list_py:
            img = cv2.imread(self.ext_imgpath + filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)
        print("creating video strart!")
        out = cv2.VideoWriter(save_vidpath, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

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
        dst_train = self.my_dir + "case_data/%s/train" % (self.case_name)
        dst_val = self.my_dir + "case_data/%s/val" % (self.case_name)

        if os.path.exists(self.my_dir + "0.raw_data/" + self.case_name):
            print("%s folder already exists. Change case_name or delete existing folder(%s)." % (self.case_name, self.case_name))

        else:
            for i in range(len(self.train_dir)):
                try:
                    copy_tree(self.my_dir + "raw_data/%s/images/" % (self.train_dir[i]), dst_train + "/images/")
                    copy_tree(self.my_dir + "raw_data/%s/labels/" % (self.train_dir[i]), dst_train + "/labels/")
                except distutils.errors.DistutilsError:
                    print("%s does not exist in %s input train list. Exclude and upload.." % (self.train_dir[i]), self.case_name)

            for j in range(len(self.val_dir)):
                try:
                    copy_tree(self.my_dir + "raw_data/%s/images/" % (self.val_dir[j]), dst_val + "/images/")
                    copy_tree(self.my_dir + "raw_data/%s/labels/" % (self.val_dir[j]), dst_val + "/labels/")
                except distutils.errors.DistutilsError:
                    print("%s does not exist in %s input validation list. Exclude and upload.." % (self.val_dir[i]), self.case_name)

            data = {
                'train': "/content/proj_OBYS/dataset/case_data/%s/train" % (self.case_name),
                'val': "/content/proj_OBYS/dataset/case_data/%s/val" % (self.case_name),
                'nc': 11,
                'names': "[\"drill_jumbo\", \"gunpowder_carrier\", \"work platform\", \"breaker\", \"excavator\", \"payloader\", \"dump_truck\", \"sprayer\", \"h_beam_holder\", \"mixer_truck\", \"mortar_trolley_truck\"]"
        }
            file = open("%scase_data/%s/%s.yaml" % (self.my_dir, self.case_name, self.case_name), "w")
            yaml.dump(data, file, default_flow_style=None )
            file.close()

            print("**%s uploaded**" % (self.case_name))
        return


class Foldering_Random:
    def __init__(self, my_dir, case_name, threshold):
        self.my_dir = my_dir
        self.case_name = case_name
        self.threshold = threshold

        self.filepath = my_dir + "%s/train/labels/*.txt" % (case_name)
        self.file_list = glob.glob(self.filepath)

        Foldering_Random.make_merge_txt(self)

    # create dataframe
    def origin_df(self):
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
        data = pd.read_csv(self.my_dir + "%s.txt" % (self.case_name), sep="   ", engine='python', encoding="cp949",
                           names=colnames)
        data["filename"] = counted_filename_list

        label_count = list()
        for filename in data["filename"]:
            label_count.append(len(Foldering_Random.label_dict(filename)))
        data["labelcount"] = label_count
        return data

    def Random_df(self):
        global dict
        origin_df = Foldering_Random.origin_df(self)

        cls_list = list(range(11))
        count_list = [0 for i in range(11)]
        dict_count = dict(zip(cls_list, count_list))

        filename_list = list()

        tryNum = 0

        while tryNum < (self.threshold/10):
            tryNum += 1
            for cls in range(0, 11):
                storage = self.threshold - dict_count[cls]

                if storage < 0:
                    pass

                else:
                    con = (origin_df.label == cls)
                    if len(origin_df[con]) <= storage:
                        df_0 = origin_df[con].sample(int(len(origin_df[con])))

                    else:
                        df_0 = origin_df[con].sample(int(storage / (self.threshold/10)))

                    filename_list.extend(df_0["filename"])

        df_Random = Foldering_Random.filter_df_by_filenamelist(origin_df, filename_list)

        filename_list = list(set(list(df_Random["filename"])))
        os.mkdir(self.my_dir + "labels/")
        for i in range(len(filename_list)):
            src = filename_list[i]
            dst = self.my_dir + "labels/"
            shutil.copy(src, dst)

        return df_Random

    # create yaml file
    def create_yaml(self):
        data = {
            'train': "/content/proj_OBYS%s%s_%s/train" % (self.my_dir, self.case_name, self.threshold),
            'val': "/content/proj_OBYS%s%s/val" % (self.my_dir, self.case_name),
            'nc': 11,
            'names': "[\"drill_jumbo\", \"gunpowder_carrier\", \"work platform\", \"breaker\", \"excavator\", \"payloader\", \"dump_truck\", \"sprayer\", \"h_beam_holder\", \"mixer_truck\", \"mortar_trolley_truck\"]"
        }
        file = open("%s%s_%s/%s_%s.yaml" % (self.my_dir, self.case_name, self.threshold, self.case_name, self.threshold), "w")
        yaml.dump(data, file,  default_flow_style=None)
        file.close()
        return

        # create merge txt
    def make_merge_txt(self):
        txt = self.my_dir + "%s.txt" % (self.case_name)
        with open(txt, 'w') as outfile:
            for filename in sorted(self.file_list):
                with open(filename) as file:
                    outfile.write(file.read())
        return

    # directory setting
    def Set_Dir(self):
        os.makedirs(self.my_dir + "%s_%s/train/images" % (self.case_name, self.threshold))
        file_name = []
        file_list = os.listdir(self.my_dir + "labels")
        for file in file_list:
            if file.count(".") == 1:
                name = file.split('.')[0]
                file_name.append(name)
            else:
                for k in range(len(file) - 1, 0, -1):
                    if file[k] == '.':
                        file_name.append(file[:k])
                        break

        dst = self.my_dir + "%s_%s/train/images/" % (self.case_name, self.threshold)
        for file in file_name:
            src = self.my_dir + "%s/train/images/" % (self.case_name) + file + ".jpg"
            shutil.copy(src, dst)

        shutil.move(self.my_dir + "labels", self.my_dir + "%s_%s/train" % (self.case_name, self.threshold))
        # shutil.move(self.my_dir+"%s/val"%(self.case_name), self.my_dir + "%s_%s/"%(self.case_name, self.threshold))
        return

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

    # save histogram by dataframe
    @classmethod
    def save_plot(cls, df, threshold, figpath):
        label_list = list(range(11))
        count_list = list()
        for i in label_list:
            count_list.append(list(df['label']).count(i))
        plot_df = pd.DataFrame({'label': label_list, 'count': count_list})
        plot_df.plot.bar(x='label', y='count', rot=0)
        plt.axhline(y=threshold, color='r', linewidth=1)
        plt.savefig(figpath)
        return

    @classmethod
    # filename class count
    def count_cls_by_filenamelist(cls, origin_df, filename_list):
        label_list = list()
        for filename in filename_list:
            label_list.extend(origin_df[origin_df.filename == filename]["label"])
        return label_list

    @classmethod
    def get_count_dict(cls, label_list):
        cls_list = list(range(11))
        count_list = list()
        for i in cls_list:
            count_list.append(label_list.count(i))
        dict_count = dict(zip(cls_list, count_list))
        return dict_count

    @classmethod
    # filename_df
    def filter_df_by_filenamelist(cls, origin_df, filename_list):
        index_list = list()
        for i in origin_df.index:
            if origin_df.at[i, "filename"] in filename_list:
                index_list.append(i)
            else:
                pass
        return origin_df.loc[index_list]
