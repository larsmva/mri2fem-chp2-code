#!/bin/bash --
if [ ! -z "${FREESURFER_HOME}" ];
then
   echo "FreeSurfer found"  
else 
   echo "FreeSurfer not found" 
   exit 
fi

# Extracting dura surface based on the dura mask.
mris_convert ../freesurfer/surf/lh.pial ./lhpial.stl
mris_convert ../freesurfer/surf/rh.pial ./rhpial.stl
mris_convert ../freesurfer/surf/lh.white ./lhwhite.stl
mris_convert ../freesurfer/surf/rh.white ./rhwhite.stl


# Extracting bounding surface based on the inner dura mask.
mri_binarize --i Dura.mgz --match 1 --surf-smooth 5 --surf ./bounding_surface.stl
# Creating a mask of the cerebellum and the 4th ventricle. 
mri_binarize --i ../aseg.modified.mgz  --match 7 46 8 47 15  --o cerebellum.mgz 
# Fill holes that can result in surface errors.
mri_morphology cerebellum.mgz  fill_holes 5 cerebellum.mgz 
# Extracting cerebellum surface 
mri_binarize --i cerebellum.mgz --match 1 --surf-smooth 5 --surf ./cerebellum.stl
# Creating a mask of the brainstem, with thalamus and ventral diencephalon of each hemisphere.
mri_binarize --i ../aseg.modified.mgz --match 10 28 16 15 14 60 49 --o brainstem.mgz
# Fill holes that can result in surface errors.
mri_morphology  brainstem.mgz  fill_holes 5  brainstem.mgz
# Extracting brainstem surface 
mri_binarize --i brainstem.mgz --match 1 --surf-smooth 5 --surf ./brainstem.mgz
