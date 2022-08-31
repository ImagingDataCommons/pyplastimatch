# PyPlastimatch

**WORK IN PROGRESS** - dummy python plastimatch wrapper and other useful functions for exploration.


# Table of Contents
- [Dependencies](#dependencies)
- [Usage Example](#usage-example)
- [Further Reading](#further-reading)


# Dependencies

In order to run the code found in this repository, all the python libraries found in `requirements.txt` must be installed. This can be achieved running the command:

```
pip3 install -r requirements.txt
```

In addition, you will need to download [plastimatch](http://plastimatch.org/) by running:

```
sudo apt install plastimatch
```

and the DICOM for [Quantitative Imaging (dcmqi) library](https://github.com/QIICR/dcmqi) (e.g., under Linux, download the latest release, move the content of the `bin` folder under `usr/local/bin`, and make the files executable).


# Usage Example

Since Plastimatch and this wrapper are being used for the development of AI-base medical image analysis pipelines on the [NIH CRDC Imaging Data Commons](https://datacommons.cancer.gov/repository/imaging-data-commons) plaftorm, some examples on how to use PyPlastimatch can be found at the [IDC-Examples/notebooks](https://github.com/ImagingDataCommons/IDC-Examples/tree/master/notebooks) repository. 

For instance, the "Cohort Preparation" Colab notebook contains a simple tutorial on how to get a cohort ready for any image processing applications (e.g., best practices for the conversion from DICOM to NRRD and NIfTI, pointers to pre-processing utilities).

To open the Colab notebook, click here:  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ImagingDataCommons/IDC-Examples/blob/master/notebooks/cohort_preparation.ipynb) 

Note: provided you have a Google Cloud Platform project correctly setup, you will be able to run this and all the other notebooks for free, completely on the cloud.

# Further Reading
[Paolo Zaffino's (un)"official" wrapper](https://gitlab.com/plastimatch/plastimatch/-/tree/master/extra/python).

Further discussion about the python-wrapping of Plastimatch can be found at [this discourse.slicer thread](https://discourse.slicer.org/t/python-wrapping-of-plastimatch/6722/10).
