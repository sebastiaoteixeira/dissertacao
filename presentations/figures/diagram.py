"""Shared vocabulary of the deck's block diagrams: palette, blocks, arrows and export."""
from typing import NamedTuple

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

GREEN, LIGHT, NAVY, GREY, INK, MUTED = "#275727", "#e3eee3", "#254061", "#8a8a8a", "#404040", "#7a7a7a"
plt.rcParams.update({"font.family": "URW Gothic", "font.size": 9})


class Block(NamedTuple):
    x: float
    y: float
    width: float
    height: float
    title: str
    caption: str = ""
    color: str = GREEN
    fill: str = "none"
    line: str = "-"
    weight: str = "bold"

    @property
    def top(self):
        return self.x + self.width / 2, self.y

    @property
    def bottom(self):
        return self.x + self.width / 2, self.y + self.height

    def draw(self, axes, size=11.5):
        axes.add_patch(FancyBboxPatch((self.x, self.y), self.width, self.height, boxstyle="round,pad=0,rounding_size=0.25",
                                      linewidth=1.4, edgecolor=self.color, facecolor=self.fill, linestyle=self.line))
        centre = self.x + self.width / 2
        lift = 0.22 if self.caption else 0
        axes.text(centre, self.y + self.height / 2 - lift, self.title, ha="center", va="center", fontsize=size,
                  fontweight=self.weight, color=self.color)
        axes.text(centre, self.y + self.height / 2 + 0.3, self.caption, ha="center", va="center", fontsize=8.5, color=INK)


def arrow(axes, start, end, label="", style="-|>", color=GREEN, bend=0.0, offset=(0.25, 0)):
    axes.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=11, linewidth=1.4, color=color,
                                   connectionstyle=f"arc3,rad={bend}"))
    middle = ((start[0] + end[0]) / 2 + offset[0], (start[1] + end[1]) / 2 + offset[1])
    axes.text(*middle, label, ha="left", va="center", fontsize=8.5, color=INK)


def save(figure, axes, path, width, height):
    """Export with y growing downwards, so blocks are laid out top to bottom."""
    axes.set_xlim(-0.2, width + 0.2)
    axes.set_ylim(height, -0.2)
    axes.set_aspect("equal")
    axes.axis("off")
    figure.savefig(path, bbox_inches="tight", pad_inches=0.05, transparent=True)
