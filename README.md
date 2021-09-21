# PyPlastimatch

**WORK IN PROGRESS** - dummy python plastimatch wrapper and other useful functions for exploration etc.

[Paolo Zaffino's (un)"official" wrapper](https://gitlab.com/plastimatch/plastimatch/-/tree/master/extra/python).

Further discussion about the python-wrapping of Plastimatch can be found at [this discourse.slicer thread](https://discourse.slicer.org/t/python-wrapping-of-plastimatch/6722/10).

## Install Dependencies

In order to run the code found in this repository, all the python libraries found in `requirements.txt` must be installed. This can be achieved running the command:

```
pip3 install -r requirements.txt
```

In addition, you will need to download [plastimatch](http://plastimatch.org/) by running:

```
sudo apt install plastimatch
```

and the DICOM for [Quantitative Imaging (dcmqi) library](https://github.com/QIICR/dcmqi) (e.g., under Linux, download the latest release, move the content of the `bin` folder under `usr/local/bin`, and make the files executable).
