"""
Implementation of functions for creating plots.
"""

from typing import Any, Literal, Tuple

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from ..layout_engine import GridLayoutEngine


def gridplots(
    nrows: int,
    ncols: int,
    *,
    width: float = 1.0,
    height: float = 1.0,
    sharex: bool | Literal["none", "all", "row", "col"] = False,
    sharey: bool | Literal["none", "all", "row", "col"] = False,
) -> Tuple[Figure, Any]:
    """
    Create a tight grid of plots.
    """

    return plt.subplots(
        nrows,
        ncols,
        figsize=(ncols * width, nrows * height),
        sharex=sharex,
        sharey=sharey,
        squeeze=False,
        layout=GridLayoutEngine(),
    )
