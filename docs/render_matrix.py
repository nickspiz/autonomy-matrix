#!/usr/bin/env python3
"""Render docs/matrix.png from the matrix in the README (needs Pillow)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "matrix.png"
S = 2  # scale for a crisp image
ROWS = [
    ("Yes", "Only your machine", "Do it. Say nothing.", (46, 160, 90)),
    ("Yes", "One project", "Do it. One short sentence afterwards.", (46, 160, 90)),
    ("Yes", "Several projects or shared infra", "Do it, but always report it.", (196, 160, 30)),
    ("No", "Only your machine", "Ask once, then don't ask again this session.", (214, 126, 40)),
    ("No", "Shared or production", "Ask every time.", (214, 84, 60)),
    ("No", "Money, users, or data", "Ask, explain the consequences, offer a way to cancel.", (190, 50, 70)),
]
HEAD = ("Undoable?", "Blast radius", "What the agent does")
COLS = [150, 430, 700]
BG, FG, MUTED, LINE = (250, 250, 247), (28, 30, 36), (110, 114, 126), (226, 227, 222)


def font(size, bold=False):
    for p in ("/System/Library/Fonts/HelveticaNeue.ttc", "/System/Library/Fonts/Helvetica.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(p, size * S, index=1 if bold and p.endswith(".ttc") else 0)
        except OSError:
            pass
    return ImageFont.load_default()


def main():
    pad, title_h, head_h, row_h = 40, 110, 56, 74
    w = sum(COLS) + 2 * pad
    h = title_h + head_h + row_h * len(ROWS) + pad + 44
    img = Image.new("RGB", (w * S, h * S), BG)
    d = ImageDraw.Draw(img)
    d.text((pad * S, 30 * S), "Should the agent ask?", font=font(34, True), fill=FG)
    d.text((pad * S, 76 * S), "Score every action on two things: can it be undone, and who gets hurt if it goes wrong.",
           font=font(17), fill=MUTED)
    y = title_h
    x = pad
    for i, label in enumerate(HEAD):
        d.text(((x + 22) * S, (y + 18) * S), label.upper(), font=font(14, True), fill=MUTED)
        x += COLS[i]
    y += head_h
    d.line([(pad * S, y * S), ((w - pad) * S, y * S)], fill=LINE, width=2 * S)
    for undo, radius, action, color in ROWS:
        d.rounded_rectangle([pad * S, (y + 8) * S, (pad + 8) * S, (y + row_h - 8) * S], radius=4 * S, fill=color)
        x = pad
        for i, text in enumerate((undo, radius, action)):
            f = font(21, True) if i == 2 else font(21)
            d.text(((x + 22) * S, (y + 24) * S), text, font=f, fill=FG)
            x += COLS[i]
        y += row_h
        d.line([(pad * S, y * S), ((w - pad) * S, y * S)], fill=LINE, width=S)
    d.text((pad * S, (y + 14) * S), "When two rules disagree, the stricter one wins.", font=font(16), fill=MUTED)
    img.resize((w, h), Image.LANCZOS).save(OUT, optimize=True)


if __name__ == "__main__":
    main()
