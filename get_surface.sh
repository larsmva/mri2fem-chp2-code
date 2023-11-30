#!/bin/bash --
if [ ! -z "${FREESURFER_HOME}" ];
then
   echo "FreeSurfer found"  
else 
   echo "FreeSurfer not found" 
   exit 
fi

echo "Checking if path to mri2femii dataset is set" 
if  [ ! -z "${MRI2FEMDATA}" ]; 
then
   echo "mri2femii dataset found"
else
   echo "mri2femii dataset not found"
   echo "Run setup in mri2fem-dataset folder" 
   echo "source Setup_mri2fem_dataset.sh" 
   exit
fi



get_surface () {

mri_binarize --i "${MRI2FEMDATA}/freesurfer/orig/aseg.modified.mgz"  --match "${@:2}"  --o $1.mgz 
mri_morphology $1.mgz  fill_holes 5 $1.mgz
mri_binarize --i $1.mgz --match 1 --surf-smooth 5 --surf ./$1.stl
rm $1.mgz
}

#while [[ $# -gt 0 ]]; do
while [[ $# -gt 0 ]]; do
  case $1 in
    -h)  
      echo "Error"
      shift
      ;;
    --dura) 
      mri_binarize --i dura.inner.mgz --match 1 --surf-smooth 5 --surf ./dura.stl
      shift    
      ;;
    --ventricles)
      get_surface "ventricles" 4 5 14 15 31 43 44 63
      shift    
      ;;
    --brainstem)
      get_surface "brainstem" 10 28 16 15 14 60 49
      shift
      ;; 
    --cerebellum)
      get_surface "cerebellum" 7 46 8 47 15
      shift
      ;; 
    --cerebrum) 
      mris_convert ../freesurfer/surf/lh.pial ./lhpial.stl
      mris_convert ../freesurfer/surf/rh.pial ./rhpial.stl
      mris_convert ../freesurfer/surf/lh.white ./lhwhite.stl
      mris_convert ../freesurfer/surf/rh.white ./rhwhite.stl      
      shift
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done







