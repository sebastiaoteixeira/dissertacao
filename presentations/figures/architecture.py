# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib"]
# ///
"""Proposed architecture: generated enforcement points deferring to a runtime decision point."""
from pathlib import Path

import matplotlib.pyplot as plt

from diagram import GREEN, LIGHT, MUTED, NAVY, Block, arrow, save

SPEC = Block(0.5, 0, 9, 1.3, "Declarative specification", "entities, roles, policies")
APP = Block(0, 2.6, 10, 5.0, "", fill=LIGHT)
POINTS = [Block(0.4 + index % 2 * 4.8, 3.5 + index // 2 * 1.9, 4.4, 1.5, title, caption, fill="white")
          for index, (title, caption) in enumerate([
              ("UI guards", "frontend"), ("API checks", "backend endpoints"),
              ("Gateway / mesh", "micro-segmentation"), ("Workload identity", "mTLS, service tokens")])]
PDP = Block(0.5, 9.0, 9, 1.3, "Runtime decision point", "Cedar, OPA, SAPL", NAVY)


def draw(path):
    figure, axes = plt.subplots(figsize=(4.0, 5.3), dpi=300)
    SPEC.draw(axes)
    APP.draw(axes)
    axes.text(5, 3.05, "Generated enforcement points", ha="center", va="center", fontsize=10.5,
              fontweight="bold", color=GREEN)
    for point in POINTS:
        point.draw(axes, size=9.5)
    PDP.draw(axes)
    arrow(axes, SPEC.bottom, APP.top, "Stackform generates")
    arrow(axes, (3.6, APP.y + APP.height), (3.6, PDP.y), "AuthZEN\nrequest", offset=(-1.9, 0))
    arrow(axes, (6.4, PDP.y), (6.4, APP.y + APP.height), "permit / deny\nrevoke", color=NAVY)
    axes.text(5, PDP.y + PDP.height + 0.55, "Re-evaluated on telemetry and posture (UCON)",
              ha="center", va="center", fontsize=8.5, color=MUTED)
    save(figure, axes, path, 10, PDP.y + PDP.height + 0.9)


if __name__ == "__main__":
    draw(Path(__file__).with_suffix(".png"))
