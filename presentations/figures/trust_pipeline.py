# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib"]
# ///
"""Zero trust layer on Stackform, one row per concern: from the specification to the criteria it covers."""
from itertools import accumulate
from pathlib import Path

import matplotlib.pyplot as plt

from diagram import GREEN, GREY, INK, LIGHT, MUTED, NAVY, Block, arrow, save

GAP, TOP, STEP, HEIGHT, SIZE = 0.8, 1.0, 1.5, 1.15, 10
HEADERS = {"spec": "Spec", "model": "Stackform IR", "emitter": "Emitter", "artefact": "Generated artefact",
           "runtime": "Runtime\n(off the shelf)", "external": "External\n(standards)", "criteria": "Criteria"}
WIDTHS = dict(zip(HEADERS, [2.8, 3.4, 3.4, 4.6, 3.6, 3.4, 2.2]))
LEFT = dict(zip(HEADERS, accumulate(list(WIDTHS.values())[:-1], lambda left, width: left + width + GAP, initial=0)))
ROWS = [
    ("backend /\nfrontend", "App code with\nPEPs and UI guards", "Generated app", "IdP (OIDC)", "-"),
    ("policies", "Cedar schema\nand policies", "Cedar PDP (AuthZEN)", "", "T1 T3 T4 LP"),
    ("identity", "SPIRE entries,\nattestation selectors", "SPIRE", "", "WID T2 T5"),
    ("segmentation", "Docker networks per\ncall-graph edge", "Docker", "", "MS"),
    ("telemetry", "OTel config,\nOCSF mapping", "OTel Collector", "SIEM (OTLP)", "T7"),
    ("re-evaluation", "CAEP receiver,\nsession revocation", "Cedar PDP", "SIEM / IdP (CAEP)", "T6"),
    ("conformance", "Misuse-case tests,\nZT report", "CI pipeline", "", "all"),
]
LINKS = [("model", "emitter", GREEN), ("emitter", "artefact", GREEN), ("artefact", "runtime", NAVY)]
LEGEND = [("Stackform today", {}), ("new in the fork", {"fill": LIGHT}), ("deployed unmodified", {"color": NAVY}),
          ("outside the system", {"color": GREY, "line": "--"})]


def cell(column, row, text, rows=1, **style):
    return Block(LEFT[column], TOP + row * STEP, WIDTHS[column], HEIGHT + (rows - 1) * STEP, text,
                 **{"fill": "white", "weight": "normal", **style})


def right(column):
    return LEFT[column] + WIDTHS[column]


SPEC = cell("spec", 0, "YAML spec\n\nentities\nroles\naccess rules\nservice calls\ndeploy target", len(ROWS),
            weight="bold")
API = cell("model", 0, "API IR", weight="bold")
TRUST = cell("model", 1, "Trust IR\n\nworkloads\ncall graph\nenforcement sites\nevents", len(ROWS) - 1,
             fill=LIGHT, weight="bold")


def row(index, emitter, artefact, runtime, external):
    yield cell("emitter", index, emitter, fill=LIGHT if index else "white", weight="bold")
    yield cell("artefact", index, artefact)
    yield cell("runtime", index, runtime, color=NAVY if index else GREEN)
    if external:
        yield cell("external", index, external, color=GREY, line="--")


def draw(path):
    figure = plt.figure(figsize=(12, 5.5), dpi=300)
    axes = figure.add_axes((0, 0, 1, 1))
    for column, header in HEADERS.items():
        axes.text(LEFT[column] + WIDTHS[column] / 2, 0.45, header, ha="center", va="center", fontsize=11,
                  fontweight="bold", color=MUTED)
    for block in [SPEC, API, TRUST]:
        block.draw(axes, SIZE)
    arrow(axes, (right("spec"), SPEC.y + SPEC.height / 2), (LEFT["model"], SPEC.y + SPEC.height / 2))
    arrow(axes, API.bottom, TRUST.top)
    for index, (*cells, criteria) in enumerate(ROWS):
        middle = TOP + index * STEP + HEIGHT / 2
        for block in row(index, *cells):
            block.draw(axes, SIZE)
        for source, target, color in LINKS:
            arrow(axes, (right(source), middle), (LEFT[target], middle), color=color)
        if cells[-1]:
            arrow(axes, (right("runtime"), middle), (LEFT["external"], middle), style="<|-|>", color=GREY)
        axes.text(LEFT["criteria"] + WIDTHS["criteria"] / 2, middle, criteria, ha="center", va="center",
                  fontsize=10.5, fontweight="bold", color=GREEN)
    legend = SPEC.y + SPEC.height + 0.5
    for index, (text, style) in enumerate(LEGEND):
        x = LEFT["model"] + index * 5.6
        Block(x, legend, 0.8, 0.5, "", **style).draw(axes)
        axes.text(x + 1.1, legend + 0.25, text, va="center", fontsize=SIZE, color=INK)
    save(figure, axes, path, right("criteria"), legend + 0.8)


if __name__ == "__main__":
    draw(Path(__file__).with_suffix(".png"))
