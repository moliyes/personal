% An example for the visualization of 3D-bandstructure for graphene by using MATLAB
clc
clear 

kx_mesh=load('KX.grd');      
ky_mesh=load('KY.grd');   
CBM_mesh=load('BAND_LUMO.grd');         
VBM_mesh=load('BAND_HOMO.grd');
surf(kx_mesh,ky_mesh,VBM_mesh);
hold on
surf(kx_mesh,ky_mesh,CBM_mesh);
contourf(kx_mesh,ky_mesh,CBM_mesh,4)
grid on
hold off
xlabel('$\it{k}_{x} (\textrm{1/\AA})$','Interpreter','latex','Fontname','TimesNewRoman')
ylabel('$\it{k}_{y} (\textrm{1/\AA})$','Interpreter','latex','Fontname','TimesNewRoman')
zlabel('Energy (eV)')
axis image
axis vis3d
shading interp;
colormap(hsv);
set(gca,'FontSize',18);
hold off
zlim([-6,6]);
