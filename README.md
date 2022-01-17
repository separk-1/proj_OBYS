<div id="top"></div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

OBYS pjt 코드 정리
<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/separk-1/proj_OBSYS.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### 1. Frame Extraction - video to frame & frame to video
path는 MobaXterm을 기준으로 하였음
```sh
   from DataPreprocessing import FrameExtraction
   
   ext_vidpath="/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/spot.mp4"
   save_imgpath="/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/resized_spot/"
   ext_imgpath="/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/resized_frog/"
   save_vidpath="/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/new_frog.mp4"
   
   FrameExtraction_1 = FrameExtraction(ext_vidpath, save_imgpath, ext_imgpath, save_vidpath)
   
   FrameExtraction_1.video_to_frame()
   FrameExtraction_1.video_to_frame()
   ```
   
### 2. File Filter
```sh
   from DataPreprocessing import FormatRevision
   import os
   
   label_list = os.listdir("**dir")
   image_list = os.listdir("**dir")
   
   FormatRevision_1 = FormatRevision(label_list, image_list)
   
   FormatRevision_1.file_filter()
   ```

### 3. Foldering
```sh
   from DataPreprocessing import Foldering
   
   my_dir = "/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/"
   case_name = "case_1"
   train_dir = ["cycle_1", "cycle_2", "cycle_4"]
   val_dir = ["cycle_3", "cycle_5"]
   
   Foldering_1 = Foldering(my_dir, case_name, train_dir, val_dir)
   
   Foldering_1.foldering()
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

![Createplan](./image/Architecture.png)

<p align="right">(<a href="#top">back to top</a>)</p>
