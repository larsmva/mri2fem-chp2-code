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


# Creates a mask of the brainstem segmentation
mri_binarize --i ${SUBJECT}/mri/aseg.mgz --match 16 --o ${SUBJECT}/output/brainstem.mgz
# Creates a mask of the CSF inside the brainstem mask.
mri_binarize --i ${SUBJECT}/output/T2.norm.mgz --min 40 --mask ${SUBJECT}/output/brainstem.mgz --o ${SUBJECT}/output/cerebral.aqueduct.mgz
# Catagorize different voxel clusters of the mask
mri_volcluster --in  ${SUBJECT}/output/cerebral.aqueduct.mgz  --thmin 1 --ocn  ${SUBJECT}/output/aqueduct.clusters.mgz 
# Create a mask of the largest voxel cluster and set the value to 15
mri_binarize --i ${SUBJECT}/output/aqueduct.clusters.mgz  --match 1 --o ${SUBJECT}/output/cerebral.aqueduct.mgz --binval 15 
# Combine the maks voxels with the freesurfer segmentation 
mri_mask -transfer 15 ${SUBJECT}/output/aseg.modified.mgz ${SUBJECT}/output/cerebral.aqueduct.mgz ${SUBJECT}/output/aseg.modified.mgz 

rm ${SUBJECT}/output/aqueduct.clusters.mgz





