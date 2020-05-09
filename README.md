# Eye-Tracking: a way to record gaze data and process them

This repository is a compilation of Python scripts to record gaze data from a Tobii Pro Nano and process them.

## Installation

Clone this repository and use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the requirements.

```bash
pip install -r requirements.txt
```

You need to create folders in root before launching the scripts :  __data__, __examples__,  __processed_data__, __videos__.

## Video example

[![Alt text](https://img.youtube.com/vi/Ned9yNGzGjw/0.jpg)](https://www.youtube.com/watch?v=Ned9yNGzGjw)

## Usage

The file [main.py](main.py) record all the gaze data and process them with the scripts in the __components__ folder :

* [detectors.py](components/detectors.py) which is based on a script from the package [PyGazeAnalyzer](https://github.com/esdalmaijer/PyGazeAnalyser/tree/master/pygazeanalyser) and which permits to detect fixations in gaze datas.

* [plot_fixations.py](components/plot_fixations.py) which permits to plot the fixations and the gaze's path on a picture

Calibration is done with [Eye Tracker Manager](https://www.tobiipro.com/fr/formation-assistance/telechargements/) here.
## Data collected 

### Natively (with [tobii_research](https://pypi.org/project/tobii-research/) package) :

Definitions according to the [Tobii documentation](http://developer.tobiipro.com/commonconcepts.html)

* __device_time_stamp__ : timestamp of the Tobii device (in microseconds). [More informations...](http://developer.tobiipro.com/commonconcepts/timestamp-and-timing.html)
* __system_time_stamp__ : timestamp of the system (in microseconds). [More informations...](http://developer.tobiipro.com/commonconcepts/timestamp-and-timing.html)
* __left_gaze_point_on_display_area__ :  Coordinates of the point watched by the user on the screen. The origin is the upper left corner of the display area. The point (0, 0) denotes the upper left corner and (1, 1) the lower right corner of it. 

![](http://developer.tobiipro.com/images/sdk-images/ADCS.png)

* __left_gaze_point_in_user_coordinate_system__ : 3D space coordinates are given in the so-called User Coordinate System (UCS). The coordinate axes are oriented as follows: the x-axis points horizontally towards the user’s right, the y-axis points vertically towards the user’s up and the z-axis points towards the user, perpendicular to the front surface of the eye tracker. UCS is defined as follow :

![](http://developer.tobiipro.com/images/sdk-images/UCS.png)
* __left_gaze_point_validity__ : Denotes if the data is trustworthy or not
* __left_pupil_diameter__ : Internal physical size of the left pupil (not the size it appears to be when looking at the eye from the outside)
* __left_pupil_validity__ : Denotes if the data is trustworthy or not
* __left_gaze_origin_in_user_coordinate_system__ : Coordinates of the origin of UCS
* __left_gaze_origin_in_trackbox_coordinate_system__ : The track box is the volume in which the eye tracker is theoretically able to track the eyes. [More informations...](http://developer.tobiipro.com/commonconcepts/coordinatesystems.html)
* __left_gaze_origin_validity__ : Denotes if the data is trustworthy or not

* __right_gaze_point_on_display_area__ : Same as the left eye
* __right_gaze_point_in_user_coordinate_system__ : Same as the left eye
* __right_gaze_point_validity__ : Same as the left eye
* __right_pupil_diameter__ : Same as the left eye
* __right_pupil_validity__ : Same as the left eye
* __right_gaze_origin_in_user_coordinate_system__ : Same as the left eye
* __right_gaze_origin_in_trackbox_coordinate_system__ : Same as the left eye
* __right_gaze_origin_validity__ : Same as the left eye


### Calculated
* x : Mean of the left x and right x gaze data to get the position x watched on the screen
* y : Mean of the left y and right y gaze data to get the position y watched on the screen

The two coordinates are converted in pixels by a multiplication with the screen's resolution
### Created
* mouse_position : (x, y) position of the mouse on the screen



## Contributing
Made with <3 by Alphonse Terrier & Antoine Pasqualini (ISEP - Promotion 2020).

