for i in *.cif
do
prefix=`echo $i|awk  -F '.'  '{print $1}'`
cif2cell $i -p vasp --no-reduce --vasp-format=5
cp POSCAR ${prefix}_c5.vasp
cif2cell $i -p vasp --vasp-format=5
cp POSCAR ${prefix}_p5.vasp
done
