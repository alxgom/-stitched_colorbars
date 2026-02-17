"""Resample a colormap to a different number of colors or a sub-range."""

from __future__ import annotations

from typing import Union

import numpy as np
from matplotlib.colors import ListedColormap


def _resolve_colormap(cmap, n: int = 256) -> np.ndarray:
    """Convert a colormap name, Colormap object, or array into an Nx3/Nx4 numpy array."""
    from matplotlib.colors import Colormap

    if isinstance(cmap, str):
        import matplotlib.pyplot as plt

        return np.array(plt.colormaps[cmap](np.linspace(0, 1, n)))
    if isinstance(cmap, Colormap):
        return np.array(cmap(np.linspace(0, 1, n)))
    return np.asarray(cmap)


def interpolate_colormap(
    cmap: Union[str, np.ndarray],
    num_colors: int,
    vmin: float = 0,
    vmax: float = 1,
) -> ListedColormap:
    """Resample a colormap to *num_colors*, optionally from a sub-range.

    Parameters:
        cmap:       A matplotlib colormap name (e.g. ``"viridis"``) or an
                    Nx3/Nx4 array of RGB(A) values.
        num_colors: Number of colors in the output colormap.
        vmin:       Start of the range to sample from (0–1, default ``0``).
        vmax:       End of the range to sample from (0–1, default ``1``).

    Returns:
        A ``ListedColormap`` with *num_colors* evenly spaced colors sampled
        from the *vmin*–*vmax* portion of *cmap*.

    Raises:
        ValueError: If *vmin* / *vmax* are outside [0, 1] or mis-ordered.

    Example::

        >>> from stitched_colorbars import interpolate_colormap
        >>> warm_half = interpolate_colormap("coolwarm", 128, vmin=0.5, vmax=1.0)
    """
    cmap = _resolve_colormap(cmap)

    if not (0 <= vmin < vmax <= 1):
        raise ValueError(
            "vmin and vmax must satisfy 0 <= vmin < vmax <= 1"
        )

    interp_range = np.linspace(vmin, vmax, num_colors)
    colors = np.array([
        np.interp(interp_range, np.linspace(0, 1, len(cmap)), cmap[:, i])
        for i in range(cmap.shape[1])
    ]).T

    return ListedColormap(colors)