#!/bin/bash
# just for reference
path=`pwd`
for c in C11 C12 C22 C66
do
  cd $c
  for i in strain_*
  do
   cd ${path}/$c/$i
   echo `pwd`
   SA 
   #  qsub job.sh   ! You edit only this line to submit jobs 
  done
  cd ${path}
done
