#!/bin/bash
vaspkit_path=`pwd`
vaspkit_env=~
cp ~/.bashrc ~/.bashrc.bk
   echo "+------------------------------------------------------------------------+"
if [ ! -f "${vaspkit_env}/.vaspkit" ]; then
   cp how_to_set_environment_variables ~/.vaspkit
   echo "| The ~/.vaspkit file for vaspkit code has been added.                   |"
   echo "| Please modify ~/.vaspkit based on your account settings!               |"
else
   echo "| The ~/.vaspkit file already exists and has not been overwritten.       |"
fi
if [ `grep -c "vaspkit" ~/.bashrc` -eq '1' ]; then
   n=`grep -rin "vaspkit" ~/.bashrc|awk  -F ':'  '{print $1}'`
   sed -i ""${n}"c  export PATH=${vaspkit_path}/bin:\${PATH}" ~/.bashrc
   echo "| The PATH variable for vaspkit code has been updated.                   |"
else
   echo "export PATH=${vaspkit_path}/bin:\${PATH}" >>~/.bashrc
   echo "| The PATH variable for vaspkit code has been added.                     |"
fi

VASPKIT_UTILITIES_PATH_VARIABLE="VASPKIT_UTILITIES_PATH    ${vaspkit_path}/utilities"
if [ `grep -c "VASPKIT_UTILITIES_PATH" ~/.vaspkit` -eq '1' ]; then
   n=`grep -rin "VASPKIT_UTILITIES_PATH" ~/.vaspkit|awk  -F ':'  '{print $1}'`
   sed -i ""${n}"c  ${VASPKIT_UTILITIES_PATH_VARIABLE}" ~/.vaspkit
   echo "| The VASPKIT_UTILITIES_PATH variable has been updated.                  |"
else
   echo "${VASPKIT_UTILITIES_PATH_VARIABLE}" >>~/.vaspkit
   echo "| The VASPKIT_UTILITIES_PATH variable has been added.                    |"
fi
   echo "| The old environment variables have been backed up to ~/.bashrc.bk file |"
   echo "+------------------------------------------------------------------------+"
   echo ' The last step left to complete installation. '
   echo ' Please run source ~/.bashrc '
