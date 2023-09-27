# PyPlastimatch

PyPlastimatch is a python wrapper for [Plastimatch](http://plastimatch.org/), an ITK-based open source software designed for volumetric medical image processing and radiation therapy applications.

The main reason behing the development of PyPlastimatch is being able to use the Plastimatch functions within python scripts without having to code using `os.system` or `subprocess` all the time. Also, we are working on making the output of some of the functions Plastimatch implements for evaluation (e.g., Dice Coefficient and Hausdorff Distance) more pythonic/easily usable in python-based data analysis pipelines.

Together with the wrapping functions, we are also developing simple but handy functions that can be used for quick data exploration (e.g., simple widgets based on ipywidgets) in ipython notebooks and JupyterLab.

<br>

PyPlastimatch is completely independent from the main software Plastimatch, and it is being developed mainly for internal use. For this reason, most of the Plastimatch functions might be missing. If you would like to see something added or point out how we could improve anything in the wrapper, you are very welcome to [open an issue at the issue page](https://github.com/AIM-Harvard/pyplastimatch/issues).


# Table of Contents
- [Install Via pip](#install-via-pip)
- [Dependencies](#dependencies)
  - [Python](#python)
  - [Plastimatch](#plastimatch)
  - [dcmqi](#dcmqi)
- [Usage Example](#usage-example)
- [Run in a Docker Container](#ubuntu-2204-lts-plastimatch-docker-container)
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

### Ubuntu 20.04 LTS

For users running Ubuntu 20.04 LTS (and distributions that fetch the same packages), Plastimatch can be installed simply by running:

```
sudo apt install plastimatch
```

### Ubuntu 22.04 LTS

Users running Ubuntu 22.04 LTS will unfortunately not be able to install Plastimatch via `apt` (see [this Issue on the official Plastimatch GitLab](https://gitlab.com/plastimatch/plastimatch/-/issues/87)). To remedy this, we compiled a binary file for Ubuntu 22.04 LTS that you can find [in our releases](https://github.com/AIM-Harvard/pyplastimatch/releases) and you can download running the following once PyPlastimatch is installed (from a Python3 shell):

```
from pyplastimatch.utils.install import install_precompiled_binaries
install_precompiled_binaries()
```

and, of course, its equivalent from CLI:

```
RUN python3 -c 'from pyplastimatch.utils.install import install_precompiled_binaries; install_precompiled_binaries()'
```

The plastimatch binary we provide was compiled dinamically, so it will not work without installing some dependencies (`itk` via `pip`, and some system dependencies that the `install_precompiled_binaries()` function takes care of automatically). Depending on the python version you are using and your environment (i.e., packages already installed), you might need to install `itk` via `pip` before installing `pyplastimatch`.

In the future, we might support binaries pre-compiled statically, and for other distributions/OSs. 

### Other OSs

For Windows users, Plastimatch can be installed following [the guide at this webpage](http://plastimatch.org/windows_installation.html).

### Building from Source

Plastimatch can also be build from source following [the guide at this webpage](http://plastimatch.org/building_plastimatch.html). The guide could be slightly outdated, but it should be enough to get you started.

## DCMQI

Some functions might be based on the [DICOM for Quantitative Imaging (dcmqi) library](https://github.com/QIICR/dcmqi), that must be installed separately (e.g., under Linux, download the latest release, move the content of the `bin` folder under `usr/local/bin`, and make the files executable).


# Usage Example

Since Plastimatch and this wrapper are being used for the development of AI-base medical image analysis pipelines on the [NIH CRDC Imaging Data Commons](https://datacommons.cancer.gov/repository/imaging-data-commons) plaftorm, some examples on how to use PyPlastimatch can be found at the [IDC-Examples/notebooks](https://github.com/ImagingDataCommons/IDC-Examples/tree/master/notebooks) repository. 

For instance, the "Cohort Preparation" Colab notebook contains a simple tutorial on how to get a cohort ready for any image processing applications (e.g., best practices for the conversion from DICOM to NRRD and NIfTI, pointers to pre-processing utilities).

To open the Colab notebook, click here:  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ImagingDataCommons/IDC-Examples/blob/master/notebooks/cohort_preparation.ipynb) 

Note: provided you have a Google Cloud Platform project correctly setup, you will be able to run this and all the other notebooks for free, completely on the cloud.

# Ubuntu 22.04 LTS Plastimatch Docker Container

If you want to test Plastimatch for Ubuntu 22.04 LTS, you can use the Docker image we shared for this purpose under `dockerfiles`.

## Build the Docker Container

To build the Ubuntu 22.04 LTS Platimatch Docker container, run the following commands from the root of the PyPlastimatch repository:

```
cd dockerfiles/

docker build --tag pypla_22.04 .
```

## Run the Docker Container

Assuming the data you want to convert/manipulate with Plastimatch is stored at `/home/dennis/Desktop/sample_data/`, the Docker command to run will look like the following

```
docker run --rm -it --entrypoint bash -v /home/dennis/Desktop/sample_data/:/app/data pypla_22.04
```

This will mount the data directory to the container's `/app/data` directory, and you can then run Plastimatch commands from within the container. For example, if `/home/dennis/Desktop/sample_data/` is structured as follows:

```
(base) dennis@W2-S1:~$ tree /home/dennis/Desktop/sample_data/ -L 1
/home/dennis/Desktop/sample_data/
└── dicom
```

Then, once inside the container, you can run the following command to convert the DICOM files to a volume saved in the NRRD format:

```
cd /app/data

plastimatch convert --input input_dcm/ --output-img test.nrrd
```


# Further Reading
[Paolo Zaffino's (un)"official" wrapper](https://gitlab.com/plastimatch/plastimatch/-/tree/master/extra/python).

Further discussion about the python-wrapping of Plastimatch can be found at [this discourse.slicer thread](https://discourse.slicer.org/t/python-wrapping-of-plastimatch/6722/10).
