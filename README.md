
# Code for MRI2FEMII chapter 2.

This repository contains script from chapter 2.


## Data 

The scripts runs with the dataset [Data](https://doi.org/10.5281/zenodo.14536218).

After the dataset is downloaded.


## Installation

### Docker

Either run the docker image available under

```bash
docker run -ti -v $(pwd):/root/shared -w /root/shared --rm ghcr.io/larsmva/mri2fem-ii-chapter-2-code
```

or build it locally with

```bash
docker build -t mri2fem-chapter2 -f ./docker/Dockerfile .
```

The image can be started with

```bash
docker run -ti -v $(pwd):/root/shared -w /root/shared --rm  mri2fem-chapter2
```

### Conda

```bash
conda env create -f environment.yml
conda activate mri2fem-chapter2

```

### Requirements 

Install [FreSurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall) and [SVMTK](https://github.com/SVMTK/SVMTK) from source following each of the installation notes.
 





