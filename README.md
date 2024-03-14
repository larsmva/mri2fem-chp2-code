
# Code for chapter 2 of MRI2FEM book

#TODO 

Rename repo 

Link to data


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

### Source

Install [FreSurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall) and [SVMTK](https://github.com/SVMTK/SVMTK) from source following the respective installation notes.
 
### Obtaining Data 

TO BE SET


## Running the code

To generate the meshes call

```bash
python3 create_mesh.py
python3 convert_mesh.py
```


