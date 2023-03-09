clear all
close all 
clc


% The cmocean colormap, the elvation function to get the upper 'topo'
% colours and the functions to paste the colorbars are defined in this
% path
addpath(genpath(fullfile('colormaps')));


%Generate example function.
x = linspace(-10,10,100);
y = linspace(-10,10,100);
[X,Y] = meshgrid(x,y);
Z = abs(sin(X) + cos(Y)).*exp(-0.02.*(X.^2+Y.^2))+2.*exp(-0.04.*(X.^2+Y.^2))-1.2;
s=surf(X,Y,Z);
set(s, 'EdgeColor', 'None','LineWidth',1.,'FaceColor','interp');


level=0; %choose the value for at which the colormaps get 'pasted'
min_caxis=-3; %minimal colorbar value
max_caxis=2;%maximal colorbar value

caxis([min_caxis max_caxis]);
stich_point=100.*(level-min_caxis)./(max_caxis-min_caxis);


cmap1=flipud(cmocean('deep')); %Lower colormap
cmap2=elevation(); %Upper colormap

cmap = stiched_colormap(cmap1, cmap2, stich_point); %function to paste the colormaps

colormap(cmap);
view(2)
% add a colorbar
colorbar


%% Interpolation test to see if the colormap is well ineterpolated.
% interp_colormap_test(colormap('jet'),0.2)

%%

function [] = interp_colormap_test(cmap1,sample_factor)

a= cmap1;
figure()
hold on
plot([0:1:255],a(:,1),'.r')
plot([0:1:255],a(:,2),'.g')
plot([0:1:255],a(:,3),'.b')
hold off

cmap=a;

% Set subsampling factor
subsample_factor = sample_factor;

% Compute new array length
new_length = round(subsample_factor * size(cmap, 1));

% Create new array by linearly interpolating between original values
new_cmap = interp1(1:size(cmap, 1), cmap, linspace(1, size(cmap, 1), new_length), 'linear');

% Display original and subsampled colormap sizes
disp(['Original colormap size: ' num2str(size(cmap, 1))]);
disp(['Subsampled colormap size: ' num2str(size(new_cmap, 1))]);

pixels=size(new_cmap, 1);

hold on
plot([0:1:pixels-1]./sample_factor,new_cmap(:,1),'or')
plot([0:1:pixels-1]./sample_factor,new_cmap(:,2),'og')
plot([0:1:pixels-1]./sample_factor,new_cmap(:,3),'ob')
hold off



end


