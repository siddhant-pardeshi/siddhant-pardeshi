#!/usr/bin/env python3
"""Build THE_SAGA anime quest-log panels for the GitHub profile README.

Each panel is a self-contained animated SVG: the artwork is embedded as a
base64 data-URI (GitHub blocks external refs inside SVGs) and layered with
SMIL effects themed to each arc. Re-run after replacing artwork in Hajime_Images.
"""
import base64
import io
import os

from PIL import Image

SRC = r"C:\Users\siddh\Downloads\Hajime_Images"
OUT = os.path.join("assets", "svg", "saga")
FONT = "Cascadia Code, Consolas, 'JetBrains Mono', Menlo, monospace"

os.makedirs(OUT, exist_ok=True)


def b64(path: str, target_h: int) -> tuple[str, int, int]:
    im = Image.open(path).convert("RGB")
    w = round(im.width * target_h / im.height)
    im = im.resize((w, target_h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80, optimize=True)
    return base64.b64encode(buf.getvalue()).decode(), w, target_h


PANEL_DEFS = """
    <linearGradient id="{pid}bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{bg1}"/><stop offset="0.55" stop-color="{bg2}"/><stop offset="1" stop-color="{bg3}"/>
    </linearGradient>
    <radialGradient id="{pid}glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{glow}" stop-opacity="0.55"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/>
    </radialGradient>
    <filter id="{pid}soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6"/></filter>
    <pattern id="{pid}dots" width="34" height="34" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#22304a"/></pattern>
"""


def panel_base(pid: str, w: int, h: int, bg: tuple, arc: str, accent: str) -> tuple[str, str]:
    head = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'''
    defs = f"<defs>{PANEL_DEFS.format(pid=pid, bg1=bg[0], bg2=bg[1], bg3=bg[2], glow=accent)}</defs>"
    body = f'''
  <rect x="16" y="16" width="{w-32}" height="{h-32}" rx="18" fill="url(#{pid}bg)"/>
  <rect x="16" y="16" width="{w-32}" height="{h-32}" rx="18" fill="url(#{pid}dots)" opacity="0.5"/>
  <rect x="16" y="16" width="{w-32}" height="{h-32}" rx="18" fill="none" stroke="#1c2a44" stroke-width="1.5"/>
  <g stroke="{accent}" stroke-width="2.4" fill="none" opacity="0.85">
    <path d="M 38 52 L 38 36 L 54 36"/><path d="M {w-54} 36 L {w-38} 36 L {w-38} 52"/>
    <path d="M 38 {h-52} L 38 {h-36} L 54 {h-36}"/><path d="M {w-54} {h-36} L {w-38} {h-36} L {w-38} {h-52}"/>
  </g>
  <text x="56" y="58" font-family="{FONT}" font-size="14" letter-spacing="3" fill="{accent}" opacity="0.9">{arc}</text>'''
    return head, defs + body


def glint(pid: str, w: int, h: int) -> str:
    return f'''
  <rect x="-260" y="16" width="220" height="{h-32}" fill="url(#{pid}glow)" opacity="0.25">
    <animate attributeName="x" values="-260;{w}" dur="6.5s" repeatCount="indefinite"/>
  </rect>'''


def img_block(b64data: str, w: int, h: int, ix: int, iy: int, accent: str, flicker: str = "") -> str:
    border = f'''
  <rect x="{ix-3}" y="{iy-3}" width="{w+6}" height="{h+6}" rx="8" fill="none" stroke="{accent}" stroke-width="1.6" opacity="0.6">
    <animate attributeName="stroke-opacity" values="0.4;1;0.4" dur="3s" repeatCount="indefinite"/>
  </rect>'''
    return border + f'''
  <image x="{ix}" y="{iy}" width="{w}" height="{h}" href="data:image/jpeg;base64,{b64data}"/>{flicker}'''


def embers(pid: str, w: int, bottom: int, top: int, n: int, colors: list, seed: int = 0) -> str:
    parts = []
    for i in range(n):
        x0 = 60 + ((i * 97 + seed * 31) % (w - 120))
        sway = 14 + (i % 3) * 6
        dur = 5.5 + (i % 4) * 1.3
        col = colors[i % len(colors)]
        parts.append(f'''
    <circle cx="{x0}" r="{1.6 + (i % 3) * 0.8}" cy="{bottom}" fill="{col}" opacity="0">
      <animate attributeName="cy" values="{bottom};{top}" dur="{dur}s" begin="{i * 0.55}s" repeatCount="indefinite"/>
      <animate attributeName="cx" values="{x0};{x0 + sway};{x0 - sway};{x0}" dur="{dur}s" begin="{i * 0.55}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.85;0.7;0" dur="{dur}s" begin="{i * 0.55}s" repeatCount="indefinite"/>
    </circle>''')
    return "".join(parts)


def caption(w: int, h: int, text: str, accent: str) -> str:
    return f'''
  <line x1="36" y1="{h-64}" x2="{w-36}" y2="{h-64}" stroke="#1c2a44" stroke-width="1.2"/>
  <text x="{w//2}" y="{h-34}" text-anchor="middle" font-family="{FONT}" font-size="15.5" letter-spacing="1" fill="{accent}">{text}</text>'''


# ─────────────────────────── ARC 01 — NARUTO (the grind) ───────────────────────────
def build_naruto() -> None:
    data, iw, ih = b64(os.path.join(SRC, "Naruto.jpg"), 610)
    w, h = 700, 780
    ix, iy = (w - iw) // 2, 30
    head, body = panel_base("nz", w, h, ("#101408", "#0d1117", "#05070d"), "ARC 01 — THE GRIND", "#ffb347")
    svg = head + defs_part(body) + f'''
  <ellipse cx="{ix + iw//2}" cy="{iy + 170}" rx="230" ry="170" fill="url(#nzglow)">
    <animate attributeName="opacity" values="0.35;0.7;0.35" dur="3.4s" repeatCount="indefinite"/>
  </ellipse>''' + img_block(data, iw, ih, ix, iy, "#ffb347") + embers("nz", w, h - 80, 120, 11, ["#ffd166", "#ffb347", "#ffe28a"], 1) + glint("nz", w, h) + caption(w, h, "THE NINJA WAY — grind in silence, let the results make the noise", "#ffd166") + "\n</svg>\n"
    write("saga-naruto.svg", svg)


# ─────────────────────── ARC 02 — SOLO LEVELING (level up) ───────────────────────
def build_solo() -> None:
    data, iw, ih = b64(os.path.join(SRC, "Solo Leveling.jpg"), 640)
    w, h = 1400, 760
    ix, iy = 955, 40
    head, body = panel_base("sl", w, h, ("#0a0618", "#0b0d1e", "#05060d"), "ARC 02 — LEVEL UP", "#a78bfa")
    flames = ""
    for i, (fx, fs) in enumerate([(200, 1.0), (330, 0.8), (470, 1.15), (600, 0.9), (760, 1.05), (880, 0.85)]):
        base_y = 118 + fs * 10
        flames += f'''
    <g transform="translate({fx},{base_y})">
      <path d="M 0,0 C -26,18 20,34 0,60 C -18,36 -8,12 0,0 Z" fill="#8b5cf6" opacity="0.65">
        <animateTransform attributeName="transform" type="scale" values="1;0.72;1.06;0.8;1" dur="{0.9 + i * 0.17:.2f}s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.65;0.35;0.8;0.4;0.65" dur="{0.9 + i * 0.17:.2f}s" repeatCount="indefinite"/>
      </path>
    </g>'''
    sys_lines = [
        (0.6, "&#8250; quest complete — 12 certifications sealed in the vault"),
        (1.2, "&#8250; level up — software developer · entry class broken through"),
        (1.8, "&#8250; boss cleared — DevDay Exchange · 4th place overall"),
        (2.4, "&#8250; shadow army — 47 repositories recruited and counting"),
    ]
    lines_svg = "".join(
        f'\n  <text x="130" y="{215 + i * 34}" font-family="{FONT}" font-size="16" fill="#93c5fd" opacity="0">{txt}<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{b}s" fill="freeze"/></text>'
        for i, (b, txt) in enumerate(sys_lines)
    )
    svg = head + defs_part(body) + flames + f'''
  <rect x="90" y="130" width="640" height="420" rx="12" fill="#040a18" opacity="0.92" stroke="#00b0ff" stroke-width="2"/>
  <rect x="90" y="130" width="640" height="42" rx="12" fill="#061021"/>
  <circle cx="116" cy="151" r="5" fill="#00b0ff"><animate attributeName="opacity" values="1;0.25;1" dur="1.3s" repeatCount="indefinite"/></circle>
  <text x="134" y="157" font-family="{FONT}" font-size="15" letter-spacing="4" fill="#00b0ff">SYSTEM</text>
  <text x="705" y="157" text-anchor="end" font-family="{FONT}" font-size="12" fill="#3b82f6">PLAYER: SIDDHANT-PARDESHI</text>{lines_svg}
  <text x="130" y="380" font-family="{FONT}" font-weight="bold" font-size="44" letter-spacing="10" fill="#dbeafe" opacity="0" filter="url(#slsoft)">ARISE.
    <animate attributeName="opacity" from="0" to="1" dur="0.7s" begin="3.1s" fill="freeze"/>
    <animate attributeName="opacity" values="1;0.75;1" dur="2s" begin="3.8s" repeatCount="indefinite"/>
  </text>
  <rect x="130" y="404" width="14" height="26" fill="#93c5fd">
    <animate attributeName="opacity" values="1;0;1" dur="1.05s" begin="3.9s" repeatCount="indefinite"/>
  </rect>
  <rect x="16" y="16" width="{w-32}" height="{h-32}" fill="#cdb9ff" opacity="0">
    <animate attributeName="opacity" values="0;0;0.13;0;0;0.07;0" keyTimes="0;0.5;0.53;0.56;0.85;0.88;1" dur="6.5s" repeatCount="indefinite"/>
  </rect>''' + img_block(data, iw, ih, ix, iy, "#8b5cf6") + embers("sl", w, h - 70, 90, 12, ["#a78bfa", "#8b5cf6", "#c4b5fd"], 2) + glint("sl", w, h) + caption(w, h, "ARISE — level ups compound: certifications &#8594; hackathons &#8594; offers", "#c4b5fd") + "\n</svg>\n"
    write("saga-solo.svg", svg)


# ─────────────────────── ARC 03 — SHIELD HERO (defend) ───────────────────────
def build_shield() -> None:
    data, iw, ih = b64(os.path.join(SRC, "Shield_Hero.jpg"), 610)
    w, h = 700, 780
    ix, iy = (w - iw) // 2, 30
    cx, cy = ix + iw // 2, iy + 300
    head, body = panel_base("sh", w, h, ("#0e130a", "#0d1117", "#05070d"), "ARC 03 — SHIELD UP", "#ffd166")
    rings = ""
    for r, dur, rev in [(120, 26, True), (88, 18, False), (58, 12, True)]:
        rot = f'from="360 {cx} {cy}" to="0 {cx} {cy}"' if rev else f'from="0 {cx} {cy}" to="360 {cx} {cy}"'
        rings += f'''
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ffd166" stroke-width="1.4" stroke-dasharray="6 12" opacity="0.5">
    <animateTransform attributeName="transform" type="rotate" {rot} dur="{dur}s" repeatCount="indefinite"/>
  </circle>'''
    svg = head + defs_part(body) + f'''
  <ellipse cx="{cx}" cy="{cy}" rx="240" ry="200" fill="url(#shglow)">
    <animate attributeName="opacity" values="0.3;0.6;0.3" dur="3.8s" repeatCount="indefinite"/>
  </ellipse>{rings}''' + img_block(data, iw, ih, ix, iy, "#ffd166") + embers("sh", w, h - 80, 110, 9, ["#ffd166", "#fbbf24", "#fde68a"], 3) + glint("sh", w, h) + caption(w, h, "SHIELD UP — defending the realm: HospitalShield-AI &#183; FUSION 2026", "#fde68a") + "\n</svg>\n"
    write("saga-shield.svg", svg)


# ──────────────────── ARC 04 — HAJIME REFORGED (red burst) ────────────────────
def build_hajime_red() -> None:
    data, iw, ih = b64(os.path.join(SRC, "Hajime_1.jpg"), 560)
    w, h = 700, 780
    ix, iy = (w - iw) // 2, 30
    head, body = panel_base("hj", w, h, ("#140508", "#0d0b10", "#070508"), "ARC 04 — REFORGED", "#ff2e97")
    shake = f'''
  <g>
    <animateTransform attributeName="transform" type="translate" values="0,0;-1.4,0.9;1.1,-0.7;-0.8,-1;0,0" dur="0.4s" repeatCount="indefinite"/>''' + img_block(data, iw, ih, ix, iy, "#ff2e97") + '''
    <rect x="{gx}" y="{gy1}" width="342" height="7" fill="#ff2e97" opacity="0">
      <animate attributeName="opacity" values="0;0;0.8;0;0" keyTimes="0;0.62;0.66;0.7;1" dur="3.8s" repeatCount="indefinite"/>
      <animate attributeName="x" values="{gx};{gx2};{gx};{gx2};{gx}" dur="0.24s" repeatCount="indefinite"/>
    </rect>
    <rect x="{gx}" y="{gy2}" width="266" height="5" fill="#61dafb" opacity="0">
      <animate attributeName="opacity" values="0;0;0.7;0;0" keyTimes="0;0.3;0.34;0.38;1" dur="4.6s" repeatCount="indefinite"/>
      <animate attributeName="x" values="{gx};{gx2};{gx};{gx2};{gx}" dur="0.2s" repeatCount="indefinite"/>
    </rect>
  </g>'''.replace("{gx}", str(ix)).replace("{gx2}", str(ix + 52)).replace("{gy1}", str(iy + 160)).replace("{gy2}", str(iy + 330))
    sparks = ""
    for i in range(6):
        x0 = 120 + (i * 103) % 460
        sparks += f'''
    <line x1="{x0}" y1="{iy + 240}" x2="{x0 + 14}" y2="{iy + 228}" stroke="#ff4d6d" stroke-width="2.4" stroke-linecap="round" opacity="0">
      <animate attributeName="opacity" values="0;0;0.95;0;0" keyTimes="0;0.4;0.48;0.56;1" dur="{3 + i * 0.7:.1f}s" begin="{i * 0.35}s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" values="0,0;{(-1) ** i * 26},{-18 - i * 2}" dur="{3 + i * 0.7:.1f}s" begin="{i * 0.35}s" repeatCount="indefinite"/>
    </line>'''
    svg = head + defs_part(body) + f'''
  <ellipse cx="{ix + iw//2}" cy="{iy + 280}" rx="260" ry="220" fill="url(#hjglow)">
    <animate attributeName="opacity" values="0.4;0.75;0.4" dur="2.9s" repeatCount="indefinite"/>
  </ellipse>''' + shake + sparks + embers("hj", w, h - 80, 120, 8, ["#ff2e97", "#ff4d6d", "#ffd166"], 4) + glint("hj", w, h) + caption(w, h, "FROM COMMONPLACE TO WORLD'S STRONGEST — fresher today, industry-ready today", "#ff9ec7") + "\n</svg>\n"
    write("saga-hajime-reforged.svg", svg)


# ──────────────────── ARC 05 — HAJIME LOCK ON (precision) ────────────────────
def build_hajime_aim() -> None:
    data, iw, ih = b64(os.path.join(SRC, "Hajime_2.jpg"), 560)
    w, h = 700, 780
    ix, iy = (w - iw) // 2, 30
    mx, my = ix + int(iw * 0.2), iy + int(ih * 0.1)   # muzzle area (gun points up-left)
    head, body = panel_base("ha", w, h, ("#0d0510", "#0c0a12", "#060409"), "ARC 05 — LOCK ON", "#ff2e97")
    import math
    star_pts = " ".join(
        f"{mx + (16 if i % 2 == 0 else 6.5) * math.cos(-math.pi / 2 + i * math.pi / 5):.1f},"
        f"{my + (16 if i % 2 == 0 else 6.5) * math.sin(-math.pi / 2 + i * math.pi / 5):.1f}"
        for i in range(10)
    )
    svg = head + defs_part(body) + f'''
  <ellipse cx="{ix + iw//2}" cy="{iy + 270}" rx="250" ry="215" fill="url(#haglow)">
    <animate attributeName="opacity" values="0.38;0.7;0.38" dur="3.1s" repeatCount="indefinite"/>
  </ellipse>''' + img_block(data, iw, ih, ix, iy, "#ff2e97") + f'''
  <g opacity="0">
    <animate attributeName="opacity" values="0;0;0.95;0;0" keyTimes="0;0.86;0.9;0.94;1" dur="3.7s" repeatCount="indefinite"/>
    <polygon points="{star_pts}" fill="#fff0f5"/>
    <circle cx="{mx}" cy="{my}" r="20" fill="none" stroke="#ff2e97" stroke-width="2.5" opacity="0.9"/>
  </g>
  <circle cx="{mx}" cy="{my}" r="12" fill="none" stroke="#ff2e97" stroke-width="2" opacity="0">
    <animate attributeName="r" values="10;66" dur="3.7s" keyTimes="0;0.94" begin="0s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.85;0" dur="3.7s" keyTimes="0;0.94" begin="0s" repeatCount="indefinite"/>
  </circle>''' + embers("ha", w, h - 80, 120, 9, ["#ff2e97", "#ff6b9d", "#ffd166"], 5) + glint("ha", w, h) + caption(w, h, "AIM TRUE — precision shipping: 18+ REST APIs &#183; 4 hackathons &#183; 12 certifications", "#ff9ec7") + "\n</svg>\n"
    write("saga-hajime-lockon.svg", svg)


def defs_part(body_with_defs: str) -> str:
    # panel_base returns (head, defs+body); we pass the combined string through
    return body_with_defs


def write(name: str, svg: str) -> None:
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"{path}: {os.path.getsize(path) // 1024} KB")


if __name__ == "__main__":
    build_naruto()
    build_solo()
    build_shield()
    build_hajime_red()
    build_hajime_aim()
