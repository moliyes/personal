#!/bin/bash

for i in ST MG D3 PU GW DC BD EC FD NE FQ SR SO H6 MD BS EL OP PC DT DM LR
  do
   (echo "101" ; echo ${i} )| ../../src/vaspkit
   mv INCAR ${i}
 done