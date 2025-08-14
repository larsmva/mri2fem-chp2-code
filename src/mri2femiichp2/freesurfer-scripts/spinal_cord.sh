#!/bin/bash --

if [ ! -z "${FREESURFER_HOME}" ];
then
   echo "FreeSurfer found"  
else 
   echo "FreeSurfer not found" 
   exit 
fi

echo "Checking if path to mri2femii-chp2 dataset is set" 
if  [ ! -z "${MRI2FEMIIDATA}" ]; 
then
   echo "mri2femii-chp2 dataset found"
else
   echo "mri2femii dataset not found"
   echo "Run setup in mri2femii-chp2-dataset folder" 
   echo "source setup_mri2femii_chp2_dataset.sh" 
   exit
fi

if [ ! -f "${SUBJECT}/output/aseg.modified.mgz" ]; then
   cp  ${SUBJECT}/mri/aseg.mgz  ${SUBJECT}/output/aseg.modified.mgz 
fi

cd ${SUBJECT}/mri
# Creates a mask of tissue inside the dura mask.
mri_binarize --i ${SUBJECT}/mri/T1.mgz --min 65 --mask ${SUBJECT}/output/dura.mgz --o ${SUBJECT}/output/brainstem.extended.mgz   
# Subtracts the freesurfer segmentation from the previous mask 
mri_binarize --i ${SUBJECT}/mri/aseg.mgz --match 0 --mask ${SUBJECT}/output/brainstem.extended.mgz --o ${SUBJECT}/output/brainstem.extended.mgz   
# Catagorize different voxel clusters of the mask
mri_volcluster --in ${SUBJECT}/output/brainstem.extended.mgz  --thmin 1 --ocn ${SUBJECT}/output/brainstem.clusters.mgz
# Create a mask of the largest voxel cluster and set the value to 16 
mri_binarize --i ${SUBJECT}/output/brainstem.clusters.mgz --match 1 --o ${SUBJECT}/output/brainstem.extended.mgz --binval 16
# Closes any holes/concave region in the mask.
mri_morphology  ${SUBJECT}/output/brainstem.extended.mgz close 4 ${SUBJECT}/output/brainstem.extended.mgz
# Combine the maks voxels with the freesurfer segmentation
mri_mask -transfer 16 ${SUBJECT}/output/aseg.modified.mgz ${SUBJECT}/output/brainstem.extended.mgz ${SUBJECT}/output/aseg.modified.mgz 

rm ${SUBJECT}/output/brainstem.clusters.mgz 



