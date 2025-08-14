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

export SUBJECTS_DIR=${MRI2FEMIIDATA}

# Convert the T2 image to size 256^3 with voxel size 1 mm^3
mri_convert -odt float -c ${MRI2FEMIIDATA}/MRI/T2.original.nii.gz ${SUBJECT}/output/T2.conformed.mgz 
# bbregister perform within-subject cross-modal registration 
bbregister --s $(basename $SUBJECT) --mov  ${MRI2FEMIIDATA}/MRI/T2.original.nii.gz --lta ${SUBJECT}/output/T2raw.lta --init-fsl --T2 
# Apply transformation to the conformed T2 image. 
mri_vol2vol --mov ${SUBJECT}/output/T2.conformed.mgz --targ ${SUBJECT}/mri/orig.mgz --lta ${SUBJECT}/output/T2raw.lta --o ${SUBJECT}/output/T2.registered.mgz 
# Rescale the T2 image.
mri_nu_correct.mni --i ${SUBJECT}/output/T2.registered.mgz --o ${SUBJECT}/output/T2.nu.mgz
mri_normalize ${SUBJECT}/output/T2.nu.mgz ${SUBJECT}/output/T2.norm.mgz

