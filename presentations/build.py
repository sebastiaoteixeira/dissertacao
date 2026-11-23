# /// script
# requires-python = ">=3.11"
# dependencies = ["python-pptx", "pyyaml"]
# ///
"""Render the sprints given as arguments (default: all) in sprints.yaml onto the PDE sprint template."""
import sys
from copy import deepcopy
from itertools import chain
from pathlib import Path
from typing import NamedTuple

import yaml
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Pt

HERE = Path(__file__).parent
NAVY, GREEN, GREY = RGBColor(0x25, 0x40, 0x61), RGBColor(0x27, 0x57, 0x27), RGBColor(0x40, 0x40, 0x40)


class Style(NamedTuple):
    size: Pt
    color: RGBColor
    bold: bool = False


HEADING, FIGURE, CAPTION, NOTE = Style(Pt(16), NAVY, True), Style(Pt(30), GREEN, True), Style(Pt(12), GREY), Style(Pt(9), GREY)


class Box(NamedTuple):
    left: int
    top: int
    width: int
    height: int

    def split(self, ratio, gap=Emu(300000)):
        cut = int(self.width * ratio)
        return (Box(self.left, self.top, cut, self.height),
                Box(self.left + cut + gap, self.top, self.width - cut - gap, self.height))


BODY = Box(609600, 1196975, 10972800, 4929188)
TOP_LEVEL_GAP = Pt(14)


def entry(item):
    return next(iter(item.items())) if isinstance(item, dict) else (item, [])


def flatten(points, level=0):
    for point in points:
        text, children = entry(point)
        yield text, level
        yield from flatten(children, level + 1)


def paragraphs(frame):
    frame.clear()
    return chain(frame.paragraphs, iter(frame.add_paragraph, None))


def write(frame, points):
    for index, ((text, level), paragraph) in enumerate(zip(flatten(points), paragraphs(frame))):
        paragraph.text, paragraph.level = text, level
        if index and not level:
            paragraph.space_before = TOP_LEVEL_GAP


def retext(frame, lines):
    """Replace text in the template's own paragraphs, keeping their formatting."""
    for paragraph, text in zip(frame.paragraphs, lines, strict=True):
        paragraph.runs[0].text = text


def typeset(frame, lines):
    """Centre `(text, style)` lines in a frame."""
    frame.word_wrap, frame.vertical_anchor = True, MSO_ANCHOR.MIDDLE
    for (text, style), paragraph in zip(lines, paragraphs(frame)):
        paragraph.alignment, paragraph.space_before, paragraph.space_after = PP_ALIGN.CENTER, 0, 0
        run = paragraph.add_run()
        run.text, run.font.size, run.font.color.rgb, run.font.bold = text, *style


def cards(shapes, items, box, title, gap, height=Emu(1050000)):
    """Stack `title: [captions]` cards, vertically centred in box; yield each card's top."""
    top = box.top + (box.height - len(items) * height - (len(items) - 1) * gap) // 2
    for index, (heading, captions) in enumerate(map(entry, items)):
        y = top + index * (height + gap)
        card = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, box.left, y, box.width, height)
        card.fill.background()
        card.line.color.rgb, card.line.width = GREEN, Pt(1.5)
        captions = [captions] if isinstance(captions, str) else captions
        typeset(card.text_frame, [(heading, title), *((caption, CAPTION) for caption in captions)])
        yield y


def flow(shapes, stages, box, arrow=Emu(380000)):
    """Stages joined top to bottom by arrows."""
    for y in list(cards(shapes, stages, box, HEADING, arrow))[1:]:
        link = shapes.add_shape(MSO_SHAPE.DOWN_ARROW, box.left + (box.width - arrow) // 2, y - arrow, arrow, arrow)
        link.fill.solid()
        link.fill.fore_color.rgb = GREEN
        link.line.fill.background()


def stat(shapes, spec, box, gap=Emu(250000), height=Emu(1050000), footer=Emu(300000)):
    """Headline figures with their source underneath, centred as one group."""
    tops = list(cards(shapes, spec["figures"], box._replace(height=box.height - footer), FIGURE, gap, height))
    source = shapes.add_textbox(box.left, tops[-1] + height, box.width, footer)
    typeset(source.text_frame, [(f"Source: {spec['source']}", NOTE)])


def image(shapes, path, box):
    """Picture scaled to fit the box and centred in it."""
    picture = shapes.add_picture(str(HERE / path), box.left, box.top, width=box.width)
    scale = min(1, box.height / picture.height)
    picture.width, picture.height = int(picture.width * scale), int(picture.height * scale)
    picture.left = box.left + (box.width - picture.width) // 2
    picture.top = box.top + (box.height - picture.height) // 2


FIGURES = {"flow": flow, "stat": stat, "image": image}


def duplicate(presentation, slide):
    """Append a copy of a slide, footer included; python-pptx has no slide copy."""
    copy = presentation.slides.add_slide(slide.slide_layout)
    for shape in list(copy.shapes):
        shape.element.getparent().remove(shape.element)
    for shape in slide.shapes:
        copy.shapes._spTree.append(deepcopy(shape.element))
    return copy


def beside(body):
    """Narrow the body to the left, leaving the right of it to a figure."""
    text, figure = BODY.split(0.6)
    body.left, body.top, body.width, body.height = text
    body.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    return figure


def fill(slide, spec):
    """Bullets, a figure, or bullets with a figure beside them."""
    body = slide.placeholders[1]
    if "points" in spec:
        write(body.text_frame, spec["points"])
    else:
        body.element.getparent().remove(body.element)
    if "figure" in spec:
        kind, figure_spec = entry(spec["figure"])
        FIGURES[kind](slide.shapes, figure_spec, beside(body) if "points" in spec else BODY)


def build(deck, sprint):
    presentation = Presentation(HERE / "template.pptx")
    cover, *content = presentation.slides
    content += [duplicate(presentation, content[-1]) for _ in sprint["slides"][len(content):]]
    cover.shapes.title.text = deck["title"]
    write(cover.placeholders[10].text_frame, [f"Sprint {sprint['number']}: {sprint['focus']}", *sprint["summary"]])
    retext(cover.placeholders[11].text_frame, deck["authors"])
    cover.notes_slide.notes_text_frame.text = sprint["intro"]
    for slide, spec in zip(content, sprint["slides"], strict=True):
        slide.shapes.title.text = spec["title"]
        slide.notes_slide.notes_text_frame.text = spec.get("notes", "")
        fill(slide, spec)
    presentation.save(HERE / f"sprint-{sprint['number']}.pptx")


if __name__ == "__main__":
    deck = yaml.safe_load((HERE / "sprints.yaml").read_text())
    chosen = set(map(int, sys.argv[1:])) or {sprint["number"] for sprint in deck["sprints"]}
    for sprint in filter(lambda sprint: sprint["number"] in chosen, deck["sprints"]):
        build(deck, sprint)
