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

get_surface () {

mri_binarize --i "${SUBJECT}/output/aseg.modified.mgz"  --match "${@:2}"  --o "${SUBJECT}/output/$1.mgz" 
mri_morphology   "${SUBJECT}/output/$1.mgz"   fill_holes 5 "${SUBJECT}/output/$1.mgz" 
mri_binarize --i "${SUBJECT}/output/$1.mgz"  --match 1 --surf-smooth 5 --surf "${SUBJECT}/output/$1.stl"
rm "${SUBJECT}/output/$1.mgz"
}

while [[ $# -gt 0 ]]; do
  case $1 in
    -h)  
      echo "Error"
      shift
      ;;
    --dura) 
      mri_binarize --i ${SUBJECT}/output/dura.mgz --match 1 --surf-smooth 5 --surf ${SUBJECT}/output/dura.stl
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
    --white) 
      mris_convert  ${SUBJECT}/surf/lh.white ${SUBJECT}/output/lhwhite.stl
      mris_convert  ${SUBJECT}/surf/rh.white ${SUBJECT}/output/rhwhite.stl      
      shift
      ;;
    --pial) 
      mris_convert  ${SUBJECT}/surf/lh.pial  ${SUBJECT}/output/lhpial.stl
      mris_convert  ${SUBJECT}/surf/rh.pial  ${SUBJECT}/output/rhpial.stl
      shift
      ;; 
      --choroid-plexus)
      get_surface "lh-choroid-plexus" 31 
      get_surface "rh-choroid-plexus" 63 
      shift
      ;;       
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done







