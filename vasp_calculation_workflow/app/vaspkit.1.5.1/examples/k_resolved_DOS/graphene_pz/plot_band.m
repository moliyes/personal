function plot_band
% First run vaspkit (version => 1.2.3) with task 216, 257 or 285 to get MOMENTUM.grd, ENERGY.grd and WEIGHT.grd 
clc
clear
momentum=load('MOMENTUM.grd');
energy=load('ENERGY.grd');
weight=load('WEIGHT.grd');
momentum_min = min(momentum(:));
momentum_max = max(momentum(:));
energy_min   = min(energy(:));
energy_max   = max(energy(:));
colormap('jet')
set(gca,'Fontsize',20)
fig = pcolor(momentum, energy, weight);
shading interp;
set(fig, 'LineStyle', 'none')
%title(fig_title)
ylabel('Energy (eV)')
ylim([-6 9]);
set(gca,'ytick',-6:3:9)
set(gca, 'XTickLabel', {'K','\Gamma', 'M', 'K'}, 'XTick', [momentum_min 1.543 2.879 momentum_max],'Fontsize',20)  % '\Gamma', 'M', 'K', '\Gamma', 1.137 and 1.793 is read from KLABEL file
line([momentum_min momentum_max], [0 0], 'LineStyle', '--', 'Color', 'w', 'LineWidth',1)                                
line([1 1]*1.543, [energy_min energy_max], 'LineStyle', '--', 'Color', 'w', 'LineWidth',1)                        % 1.137 is read from KLABEL file
line([1 1]*2.879, [energy_min energy_max], 'LineStyle', '--', 'Color', 'w', 'LineWidth',1)                        % 1.793 is read from KLABEL file

