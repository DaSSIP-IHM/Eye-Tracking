# Eye-Tracking: a way to record gaze data and process them

This repository is a compilation of Python scripts to record gaze data from a Tobii Pro Nano and process them.

## Installation

Clone this repository and use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the requirements.

```bash
pip install -r requirements.txt
```

You need to create folders in root before launching the scripts :  __data__, __examples__, __images__, __processed_data__.

## Usage

The file [main.py](blob/master/main.py) record all the gaze data and process them with the scripts in the __components__ folder :

* [detectors.py](blob/master/components/detectors.py) which is based on a script from the package [PyGazeAnalyzer](https://github.com/esdalmaijer/PyGazeAnalyser/tree/master/pygazeanalyser) and which permits to detect fixations in gaze datas.

* [plot_fixations.py](blob/master/components/plot_fixations.py) which permits to plot the fixations and the gaze's path on a picture


## Contributing
Made with __<3__ by Alphonse Terrier & Antoine Pasqualini (ISEP - Promotion 2020).
