!Unless otherwise specified, all intermediate quantities are in J/mol or J/mol/K
program Shermo
implicit real*8 (a-h,o-z)
real*8,parameter :: R=8.3144648D0, Kb=1.3806503D-23 !Ideal gas constant (J/mol/K), Boltzmann constant (J/K)
real*8,parameter :: NA=6.02214179D23 !Avogadro constant
real*8,parameter :: au2kcal_mol=627.51D0,au2KJ_mol=2625.5D0,au2J=4.359744575D-18,au2cm_1=219474.6363D0 !Hartree to various units
real*8,parameter :: cal2J=4.184D0 !This is consistent with G09, though 4.186 is more generally accepted
real*8,parameter :: wave2freq=2.99792458D10 !cm^-1 to s^-1 (Hz)
real*8,parameter :: h=6.62606896D-34 !Planck constant, in J*s
real*8,parameter :: amu2kg=1.66053878D-27
real*8,parameter :: pi=3.141592653589793D0
real*8,parameter :: b2a=0.52917720859D0 !Bohr to Angstrom
real*8,allocatable :: xyz(:,:),freq(:),wavenum(:),mass(:)
real*8 inert1,inert2,inert3
character,allocatable :: elem(:)*2
character :: c80*80
character*2 :: name2ind(1:118)=(/ "H ","He", &
"Li","Be","B ","C ","N ","O ","F ","Ne", & !3~10
"Na","Mg","Al","Si","P ","S ","Cl","Ar", & !11~18
"K ","Ca","Sc","Ti","V ","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr", & !19~36
"Rb","Sr","Y ","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I ","Xe", & !37~54
"Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu", & !55~71
"Hf","Ta","W ","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn", & !72~86
"Fr","Ra","Ac","Th","Pa","U ","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr", & !87~103
"Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Ut","Fl","Up","Lv","Us","Uo" /) !104~all  Such as Uuo/Uup is replaced by Uo/Up


write(*,*) "Shermo: A utility to calculate various thermodynamic properties"
write(*,*) "Programmed by Sobereva (sobereva@sina.com)"
write(*,*) "First release: 2015-Dec-26  Last update: 2016-Jan-8"
write(*,*)


open(10,file="Shermo.ini",status="old")
read(10,*)
read(10,*)
read(10,*) T  !Temperature
write(*,"(' Temperature(K):',f12.3)") T
read(10,*)
read(10,*) P  !Pressure
write(*,"(' Pressure(Atm):',f12.3)") P
P=P*101325 !From Atm to Pa
read(10,*)
read(10,*) nRotsym  !Rotational symmetry number, negative for linear molecule
write(*,"(' Rotational symmetry number:',i2)") abs(nRotsym)
read(10,*)
if (nRotsym>0) then
	read(10,*) inert1,inert2,inert3  !Moments of inertia for non-linear molecule
	write(*,*) "Note: This is a non-linear molecule"
	write(*,"(' Moments of inertia: ',3f12.6,' amu*Bohr^2')") inert1,inert2,inert3
	rotcst1=h/(8D0*pi**2*inert1*amu2kg*(b2a*1D-10)**2) !in 1Hz=1/s
	rotcst2=h/(8D0*pi**2*inert2*amu2kg*(b2a*1D-10)**2)
	rotcst3=h/(8D0*pi**2*inert3*amu2kg*(b2a*1D-10)**2)
	write(*,"(' Rotational constant:',3f12.6,' GHz')") rotcst1/1D9,rotcst2/1D9,rotcst3/1D9
	rotT1=rotcst1*h/kb
	rotT2=rotcst2*h/kb
	rotT3=rotcst3*h/kb
	write(*,"(' Rotational temperature:',3f12.6,' K')") rotT1,rotT2,rotT3
else if (nRotsym<0) then
	read(10,*) inert1  !Moments of inertia for linear molecule
	write(*,*) "Note: This is a linear molecule"
	write(*,"(' Moment of inertia: ',f12.6,' amu*Bohr^2')") inert1
	rotcst1=h/(8D0*pi**2*inert1*amu2kg*(b2a*1D-10)**2) !in 1Hz=1/s
	write(*,"(' Rotational constant:',f12.6,' GHz')") rotcst1/1D9
	rotT1=rotcst1*h/kb
	write(*,"(' Rotational temperature:',f12.6,' K')") rotT1
end if
read(10,*)
read(10,*) nSpinmulti  !Spin multiplicity
write(*,"(' Spin multiplicity:',i2)") nSpinmulti
read(10,*)
read(10,*) natm  !The number of atoms
write(*,"(' The number of atoms:',i5)") natm
!Load elements and XYZ coordinates
allocate(xyz(natm,3),elem(natm))
read(10,*)
do iatm=1,natm
	read(10,*) elem(iatm),xyz(iatm,:)
end do
!Load frequencies
read(10,*)
read(10,*) iprtvib
nfreq=3*natm-6
if (nRotsym<0) nfreq=3*natm-5
allocate(freq(nfreq),wavenum(nfreq)) !Frequencies (s^-1) and wavenumber (cm^-1)
write(*,*)
write(*,"(' The number of frequencies:',i5)") nfreq
read(10,*)
do ifreq=1,nfreq
	read(10,*) wavenum(ifreq)
	freq(ifreq)=wavenum(ifreq)*wave2freq
end do
!Determine masses
read(10,*)
allocate(mass(natm))
mass=0
do while(.true.)
	read(10,*,iostat=ierror) c80,tmpmass
	if (ierror/=0) exit
	if (iachar(c80(1:1))>=48.and.iachar(c80(1:1))<=57) then
		read(c80,*) iatm
		mass(iatm)=tmpmass
	else
		do iatm=1,natm
			if (c80(1:2)==elem(iatm)) mass(iatm)=tmpmass 
		end do
	end if
end do
if (any(mass==0)) write(*,*) "Warning: Mass of some atoms are not specified!"
do iatm=1,natm
	write(*,"(' Atom:',i5,'   Mass:',f8.3,' amu')") iatm,mass(iatm)
end do
totmass=sum(mass(:))
write(*,"(' Total mass:',f12.6,' amu')") totmass
close(10)



!Loading finished, now output results
write(*,"(/,a)") " Note: Only for translation motion, contribution to CV and U are different to CP and H, respectively"

write(*,*)
write(*,*) "                         ======= Translation ======="
write(*,*)
q_trans=(2*pi*(totmass*amu2kg)*kb*T/h**2)**(3D0/2D0)*R*T/P
CV_trans=3D0/2D0*R
CP_trans=5D0/2D0*R
U_trans=3D0/2D0*R*T
H_trans=5D0/2D0*R*T
S_trans=R*(log(q_trans/NA)+5D0/2D0)

write(*,"(' Translational q(T):  ',E18.6)") q_trans
write(*,"(' Translational q(T)/N:',E18.6)") q_trans/NA
write(*,"(' Translational U(T):',f12.6,' kcal/mol')") U_trans/cal2J/1000
write(*,"(' Translational H(T):',f12.6,' kcal/mol')") H_trans/cal2J/1000
write(*,"(' Translational CV:  ',f12.6,' cal/mol/K')") CV_trans/cal2J
write(*,"(' Translational CP:  ',f12.6,' cal/mol/K')") CP_trans/cal2J
write(*,"(' Translational S(T):',f12.6,' cal/mol/K')") S_trans/cal2J

write(*,*)
write(*,*) "                         ========= Rotation ========"
write(*,*)
!Convert moment of inertia from a.u.(amu*bohr^2) to kg*m^2
inert1=inert1*amu2kg*(b2a*1D-10)**2
inert2=inert2*amu2kg*(b2a*1D-10)**2
inert3=inert3*amu2kg*(b2a*1D-10)**2
if (nRotsym<0) then !Linear molecule
	q_rot=8*pi**2*inert1*kb*T/abs(nRotsym)/h**2
	U_rot=R*T
	CV_rot=R
	S_rot=R*(log(q_rot)+1)
else !Non-linear molecule
	q_rot=8*pi**2/nRotsym/h**3*(2*pi*kb*T)**(3D0/2D0)*dsqrt(inert1*inert2*inert3)
	U_rot=3D0*R*T/2D0
	CV_rot=3D0*R/2D0
	S_rot=R*(log(q_rot)+3D0/2D0)
end if
write(*,"(' Rotational q(T):',E18.6)") q_rot
write(*,"(' Rotational U(T):',f12.6,' kcal/mol')") U_rot/cal2J/1000
write(*,"(' Rotational CV:  ',f12.6,' cal/mol/K')") CV_rot/cal2J
write(*,"(' Rotational S(T):',f12.6,' cal/mol/K')") S_rot/cal2J


write(*,*)
write(*,*) "                         ======== Vibration ========"
write(*,*)
where (freq<0) freq=0 !Ignore imaginary frequencies
where (wavenum<0) wavenum=0 !Ignore imaginary frequencies

if (iprtvib==1) then
	write(*,*) " Mode  Wavenumber   Freq     Vib. Temp.   q(V=0)      q(BOT)"
	write(*,*) "         cm^-1      GHz          K"
end if
qvib_v0=1
qvib_bot=1
do i=1,nfreq
	if (freq(i)==0) cycle !Ignore imaginary frequency
	tmpv0=1/( 1-exp( -h*freq(i)/(Kb*T) ) )
	tmpbot=exp(-h*freq(i)/(Kb*2*T)) / (1-exp( -h*freq(i)/(Kb*T) ))
	qvib_v0=qvib_v0*tmpv0
	qvib_bot=qvib_bot*tmpbot
	if (iprtvib==1) write(*,"(i5,f10.2,E13.4,f10.2,2f12.6)") i,wavenum(i),freq(i)/1D9,freq(i)*h/Kb,tmpv0,tmpbot
end do

if (iprtvib==1) then
	write(*,*)
	write(*,*) " Mode  Wavenumber     ZPE      U(T)-U(0)    U(T)      CV(T)       S(T)"
	write(*,*) "         cm^-1      kcal/mol   kcal/mol   kcal/mol  cal/mol/K  cal/mol/K"
end if
U_vib_heat=0
CV_vib=0
S_vib=0
do i=1,nfreq
	if (freq(i)==0) cycle !Ignore imaginary frequency
	prefac=h*freq(i)/(Kb*T)
	term=exp(-h*freq(i)/(Kb*T))
	tmp1=R*T*prefac*term/(1-term)
	U_vib_heat=U_vib_heat+tmp1
	tmp2=R*prefac**2 * term/(1-term)**2
	CV_vib=CV_vib+tmp2
	tmp3=R*(prefac*term/(1-term)-log(1-term))
	S_vib=S_vib+tmp3
	tmpZPE=wavenum(i)/au2cm_1*au2kcal_mol/2 !kcal/mol
	if (iprtvib==1) write(*,"(i5,6f11.3)") i,wavenum(i),tmpZPE,tmp1/1000/cal2J,tmp1/1000/cal2J+tmpZPE,tmp2/cal2J,tmp3/cal2J
end do
ZPE=h*sum(freq)/2*NA
U_vib=U_vib_heat+ZPE

write(*,*)
write(*,"(' Vibrational q(V=0):   ',E18.6)") qvib_v0
write(*,"(' Vibrational q(BOT):   ',E18.6)") qvib_bot
write(*,"(' Vibrational ZPE:',f12.6,' a.u.',f12.3,' kcal/mol',f12.3,' kJ/mol')") ZPE/1000/au2KJ_mol,ZPE/1000/cal2J,ZPE/1000
write(*,"(' Vibrational U(T)-U(0):',f12.6,' kcal/mol')") U_vib_heat/1000/cal2J
write(*,"(' Vibrational U(T):     ',f12.6,' kcal/mol')") U_vib/1000/cal2J
write(*,"(' Vibrational CV(T):    ',f12.6,' cal/mol/K')") CV_vib/cal2J
write(*,"(' Vibrational S(T):     ',f12.6,' cal/mol/K')") S_vib/cal2J


write(*,*)
write(*,*) "                        ======== Electron spin ========"
write(*,*)
write(*,"(a)") " Note: Thermal excitation of electronic states is not taken into account, so electronic contribution to CV and U are zero"
CV_ele=0
U_ele=0
q_ele=nSpinmulti
S_ele=R*log(q_ele)
write(*,"(' Electronic q: ',f12.6)") q_ele
write(*,"(' Electronic S: ',f12.6,' cal/mol/K')") S_ele/cal2J


write(*,*)
write(*,*) "                          ==========================="
write(*,*) "                          ========== Total =========="
write(*,*) "                          ==========================="
write(*,*)
write(*,"(' Total q(V=0):     ',E18.6)") q_trans*q_rot*qvib_v0*q_ele
write(*,"(' Total q(BOT):     ',E18.6)") q_trans*q_rot*qvib_BOT*q_ele
write(*,"(' Total q(V=0)/N:   ',E18.6)") q_trans*q_rot*qvib_v0*q_ele/NA
write(*,"(' Total q(BOT)/N:   ',E18.6)") q_trans*q_rot*qvib_BOT*q_ele/NA
CV_tot=CV_trans+CV_rot+CV_vib+CV_ele
write(*,"(' Total CV(T):  ',f12.6,' cal/mol/K')") CV_tot/cal2J
CP_tot=CP_trans+CV_rot+CV_vib+CV_ele
write(*,"(' Total CP(T):  ',f12.6,' cal/mol/K')") CP_tot/cal2J
S_tot=S_trans+S_rot+S_vib+S_ele
write(*,"(' Total S(T):   ',f12.6,' cal/mol/K')") S_tot/cal2J
thermU=U_trans+U_rot+U_vib+U_ele
write(*,"(' Thermal correction to U(T):',f12.3,' kcal/mol',f12.6,' a.u.')") thermU/1000/cal2J,thermU/1000/au2kJ_mol
thermH=H_trans+U_rot+U_vib+U_ele
write(*,"(' Thermal correction to H(T):',f12.3,' kcal/mol',f12.6,' a.u.')") thermH/1000/cal2J,thermH/1000/au2kJ_mol
thermG=thermH-T*S_tot
write(*,"(' Thermal correction to G(T):',f12.3,' kcal/mol',f12.6,' a.u.')") thermG/1000/cal2J,thermG/1000/au2kJ_mol


write(*,*)
write(*,*) "Finished, press Enter to exit"
read(*,*)

end program