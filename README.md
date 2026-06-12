# multipole-symmetry

Figure-generation source for a review article by A. C. Berceanu and
A. Del Dotto, to appear in *Symmetry* (MDPI), Special Issue "Symmetry in
Beam-Plasma Physics."

The article itself contains no new experimental or simulation data; these
scripts evaluate analytic models and reproduce or restyle published
figures, with full attribution to the original works.

## Contents

| Source | Output | Provenance |
|---|---|---|
| `azimuthal_modes.py` | Figure 1 | Original schematic of the m = 0, 1, 2, 3 channels of the blowout wake. |
| `migliorati_chromatic.tex` | Figure 2 | Analytic chromatic-filamentation model from Migliorati et al., *Phys. Rev. ST Accel. Beams* **16**, 011302 (2013), Eq. (5). |
| `deldotto_hi_smi.tex` | Figure 3 | Adapted from Del Dotto et al., *Phys. Plasmas* **29**, 113104 (2022), Fig. 4(a). Data points are approximate digitisations of the published figure. |
| `diederichs_mixing.tex` | Figure 4 | Stylised redrawing of Diederichs et al., *Phys. Rev. Lett.* **135**, 015001 (2025), Fig. 2(b), using a dimensionless detuning parameter. |

## Build

The Python figure has its dependencies declared inline (PEP 723) and is
intended to be run with [`uv`](https://github.com/astral-sh/uv):

```sh
uv run azimuthal_modes.py
```

The TikZ figures compile with any TeX Live distribution that includes
`pgfplots`:

```sh
pdflatex migliorati_chromatic.tex
pdflatex deldotto_hi_smi.tex
pdflatex diederichs_mixing.tex
```

## License

Released under the Creative Commons Attribution 4.0 International license
(CC BY 4.0), matching the license of the journal article. See `LICENSE`.
