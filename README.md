# PyPlastimatch

PyPlastimatch is a python wrapper for [Plastimatch](http://plastimatch.org/), an ITK-based open source software designed for volumetric medical image processing and radiation therapy applications.

The main reason behing the development of PyPlastimatch is being able to use the Plastimatch functions within python scripts without having to code using `os.system` or `subprocess` all the time. Also, we are working on making the output of some of the functions Plastimatch implements for evaluation (e.g., Dice Coefficient and Hausdorff Distance) more pythonic/easily usable in python-based data analysis pipelines.

Together with the wrapping functions, we are also developing simple but handy functions that can be used for quick data exploration (e.g., simple widgets based on ipywidgets) in ipython notebooks and JupyterLab.

# Table of Contents
- [Dependencies](#dependencies)
- [Usage Example](#usage-example)
- [Further Reading](#further-reading)


# Install Via `pip`

PyPlastimatch can be installed via pip:

```
pip install pyplastimatch
```

# Dependencies

## Python

If you decide to clone the PyPlastimatch repository and not to install it with `pip`, in order to run the code as intended, all the python libraries found in `requirements.txt` must be installed. This can be done running the command:

```
pip3 install -r requirements.txt
```

## Plastimatch

Since PyPlastimatch is a python wrapper and doesn't include any processing code, Plastimatch must be installed on the machine separately.

For Linux users, Plastimatch can be installed simply by running:

```
sudo apt install plastimatch
```

For Windows users, Plastimatch can be installed following [the guide at this webpage](http://plastimatch.org/windows_installation.html).

Plastimatch can also be build from source following [the guide at this webpage](http://plastimatch.org/building_plastimatch.html).


## DCMQI

Some functions might be based on the [DICOM for Quantitative Imaging (dcmqi) library](https://github.com/QIICR/dcmqi), that must be installed separately (e.g., under Linux, download the latest release, move the content of the `bin` folder under `usr/local/bin`, and make the files executable).


# Usage Example

Since Plastimatch and this wrapper are being used for the development of AI-base medical image analysis pipelines on the [NIH CRDC Imaging Data Commons](https://datacommons.cancer.gov/repository/imaging-data-commons) plaftorm, some examples on how to use PyPlastimatch can be found at the [IDC-Examples/notebooks](https://github.com/ImagingDataCommons/IDC-Examples/tree/master/notebooks) repository. 

For instance, the "Cohort Preparation" Colab notebook contains a simple tutorial on how to get a cohort ready for any image processing applications (e.g., best practices for the conversion from DICOM to NRRD and NIfTI, pointers to pre-processing utilities).

To open the Colab notebook, click here:  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ImagingDataCommons/IDC-Examples/blob/master/notebooks/cohort_preparation.ipynb) 

Note: provided you have a Google Cloud Platform project correctly setup, you will be able to run this and all the other notebooks for free, completely on the cloud.

# Further Reading
[Paolo Zaffino's (un)"official" wrapper](https://gitlab.com/plastimatch/plastimatch/-/tree/master/extra/python).

Further discussion about the python-wrapping of Plastimatch can be found at [this discourse.slicer thread](https://discourse.slicer.org/t/python-wrapping-of-plastimatch/6722/10).
