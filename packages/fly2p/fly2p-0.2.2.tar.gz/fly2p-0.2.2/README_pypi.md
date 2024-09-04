<img src="https://user-images.githubusercontent.com/10639803/126242184-65bc84c4-3fa2-4034-be51-3e8c2e4d9f8c.png" align="middle" width="3000"/>

# fly2p

Tools for analyzing imaging data collected with [Vidrio Scanimage software](https://vidriotechnologies.com/scanimage/) or [micromanger](https://micro-manager.org/). Loading ScanImage data relies on [scanimageReader](https://pypi.org/project/scanimage-tiff-reader/), which can be installed via 'pip install scanimage-tiff-reader'. Other dependencies are tracked using poetry.

### Organization
The fly2p package contains the following submodules:
* **preproc**: Some file-format specific functions that extract metadata and load the imaging data. imgPreproc.py defines a data object to hold metadata and imaging data as well as basic proporcessing functions.
* **viz**: A collection of utility functions related to plotting flourescence traces and images.

In addition, the **scripts** folder contains notebooks that illustrate how to use functions in this module based on example files in **sample** (sample files are not currently pushed to repo, but will be made available through figshare).