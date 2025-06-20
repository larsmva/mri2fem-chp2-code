#!/bin/bash --

if [ ! -z "${FREESURFER_HOME}" ];
then
   echo "FreeSurfer found"  
else 
   echo "FreeSurfer not found" 
   exit 
fi
export SUBJECTS_DIR=$WORKDIR
cd $SUBJECT/mri

# Creates a mask of the brainstem segmentation
mri_binarize --i aseg.mgz --match 16 --o brainstem.mgz
# Creates a mask of the CSF inside the brainstem mask.
mri_binarize --i T2.norm.mgz --min 30 --mask brainstem.mgz --o cerebral.aqueduct.mgz
# Catagorize different voxel clusters of the mask
mri_volcluster --in  cerebral.aqueduct.mgz  --thmin 1 --ocn  aqueduct.clusters.mgz 
# Create a mask of the largest voxel cluster and set the value to 15
mri_binarize --i aqueduct.clusters.mgz  --match 1 --o cerebral.aqueduct.mgz --binval 15 
# Combine the maks voxels with the freesurfer segmentation 
mri_mask -transfer 15 aseg.modified.mgz cerebral.aqueduct.mgz aseg.modified.mgz 

rm aqueduct.clusters.mgz





