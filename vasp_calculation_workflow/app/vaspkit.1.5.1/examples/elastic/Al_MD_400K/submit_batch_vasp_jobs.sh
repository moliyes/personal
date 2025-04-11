#!/bin/bash
root_path=`pwd`
for cij in `ls -F | grep /$`
do
  cd ${root_path}/$cij
  for s in strain_*
  do
    cd ${root_path}/$cij/$s
    echo `pwd`
    P_016_1
    # Add here your vasp_submit_job_script
  done
done
