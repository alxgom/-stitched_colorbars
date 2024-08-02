def interpolate_colormap(cmap, num_colors, vmin=0, vmax=1):
    """
    Interpolates an existing colormap to create a new colormap with a specified number of colors
    and within a specified range of the original colormap.
    
    Parameters:
        cmap (ndarray): Original colormap array (Nx3 or Nx4, where N is the number of colors).
        num_colors (int): The number of colors in the new interpolated colormap.
        vmin (float, optional): Minimum value (0 to 1) in the range of the original colormap to interpolate from.
        vmax (float, optional): Maximum value (0 to 1) in the range of the original colormap to interpolate to.

    Returns:
        ndarray: The new interpolated colormap array.
    """
    import numpy as np
    
    # Ensure vmin and vmax are within valid range
    if not (0 <= vmin < vmax <= 1):
        raise ValueError("vmin and vmax must be between 0 and 1, and vmin must be less than vmax")

    # Generate the interpolated colormap within the specified range
    interp_range = np.linspace(vmin, vmax, num_colors)
    interpolated_cmap = np.array([np.interp(interp_range, np.linspace(0, 1, len(cmap)), cmap[:, i]) for i in range(cmap.shape[1])]).T
    
    return interpolated_cmap