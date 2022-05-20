import os
import pandas as pd

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def crop_img_label(equip_class, imagepath, labelpath):
    image_path = imagepath+equip_class
    if not os.path.exists(image_path):
        print(equip_class +" is not existed")
        pass

    else:
        file_list = os.listdir(image_path)
        df=pd.DataFrame(file_list)
        new_list=[]
        for i in range(len(df)):
            title_jpg = df.iloc[i][0]
            title = title_jpg.split('.')[0]
            new_list.append(title)

        label_path=labelpath+equip_class+'/'
        createFolder(label_path)

        for j in new_list:
            f= open(label_path+j+'.txt','w')
            label= "0   0.5   0.5   1   1"
            f.write(label)
            f.close()
        print(equip_class + " completed!")


equipment_class=["drill_jumbo", "gunpowder_carrier", "work platform", "breaker", "excavator", "payloader", "dump_truck", "sprayer", "h_beam_holder", "mixer_truck", "mortar_trolley_truck"]
imagepath="./test/crops/"
labelpath="./test/images/"

for i in equipment_class:
    crop_img_label(i, imagepath, labelpath)

