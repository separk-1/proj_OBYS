import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import glob

class Augmentation:
    def __init__(self, input_path, output_path, n):
        self.ImageFiles = sorted(glob.glob(input_path + "/images/*.*"))
        self.LabelFiles = sorted(glob.glob(input_path + "/labels/*.*"))
        self.x_size = round(1280/n)
        self.y_size = round(780/n)
        self.input_path = input_path
        self.output_path = output_path
        self.n = n

    def Run(self):
        for count in range(1, int(len(self.ImageFiles)/(self.n*self.n))+2):
            imgfiles = self.ImageFiles[(count - 1) * (self.n * self.n):count * (self.n * self.n)]
            resized_x_size, resized_y_size = self.ResizeImages(imgfiles)
            new_image = self.ImageMerge(imgfiles, resized_x_size, resized_y_size)
            new_image.save(self.output_path + "/images/merge_%s.png" % (count), "PNG")
            new_image.close()
            labelfiles = self.LabelFiles[(count - 1) * (self.n * self.n):count * (self.n * self.n)]
            self.LabelMerge(labelfiles, resized_x_size, resized_y_size, count)
        return

    def ResizeImages(self, files):
        resized_x_size_list = []
        resized_y_size_list = []
        for file in files:
            image = Image.open(file)
            if image.size[1] / image.size[0] >= 780 / 1280:
                resized_x_size = round(self.y_size * image.size[0] / image.size[1])
                resized_y_size = self.y_size
            else:
                resized_x_size = self.x_size
                resized_y_size = round(self.x_size / image.size[0] * image.size[1])

            resized_x_size_list.append(resized_x_size)
            resized_y_size_list.append(resized_y_size)
        return resized_x_size_list, resized_y_size_list

    def ImageMerge(self, files, resized_x_size, resized_y_size):
        row = 0
        new_image = Image.new("RGB", (1280, 780), (256, 256, 256))
        for index in range(len(files)):
            if (index%self.n==0) & (index%(self.n*self.n)!=0):
                row+=1
            white_image = Image.new("RGB", (self.x_size, self.y_size), (256, 256, 256))
            image = Image.open(files[index])
            white_image.paste(image.resize((resized_x_size[index], resized_y_size[index])), (0, 0))
            new_image.paste(white_image, ((index%self.n)*self.x_size, row*self.y_size))
        return new_image

    def LabelMerge(self, files, resized_x_size, resized_y_size, count):
        row = 0
        new_text_content = ''
        for index in range(len(files)):
            if (index%self.n==0) & (index%(self.n*self.n)!=0):
                row+=1
            with open(files[index], 'r') as f:
                lines = f.readlines()
                for line in lines:
                    ann = line.split()
                    x = str(((float(ann[1])*resized_x_size[index]/self.x_size) +index%self.n)/self.n)
                    y = str(((float(ann[2])*resized_y_size[index]/self.y_size) + row)/self.n)
                    w = str(((float(ann[3])*resized_x_size[index])/self.x_size)/self.n)
                    h = str(((float(ann[4])*resized_y_size[index])/self.y_size)/self.n)
                    new_string = ann[0]+"   "+x+"   "+y+"   "+w+"   "+h
                    new_text_content += new_string+'\n'
                f.close()

        with open(self.output_path+'/labels/merge_%s.txt'%(count), 'w') as f:
            f.write(new_text_content)
            f.close()
        return

    def Annotation(self):
        LabelFiles = sorted(glob.glob(self.input_path + "/labels/*.*"))

        for count in range(1, int(len(LabelFiles) / (self.n * self.n)) + 2):
            im = Image.open(self.output_path + '/images/merge_%s.png' % (count)).convert('RGB')
            plt.figure(figsize=(12.8, 7.8))
            plt.imshow(im)
            ax = plt.gca()

            with open(self.output_path + '/labels/merge_%s.txt' % (count), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    ann = line.split()
                    x = float(ann[1])
                    y = float(ann[2])
                    w = float(ann[3])
                    h = float(ann[4])
                    rect = patches.Rectangle(
                        ((x - (0.5 * w)) * im.size[0], (y - (0.5 * h)) * im.size[1])
                        , w * im.size[0], h * im.size[1], edgecolor='cyan', fill=False)
                    ax.add_patch(rect)
                f.close()

            plt.savefig(self.output_path + "/annotation/merge_%s.png" % (count))
            plt.close()
        return