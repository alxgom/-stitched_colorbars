"""
Stitched Colormaps — Python Example
====================================
Reproduces the MATLAB example: generates a 2D surface plot and applies
two different stitched colormap combinations at a chosen threshold level.

Requires: matplotlib, numpy, cmocean (pip install cmocean)
"""

import sys
import os

import matplotlib.pyplot as plt
import numpy as np

# Allow importing the local package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stitched_colorbars import stitch_colormaps
from stitched_colorbars.interpolate_colormap import interpolate_colormap

# ---------------------------------------------------------------------------
# Generate the same example surface as the MATLAB script
# Z = |sin(X) + cos(Y)| * exp(-0.02*(X²+Y²)) + 2*exp(-0.04*(X²+Y²)) - 1.2
# ---------------------------------------------------------------------------
x = np.linspace(-10, 10, 300)
y = np.linspace(-10, 10, 300)
X, Y = np.meshgrid(x, y)
Z = (np.abs(np.sin(X) + np.cos(Y))
     * np.exp(-0.02 * (X**2 + Y**2))
     + 2 * np.exp(-0.04 * (X**2 + Y**2))
     - 1.2)

level = 0  # value at which the colormaps are stitched
z_min, z_max = Z.min(), Z.max()
stitch_point = (level - z_min) / (z_max - z_min)

SAVE_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(SAVE_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Figure 1 — cmocean deep (flipped) below + terrain above
# ---------------------------------------------------------------------------
try:
    import cmocean
    cmap1_colors = cmocean.cm.deep_r  # flipped deep
    cmap1_name = "cmocean deep (reversed)"
    # Replicate MATLAB's elevation(): upper half of cmocean 'topo'
    cmap2_colors = interpolate_colormap(cmocean.cm.topo, 256, vmin=0.5, vmax=1.0)
    cmap2_name = "cmocean topo (upper half)"
except ImportError:
    cmap1_colors = "Blues_r"  # fallback if cmocean is not installed
    cmap1_name = "Blues_r"
    cmap2_colors = interpolate_colormap("gist_earth", 256, vmin=0.25, vmax=0.9)
    cmap2_name = "gist_earth"

fig1, ax1 = plt.subplots(figsize=(10, 7))
cmap_topo = stitch_colormaps(cmap1_colors, cmap2_colors, stitch_point)
im1 = ax1.pcolormesh(X, Y, Z, cmap=cmap_topo, shading="auto")
fig1.colorbar(im1, ax=ax1, label="Z value")
ax1.set_title(f"Stitched colormap: {cmap1_name} + {cmap2_name}  (split at Z={level})")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
fig1.savefig(os.path.join(SAVE_DIR, "topo_example_python.png"),
             dpi=200, bbox_inches="tight")

# ---------------------------------------------------------------------------
# Figure 2 — gray below + jet above
# ---------------------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(10, 7))
cmap_jet = stitch_colormaps("gray", "jet", stitch_point)
im2 = ax2.pcolormesh(X, Y, Z, cmap=cmap_jet, shading="auto")
fig2.colorbar(im2, ax=ax2, label="Z value")
ax2.set_title(f"Stitched colormap: gray + jet  (split at Z={level})")
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
fig2.savefig(os.path.join(SAVE_DIR, "jet_example_python.png"),
             dpi=200, bbox_inches="tight")

plt.show()
