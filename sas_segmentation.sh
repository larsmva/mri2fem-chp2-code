
if [ ! -z "${FREESURFER_HOME}" ];
then
   echo "FreeSurfer found"  
else 
   echo "FreeSurfer not found" 
   exit 
fi

export SUBJECTS_DIR="freesurfer"

# Create a mask of CSF in T2-weighted image. 
mri_binarize --i T2.norm.mgz --min 110 --o T2.threshold.mgz  
# Subtract any voxels with tissue or skull based on T1-weighted image. 
mri_binarize --i freesurfer/mri/T1.mgz --max 65 --mask T2.threshold.mgz  --o SAS.mgz
# Merge mask with freesurfer segmentattion.  
mri_binarize --i aseg.mgz --min 1 --o Dura.inner.mgz --merge SAS.mgz 
# Catagorize different voxel clusters of the mask.
mri_volcluster --in Dura.inner.mgz --thmin 1 --ocn Dura.clusters.mgz
# Create a mask of the largest voxel cluster. 
mri_binarize --i Dura.clusters.mgz --match 1 --o Dura.inner.mgz 
# Closes any holes/concave region in the mask.
mri_morphology Dura.inner.mgz close 4 Dura.mgz



