<div id="top"></div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

* Obayashi project code
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/separk-1/proj_OBSYS.git
   ```
3. Install packages
   ```sh
   pip install -r requirements.txt  
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### 1. Frame Extraction
* video to frame & frame to video
```sh
   from DataPreprocessing import FrameExtraction
   
   ext_vidpath="[추출하고자 하는 video path]"
   save_imgpath="[추출한 이미지를 저장하는 image path]"
   ext_imgpath="[변환하고자 하는 image path]"
   save_vidpath="[변환한 이미지를 저장하는 video path]"
   
   FrameExtraction_1 = FrameExtraction(ext_vidpath, save_imgpath, ext_imgpath, save_vidpath)
   
   FrameExtraction_1.video_to_frame()
   FrameExtraction_1.video_to_frame()
   ```
   
### 2. Format Revision
* file filter
```sh
   from DataPreprocessing import FormatRevision
   import os
   
   label_list = os.listdir("[file path]")
   image_list = os.listdir("[file path]")
   
   FormatRevision_1 = FormatRevision(label_list, image_list)
   
   FormatRevision_1.file_filter()
   ```
* txt_revised
```sh
   import os
   import re
   import natsort
   
   FormatRevision.txt_revised("[file path]")
   ```


### 3.1 Foldering
```sh
   from DataPreprocessing import Foldering
   
   my_dir = "[dataset folder]"
   case_name = "case_1"
   train_dir = ["cycle_1", "cycle_2", "cycle_4"]
   val_dir = ["cycle_3", "cycle_5"]
   
   Foldering_1 = Foldering(my_dir, case_name, train_dir, val_dir)
   
   Foldering_1.foldering()
   ```

### 3.2 Foldering_Random
```sh
   from DataPreprocessing import Foldering_Random
  
   Foldering_Random_1 = Foldering_Random(case_name= "[Case_name]",
                                      threshold = "[Threshold]",
                                      txt_path='"[Anyfilename]".txt')
  origin_df = Foldering_Random_1.origin_df()
  Foldering_Random_1.save_plot(df = origin_df, figpath='"[Original_Plot_name]".png')
  
  Random_df = Foldering_Random_1.Random_df()
  Foldering_Random_1.save_plot(df = Random_df, figpath='"[Random_Plot_name]".png')
   ```
   
   ```
   python Set_Dir.py (folder dir 정리)
   ```
   
<p align="right">(<a href="#top">back to top</a>)</p>

### 4. Activity Classification
   * We use LSTM networks here for classifying (&predicting) classes of activities. 
   It could be divided into "Train" part, and "Test" part. 
   Each you can check in python files belows:
   Train >lstm_obayashi.py 
   Test > lstm_obayashi_test.py
   
   While training (run lstm_obayashi.py file), "*.h5" files are being made.
   Testing(Predicting) could be done by importing "*.h5" files, maded while training. 
   
   You could train with your custom data by changing the path : code below.
```sh
   DATASET_PATH = "*.csv"
   x_train_path = DATASET_PATH + "X_train.csv"
   x_test_path = DATASET_PATH + "X_test.csv"
   y_train_path = DATASET_PATH + "y_train.csv"
   y_test_path = DATASET_PATH + "y_test.csv"
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap
### Data Preprocessing
- [x] 1. Frame Extraction 
    - [x] video_to_frame.py
    - [x] frame_to_video.py
- [ ] 2. FormatRivision (Utils)
    - [x] file_filter.py : 라벨 안 된 이미지 파일 삭제
    - [ ] dataset_randoim_div : data를 train, val set으로 분리
    - [ ] txt_revised : labeling 결과 txt format 변환 (,)->( )
    - [ ] txt_to_timetable.py 
- [x] 3. Foldering

### Next Step

![Createplan](./image/architecture.png)

<p align="right">(<a href="#top">back to top</a>)</p>
