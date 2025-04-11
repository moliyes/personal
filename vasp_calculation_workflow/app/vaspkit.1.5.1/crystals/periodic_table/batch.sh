for i in `ls *.cif`
do
# --no-reduce means that do not reduce to the primitive cell.
cif2cell $i --vasp-format 5 -p vasp --no-reduce 
mv POSCAR  ${i%%.cif}_c5.vasp

cif2cell $i --vasp-format 5 -p vasp
mv POSCAR  ${i%%.cif}_p5.vasp
done

