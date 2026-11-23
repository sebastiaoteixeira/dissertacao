# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib"]
# ///
"""Zero trust layer on Stackform: one generator module per concern, configuring off-the-shelf runtime."""
from pathlib import Path

import matplotlib.pyplot as plt

from diagram import GREEN, GREY, LIGHT, NAVY, Block, arrow, save

SPEC = Block(0.5, 0, 9, 1.3, "Declarative specification", "entities, roles, access rules, service calls")
LAYER = Block(0, 2.4, 10, 5.9, "", fill=LIGHT)
MODULES = [Block(0.4 + index % 2 * 4.8, 3.4 + index // 2 * 1.6, 4.4, 1.3, title, caption, fill="white")
           for index, (title, caption) in enumerate([
               ("Policies", "T1 T3 T4 LP"), ("Identity", "WID T2 T5"),
               ("Segmentation", "MS"), ("Telemetry", "T7"),
               ("Re-evaluation", "T6"), ("Conformance", "misuse tests")])]
APP = Block(0, 9.5, 4.2, 1.5, "Generated app", "enforcement points")
RUNTIME = Block(5.8, 9.5, 4.2, 1.5, "Runtime", "Cedar, SPIRE, OTel", NAVY)
EXTERNAL = Block(0.5, 12.6, 9, 1.0, "SIEM, IdP", color=GREY, line="--")
STANDARDS = {APP: "login (OIDC)\nrevocations (CAEP)", RUNTIME: "events (OTLP)"}
TITLE_SIZES = {11.5: [SPEC, LAYER, EXTERNAL], 10.5: [APP, RUNTIME], 9.5: MODULES}


def draw(path):
    figure, axes = plt.subplots(figsize=(4.0, 5.3), dpi=300)
    for size, blocks in TITLE_SIZES.items():
        for block in blocks:
            block.draw(axes, size)
    axes.text(5, 2.9, "Stackform trust layer", ha="center", va="center", fontsize=10.5, fontweight="bold", color=GREEN)
    arrow(axes, SPEC.bottom, LAYER.top, "trust model")
    arrow(axes, (APP.top[0], LAYER.bottom[1]), APP.top, "generates")
    arrow(axes, (RUNTIME.top[0], LAYER.bottom[1]), RUNTIME.top, "configures", color=NAVY)
    arrow(axes, (APP.x + APP.width, 10.25), (RUNTIME.x, 10.25), style="<|-|>", color=NAVY)
    for block, label in STANDARDS.items():
        arrow(axes, block.bottom, (block.bottom[0], EXTERNAL.y), label, style="<|-|>", color=GREY)
    save(figure, axes, path, 10, EXTERNAL.y + EXTERNAL.height + 0.2)


if __name__ == "__main__":
    draw(Path(__file__).with_suffix(".png"))
