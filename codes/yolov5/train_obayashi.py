import os

batch = "8"
epochs = "100"
data = "/home/obayashi/data/cctv_video/train_data/Case/case_12_1000/case_12_1000.yaml"
pre_weights = "yolov5s.pt"

#pre_weights = "/home/obayashi/Projects/proj_obayashi/results/case_train_result/case11_1000_0322/weights/best.pt"

save_name = "test_0517"
save_dir = "/home/obayashi/Projects/proj_obayashi/results/train_result/"

command1 = 'CUDA_VISIBLE_DEVICES=0,1 python ./train.py --batch '
command1 += batch
command1 += ' --epochs '
command1 += epochs
command1 += ' --data ' 
command1 += data
command1 += ' --weights '
command1 += pre_weights
command1 += ' --name '
command1 += save_name
command1 += ' --project '
command1 += save_dir

print(command1)
os.system(command1)
