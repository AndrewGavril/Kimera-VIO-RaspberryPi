<div align="center">
  <a href="http://mit.edu/sparklab/">
    <img align="left" src="docs/media/sparklab_logo.png" width="80" alt="sparklab">
  </a> 
  <a href="https://www.mit.edu/~arosinol/">
    <img align="center" src="docs/media/kimeravio_logo.png" width="150" alt="kimera">
  </a> 
  <a href="https://mit.edu"> 
    <img align="right" src="docs/media/mit.png" width="100" alt="mit">
  </a>
</div>

# Kimera-VIO: Open-Source Visual Inertial Odometry

**Authors:** [Antoni Rosinol](https://www.mit.edu/~arosinol/), Yun Chang, Marcus Abate, Sandro Berchier, [Luca Carlone](https://lucacarlone.mit.edu/)

## Current Optimization changes

We have reached the following results in optimizing Kimera for using it on the Raspberry Pi platform:

1. The reading of images from dataset files was transferred from the spin loop in EurocDataProvider to the parse function, so that the files are accessed only during dataset parsing and not on every loop iteration. We have added a parseImages function, which pushes back the images into the left_camera_frames_ and right_camera_frames_ vectors, and the functions for processing the images are later called for the elements of these vectors. These two commits contain this change: https://github.com/AndrewGavril/Kimera-VIO-RaspberryPi/commit/5507c5c875119e309192db1e22000a1a8b20e929, https://github.com/AndrewGavril/Kimera-VIO-RaspberryPi/commit/aa2f8bb7c6425e3bda4120b42f011961c4ddfb9a

2. The compens_by_keyframe branch contains a version of StereoVisionFrontEnd where keyframes are chosen simply every certain interval, defined by the FRAMES_BEFORE_KEYFRAME constant. The value of FRAMES_BEFORE_KEYFRAME is the number of consecutive non-key frames before a keyframe. This version was added in this commit: https://github.com/AndrewGavril/Kimera-VIO-RaspberryPi/commit/d8a443abffe41d2134213fb42115f830d114543f

3. We have listed the parameters (from the params/Euroc folder) that may affect the frame rate. The only one that showed a considerable difference was feature_detector_type in Frontend parameters. FAST type proved more efficient than the default GFTT, while ORB and AGAST do not seem to be correctly implemented at all. The other parameters we checked were:
    • backend_type and regular_vio_backend_modality in stereoVIOEuroc.flags
    • linearizationMode and degeneracyMode in BackendParams.yaml
    • non_max_suppression_type in FrontendParams.yaml
    4. Image rectification is now only done for the first frame, and the calculations are then used for the next frames as well (implemented in the init_stereoframe_optimization branch).
All the optimal conditions were added in the optimized_version branch.

## What is Kimera-VIO?

Kimera-VIO is a Visual Inertial Odometry pipeline for accurate State Estimation from **Stereo** + **IMU** data.

## Publications

We kindly ask to cite our paper if you find this library useful:

- A. Rosinol, M. Abate, Y. Chang, L. Carlone, [**Kimera: an Open-Source Library for Real-Time Metric-Semantic Localization and Mapping**](https://arxiv.org/abs/1910.02490). IEEE Intl. Conf. on Robotics and Automation (ICRA), 2020. [arXiv:1910.02490](https://arxiv.org/abs/1910.02490).
 
 ```bibtex
 @InProceedings{Rosinol20icra-Kimera,
   title = {Kimera: an Open-Source Library for Real-Time Metric-Semantic Localization and Mapping},
   author = {Rosinol, Antoni and Abate, Marcus and Chang, Yun and Carlone, Luca},
   year = {2020},
   booktitle = {IEEE Intl. Conf. on Robotics and Automation (ICRA)},
   url = {https://github.com/MIT-SPARK/Kimera},
   pdf = {https://arxiv.org/pdf/1910.02490.pdf}
 }
```

### Related Publications

Backend optimization is based on:

 - C. Forster, L. Carlone, F. Dellaert, and D. Scaramuzza. **On-Manifold Preintegration Theory for Fast and Accurate Visual-Inertial Navigation**. IEEE Trans. Robotics, 33(1):1-21, 2016.

 - L. Carlone, Z. Kira, C. Beall, V. Indelman, and F. Dellaert. **Eliminating Conditionally Independent Sets in Factor Graphs: A Unifying Perspective based on Smart Factors.** IEEE Intl. Conf. on Robotics and Automation (ICRA), 2014.

Alternatively, the `Regular VIO` backend, using structural regularities, is described in this paper:

- A. Rosinol, T. Sattler, M. Pollefeys, and L. Carlone. **Incremental Visual-Inertial 3D Mesh Generation with Structural Regularities**. IEEE Int. Conf. on Robotics and Automation (ICRA), 2019.

## Demo

<div align="center">
  <img src="docs/media/kimeravio_ROS_mesh.gif"/>
</div>

# 1. Installation

Tested on Mac, Ubuntu 14.04 & 16.04 & 18.04.

## Prerequisites

- [GTSAM](https://github.com/borglab/gtsam) >= 4.0
- [OpenCV](https://github.com/opencv/opencv) >= 3.3.1
- [OpenGV](https://github.com/laurentkneip/opengv)
- [Glog](http://rpg.ifi.uzh.ch/docs/glog.html), [Gflags](https://gflags.github.io/gflags/)
- [Gtest](https://github.com/google/googletest/blob/master/googletest/docs/primer.md) (installed automagically).
- [DBoW2](https://github.com/dorian3d/DBoW2)
- [Kimera-RPGO](https://github.com/MIT-SPARK/Kimera-RPGO)
- [ANMS](https://github.com/BAILOOL/ANMS-Codes) (source files in `src/frontend/feature-detector/anms`, used for adaptive non-max suppression).

> Note: if you want to avoid building all dependencies yourself, we provide a docker image that will install them for you. Check installation instructions in [docs/kimera_vio_install.md](./docs/kimera_vio_install.md).

> Note 2: if you use ROS, then [Kimera-VIO-ROS](https://github.com/MIT-SPARK/Kimera-VIO-ROS) can install all dependencies and Kimera inside a catkin workspace.

## Installation Instructions

Find how to install Kimera-VIO and its dependencies here: **[Installation instructions](./docs/kimera_vio_install.md)**.

# 2. Usage

## General tips

The LoopClosureDetector (and PGO) module is disabled by default. If you wish to run the pipeline with loop-closure detection enabled, set the `use_lcd` flag to true. For the example script, this is done by passing `-lcd` at commandline like so:
```bash
./scripts/stereoVIOEUROC.bash -lcd
```

To log output, set the `log_output` flag to true. For the script, this is done with the `-log` commandline argument. By default, log files will be saved in [output_logs](output_logs/).

To run the pipeline in sequential mode (one thread only), set `parallel_run`to false. This can be done in the example script with the `-s` argument at commandline.

## i. [Euroc](http://projects.asl.ethz.ch/datasets/doku.php?id=kmavvisualinertialdatasets) Dataset

#### Download Euroc's dataset

- Download one of Euroc's datasets, for example [V1_01_easy.zip](http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/vicon_room1/V1_01_easy/V1_01_easy.zip).

> Datasets MH_04 and V2_03 have different number of left/right frames. We suggest using instead [**our version of Euroc here**](https://drive.google.com/open?id=1_kwqHojvBusHxilcclqXh6haxelhJW0O).

- Unzip the dataset to your preferred directory, for example, in `~/Euroc/V1_01_easy`:
```bash
mkdir -p ~/Euroc/V1_01_easy
unzip -o ~/Downloads/V1_01_easy.zip -d ~/Euroc/V1_01_easy
```

#### Yamelize Euroc's dataset

Add `%YAML:1.0` at the top of each `.yaml` file inside Euroc.
You can do this manually or run the `yamelize.bash` script by indicating where the dataset is (it is assumed below to be in `~/path/to/euroc`):
> You don't need to yamelize the dataset if you download our version [here](https://drive.google.com/open?id=1_kwqHojvBusHxilcclqXh6haxelhJW0O)
```bash
cd Kimera-VIO
bash ./scripts/euroc/yamelize.bash -p ~/path/to/euroc
```

### Run Kimera-VIO in Euroc's dataset

Using a bash script bundling all command-line options and gflags:

```bash
cd Kimera-VIO
bash ./scripts/stereoVIOEuroc.bash -p "PATH_TO_DATASET/V1_01_easy"
```

> Alternatively, one may directly use the executable in the build folder:
`./build/stereoVIOEuroc`. Nevertheless, check the script `./scripts/stereoVIOEuroc.bash` to understand what parameters are expected, or check the [parameters](#Parameters) section below.

## ii. Using [ROS wrapper](https://github.com/MIT-SPARK/Kimera-VIO-ROS)

We provide a ROS wrapper of Kimera-VIO that you can find at: https://github.com/MIT-SPARK/Kimera-VIO-ROS.

This library can be cloned into a catkin workspace and built alongside the ROS wrapper.

## iii. Evaluation and Debugging

For more information on tools for debugging and evaluating the pipeline, see [our documentation](/docs/kimera_vio_debug_evaluation.md)

## iv. Unit Testing

We use [gtest](https://github.com/google/googletest) for unit testing.
To run the unit tests: build the code, navigate inside the `build` folder and run `testKimeraVIO`:
```bash
cd build
./testKimeraVIO
```

A useful flag is `./testKimeraVIO --gtest_filter=foo` to only run the test you are interested in (regex is also valid).

# 3. Parameters
Kimera-VIO accepts two independent sources of parameters:
- YAML files: contains parameters for Backend and Frontend.
- [gflags](https://gflags.github.io/gflags/) contains parameters for all the rest.

To get help on what each gflag parameter does, just run the executable with the `--help` flag: `./build/stereoVIOEuroc --help`. You should get a list of gflags similar to the ones [here](./docs/gflags_parameters.md).

  - Optionally, you can try the VIO using structural regularities, as in [our ICRA 2019 paper](https://ieeexplore.ieee.org/abstract/document/8794456), by specifying the option ```-r```: ```./stereoVIOEuroc.bash -p "PATH_TO_DATASET/V1_01_easy" -r```

OpenCV's 3D visualization also has some shortcuts for interaction: check [tips for usage](./docs/tips_usage.md)

# 4. Contribution guidelines

We strongly encourage you to submit issues, feedback and potential improvements.
We follow the branch, open PR, review, and merge workflow.

To contribute to this repo, ensure your commits pass the linter pre-commit checks.
To enable these checks you will need to [install linter](./docs/linter_install.md).
We also provide a `.clang-format` file with the style rules that the repo uses, so that you can use [`clang-format`](https://clang.llvm.org/docs/ClangFormat.html) to reformat your code.

Also, check [tips for development](./docs/tips_development.md) and our **[developer guide](./docs/developer_guide.md)**.

# 5. FAQ

### Issues
  If you have problems building or running the pipeline and/or issues with dependencies, you might find useful information in our [FAQ](./docs/faq.md) or in the issue tracker.

### How to interpret console output

```
I0512 21:05:55.136549 21233 Pipeline.cpp:449] Statistics
-----------                                  #	Log Hz	{avg     +- std    }	[min,max]
Data Provider [ms]                      	    0	
Display [ms]                            	  146	36.5421	{8.28082 +- 2.40370}	[3,213]
VioBackEnd [ms]                         	   73	19.4868	{15.2192 +- 9.75712}	[0,39]
VioFrontEnd Frame Rate [ms]             	  222	59.3276	{5.77027 +- 1.51571}	[3,12]
VioFrontEnd Keyframe Rate [ms]          	   73	19.6235	{31.4110 +- 7.29504}	[24,62]
VioFrontEnd [ms]                        	  295	77.9727	{12.1593 +- 10.7279}	[3,62]
Visualizer [ms]                         	   73	19.4639	{3.82192 +- 0.805234}	[2,7]
backend_input_queue Size [#]            	   73	18.3878	{1.00000 +- 0.00000}	[1,1]
data_provider_left_frame_queue Size (#) 	  663	165.202	{182.265 +- 14.5110}	[1,359]
data_provider_right_frame_queue Size (#)	  663	165.084	{182.029 +- 14.5150}	[1,359]
display_input_queue Size [#]            	  146	36.5428	{1.68493 +- 0.00000}	[1,12]
stereo_frontend_input_queue Size [#]    	  301	75.3519	{4.84718 +- 0.219043}	[1,5]
visualizer_backend_queue Size [#]       	   73	18.3208	{1.00000 +- 0.00000}	[1,1]
visualizer_frontend_queue Size [#]      	  295	73.9984	{4.21695 +- 1.24381}	[1,7]
```

- `#` number of samples taken.
- `Log Hz` average number of samples taken per second in Hz.
- `avg` average of the actual value logged. Same unit as the logged quantity.
- `std` standard deviation of the value logged.
- `[min,max]` minimum and maximum values that the logged value took.

There are two main things logged: the time it takes for the pipeline modules to run (i.e. `VioBackEnd`, `Visualizer` etc), and the size of the queues between pipeline modules (i.e. `backend_input_queue`).

For example:
```
VioBackEnd [ms]                         	   73	19.4868	{15.2192 +- 9.75712}	[0,39]
```

Shows that the backend runtime got sampled `73` times, at a rate of `19.48`Hz (which accounts for both the time the backend waits for input to consume and the time it takes to process it). That it takes `15.21`ms to consume its input with a standard deviation of `9.75`ms and that the least it took to run for one input was `0`ms and the most it took so far is `39`ms.

For the queues, for example:
```
stereo_frontend_input_queue Size [#]    	  301	75.3519	{4.84718 +- 0.219043}	[1,5]
```

Shows that the frontend input queue got sampled `301` times, at a rate of `75.38`Hz. That it stores an average of `4.84` elements, with a standard deviation of `0.21` elements, and that the min size it had was `1` element, and the max size it stored was of `5` elements.

# 6. Chart

![vio_chart](./docs/media/kimeravio_chart.png)

![overall_chart](./docs/media/kimera_chart_23.jpeg)

# 7. BSD License

Kimera-VIO is open source under the BSD license, see the [LICENSE.BSD](LICENSE.BSD) file.
