#!/usr/bin/env python3
"""Build the Naruto cinematic banner (ARC 04 — THE GRIND) for the hero slot
in front of ACHIEVEMENT_LOG. Reuses helpers from build_saga."""
import math
import os

import build_saga as B

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def build_naruto_banner() -> None:
    data, iw, ih = B.b64(os.path.join(B.SRC, "Naruto.jpg"), 480)
    w, h = 1500, 560
    ix, iy = 1160, 40
    cx, cy = ix + iw // 2, iy + 240
    FONT = B.FONT

    panel_defs = B.PANEL_DEFS.format(pid="nb", bg1="#12130a", bg2="#0d1117", bg3="#05070d", glow="#ffd166")
    extra_defs = (
        '<linearGradient id="nbtitle" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#ffe28a"/><stop offset="0.5" stop-color="#ffb347"/>'
        '<stop offset="1" stop-color="#ff8c42"/></linearGradient>'
        '<linearGradient id="nbrule" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#ffb347"/><stop offset="0.8" stop-color="#ffb347"/>'
        '<stop offset="1" stop-color="#ffb347" stop-opacity="0"/></linearGradient>'
        '<radialGradient id="rsgcore" cx="0.5" cy="0.5" r="0.5">'
        '<stop offset="0" stop-color="#e0f2fe"/><stop offset="0.55" stop-color="#7dd3fc"/>'
        '<stop offset="1" stop-color="#0ea5e9" stop-opacity="0.2"/></radialGradient>'
        '<filter id="nbsoft" x="-40%" y="-40%" width="180%" height="180%">'
        '<feGaussianBlur stdDeviation="7"/></filter>'
        f'<clipPath id="nbclip"><rect x="16" y="16" width="{w-32}" height="{h-32}" rx="18"/></clipPath>'
    )
    head = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Naruto cinematic banner - rasengan orb, falling gold sparks and chakra glow around the grind">'
    defs = "<defs>" + panel_defs + extra_defs + "</defs>"

    rays = ""
    for k in range(8):
        a = k * 45 * math.pi / 180
        x2, y2 = cx + 620 * math.cos(a), cy + 620 * math.sin(a)
        rays += f'<line x1="{cx}" y1="{cy}" x2="{x2:.0f}" y2="{y2:.0f}" stroke-width="26"/>'
    falling = ""
    for i in range(12):
        x0 = 80 + ((i * 89) % (w - 160))
        dur = 4.5 + (i % 4) * 1.2
        col = ["#ffd166", "#ffb347", "#ffe28a", "#fbbf24"][i % 4]
        falling += (
            f'<circle cx="{x0}" r="{1.5 + (i % 3) * 0.7}" cy="-10" fill="{col}" opacity="0">'
            f'<animate attributeName="cy" values="-10;{h + 10}" dur="{dur}s" begin="{i * 0.4}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cx" values="{x0};{x0 + 16};{x0 - 12};{x0}" dur="{dur}s" begin="{i * 0.4}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.85;0" dur="{dur}s" begin="{i * 0.4}s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    smoke = ""
    for i, (sx, sw) in enumerate([(300, 380), (750, 460), (1150, 400)]):
        smoke += (
            f'<ellipse cx="{sx}" cy="{h - 46}" rx="{sw}" ry="26" fill="#9aa3ad" opacity="0.07">'
            f'<animate attributeName="cx" values="{sx};{sx + 60};{sx}" dur="{11 + i * 3}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.05;0.14;0.05" dur="{8 + i * 2}s" repeatCount="indefinite"/>'
            f'</ellipse>'
        )

    body = f'''
  <rect x="16" y="16" width="{w-32}" height="{h-32}" rx="18" fill="url(#nbbg)"/>
  <rect x="16" y="16" width="{w-32}" height="{h-32}" rx="18" fill="url(#nbdots)" opacity="0.5"/>
  <rect x="16" y="16" width="{w-32}" height="{h-32}" rx="18" fill="none" stroke="#1c2a44" stroke-width="1.5"/>
  <g stroke="#ffb347" stroke-width="2.4" fill="none" opacity="0.85">
    <path d="M 38 52 L 38 36 L 54 36"/><path d="M {w-54} 36 L {w-38} 36 L {w-38} 52"/>
    <path d="M 38 {h-52} L 38 {h-36} L 54 {h-36}"/><path d="M {w-54} {h-36} L {w-38} {h-36} L {w-38} {h-52}"/>
  </g>
  <g clip-path="url(#nbclip)">
    <g opacity="0.12" stroke="#ffb347">
      <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="75s" repeatCount="indefinite"/>
      {rays}
    </g>
    <ellipse cx="{cx}" cy="{cy}" rx="320" ry="260" fill="url(#nbglow)">
      <animate attributeName="opacity" values="0.5;0.9;0.5" dur="3.4s" repeatCount="indefinite"/>
    </ellipse>
    {falling}
    {smoke}
  </g>
  <text x="90" y="120" font-family="{FONT}" font-size="15" letter-spacing="4" fill="#ffb347" opacity="0.9">ARC 04 — THE GRIND</text>
  <text x="88" y="212" font-family="{FONT}" font-weight="bold" font-size="76" letter-spacing="8" fill="#ffb347" opacity="0.4" filter="url(#nbsoft)">THE GRIND</text>
  <text x="88" y="212" font-family="{FONT}" font-weight="bold" font-size="76" letter-spacing="8" fill="url(#nbtitle)">THE GRIND</text>
  <rect x="92" y="240" width="560" height="2.4" fill="url(#nbrule)">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite"/>
  </rect>
  <text x="92" y="288" font-family="{FONT}" font-size="21" letter-spacing="3" fill="#fde68a">THE NINJA WAY — GRIND IN SILENCE, SHINE IN RESULTS</text>
  <text x="92" y="500" font-family="{FONT}" font-size="16" fill="#c9d1d9"><tspan fill="#ffb347">&#8250;</tspan> grind: <tspan fill="#7ee0ff">GATE 2025</tspan> — AIR 18571 of 170,825 · CGPA 8.13/10</text>
  <text x="92" y="528" font-family="{FONT}" font-size="16" fill="#c9d1d9"><tspan fill="#ffb347">&#8250;</tspan> train: <tspan fill="#7ee0ff">DSA daily</tspan> · IT Vedant full-stack · 47 repositories</text>
'''

    # rasengan orb — bobbing, spinning, pulsing beside the raised hand
    orb = f'''
  <g>
    <animateTransform attributeName="transform" type="translate" values="0,0;0,-12;0,0" dur="3.2s" repeatCount="indefinite"/>
    <circle cx="1042" cy="130" r="34" fill="#38bdf8" opacity="0.25" filter="url(#nbsoft)">
      <animate attributeName="r" values="30;42;30" dur="2.4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1042" cy="130" r="17" fill="url(#rsgcore)"/>
    <g stroke="#7dd3fc" stroke-width="2.4" fill="none" stroke-linecap="round">
      <animateTransform attributeName="transform" type="rotate" from="0 1042 130" to="360 1042 130" dur="1.6s" repeatCount="indefinite"/>
      <path d="M 1042 112 A 18 18 0 0 1 1058 136"/>
      <path d="M 1042 148 A 18 18 0 0 1 1026 124"/>
      <path d="M 1029 118 A 18 18 0 0 1 1054 120"/>
    </g>
    <circle cx="1042" cy="130" r="24" fill="none" stroke="#bae6fd" stroke-width="1.2" opacity="0.6">
      <animate attributeName="r" values="22;34;22" dur="2.4s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.6;0.15;0.6" dur="2.4s" repeatCount="indefinite"/>
    </circle>
  </g>
'''

    svg = head + defs + body + orb
    svg += B.img_block(data, iw, ih, ix, iy, "#ffb347")
    svg += f'''
  <rect x="16" y="16" width="{w-32}" height="{h-32}" fill="#ffd166" opacity="0">
    <animate attributeName="opacity" values="0;0;0.09;0;0;0.05;0" keyTimes="0;0.5;0.53;0.56;0.86;0.89;1" dur="7.5s" repeatCount="indefinite"/>
  </rect>'''
    svg += B.embers("nb", w, h - 40, 60, 10, ["#ffd166", "#ffb347", "#ffe28a"], 8) + B.glint("nb", w, h)
    svg += f'''
  <rect x="21" y="30" width="{w-42}" height="1.5" fill="#ffb347" opacity="0.16">
    <animate attributeName="y" values="30;{h-32};30" dur="9s" repeatCount="indefinite"/>
  </rect>
</svg>'''
    B.write("naruto-banner.svg", svg)


if __name__ == "__main__":
    build_naruto_banner()
