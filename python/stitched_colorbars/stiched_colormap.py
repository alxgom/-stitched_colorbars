"""Stitch two colormaps into one at a configurable split point."""

from __future__ import annotations

from typing import Union

import numpy as np
from matplotlib.colors import ListedColormap


def _resolve_colormap(cmap, n: int = 256) -> np.ndarray:
    """Convert a colormap name, Colormap object, or array into an Nx3/Nx4 numpy array.

    Parameters:
        cmap: A matplotlib colormap name (e.g. ``"viridis"``), a
              ``matplotlib.colors.Colormap`` instance, or an Nx3/Nx4 array.
        n:    Number of colors to sample when *cmap* is a string or Colormap.

    Returns:
        An (N, 3) or (N, 4) numpy array of color values.
    """
    from matplotlib.colors import Colormap

    if isinstance(cmap, str):
        import matplotlib.pyplot as plt

        return np.array(plt.colormaps[cmap](np.linspace(0, 1, n)))
    if isinstance(cmap, Colormap):
        return np.array(cmap(np.linspace(0, 1, n)))
    return np.asarray(cmap)


def stiched_colormap(
    c1: Union[str, np.ndarray],
    c2: Union[str, np.ndarray],
    stich_point: float,
) -> ListedColormap:
    """Create a colormap by stitching two colormaps at a given split point.

    Parameters:
        c1:          First colormap — a name (e.g. ``"Blues"``) or an Nx3/Nx4
                     array. Used for the **lower** portion of the result.
        c2:          Second colormap — a name or array. Used for the **upper**
                     portion.
        stich_point: Where to split, as a proportion **0.0 – 1.0**.
                     For example ``0.3`` means 30 % of the colorbar comes from
                     *c1* and 70 % from *c2*.

    Returns:
        A ``ListedColormap`` ready to pass to matplotlib.

    Raises:
        ValueError: If *stich_point* is not strictly between 0 and 1.

    Example::

        >>> from stitched_colorbars import stitch_colormaps
        >>> cmap = stitch_colormaps("cmo.deep", "terrain", 0.4)
        >>> plt.imshow(data, cmap=cmap)
    """
    # Resolve inputs
    c1 = _resolve_colormap(c1)
    c2 = _resolve_colormap(c2)

    # Validate
    if not (0.0 < stich_point < 1.0):
        raise ValueError("stich_point must be between 0.0 and 1.0 (exclusive)")

    # Interpolate each half
    n1 = round(stich_point * len(c1))
    new_cmap1 = np.array([
        np.interp(np.linspace(0, 1, n1), np.linspace(0, 1, len(c1)), c1[:, i])
        for i in range(c1.shape[1])
    ]).T

    n2 = round((1 - stich_point) * len(c2))
    new_cmap2 = np.array([
        np.interp(np.linspace(0, 1, n2), np.linspace(0, 1, len(c2)), c2[:, i])
        for i in range(c2.shape[1])
    ]).T

    return ListedColormap(np.vstack((new_cmap1, new_cmap2)))


# Convenience alias with corrected spelling
stitch_colormaps = stiched_colormap