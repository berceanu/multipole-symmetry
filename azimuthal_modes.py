#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""
Figure 1 (§2): azimuthal-mode decomposition of the transverse wake force in
the idealised blowout regime.

Each panel shows the transverse force field F_perp of the m-th harmonic as
a streamplot, coloured by amplitude, confined to the circular blowout
cross-section r <= r_b. The sourcing witness moment T_m that populates that
harmonic is overlaid in a distinct colour.

Harmonic forces derive from the scalar wake potential Psi_m proportional to
r^m cos(m phi). The transverse force is F = -grad Psi, giving:
    m=0 (ion-column focusing):   F = -(k_p^2 / 2) r \hat r, linear in r.
    m=1 (dipole):                F = const, uniform transverse kick.
    m=2 (quadrupole):            F linear in r, focusing/defocusing by plane.
    m=3 (hexapole):              F quadratic in r, hexapolar angular pattern.

Build:  uv run azimuthal_modes.py
Output: azimuthal_modes.pdf
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse

# Grid in k_p units; blowout radius r_b = 1 in these units.
r_b = 1.0
N = 220
extent = 1.15
x = np.linspace(-extent, extent, N)
y = np.linspace(-extent, extent, N)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
PHI = np.arctan2(Y, X)
mask = R <= r_b

# Force components for Psi_m = r^m cos(m phi), F = -grad Psi.
# In Cartesian: Psi_m = Re[(x + i y)^m] for cos(m phi) * r^m.
# F_x = -d/dx Psi, F_y = -d/dy Psi. Use closed forms per m.
def force(m):
    if m == 0:
        # Ion-column focusing: Psi_0 = (1/4) r^2 (treating k_p = 1).
        Fx, Fy = -0.5 * X, -0.5 * Y
    elif m == 1:
        # Hose-sign dipole wake: force aligned with centroid displacement
        # (positive feedback), so F points in +x when the overlay shows
        # the centroid displaced in +x.
        Fx, Fy = np.ones_like(X), np.zeros_like(Y)
    elif m == 2:
        # Psi_2 = x^2 - y^2 => F = (-2x, +2y).
        Fx, Fy = -2.0 * X, 2.0 * Y
    elif m == 3:
        # Psi_3 = x^3 - 3 x y^2 => F = -(3x^2 - 3y^2, -6 x y) = (-3(x^2-y^2), 6 x y).
        Fx, Fy = -3.0 * (X**2 - Y**2), 6.0 * X * Y
    else:
        raise ValueError(m)
    return Fx, Fy

# Sourcing moment overlays.
def draw_moment(ax, m, color="#111111"):
    kw = dict(lw=1.6, color=color, zorder=5)
    if m == 0:
        # Round, on-axis witness.
        ax.add_patch(Circle((0, 0), 0.22, fill=False, **kw))
    elif m == 1:
        # Centroid-displaced round witness.
        dx = 0.35
        ax.add_patch(Circle((dx, 0), 0.22, fill=False, **kw))
        ax.annotate("", xy=(dx, 0), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.3),
                    zorder=6)
    elif m == 2:
        # Elliptical witness (quadrupole moment).
        ax.add_patch(Ellipse((0, 0), 0.7, 0.32, angle=0, fill=False, **kw))
    elif m == 3:
        # Trefoil witness: r(phi) = r0 (1 + eps cos 3 phi).
        r0, eps = 0.35, 0.45
        phi = np.linspace(0, 2 * np.pi, 400)
        rr = r0 * (1.0 + eps * np.cos(3 * phi))
        xs = rr * np.cos(phi)
        ys = rr * np.sin(phi)
        ax.plot(xs, ys, **kw)

labels = [
    (r"$m = 0$", "axisymmetric ion-column focusing"),
    (r"$m = 1$", "dipole: uniform centroid kick"),
    (r"$m = 2$", "quadrupole: $\\varepsilon_x$--$\\varepsilon_y$ coupling"),
    (r"$m = 3$", "hexapole: predicted $T_3$ response"),
]

fig, axes = plt.subplots(1, 4, figsize=(11.2, 3.1))

for m, (ax, (top, bot)) in enumerate(zip(axes, labels)):
    Fx, Fy = force(m)
    speed = np.sqrt(Fx**2 + Fy**2)
    # Mask outside bubble (streamplot respects NaN).
    Fxm = np.where(mask, Fx, np.nan)
    Fym = np.where(mask, Fy, np.nan)
    spm = np.where(mask, speed, np.nan)
    # Per-panel normalisation so all four are visually comparable.
    smax = np.nanpercentile(spm, 95)
    lw = 0.4 + 1.8 * (spm / max(smax, 1e-9))
    # m=1 is a uniform field: streamplot would pack parallel lines to max
    # density. Use quiver instead so the uniform kick is legible.
    if m == 1:
        step = 14
        Xs = X[::step, ::step]
        Ys = Y[::step, ::step]
        Fxs = Fxm[::step, ::step]
        Fys = Fym[::step, ::step]
        mk = np.isfinite(Fxs) & np.isfinite(Fys)
        ax.quiver(Xs[mk], Ys[mk], Fxs[mk], Fys[mk],
                  color="#5a1a5c", scale=18, width=0.007,
                  headwidth=4, headlength=5, pivot="mid")
    else:
        ax.streamplot(X, Y, Fxm, Fym, color=spm, cmap="magma_r",
                      density=1.15, linewidth=lw, arrowsize=0.9,
                      norm=plt.Normalize(vmin=0, vmax=smax))
    # Bubble boundary.
    ax.add_patch(Circle((0, 0), r_b, fill=False, color="black", lw=1.3, zorder=4))
    # Sourcing moment overlay.
    draw_moment(ax, m, color="#1f77b4")
    # Axes styling.
    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    # Title stack: m number (top), descriptor (bottom).
    ax.set_title(top, fontsize=12, pad=6)
    ax.text(0.5, -0.08, bot, transform=ax.transAxes,
            ha="center", va="top", fontsize=9)
    # k_p r scale tick: a small label at the bubble edge.
    ax.text(r_b + 0.03, 0, r"$k_p r = 1$", fontsize=7, color="gray",
            ha="left", va="center")

plt.tight_layout()
plt.savefig("azimuthal_modes.pdf", bbox_inches="tight")
print("wrote azimuthal_modes.pdf")
