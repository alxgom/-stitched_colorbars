

function [cdis] = elevation()
% cm=elevation(flipud(cmocean('topo')),0.5);
cmap=cmocean('topo');
% Create new array by linearly interpolating between original values
new_cmap = interp1(128:size(cmap, 1), cmap(128:256,:,:), linspace(1, 128, 256)+128, 'linear');
cdis=new_cmap;
end
