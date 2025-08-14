#!/bin/bash
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

# Create a mask of CSF in T2-weighted image. 
mri_binarize --i ${SUBJECT}/output/T2.norm.mgz --min 40 --o ${SUBJECT}/output/T2.threshold.mgz  
# Subtract any voxels with tissue or skull based on T1-weighted image. 
mri_binarize --i ${SUBJECT}/mri/T1.mgz --max 65 --mask ${SUBJECT}/output/T2.threshold.mgz  --o ${SUBJECT}/output/SAS.mgz
# Merge mask with freesurfer segmentattion.  
mri_binarize --i ${SUBJECT}/mri/aseg.mgz --min 1 --o ${SUBJECT}/output/dura.mgz --merge ${SUBJECT}/output/SAS.mgz 
# Catagorize different voxel clusters of the mask.
mri_volcluster --in ${SUBJECT}/output/dura.mgz --thmin 1 --ocn ${SUBJECT}/output/Dura.clusters.mgz
# Create a mask of the largest voxel cluster. 
mri_binarize --i ${SUBJECT}/output/Dura.clusters.mgz --match 1 --o ${SUBJECT}/output/dura.mgz 
# Closes any holes/concave region in the mask.
mri_morphology ${SUBJECT}/output/dura.mgz close 4 ${SUBJECT}/output/dura.mgz



