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
* MobaXterm: /home/obayashi/Projects/obayashi_practice/
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
###0. Dataset
* raw_data: 가공 전 labeled dataset
* case_data: 
  - case_data: foldering 결과 dataset
  - case_data_threshold: foldering_random으로 case_data의 class별 데이터 수를 threshold로 맞춘 dataset
* test_data: video for test
* activity_recognition
    
### 1. DataPreprocessing
#### 1) Set config
* Set parameter for running
* path: /config/config.yaml
#### 2) DataPreprocessing
* Select mode by parser
* path: /bin/DataPreprocessing.bat
```sh
codes/Run_Datapreprocessing.py -m Foldering
codes/Run_Datapreprocessing.py -m Foldering_Random
codes/Run_Datapreprocessing.py -m Video_to_frame
codes/Run_Datapreprocessing.py -m Frame_to_video
codes/Run_Datapreprocessing.py -m FormatRevision
codes/Run_Datapreprocessing.py -m Augmentation
```
### 2. Train & Predict
#### 1) OD_train
#### 2) OD_predict
#### 3) AR_train
#### 4) AR_predict
### 3. Result Analysis
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Architecture
![Createplan](./image/architecture.png)

<p align="right">(<a href="#top">back to top</a>)</p>
