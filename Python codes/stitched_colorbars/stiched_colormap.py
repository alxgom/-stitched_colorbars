
def stiched_colormap(c1, c2, stich_point):
    """
    Creates a modified colormap by stitching together two other colormaps.
    
    Parameters:
        c1 (ndarray): First colormap array (Nx3 or Nx4, where N is the number of colors).
        c2 (ndarray): Second colormap array (Mx3 or Mx4, where M is the number of colors).
        stich_point (float): The point where the two colormaps will be stitched, as a proportion (0.0 to 1.0).

    Returns:
        ListedColormap: A new colormap created by stitching c1 and c2.
    """
    from matplotlib.colors import ListedColormap
    import numpy as np

    # Ensure stitch_point is within valid range
    if not (0.0 < stich_point < 1.0):
        raise ValueError("stich_point must be between 0.0 and 1.0")

    # Set subsampling factors based on the stitch point
    subsample_factor1 = stich_point
    subsample_factor2 = 1 - subsample_factor1

    # Compute new array length and interpolate colors for the first colormap
    new_length1 = round(subsample_factor1 * len(c1))
    new_cmap1 = np.array([np.interp(np.linspace(0, 1, new_length1), np.linspace(0, 1, len(c1)), c1[:, i]) for i in range(c1.shape[1])]).T

    # Compute new array length and interpolate colors for the second colormap
    new_length2 = round(subsample_factor2 * len(c2))
    new_cmap2 = np.array([np.interp(np.linspace(0, 1, new_length2), np.linspace(0, 1, len(c2)), c2[:, i]) for i in range(c2.shape[1])]).T

    # Combine the two parts into one array
    combined_colors = np.vstack((new_cmap1, new_cmap2))

    # Create a new ListedColormap with the combined colors
    cdis = ListedColormap(combined_colors)
    return cdis