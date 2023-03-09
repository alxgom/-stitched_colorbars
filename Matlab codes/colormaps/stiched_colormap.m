function [cdis] = stiched_colormap(cmap1, cmap2, stich_point)
    % % Creates a modified colormap by stitching together two other colormaps.
    % % cmap1: name of first colormap
    % % cmap2: name of second colormap
    % % stich_point: the point where the two colormaps will be stitched (0-100)
    
    % Import necessary libraries
    %import matlab.graphics.*
    
    % Set subsampling factor
    subsample_factor= stich_point/100;
    
    %%% Get colors from first colormap up to stitch point %%%
    
    % Compute new array length
    new_length1 = round(subsample_factor * size(cmap1, 1));
    % Create new array by linearly interpolating between original values
    new_cmap1 = interp1(1:size(cmap1, 1), cmap1, linspace(1, size(cmap1, 1), new_length1), 'linear');
    pixels1=size(new_cmap1, 1);
    
    
    %%% Get colors from second colormap from stitch point to end %%%
    
    % Compute new array length
    subsample_factor2=1-subsample_factor;
    new_length2 = round(subsample_factor2 * size(cmap2, 1));
    
    % Create new array by linearly interpolating between original values
    new_cmap2 = interp1(1:size(cmap2, 1), cmap2, linspace(1, size(cmap2, 1), new_length2), 'linear');
    pixels2=size(new_cmap2, 1);
    disp(['Check total pixels: ' num2str(pixels1+pixels2)]);
    
    cdis=cmap1;
    cdis(1:length(new_cmap1),:,:)=new_cmap1;
    cdis(pixels1+1:pixels1+pixels2,:,:)=new_cmap2;
end

