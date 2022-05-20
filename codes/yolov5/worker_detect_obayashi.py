import os


detect_model="detect.py"
source= "/home/obayashi/data/cctv_video/test_data/cycle1.mp4"
weights = "yolov5x.pt"
conf = "0.30"
save_dir = "/home/obayashi/Projects/proj_obayashi/results/train_result/New_Worker_Results/"
#save_dir = "/home/obayashi/Projects/proj_obayashi/results/train_result/Test_Worker_results/"
#save_dir = "/home/obayashi/Projects/proj_obayashi/results/worker_detect_result/"
save_name ="New_Worker_Results_Test"
#save_name ="worker_test01"


command1 = 'python '
command1 += detect_model
command1 += ' --source '
command1 += source
command1 += ' --weights '
command1 += weights
command1 += ' --conf '
command1 += conf
command1 += ' --project '
command1 += save_dir
command1 += ' --name '
command1 += save_name
command1 += ' --classes 0'

print(command1)
os.system(command1)
