#!/usr/bin/env python3
"""
Build the themed SVG assets and README for the UVARAJAND GitHub profile.

Design system is taken from uvarajan-linkedin-banner-v3.svg:
  deep navy background, amber accent, isometric DATA -> LLM -> API motif.

Run:
    python scripts/build_svgs.py
"""

from __future__ import annotations

import html
import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

PROFILE = json.loads((ROOT / "scripts" / "profile.json").read_text(encoding="utf-8"))

# ── palette (from the LinkedIn banner) ────────────────────────────────────────
INK_900 = "#0A0D14"
INK_850 = "#0C121C"
INK_800 = "#0F1522"
NAVY_900 = "#121A2A"
NAVY_800 = "#141C2B"
NAVY_700 = "#182032"
SLATE_700 = "#1B2434"
SLATE_600 = "#26324A"
SLATE_500 = "#34435C"
SLATE_400 = "#3A4A63"
SLATE_300 = "#4B5C79"
TEXT = "#E8ECF4"
TEXT_SOFT = "#CBD4E2"
MUTED = "#98A5B8"
FAINT = "#566277"
AMBER = "#FFB224"
AMBER_SOFT = "#FFD27A"
AMBER_DARK = "#B87A0E"
AMBER_DEEP = "#8F5F0A"

SANS = "Segoe UI, Inter, Helvetica Neue, Arial, sans-serif"
MONO = "Consolas, 'JetBrains Mono', 'Courier New', monospace"


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def n(value: float) -> str:
    if isinstance(value, float):
        out = f"{value:.2f}".rstrip("0").rstrip(".")
        return out
    return str(value)


def text(
    x: float,
    y: float,
    value: str,
    size: float = 14,
    fill: str = TEXT,
    weight: int = 400,
    family: str = SANS,
    anchor: str = "start",
    letter: float | None = None,
    opacity: float | None = None,
    extra: str = "",
) -> str:
    attrs = [
        f'x="{n(x)}"',
        f'y="{n(y)}"',
        f'fill="{fill}"',
        f'font-size="{n(size)}"',
        f'font-family="{family}"',
        f'font-weight="{weight}"',
    ]
    if anchor != "start":
        attrs.append(f'text-anchor="{anchor}"')
    if letter is not None:
        attrs.append(f'letter-spacing="{n(letter)}"')
    if opacity is not None:
        attrs.append(f'opacity="{n(opacity)}"')
    if extra:
        attrs.append(extra)
    return f'<text {" ".join(attrs)}>{esc(value)}</text>'


def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    r: float = 0,
    fill: str = "none",
    stroke: str = "none",
    sw: float = 1,
    opacity: float | None = None,
    extra: str = "",
) -> str:
    attrs = [
        f'x="{n(x)}"',
        f'y="{n(y)}"',
        f'width="{n(w)}"',
        f'height="{n(h)}"',
        f'rx="{n(r)}"',
        f'fill="{fill}"',
        f'stroke="{stroke}"',
        f'stroke-width="{n(sw)}"',
    ]
    if opacity is not None:
        attrs.append(f'opacity="{n(opacity)}"')
    if extra:
        attrs.append(extra)
    return f'<rect {" ".join(attrs)}/>'


def line(x1, y1, x2, y2, stroke=SLATE_400, sw=1, dash=None, opacity=None, extra="") -> str:
    attrs = [
        f'x1="{n(x1)}"', f'y1="{n(y1)}"', f'x2="{n(x2)}"', f'y2="{n(y2)}"',
        f'stroke="{stroke}"', f'stroke-width="{n(sw)}"',
    ]
    if dash:
        attrs.append(f'stroke-dasharray="{dash}"')
    if opacity is not None:
        attrs.append(f'opacity="{n(opacity)}"')
    if extra:
        attrs.append(extra)
    return f'<line {" ".join(attrs)}/>'


def chip(x: float, y: float, label: str, accent: bool = False, size: float = 11, h: float = 30) -> tuple[str, float]:
    width = 24 + len(label) * size * 0.59
    fill = "#1A1608" if accent else "#121A2A"
    stroke = AMBER_DEEP if accent else SLATE_600
    color = AMBER_SOFT if accent else TEXT_SOFT
    body = rect(x, y, width, h, h / 2, fill, stroke, 1)
    body += text(x + width / 2, y + h / 2 + size * 0.35, label, size, color, 500, MONO, "middle")
    return body, width


def chip_row(x: float, y: float, labels, accent=False, size=11, h=30, gap=9) -> str:
    body = ""
    cx = x
    for label in labels:
        part, width = chip(cx, y, label, accent, size, h)
        body += part
        cx += width + gap
    return body


def svg(width: int, height: int, body: str, defs: str = "", label: str = "") -> str:
    aria = f' aria-label="{esc(label)}"' if label else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img"{aria}>\n'
        f"<defs>{defs}</defs>\n{body}\n</svg>\n"
    )


def write(name: str, content: str) -> None:
    path = ASSETS / name
    path.write_text(content, encoding="utf-8")
    print(f"  {path.relative_to(ROOT)}  ({len(content) / 1024:.1f} KB)")


# ── shared defs ───────────────────────────────────────────────────────────────
def base_defs(w: int, h: int, warm_x: float = 0, warm_y: float = 0, warm_r: float = 0, panel: bool = True) -> str:
    return f"""
<linearGradient id="bg" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="{h}">
  <stop offset="0" stop-color="{NAVY_900}"/><stop offset="1" stop-color="{INK_900}"/>
</linearGradient>
<radialGradient id="warm" gradientUnits="userSpaceOnUse" cx="{n(warm_x)}" cy="{n(warm_y)}" r="{n(warm_r)}">
  <stop offset="0" stop-color="{AMBER}" stop-opacity="0.16"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{NAVY_700}"/><stop offset="1" stop-color="{INK_850}"/>
</linearGradient>
<linearGradient id="lineGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{AMBER}" stop-opacity="0"/>
  <stop offset="0.18" stop-color="{AMBER}" stop-opacity="0.55"/>
  <stop offset="0.82" stop-color="{SLATE_300}" stop-opacity="0.55"/>
  <stop offset="1" stop-color="{SLATE_300}" stop-opacity="0"/>
</linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
  <path d="M40 0H0V40" fill="none" stroke="{SLATE_600}" stroke-width="0.6" opacity="0.35"/>
</pattern>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
  <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
"""


# ── ticker ────────────────────────────────────────────────────────────────────
def build_ticker() -> None:
    w, h = 1200, 68
    lines = [" ".join(line.split()) for line in PROFILE["typing_lines"]]
    delays = [-0.3, 4.7, 9.7, 14.7, 19.7]
    css = """<style>
  .line { opacity: 0; animation: slide 25s infinite; }
  @keyframes slide {
    0% { opacity: 0; transform: translateY(6px); }
    1.2% { opacity: 1; transform: translateY(0); }
    18% { opacity: 1; transform: translateY(0); }
    20% { opacity: 0; transform: translateY(-6px); }
    100% { opacity: 0; }
  }
</style>"""
    variants = (
        ("ticker.svg", AMBER, TEXT),
        ("ticker-light.svg", AMBER_DEEP, INK_900),
    )
    for name, label_color, phrase_color in variants:
        b = text(600, 18, "WHAT I DO", 11, label_color, 600, MONO, "middle", letter=2.4)
        b += line(588, 26, 612, 26, label_color, 1.2, opacity=0.55)
        for i, phrase in enumerate(lines):
            b += (
                f'<g class="line line{i+1}" style="animation-delay:{delays[i]}s">'
                f'{text(600, 52, phrase, 24, phrase_color, 500, MONO, "middle", letter=0.2)}</g>'
            )
        write(name, svg(w, h, b, css, "Rotating list of what I do"))


# ── header ────────────────────────────────────────────────────────────────────
def iso_layer(cx, cy, w, h, d, top, left, right, stroke, inner=True) -> str:
    top_pts = f"{n(cx)},{n(cy-h/2)} {n(cx+w/2)},{n(cy)} {n(cx)},{n(cy+h/2)} {n(cx-w/2)},{n(cy)}"
    left_pts = f"{n(cx-w/2)},{n(cy)} {n(cx)},{n(cy+h/2)} {n(cx)},{n(cy+h/2+d)} {n(cx-w/2)},{n(cy+d)}"
    right_pts = f"{n(cx+w/2)},{n(cy)} {n(cx)},{n(cy+h/2)} {n(cx)},{n(cy+h/2+d)} {n(cx+w/2)},{n(cy+d)}"
    out = (
        f'<polygon points="{left_pts}" fill="{left}" stroke="{stroke}" stroke-width="1"/>'
        f'<polygon points="{right_pts}" fill="{right}" stroke="{stroke}" stroke-width="1"/>'
        f'<polygon points="{top_pts}" fill="{top}" stroke="{stroke}" stroke-width="1.2"/>'
    )
    if inner:
        iw, ih = w * 0.46, h * 0.46
        inner_pts = f"{n(cx)},{n(cy-ih/2)} {n(cx+iw/2)},{n(cy)} {n(cx)},{n(cy+ih/2)} {n(cx-iw/2)},{n(cy)}"
        out += f'<polygon points="{inner_pts}" fill="none" stroke="{stroke}" stroke-width="1" opacity="0.55"/>'
    return out


def build_header() -> None:
    w, h = 1584, 396
    defs = base_defs(w, h, 330, 200, 300) + f"""
<style>
  .float {{ animation: float 6s ease-in-out infinite; }}
  .float2 {{ animation: float 7.5s ease-in-out infinite; animation-delay: -2.2s; }}
  @keyframes float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-6px); }} }}
  .dash {{ stroke-dasharray: 6 10; animation: dash 4s linear infinite; }}
  @keyframes dash {{ to {{ stroke-dashoffset: -32; }} }}
  .pulse {{ animation: pulse 2.6s ease-in-out infinite; }}
  @keyframes pulse {{ 0%,100% {{ opacity: 0.3; }} 50% {{ opacity: 1; }} }}
  .blink {{ animation: blink 1.4s step-end infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0.15; }} }}
</style>
<radialGradient id="core" cx="50%" cy="50%" r="50%">
  <stop offset="0" stop-color="{AMBER}" stop-opacity="0.30"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
</radialGradient>
"""
    b = rect(0, 0, w, h, 0, "url(#bg)")
    b += rect(0, 0, w, h, 0, "url(#grid)", opacity=0.55)
    b += rect(0, 0, w, h, 0, "url(#warm)")
    b += f'<circle cx="292" cy="205" r="205" fill="url(#core)" opacity="0.75"/>'

    # flowing amber traces (top right)
    traces = [
        "M 1120 42 C 1210 20 1270 88 1350 66 S 1500 20 1584 44",
        "M 1150 78 C 1240 52 1300 116 1390 94 S 1510 62 1584 82",
        "M 1190 114 C 1270 92 1330 142 1420 122 S 1520 104 1584 118",
    ]
    for i, d in enumerate(traces):
        b += f'<path d="{d}" fill="none" stroke="{AMBER}" stroke-width="1.1" opacity="{0.42 - i * 0.08}" class="dash"/>'
    for cx, cy in [(1210, 24), (1350, 66), (1450, 34), (1390, 94)]:
        b += f'<circle cx="{cx}" cy="{cy}" r="3" fill="{AMBER}" class="pulse" style="animation-delay:-{cx % 7 / 3:.1f}s"/>'

    # corner brackets
    for x, y, dx, dy in [(14, 14, 1, 1), (1570, 14, -1, 1), (14, 382, 1, -1), (1570, 382, -1, -1)]:
        b += f'<path d="M {x} {y + dy * 18} L {x} {y} L {x + dx * 18} {y}" fill="none" stroke="{AMBER}" stroke-width="2"/>'

    b += text(32, 44, PROFILE["handle"] + "  //  PROFILE", 12.5, FAINT, 500, MONO, letter=1.4)
    b += line(32, 58, 1552, 58, SLATE_600, 0.8, "2 8", 0.6)

    # isometric stack
    b += '<g class="float">' + iso_layer(292, 118, 214, 104, 22, NAVY_700, INK_800, NAVY_800, SLATE_400) + "</g>"
    b += '<g class="float2">' + iso_layer(292, 204, 214, 104, 22, AMBER, AMBER_DARK, AMBER_DEEP, AMBER_SOFT) + "</g>"
    b += '<g class="float">' + iso_layer(292, 290, 214, 104, 22, NAVY_700, INK_800, NAVY_800, SLATE_400) + "</g>"
    b += f'<circle cx="292" cy="204" r="6" fill="{INK_900}"/>'
    b += f'<circle cx="292" cy="204" r="3" fill="{AMBER_SOFT}" class="pulse"/>'
    b += line(292, 145, 292, 178, AMBER, 1, "3 7", 0.55, 'class="dash"')
    b += line(292, 230, 292, 263, SLATE_300, 1, "3 7", 0.55, 'class="dash"')

    for cy, name, color in [(122, "API", MUTED), (208, "LLM", AMBER_SOFT), (294, "DATA", MUTED)]:
        b += line(408, cy, 426, cy, color, 1.2, None, 0.7)
        b += text(434, cy + 4, name, 14, color, 600, MONO, letter=2)

    # headline
    b += text(576, 88, "HELLO, I'M", 12.5, AMBER, 600, MONO, letter=3)
    b += (
        f'<text x="572" y="154" fill="{TEXT}" font-family="{SANS}" font-size="72" '
        f'font-weight="700" letter-spacing="-1.5">{esc(PROFILE["name"])}'
        f'<tspan fill="{AMBER}">.</tspan></text>'
    )

    pill_w, pill_h, pill_x, pill_y = 666, 58, 572, 174
    b += rect(pill_x, pill_y, pill_w, pill_h, 10, AMBER)
    b += text(pill_x + pill_w / 2, pill_y + 38, PROFILE["headline"], 24, INK_900, 700, SANS, "middle", letter=0.6)

    b += (
        f'<text x="572" y="286" fill="{TEXT}" font-family="{SANS}" font-size="27" font-weight="600">'
        f'{esc(PROFILE["subheadline"])}'
        f'<tspan fill="{MUTED}" font-size="21" font-weight="400">   ·   {esc(PROFILE["tagline"])}</tspan></text>'
    )
    b += chip_row(572, 306, PROFILE["chips"], False, 15, 40, 12)

    b += text(32, 374, "DATA  →  LLM  →  API", 11.5, MUTED, 500, MONO, letter=1.6)
    b += text(1552, 374, "BUILD  ·  INTEGRATE  ·  AUTOMATE", 11.5, MUTED, 500, MONO, "end", letter=1.4)

    write("header.svg", svg(w, h, b, defs, "Uvarajan D — AI Integration and Automation Engineer"))


# ── divider & labels ──────────────────────────────────────────────────────────
def build_divider() -> None:
    defs = base_defs(1200, 20, 600, 10, 220) + f"""
<linearGradient id="dividerCenter" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{AMBER}" stop-opacity="0"/>
  <stop offset="0.5" stop-color="{AMBER}" stop-opacity="0.85"/>
  <stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
</linearGradient>
"""
    b = rect(0, 9, 1200, 1, 0, SLATE_500)
    b += rect(420, 8, 360, 3, 1.5, "url(#dividerCenter)")
    b += rect(594, 5, 12, 9, 2, AMBER)
    write("divider.svg", svg(1200, 20, b, defs, "Section divider"))


def build_label(index: str, title: str, right: str) -> str:
    b = rect(0, 0, 1200, 46, 10, "#0C121C", SLATE_700, 1)
    b += rect(0, 0, 4, 46, 2, AMBER)
    b += text(24, 30, f"[ {index} ]", 12, AMBER, 600, MONO, letter=1.4)
    b += text(86, 30, title, 20, TEXT, 700, SANS, letter=3.0)
    if right:
        b += text(1176, 29, right, 10, MUTED, 500, MONO, "end", letter=1.2)
    return svg(1200, 46, b, base_defs(1200, 46, 80, 22, 220), title.title())


def build_labels() -> None:
    labels = [
        ("whoami", "01", "WHOAMI", "IDENTITY  /  FOCUS"),
        ("capabilities", "02", "WHAT I BUILD", "INTEGRATE  /  AUTOMATE  /  DESIGN"),
        ("architecture", "03", "SYSTEM ARCHITECTURE", "REQUEST LIFECYCLE"),
        ("work", "04", "SELECTED WORK", "BUILT  /  SHIPPED  /  EVALUATED"),
        ("stack", "05", "TECH STACK", "TOOLS I ACTUALLY USE"),
        ("telemetry", "06", "GITHUB TELEMETRY", "TOTAL  /  CURRENT  /  LONGEST"),
        ("activity", "07", "ACTIVITY MATRIX", "CONTRIBUTION ACTIVITY  /  SNAKE"),
    ]
    for slug, index, title, right in labels:
        write(f"label-{slug}.svg", build_label(index, title, right))


# ── terminals ─────────────────────────────────────────────────────────────────
def window(w: int, h: int, title: str) -> str:
    b = rect(1, 1, w - 2, h - 2, 10, "#0C121C", SLATE_600, 1.2)
    b += f'<path d="M 1 11 Q 1 1 11 1 L {w-11} 1 Q {w-1} 1 {w-1} 11 L {w-1} 38 L 1 38 Z" fill="{NAVY_900}" stroke="{SLATE_600}" stroke-width="1.2"/>'
    b += f'<circle cx="20" cy="19" r="5" fill="#FF5F56"/><circle cx="38" cy="19" r="5" fill="#FFBD2E"/><circle cx="56" cy="19" r="5" fill="#27C93F"/>'
    b += text(w / 2, 23, title, 10.5, MUTED, 500, MONO, "middle")
    b += line(1, 38, w - 1, 38, SLATE_600, 0.8)
    b += f'<rect x="1" y="38" width="{w-2}" height="{h-39}" fill="url(#scan)" opacity="0.35"/>'
    return b


def scan_defs() -> str:
    return f'<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="4" y2="0" stroke="{TEXT}" stroke-width="1" opacity="0.025"/></pattern>'


def whoami_panel(w: int = 640, h: int = 342) -> str:
    b = window(w, h, "whoami.yaml - bash")
    b += text(22, 76, "uvarajan@systems:~$", 13, AMBER, 600, MONO)
    b += text(196, 76, "cat whoami.yaml", 13, TEXT, 600, MONO)
    y = 108
    for key, value in PROFILE["whoami"]:
        b += text(22, y, key, 12.5, AMBER_SOFT, 600, MONO)
        b += text(118, y, ":", 12.5, FAINT, 400, MONO)
        b += text(136, y, value, 12.5, TEXT_SOFT, 400, MONO)
        y += 27
    b += rect(22, y - 14, 9, 15, 1, TEXT_SOFT, extra='class="cursor"')
    return b


def focus_panel(w: int = 460, h: int = 342) -> str:
    b = window(w, h, "focus.py - bash")
    b += text(22, 76, "uvarajan@systems:~$", 12.5, AMBER, 600, MONO)
    b += text(184, 76, "python focus.py", 12.5, TEXT, 600, MONO)
    b += text(22, 108, "current_focus = [", 12.5, TEXT_SOFT, 400, MONO)
    y = 138
    for item in PROFILE["focus"]:
        b += text(40, y, f'"{item}",', 12.5, AMBER_SOFT, 400, MONO)
        y += 27
    b += text(22, y, "]", 12.5, TEXT_SOFT, 400, MONO)
    b += rect(22, y + 14, 9, 15, 1, TEXT_SOFT, extra='class="cursor"')
    return b


def build_terminals() -> None:
    css = "<style>.cursor{animation:blink 1.1s step-end infinite}@keyframes blink{50%{opacity:0}}</style>"

    write("whoami.svg", svg(640, 342, whoami_panel(), base_defs(640, 342, 500, 80, 300) + scan_defs() + css, "whoami terminal panel"))
    write("focus.svg", svg(460, 342, focus_panel(), base_defs(460, 342, 360, 80, 260) + scan_defs() + css, "current focus terminal panel"))

    # Single responsive asset for the README (avoids table overflow on mobile).
    cw, ch = 1200, 342
    combined = '<g transform="translate(0,0)">' + whoami_panel(690, ch) + "</g>"
    combined += '<g transform="translate(710,0)">' + focus_panel(490, ch) + "</g>"
    write(
        "whoami-focus.svg",
        svg(cw, ch, combined, base_defs(cw, ch, 500, 120, 520) + scan_defs() + css, "whoami and current focus terminal panels"),
    )


# ── capabilities ──────────────────────────────────────────────────────────────
def icon_spark(cx, cy, color) -> str:
    return (
        f'<g stroke="{color}" stroke-width="1.5" fill="none">'
        f'<circle cx="{cx}" cy="{cy}" r="3" fill="{color}" stroke="none"/>'
        f'<circle cx="{cx}" cy="{cy}" r="10"/>'
        f'<path d="M {cx} {cy-18} V {cy-12} M {cx} {cy+12} V {cy+18} M {cx-18} {cy} H {cx-12} M {cx+12} {cy} H {cx+18}"/>'
        f'<path d="M {cx-12} {cy-12} L {cx-8} {cy-8} M {cx+8} {cy+8} L {cx+12} {cy+12} M {cx+12} {cy-12} L {cx+8} {cy-8} M {cx-8} {cy+8} L {cx-12} {cy+12}"/>'
        f"</g>"
    )


def icon_flow(cx, cy, color) -> str:
    return (
        f'<g stroke="{color}" stroke-width="1.5" fill="none">'
        f'<rect x="{cx-20}" y="{cy-7}" width="14" height="14" rx="3"/>'
        f'<rect x="{cx+6}" y="{cy-7}" width="14" height="14" rx="3"/>'
        f'<path d="M {cx-6} {cy} H {cx+6}"/><path d="M {cx-13} {cy-7} V {cy-14} H {cx+13} V {cy-7}"/>'
        f'<path d="M {cx+13} {cy+7} V {cy+14} H {cx-13} V {cy+7}"/>'
        f"</g>"
    )


def icon_layers(cx, cy, color) -> str:
    return (
        f'<g stroke="{color}" stroke-width="1.5" fill="none">'
        f'<path d="M {cx-18} {cy-8} L {cx} {cy-18} L {cx+18} {cy-8} L {cx} {cy+2} Z"/>'
        f'<path d="M {cx-18} {cy+2} L {cx} {cy+12} L {cx+18} {cy+2}"/>'
        f'<path d="M {cx-18} {cy+10} L {cx} {cy+20} L {cx+18} {cy+10}"/>'
        f"</g>"
    )


def build_capabilities() -> None:
    w, h = 1200, 344
    b = ""
    icons = [icon_spark, icon_flow, icon_layers]
    for i, cap in enumerate(PROFILE["capabilities"]):
        x = i * 408
        b += rect(x, 4, 384, 332, 14, "url(#panel)", SLATE_700, 1.2)
        b += rect(x + 20, 4, 86, 3, 1.5, AMBER if i == 0 else SLATE_300)
        b += text(x + 24, 44, cap["index"], 12, AMBER, 600, MONO, letter=1.5)
        b += text(x + 58, 44, "CAPABILITY", 9.5, FAINT, 500, MONO, letter=1.4)
        b += icons[i](x + 344, 38, AMBER if i == 0 else MUTED)
        b += text(x + 24, 86, cap["title"], 20, TEXT, 700, SANS, letter=1.1)
        b += text(x + 24, 114, cap["subtitle"], 12.5, MUTED, 400, SANS)
        b += line(x + 24, 132, x + 360, 132, SLATE_600, 0.8, "2 6", 0.8)
        yy = 164
        for bullet in cap["bullets"]:
            b += f'<circle cx="{x + 29}" cy="{yy - 4}" r="2.6" fill="{AMBER}"/>'
            b += text(x + 42, yy, bullet, 12.8, TEXT_SOFT, 400, SANS)
            yy += 27
        b += chip_row(x + 24, 290, cap["tags"], i == 0, 11, 30, 8)
    write("capabilities.svg", svg(w, h, b, base_defs(w, h, 250, 160, 420), "Three capabilities: AI integration, automation, backend and system design"))


# ── architecture ──────────────────────────────────────────────────────────────
def build_architecture() -> None:
    w, h = 1200, 436
    b = rect(0, 0, w, h, 14, "url(#panel)", SLATE_700, 1.2)
    b += rect(0, 0, w, 44, 14, NAVY_900)
    b += rect(0, 30, w, 14, 0, NAVY_900)
    b += text(28, 28, "REQUEST LIFECYCLE", 11, AMBER, 600, MONO, letter=2.2)
    b += text(300, 28, "//  AI-AUGMENTED BACKEND", 10, FAINT, 500, MONO, letter=1.2)
    b += text(1172, 28, "SYNC EDGE  ·  ASYNC CORE", 9.5, MUTED, 500, MONO, "end", letter=1.2)

    nodes = [
        ("CLIENT / WEBHOOK", ["HTTP requests", "events · schedules"], "edge"),
        ("FASTAPI BACKEND", ["auth · validation", "rate limits"], "api"),
        ("QUEUE + WORKERS", ["Celery · Redis", "retries · scheduling"], "queue"),
        ("AI LAYER", ["LLM APIs · RAG", "tools · fallbacks"], "ai"),
        ("DATA LAYER", ["Postgres · Pinecone", "object storage"], "data"),
    ]
    x0, y0, nw, nh, gap = 36, 68, 200, 128, 32
    positions = [x0 + i * (nw + gap) for i in range(5)]

    # async feedback path (drawn behind nodes)
    ai_cx = positions[3] + nw / 2
    q_cx = positions[2] + nw / 2
    b += f'<path d="M {n(ai_cx)} 200 V 232 H {n(q_cx)} V 202" fill="none" stroke="{AMBER}" stroke-width="1.3" stroke-dasharray="5 7" opacity="0.7" class="dash"/>'
    b += f'<path d="M {n(q_cx)} 208 L {n(q_cx)} 200 L {n(q_cx-4)} 206 M {n(q_cx)} 200 L {n(q_cx+4)} 206" fill="none" stroke="{AMBER}" stroke-width="1.3"/>'
    b += text((ai_cx + q_cx) / 2, 226, "async / streaming", 9.5, AMBER, 500, MONO, "middle")

    for i, (title, sub, kind) in enumerate(nodes):
        x = positions[i]
        accent = kind == "ai"
        b += rect(x, y0, nw, nh, 12, "#121A2A" if not accent else "#1A1608", AMBER_DEEP if accent else SLATE_600, 1.4 if accent else 1)
        b += rect(x, y0, nw, 3, 1.5, AMBER if accent else SLATE_400)
        # icon
        b += f'<circle cx="{x + 30}" cy="{y0 + 36}" r="15" fill="none" stroke="{AMBER if accent else MUTED}" stroke-width="1.3"/>'
        if kind == "edge":
            b += f'<path d="M {x+23} {y0+32} h14 v10 h-14 z" fill="none" stroke="{MUTED}" stroke-width="1.2"/>'
        elif kind == "api":
            b += f'<path d="M {x+24} {y0+30} l6 6 -6 6 M {x+33} {y0+30} l6 6 -6 6" fill="none" stroke="{MUTED}" stroke-width="1.2"/>'
        elif kind == "queue":
            b += f'<path d="M {x+23} {y0+32} h14 M {x+23} {y0+37} h14 M {x+23} {y0+42} h14" stroke="{MUTED}" stroke-width="1.2"/>'
        elif kind == "ai":
            b += f'<circle cx="{x+30}" cy="{y0+36}" r="3" fill="{AMBER}"/><path d="M {x+30} {y0+24} v6 M {x+30} {y0+42} v6 M {x+18} {y0+36} h6 M {x+36} {y0+36} h6" stroke="{AMBER}" stroke-width="1.2"/>'
        else:
            b += f'<ellipse cx="{x+30}" cy="{y0+31}" rx="8" ry="3.2" fill="none" stroke="{MUTED}" stroke-width="1.1"/><path d="M {x+22} {y0+31} v10 c0 1.8 3.6 3.2 8 3.2 s8 -1.4 8 -3.2 v-10" fill="none" stroke="{MUTED}" stroke-width="1.1"/>'
        b += text(x + 56, y0 + 40, title, 14, TEXT if not accent else AMBER_SOFT, 700, SANS, letter=0.4)
        b += text(x + 20, y0 + 78, sub[0], 10.5, MUTED, 400, MONO)
        b += text(x + 20, y0 + 96, sub[1], 10.5, MUTED, 400, MONO)
        b += text(x + 20, y0 + 118, f"0{i+1}", 9.5, FAINT, 500, MONO, letter=1.2)

        if i < 4:
            ax1 = x + nw + 4
            ax2 = x + nw + gap - 4
            b += f'<line x1="{n(ax1)}" y1="{y0+64}" x2="{n(ax2)}" y2="{y0+64}" stroke="{AMBER if i >= 2 else SLATE_300}" stroke-width="1.4" stroke-dasharray="5 6" class="dash"/>'
            b += f'<path d="M {n(ax2)} {y0+64} l-6 -3 v6 z" fill="{AMBER if i >= 2 else SLATE_300}"/>'

    # reliability layer
    b += rect(36, 266, 1128, 118, 12, "#0C121C", SLATE_700, 1)
    b += text(56, 294, "RELIABILITY LAYER", 10.5, AMBER, 600, MONO, letter=1.8)
    b += text(220, 294, "//  CROSS-CUTTING CONCERNS", 9.5, FAINT, 500, MONO, letter=1.2)
    reliabilities = [
        "idempotency keys", "retry + backoff", "fallback models",
        "structured logs", "metrics + traces", "health checks",
    ]
    for i, label in enumerate(reliabilities):
        x = 56 + i * 184
        b += rect(x, 312, 168, 32, 8, "#121A2A", SLATE_600, 1)
        b += f'<circle cx="{x+14}" cy="328" r="2.4" fill="{AMBER}"/>'
        b += text(x + 24, 332, label, 10.2, TEXT_SOFT, 500, MONO)

    b += text(36, 412, "VALIDATE AT THE EDGE  ·  ENQUEUE LONG WORK  ·  ISOLATE AI PROVIDERS  ·  PERSIST EVERY RESULT  ·  OBSERVE EVERYTHING", 10.6, MUTED, 500, MONO, letter=0.5)
    css = "<style>.dash{stroke-dasharray:5 7;animation:dash 5s linear infinite}@keyframes dash{to{stroke-dashoffset:-48}}</style>"
    write("architecture.svg", svg(w, h, b, base_defs(w, h, 300, 120, 520) + css, "Request lifecycle architecture: client, FastAPI, queue, AI layer, data layer, reliability concerns"))


# ── project cards ─────────────────────────────────────────────────────────────
def build_project_card(project: dict) -> None:
    w, h = 1200, 300
    b = rect(0, 0, w, h, 14, "url(#panel)", SLATE_700, 1.2)
    b += rect(0, 0, 8, h, 14, AMBER)
    b += rect(0, 0, 8, 60, 14, AMBER)
    b += rect(0, 54, 8, 14, 0, AMBER)
    b += rect(640, 0, 560, h, 0, "url(#grid)", opacity=0.22)

    b += text(34, 42, project["index"], 12, AMBER, 600, MONO, letter=1.4)
    b += text(70, 42, project["eyebrow"], 11, MUTED, 500, MONO, letter=1.1)
    b += text(34, 94, project["title"], 38, TEXT, 700, SANS, letter=0.8)
    for i, row in enumerate(textwrap.wrap(project["tagline"], 66)[:2]):
        b += text(34, 128 + i * 21, row, 13.8, MUTED, 400, SANS)
    b += chip_row(34, 224, project["chips"], True, 11, 30, 8)
    b += text(34, 282, "OPEN REPOSITORY  ↗", 10.2, AMBER, 600, MONO, letter=1.4)

    # flow diagram
    fx, fy, fw, fh, fgap = 664, 92, 116, 58, 20
    b += text(664, 76, "SERVICE FLOW", 9.5, FAINT, 500, MONO, letter=1.5)
    for i, (label, sub) in enumerate(project["flow"]):
        x = fx + i * (fw + fgap)
        accent = i == len(project["flow"]) - 1
        b += rect(x, fy, fw, fh, 8, "#1A1608" if accent else "#121A2A", AMBER_DEEP if accent else SLATE_600, 1.2)
        lines = textwrap.wrap(label, 14)[:2]
        for j, part in enumerate(lines):
            b += text(x + fw / 2, fy + 24 + j * 13, part, 11.2, AMBER_SOFT if accent else TEXT, 600, SANS, "middle")
        b += text(x + fw / 2, fy + 48, sub, 8.9, FAINT, 400, MONO, "middle")
        if i < 3:
            ax1, ax2 = x + fw + 3, x + fw + fgap - 3
            b += line(ax1, fy + 29, ax2, fy + 29, AMBER if i >= 2 else SLATE_300, 1.2, "4 5", 0.9, 'class="dash"')
            b += f'<path d="M {n(ax2)} {fy+29} l-5 -2.6 v5.2 z" fill="{AMBER if i >= 2 else SLATE_300}"/>'
    b += text(664, 186, "REQUEST  →  EXECUTE  →  RESPOND", 9.2, FAINT, 500, MONO, letter=1.2)
    b += line(664, 202, 1166, 202, SLATE_600, 0.8, "2 7", 0.7)
    b += text(664, 228, "DESIGNED FOR FAILURE, RETRIES AND OBSERVABILITY", 9.4, MUTED, 500, MONO, letter=0.9)
    b += text(1166, 282, "@UVARAJAND", 9.5, FAINT, 500, MONO, "end", letter=1.2)

    css = "<style>.dash{stroke-dasharray:4 5;animation:dash 4.5s linear infinite}@keyframes dash{to{stroke-dashoffset:-36}}</style>"
    write(f"card-{project['index']}.svg", svg(w, h, b, base_defs(w, h, 300, 150, 520) + css, f"{project['title']} project card"))


# ── stack marquee ─────────────────────────────────────────────────────────────
def build_stack() -> None:
    w, h = 1200, 300
    b = rect(0, 0, w, h, 14, "#0C121C", SLATE_700, 1.2)
    defs = base_defs(w, h, 200, 150, 420) + f"""
<clipPath id="viewport"><rect x="196" y="0" width="984" height="{h}" rx="0"/></clipPath>
<linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{INK_850}" stop-opacity="1"/><stop offset="1" stop-color="{INK_850}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="fadeR" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{INK_850}" stop-opacity="0"/><stop offset="1" stop-color="{INK_850}" stop-opacity="1"/>
</linearGradient>
<style>
  .left {{ animation: left 34s linear infinite; }}
  .right {{ animation: right 40s linear infinite; }}
  @keyframes left {{ to {{ transform: translateX(-{0}px); }} }}
  @keyframes right {{ from {{ transform: translateX(-{0}px); }} to {{ transform: translateX(0); }} }}
</style>
"""
    # We patch the keyframe distance per row after computing widths.
    row_css = []
    for i, (label, items) in enumerate(PROFILE["stack"]):
        y = 26 + i * 88
        b += text(26, y + 26, label.split(" / ")[0], 10.5, AMBER, 600, MONO, letter=1.3)
        b += text(26, y + 46, "/ " + label.split(" / ")[1], 9.6, MUTED, 500, MONO, letter=1.0)
        b += line(176, y + 4, 176, y + 64, SLATE_700, 0.9)
        b += line(196, y + 80, 1176, y + 80, SLATE_700, 0.7, "2 7", 0.5)

        # build one group
        group = ""
        gx = 0
        for j, item in enumerate(items):
            part, width = chip(gx, y + 16, item, j % 5 == 0, 11.5, 33)
            group += part
            gx += width + 12
        total = gx - 12
        # repeat group enough times to exceed viewport twice
        copies = max(2, int(1960 / max(total, 1)) + 1)
        content = "".join(f'<g transform="translate({n(k * total)},0)">{group}</g>' for k in range(copies))
        direction = "right" if i == 1 else "left"
        b += f'<g clip-path="url(#viewport)"><g class="{direction}">{content}</g></g>'
        row_css.append((direction, total))

    # css per row (classes are shared; use nth-child selectors instead)
    # Rebuild with per-row animation names to keep distances exact.
    # (The loop above already emitted classes; override style with row-specific classes.)
    b = b.replace('class="left"', 'class="row1"', 1).replace('class="right"', 'class="row2"', 1).replace('class="left"', 'class="row3"', 1)
    total1, total2, total3 = row_css[0][1], row_css[1][1], row_css[2][1]
    css = f"""<style>
  .row1 {{ animation: row1 {max(26, total1 / 26):.1f}s linear infinite; }}
  .row2 {{ animation: row2 {max(28, total2 / 24):.1f}s linear infinite; }}
  .row3 {{ animation: row3 {max(26, total3 / 25):.1f}s linear infinite; }}
  @keyframes row1 {{ to {{ transform: translateX(-{n(total1)}px); }} }}
  @keyframes row2 {{ from {{ transform: translateX(-{n(total2)}px); }} to {{ transform: translateX(0); }} }}
  @keyframes row3 {{ to {{ transform: translateX(-{n(total3)}px); }} }}
</style>"""
    b += rect(196, 0, 46, h, 0, "url(#fadeL)")
    b += rect(1130, 0, 46, h, 0, "url(#fadeR)")
    write("stack-marquee.svg", svg(w, h, b, defs + css, "Technology stack marquee"))


# ── footer ────────────────────────────────────────────────────────────────────
def build_footer() -> None:
    w, h = 1200, 166
    b = rect(0, 0, w, h, 14, "url(#panel)", SLATE_700, 1.2)
    b += line(0, 2, 1200, 2, "url(#lineGrad)", 1.4)
    b += rect(580, 0, 40, 4, 2, AMBER)
    for x, dx in [(24, 1), (1176, -1)]:
        b += f'<path d="M {x} 120 L {x} 100 L {x + dx*10} 100 L {x + dx*10} 92 L {x + dx*20} 92 L {x + dx*20} 80" fill="none" stroke="{AMBER}" stroke-width="1.3" opacity="0.5"/>'
    b += text(600, 48, PROFILE["name"].upper(), 25, TEXT, 700, SANS, "middle", letter=3.5)
    b += text(600, 74, "[ AI INTEGRATION  ·  AUTOMATION  ·  BACKEND  ·  SYSTEM DESIGN ]", 11, AMBER, 600, MONO, "middle", letter=1.2)
    b += text(600, 98, "DATA  →  LLM  →  API", 9.5, MUTED, 500, MONO, "middle", letter=1.6)
    b += f'<circle cx="468" cy="116" r="3" fill="{AMBER}" class="pulse"/>'
    b += text(480, 120, "github.com/UVARAJAND", 9.6, TEXT_SOFT, 500, MONO)
    b += text(600, 120, "·", 9.6, FAINT, 500, MONO, "middle")
    b += text(720, 120, "uvarajan-d.vercel.app", 9.6, TEXT_SOFT, 500, MONO)
    b += text(600, 148, "BUILT FOR RELIABLE SYSTEMS  //  2026", 9.5, MUTED, 500, MONO, "middle", letter=1.2)
    css = "<style>.pulse{animation:pulse 2.6s ease-in-out infinite}@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}</style>"
    write("footer.svg", svg(w, h, b, base_defs(w, h, 600, 80, 420) + css, "Footer"))


# ── wire buttons ──────────────────────────────────────────────────────────────
def button_icon(kind: str, cx: float, cy: float, color: str) -> str:
    if kind == "globe":
        return (
            f'<g fill="none" stroke="{color}" stroke-width="1.3">'
            f'<circle cx="{cx}" cy="{cy}" r="7.5"/><ellipse cx="{cx}" cy="{cy}" rx="3.2" ry="7.5"/>'
            f'<path d="M {cx-7.5} {cy} H {cx+7.5}"/></g>'
        )
    if kind == "linkedin":
        return (
            f'<g fill="none" stroke="{color}" stroke-width="1.3">'
            f'<rect x="{cx-8}" y="{cy-8}" width="16" height="16" rx="3"/>'
            f'<path d="M {cx-4} {cy+4} V {cy-2} M {cx-4} {cy-5.5} V {cy-5} M {cx} {cy+4} V {cy-2} M {cx} {cy-3} c0 -1.5 4 -1.8 4 1 v6"/></g>'
        )
    if kind == "telegram":
        return (
            f'<g fill="none" stroke="{color}" stroke-width="1.3">'
            f'<path d="M {cx-9} {cy} L {cx+9} {cy-6} L {cx+4} {cy+8} L {cx} {cy+3} L {cx-3} {cy+6} L {cx-3} {cy+1} L {cx+5} {cy-3} L {cx-5} {cy+2}"/></g>'
        )
    if kind == "mail":
        return (
            f'<g fill="none" stroke="{color}" stroke-width="1.3">'
            f'<rect x="{cx-9}" y="{cy-6}" width="18" height="13" rx="2"/>'
            f'<path d="M {cx-8} {cy-5} L {cx} {cy+1} L {cx+8} {cy-5}"/></g>'
        )
    # github / code
    return (
        f'<g fill="none" stroke="{color}" stroke-width="1.3">'
        f'<circle cx="{cx-5}" cy="{cy-5}" r="3"/><circle cx="{cx-5}" cy="{cy+5}" r="3"/><circle cx="{cx+6}" cy="{cy}" r="3"/>'
        f'<path d="M {cx-2} {cy-5} C {cx+2} {cy-5} {cx+2} {cy} {cx+3} {cy} M {cx-2} {cy+5} C {cx+2} {cy+5} {cx+2} {cy} {cx+3} {cy}"/></g>'
    )


def build_buttons() -> None:
    buttons = [
        ("portfolio", "PORTFOLIO", "globe"),
        ("linkedin", "LINKEDIN", "linkedin"),
        ("telegram", "TELEGRAM", "telegram"),
        ("email", "EMAIL", "mail"),
    ]
    for slug, label, icon in buttons:
        w, h = 190, 44
        b = rect(1, 1, w - 2, h - 2, 8, INK_800, SLATE_400, 1)
        b += f'<path d="M 1 12 L 1 1 L 12 1" fill="none" stroke="{AMBER}" stroke-width="1.6"/>'
        b += f'<path d="M {w-1} {h-12} L {w-1} {h-1} L {w-12} {h-1}" fill="none" stroke="{AMBER}" stroke-width="1.6"/>'
        b += button_icon(icon, 24, 22, AMBER)
        b += text(42, 27, label, 12, TEXT, 600, SANS, letter=1.3)
        b += f'<circle cx="{w-15}" cy="22" r="2.2" fill="{AMBER}" class="pulse"/>'
        css = "<style>.pulse{animation:pulse 2.8s ease-in-out infinite}@keyframes pulse{0%,100%{opacity:.3}50%{opacity:1}}</style>"
        write(f"btn-{slug}.svg", svg(w, h, b, css, f"{label} link button"))


# ── README ────────────────────────────────────────────────────────────────────
def build_readme() -> None:
    links = PROFILE["links"]
    p = PROFILE["projects"]

    def project_block(index: int, heading: str, bullets: list[str], tags: str, note: str = "") -> str:
        item = p[index]
        out = f'<a href="{item["url"]}"><img src="./assets/card-{item["index"]}.svg" width="100%" alt="{item["title"]} project card"/></a>\n\n'
        out += f'### {item["index"]} · {heading}\n\n'
        if note:
            out += f"> {note}\n\n"
        out += "\n".join(f"- {b}" for b in bullets) + "\n\n"
        out += "  ".join(f"`{t.strip()}`" for t in tags.split("·")) + "\n\n"
        return out.rstrip()

    readme = f"""<div align="center">
  <img src="./assets/header.svg" width="100%" alt="Uvarajan D — AI Integration and Automation Engineer, Backend Developer, System Design"/>
</div>

<br/>

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/ticker.svg"/>
    <source media="(prefers-color-scheme: light)" srcset="./assets/ticker-light.svg"/>
    <img src="./assets/ticker.svg" width="100%" alt="Integrating LLMs, automating pipelines and designing backends"/>
  </picture>
</div>

<br/>

<div align="center">

<a href="{links['portfolio']}"><img src="./assets/btn-portfolio.svg" height="44" alt="Portfolio"/></a>
<a href="{links['linkedin']}"><img src="./assets/btn-linkedin.svg" height="44" alt="LinkedIn"/></a>
<a href="{links['telegram']}"><img src="./assets/btn-telegram.svg" height="44" alt="Telegram"/></a>
<a href="{links['email']}"><img src="./assets/btn-email.svg" height="44" alt="Email"/></a>

</div>

<br/>

<div align="center"><img src="./assets/divider.svg" width="100%" alt=""/></div>

<div align="center"><img src="./assets/label-whoami.svg" width="100%" alt="Whoami"/></div>

<br/>

<div align="center"><img src="./assets/whoami-focus.svg" width="100%" alt="whoami and current focus terminal panels"/></div>

<br/>

<div align="center"><img src="./assets/label-capabilities.svg" width="100%" alt="What I build"/></div>

<br/>

<div align="center"><img src="./assets/capabilities.svg" width="100%" alt="Capabilities: AI integration, automation, backend and system design"/></div>

<br/>

<div align="center"><img src="./assets/label-architecture.svg" width="100%" alt="System architecture"/></div>

<br/>

<div align="center"><img src="./assets/architecture.svg" width="100%" alt="Architecture: client to FastAPI to queue to AI layer to data layer, with a reliability layer"/></div>

> **How I think about it:** validate at the edge, enqueue the slow work, isolate every AI provider behind a contract, make retries idempotent, persist the result, and instrument the whole path.

<br/>

<div align="center"><img src="./assets/label-work.svg" width="100%" alt="Selected work"/></div>

<br/>

{project_block(0, "Observe AI — Agentic Proctoring Platform", [
    "Multi-service monorepo: FastAPI core API, React dashboards, PyQt6 proctoring client, Docker code-execution sandbox, LangGraph question morphing, JIT generation and report publishing.",
    "PostgreSQL on Neon for domain data, Supabase Storage for evidence and report artifacts, Groq as the primary LLM with Gemini fallbacks.",
    "JWT auth for web roles and HMAC-signed requests for the desktop client; signed telemetry flows through the report pipeline.",
    "Coordinates adaptive exams, isolated code execution and proctoring evidence end to end.",
], "Python · FastAPI · React · PyQt6 · Docker · LangGraph · PostgreSQL · Supabase")}

{project_block(1, "ALEC — Autonomous Legal Entity for Contracts", [
    "Risk analysis at clause level with BERT-large and SHAP explanations, plus summarization, company diligence and contract drafting services.",
    "Company diligence aggregates OpenCorporates, SerpAPI, AlphaVantage and NewsAPI into one reviewable report.",
    "RAG over Pinecone with All-MiniLM-L6-v2 embeddings; LLaMA 3.3 70B handles generation and drafting.",
    "Template-based and autonomous negotiation flows share one document and session store.",
], "React · FastAPI · MongoDB · Pinecone · BERT · SHAP · LLaMA 3.3 70B", "Team project — Code Blenders")}

{project_block(2, "Agentic RAG — Knowledge Retrieval", [
    "Multi-agent RAG over the Bhagavad Gita and Yoga Sutras, with query refinement, semantic retrieval and a feedback loop.",
    "Pinecone stores Sentence Transformers embeddings; Llama 3.3 70B runs through Ollama for offline use or Groq for hosted inference.",
    "FastAPI application with SQLite session history and a JSON output format for traceable answers.",
    "Evaluated on a 46-question set spanning both source texts, with saved outputs for review.",
], "Python · FastAPI · Pinecone · Sentence Transformers · Llama 3.3 · Ollama · Groq", "Team project — Code Blenders")}

<div align="center"><img src="./assets/label-stack.svg" width="100%" alt="Tech stack"/></div>

<br/>

<div align="center"><img src="./assets/stack-marquee.svg" width="100%" alt="Technology stack"/></div>

<br/>

<div align="center"><img src="./assets/label-telemetry.svg" width="100%" alt="GitHub telemetry"/></div>

<br/>

<div align="center">
  <img src="https://camo.githubusercontent.com/a7755dbf4f2aaa452c59acf609a119cc114ed749dc4c929bcb2511162bea2167/68747470733a2f2f6769746875622d726561646d652d73747265616b2d73746174732e6865726f6b756170702e636f6d2f3f757365723d55564152414a414e442673686f775f69636f6e733d747275652662675f636f6c6f723d303030303030267469746c655f636f6c6f723d33386236666626746578745f636f6c6f723d6666666666662669636f6e5f636f6c6f723d3338623666662663616368655f6275737465723d3132333435" width="495" alt="GitHub streak stats: total contributions, current streak, longest streak"/>
</div>

<br/>

<div align="center"><img src="./assets/label-activity.svg" width="100%" alt="Activity matrix"/></div>

<br/>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/github-contribution-grid-snake-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="./assets/github-contribution-grid-snake.svg"/>
  <img alt="GitHub contribution snake" src="./assets/github-contribution-grid-snake-dark.svg" width="100%"/>
</picture>

</div>

<br/>

<div align="center"><img src="./assets/footer.svg" width="100%" alt="Uvarajan D — AI integration, automation, backend, system design"/></div>
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    print(f"  README.md  ({len(readme) / 1024:.1f} KB)")


def build_workflow() -> None:
    wf = """name: Generate Contribution Snake

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:
  push:
    branches:
      - main
    paths:
      - ".github/workflows/snake.yml"
      - "scripts/**"

concurrency:
  group: contribution-snake
  cancel-in-progress: true

jobs:
  generate:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    permissions:
      contents: write

    steps:
      - name: Checkout main
        uses: actions/checkout@v4
        with:
          ref: main

      - name: Generate snake animation
        uses: Platane/snk/svg-only@v3
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/github-contribution-grid-snake.svg
            dist/github-contribution-grid-snake-dark.svg?palette=github-dark

      - name: Publish snake SVGs to main
        run: |
          mkdir -p assets
          cp dist/github-contribution-grid-snake.svg assets/github-contribution-grid-snake.svg
          cp dist/github-contribution-grid-snake-dark.svg assets/github-contribution-grid-snake-dark.svg
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add assets/github-contribution-grid-snake.svg assets/github-contribution-grid-snake-dark.svg
          if git diff --cached --quiet; then
            echo "Snake assets are already up to date."
            exit 0
          fi
          git commit -m "chore(snake): update contribution snake [skip ci]"
          git push origin main
"""
    path = ROOT / ".github" / "workflows" / "snake.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(wf, encoding="utf-8")
    print(f"  {path.relative_to(ROOT)}")


def main() -> None:
    print("Building profile assets...")
    build_header()
    build_ticker()
    build_divider()
    build_labels()
    build_terminals()
    build_capabilities()
    build_architecture()
    for project in PROFILE["projects"]:
        build_project_card(project)
    build_stack()
    build_footer()
    build_buttons()
    build_readme()
    build_workflow()
    print("Done.")


if __name__ == "__main__":
    main()
