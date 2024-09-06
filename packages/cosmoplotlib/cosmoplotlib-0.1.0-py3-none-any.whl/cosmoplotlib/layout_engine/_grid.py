"""
Implementation of GridLayoutEngine.
"""

from matplotlib import rcParams
from matplotlib.figure import Figure
from matplotlib.backend_bases import RendererBase
from matplotlib.layout_engine import LayoutEngine
from matplotlib.transforms import Bbox


def _fix_sup_positions(fig: Figure, renderer: RendererBase) -> None:
    """
    Fix the positions of subtitle, supxlabel, and supylabel.
    """

    for subfig in fig.subfigs:
        _fix_sup_positions(subfig, renderer)

    # get tight bbox of figure (in inches)
    fig_in = fig.get_tightbbox(renderer)

    # expand by padding for title and label (in points)
    labelpad = rcParams["axes.labelpad"] / 72
    titlepad = rcParams["axes.titlepad"] / 72
    bbox_in = Bbox.from_extents(
        fig_in.x0 - labelpad,
        fig_in.y0 - labelpad,
        fig_in.x1,
        fig_in.y1 + titlepad,
    )

    # transform to figure coordinates
    bbox_pix = fig.dpi_scale_trans.transform_bbox(bbox_in)
    bbox = bbox_pix.transformed(fig.transFigure.inverted())

    # update suptitle position
    if (
        fig._suptitle is not None
        and fig._suptitle.get_in_layout()
        and getattr(fig._suptitle, "_autopos", False)
    ):
        x, _ = fig._suptitle.get_position()
        fig._suptitle.set_position((x, bbox.y1))
        fig._suptitle.set_va("bottom")

    # update supxlabel position
    if (
        fig._supxlabel is not None
        and fig._supxlabel.get_in_layout()
        and getattr(fig._supxlabel, "_autopos", False)
    ):
        x, _ = fig._supxlabel.get_position()
        fig._supxlabel.set_position((x, bbox.y0))
        fig._supxlabel.set_va("top")

    # update supylabel position
    if (
        fig._supylabel is not None
        and fig._supylabel.get_in_layout()
        and getattr(fig._supylabel, "_autopos", False)
    ):
        _, y = fig._supylabel.get_position()
        fig._supylabel.set_position((bbox.x0, y))
        fig._supylabel.set_ha("right")


class GridLayoutEngine(LayoutEngine):
    """
    Layout engine for grids with potentially empty panels.
    """

    _adjust_compatible = True
    _colorbar_gridspec = True

    def execute(self, fig: Figure) -> None:
        """
        Prepare a grid layout for drawing.
        """

        # finalise axes
        for ax in fig.axes:
            # disable all axes with no data
            if not ax.has_data():
                ax.axis("off")
            else:
                # layout looks best with ticks going in from all sides
                ax.tick_params(
                    axis="both",
                    which="both",
                    direction="in",
                    top=True,
                    bottom=True,
                    left=True,
                    right=True,
                )

        # no spacing between panels
        fig.subplots_adjust(
            left=0.0,
            bottom=0.0,
            right=1.0,
            top=1.0,
            wspace=0.0,
            hspace=0.0,
        )

        # position suptitle, supxlabel, supylabel outside panels
        renderer = fig._get_renderer()
        _fix_sup_positions(fig, renderer)
