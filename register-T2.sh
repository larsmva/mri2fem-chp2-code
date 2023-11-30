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
# Convert the T2 image to size 256^3 with voxel size 1 mm^3
mri_convert -odt float -c T2.orignal.mgz T2.conformed.mgz 
# bbregister perform within-subject cross-modal registration 
bbregister --s $SUBJECT --mov  T2.original.mgz --lta transforms/T2raw.lta --init-fsl --T2 
# Apply transformation to the conformed T2 image. 
mri_vol2vol --mov T2.conformed.mgz --targ orig.mgz --lta T2raw.lta --o T2.registered.mgz 
# Rescale the T2 image.
mri_nu_correct.mni --i T2.registered.mgz --o T2.nu.mgz
# Rescale the T2 image.
mri_normalize T2.nu.mgz T2.norm.mgz

