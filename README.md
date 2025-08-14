
# Code for MRI2FEMII Chapter 2

This repository contains the script and related code for chapter 2 of [MRI2FEMII]() 


# Installation

The python code can be installed as a python package by running the following command in the repository 

`pip install -e .`
or 
`python -m pip install -e .`


# Dataset  

The scripts and code require the dataset [Data](https://doi.org/10.5281/zenodo.14536218). The data can be downloaded from Zenodo using webrowser, or downloaded using the python package.

## Downloading Dataset 

The dataset can be downloaded from [Data](https://doi.org/10.5281/zenodo.14536218).

## Python Package Download

If the mri2femiichp2 python package is installed, then the data can be downloaded with the following command

`mri2femiichp2 download`

The user can also specify the download directory.
```
$ mri2femiichp2 download --help
usage: mri2femiichp2 download [-h] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory of the downloaded dataset.
```

# Reproducing the book 

## FreeSurfer 

FreeSurfer needs to be installed to run the bash scripts. 

The scripts relies on enviroment variables to located the nessacry files to run. The required enviroment variables will be set by running the following command in 
the dataset folder. 

`source setup_mri2femii_chp2_dataset.sh`

## Python 

The `mri2femiichp2` command have four subcommands

```
usage: mri2femiichp2 [-h] [--dry-run] [-v] {download,mesh,subject-mesh,convert-mesh} ...

positional arguments:
  {download,mesh,subject-mesh,convert-mesh}
    download            Download the dataset
    mesh                Generates mesh from surface files.
    subject-mesh        Generates mesh from surface files
    convert-mesh        Convert .mesh format to .h5

options:
  -h, --help            show this help message and exit
  --dry-run             Just print the command and do not run it (default: False)
  -v, --verbose         Print more information (default: False)
```

and these subcommands have additional subcommands. For example, the `mesh` subcommand has the following subcommands

```
$ mri2femiichp2 mesh --help
usage: mri2femiichp2 mesh [-h] [--rhpial RHPIAL] [--lhpial LHPIAL] [--lhwhite LHWHITE] [--rhwhite RHWHITE] [--brainstem BRAINSTEM] [--cerebellum CEREBELLUM] [--dura DURA]
                          [--ventricles VENTRICLES] [--edge_length EDGE_LENGTH] [--resolution RESOLUTION] [--export_fenicsx EXPORT_FENICSX] [--out OUT]

options:
  -h, --help            show this help message and exit
  --rhpial RHPIAL       The path to the right pial surface.
  --lhpial LHPIAL       The path to the left pial surface.
  --lhwhite LHWHITE     The path to the left white surface.
  --rhwhite RHWHITE     The path to the right white surface.
  --brainstem BRAINSTEM
                        The path to the brainstem surface.
  --cerebellum CEREBELLUM
                        The path to the cerebellum surface.
  --dura DURA           The path to the dura surface.
  --ventricles VENTRICLES
                        The path to the ventricular surface.
  --edge_length EDGE_LENGTH
                        Target surface edge length duirng remeshing (Default=1.0)
  --resolution RESOLUTION
                        The mesh resolution of the mesh. The bounding radius of all surfaces divided by the resolution gives targt cell_size.
  --export_fenicsx EXPORT_FENICSX
                        Option to export the mesh to xdmf format compatible with FEniCSx.
  --out OUT             The output folder
```


# Requirements 

Install [FreSurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall) and [SVMTK](https://github.com/SVMTK/SVMTK) from source following each of the installation notes.

## Optional requirements 

The installation of [fenicsx](https://fenicsproject.org/download/) is optional.


# Acknowledgement
Thanks to Henrik Nicolay Finsberg.





