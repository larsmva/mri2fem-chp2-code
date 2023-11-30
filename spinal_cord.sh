#!/bin/bash --

if [ ! -z "${FREESURFER_HOME}" ];
then
   echo "FreeSurfer found"  
else 
   echo "FreeSurfer not found" 
   exit 
fi

export SUBJECTS_DIR="freesurfer"

cd $SUBJECT/mri
# Creates a mask of tissue inside the dura mask. FIXME 
mri_binarize --i T1.mgz --min 65 --mask dura.mgz --o brainstem.extended.mgz   
# Subtracts the freesurfer segmentation from the previous mask 
mri_binarize --i aseg.mgz --match 0 --mask brainstem.extended.mgz --o brainstem.extended.mgz   
# Catagorize different voxel clusters of the mask
mri_volcluster --in brainstem.extended.mgz  --thmin 1 --ocn brainstem.clusters.mgz
# Create a mask of the largest voxel cluster and set the value to 16 
mri_binarize --i brainstem.clusters.mgz --match 1 --o brainstem.extended.mgz --binval 16
# Closes any holes/concave region in the mask. FIXME 
mri_morphology  brainstem.extended.mgz close 4  brainstem.extended.mgz
# Combine the maks voxels with the freesurfer segmentation
mri_mask -transfer 16 aseg.mgz brainstem.extended.mgz aseg.modified.mgz 

rm brainstem.clusters.mgz 



