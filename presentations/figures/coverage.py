# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib"]
# ///
"""Zero trust key coverage of the grey-literature tools, as a heatmap sized for the deck's figure box."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

KEYS = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "LP", "MS", "WID"]
FULL, PARTIAL = 1.0, 0.5
GREEN, LIGHT, EMPTY, INK, MUTED = "#275727", "#b9d3b9", "#ececec", "#404040", "#7a7a7a"

GROUPS = {
    "Generators (generate the app)": {
        "ZenStack": {"T3": FULL, "T4": PARTIAL, "LP": FULL},
        "Amplify Gen 2": {"T1": PARTIAL, "T3": FULL, "LP": FULL, "WID": PARTIAL},
        "Encore": {"T3": FULL, "MS": PARTIAL, "LP": FULL, "WID": PARTIAL},
        "JHipster": {"T3": FULL, "T7": PARTIAL},
        "Wasp": {"T3": FULL},
    },
    "Policy languages (runtime)": {
        "Cedar": dict.fromkeys(["T1", "T3", "T4", "LP"], FULL),
        "Rego / OPA": dict.fromkeys(["T1", "T3", "T4", "LP"], FULL),
        "OpenFGA": dict.fromkeys(["T1", "T3", "T4", "LP"], FULL),
        "SAPL": dict.fromkeys(["T3", "T4", "T6", "T7"], FULL),
    },
    "Infrastructure (runtime)": {
        "OpenZiti": dict.fromkeys(KEYS, FULL),
        "Pomerium": dict.fromkeys(KEYS[:8], FULL),
        "Istio": dict.fromkeys(["T1", "T2", "T3", "T4", "T7", "LP", "MS", "WID"], FULL),
        "Teleport": dict.fromkeys(["T1", "T2", "T3", "T4", "T5", "T7", "LP"], FULL) | {"T6": PARTIAL, "WID": PARTIAL},
    },
}

plt.rcParams.update({"font.family": "URW Gothic", "font.size": 9, "hatch.color": GREEN, "hatch.linewidth": 0.6})
CELL, GAP = 1.0, 0.12


def rows():
    """(y, label, coverage) per tool, with a header row opening each group."""
    y = 0
    for group, tools in GROUPS.items():
        yield y, group, None
        y += 1
        for name, coverage in tools.items():
            yield y, name, coverage
            y += 1
        y += 0.35


def draw(path):
    layout = list(rows())
    depth = layout[-1][0] + 1
    figure, axes = plt.subplots(figsize=(4.4, 5.2), dpi=300)
    for y, label, coverage in layout:
        if coverage is None:
            axes.text(-0.2, y + 0.55, label, ha="left", va="center", fontsize=8.5, color=MUTED, fontweight="bold")
            continue
        axes.text(3.6, y + 0.5, label, ha="right", va="center", color=INK)
        for x, key in enumerate(KEYS):
            value = coverage.get(key, 0)
            axes.add_patch(Rectangle((3.8 + x + GAP / 2, y + GAP / 2), CELL - GAP, CELL - GAP, linewidth=0,
                                     facecolor={FULL: GREEN, PARTIAL: LIGHT}.get(value, EMPTY),
                                     hatch="////" if value == PARTIAL else None))
        axes.text(14.7, y + 0.5, f"{sum(coverage.values()):g}", ha="center", va="center", color=INK)
    for x, key in enumerate(KEYS):
        axes.text(3.8 + x + 0.5, -0.3, key, ha="center", va="bottom", rotation=90, fontsize=8, color=INK)
    axes.text(14.7, -0.45, "/10", ha="center", va="bottom", fontsize=8, color=MUTED)
    legend = [(GREEN, None, "covered"), (LIGHT, "////", "partial"), (EMPTY, None, "absent")]
    for index, (color, hatch, text) in enumerate(legend):
        axes.add_patch(Rectangle((3.8 + index * 3.9, depth + 0.4), 0.7, 0.7, facecolor=color, hatch=hatch, linewidth=0))
        axes.text(3.8 + index * 3.9 + 0.95, depth + 0.75, text, va="center", fontsize=8, color=INK)
    glossary = ["T1-T7: NIST SP 800-207 tenets    LP: least privilege",
                "MS: micro-segmentation    WID: workload identity"]
    for index, line in enumerate(glossary):
        axes.text(7.5, depth + 1.9 + index * 0.8, line, ha="center", va="center", fontsize=7.5, color=INK)
    axes.text(7.5, depth + 3.6, "Source: purposive scan of tool documentation, Oct-Nov 2026", ha="center", va="center",
              fontsize=7, color=MUTED)
    axes.set_xlim(-0.3, 15.3)
    axes.set_ylim(depth + 4.0, -2.0)
    axes.set_aspect("equal")
    axes.axis("off")
    figure.savefig(path, bbox_inches="tight", pad_inches=0.05, transparent=True)


if __name__ == "__main__":
    draw(Path(__file__).with_suffix(".png"))
