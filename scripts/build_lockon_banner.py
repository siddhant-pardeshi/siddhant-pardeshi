#!/usr/bin/env python3
"""Build the Hajime Lock On cinematic banner (ARC 02 — LOCK ON) for the slot
after TECH_ARSENAL. Reuses helpers from build_saga."""
import math
import os

import build_saga as B

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def build_lockon_banner() -> None:
    data, iw, ih = B.b64(os.path.join(B.SRC, "Hajime_2.jpg"), 480)
    w, h = 1500, 560
    ix, iy = 100, 40
    cx, cy = ix + iw // 2, iy + 240
    mx, my = ix + int(iw * 0.2), iy + int(ih * 0.16)  # muzzle area (barrel points up-left)
    FONT = B.FONT

    panel_defs = B.PANEL_DEFS.format(pid="lk", bg1="#0d0510", bg2="#0c0a12", bg3="#060409", glow="#ff2e97")
    extra_defs = (
        '<linearGradient id="lktitle" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#ff8fb3"/><stop offset="0.5" stop-color="#ff2e97"/>'
        '<stop offset="1" stop-color="#ff6b6b"/></linearGradient>'
        '<linearGradient id="lkrule" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#ff2e97"/><stop offset="0.8" stop-color="#ff2e97"/>'
        '<stop offset="1" stop-color="#ff2e97" stop-opacity="0"/></linearGradient>'
        '<filter id="lksoft" x="-40%" y="-40%" width="180%" height="180%">'
        '<feGaussianBlur stdDeviation="7"/></filter>'
        f'<clipPath id="lkclip"><rect x="16" y="16" width="{w-32}" height="{h-32}" rx="18"/></clipPath>'
    )
    head = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Hajime Lock On cinematic banner - targeting reticle, muzzle flash strobe and shockwaves">'
    defs = "<defs>" + panel_defs + extra_defs + "</defs>"

    # targeting reticle behind the title zone
    rx, ry = 1000, 270
    ticks = ""
    for k in range(4):
        a = k * 90 * math.pi / 180
        x1, y1 = rx + 118 * math.cos(a), ry + 118 * math.sin(a)
        x2, y2 = rx + 168 * math.cos(a), ry + 168 * math.sin(a)
        ticks += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke-width="3"/>'
    reticle = f'''
  <g stroke="#ff2e97" fill="none" opacity="0.4">
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0 {rx} {ry}" to="360 {rx} {ry}" dur="24s" repeatCount="indefinite"/>
      <circle cx="{rx}" cy="{ry}" r="150" stroke-dasharray="10 16" stroke-width="2"/>
      {ticks}
    </g>
    <circle cx="{rx}" cy="{ry}" r="112" stroke-dasharray="4 10" stroke-width="1.6" opacity="0.8">
      <animateTransform attributeName="transform" type="rotate" from="360 {rx} {ry}" to="0 {rx} {ry}" dur="16s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{rx}" cy="{ry}" r="5" fill="#ff2e97" stroke="none">
      <animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/>
    </circle>
  </g>'''

    waves = ""
    for bgn in (0, 1.35, 2.7):
        waves += (
            f'<circle cx="{mx}" cy="{my}" r="24" fill="none" stroke="#ff4d6d" stroke-width="2.4" opacity="0">'
            f'<animate attributeName="r" values="24;220" dur="3.8s" begin="{bgn}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.6;0" dur="3.8s" begin="{bgn}s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    muzzle = (
        f'<g opacity="0">'
        f'<animate attributeName="opacity" values="0;0;0.95;0;0" keyTimes="0;0.86;0.9;0.94;1" dur="3.6s" repeatCount="indefinite"/>'
        f'<circle cx="{mx}" cy="{my}" r="16" fill="#fff0f5"/>'
        f'<path d="M {mx - 34} {my} L {mx + 34} {my} M {mx} {my - 34} L {mx} {my + 34}" stroke="#ff2e97" stroke-width="4" stroke-linecap="round"/>'
        f'</g>'
    )
    glitch = ""
    for gy, gc, wd in [(180, "#ff2e97", 300), (320, "#61dafb", 240), (420, "#ffffff", 200)]:
        glitch += (
            f'<rect x="600" y="{gy}" width="{wd}" height="6" fill="{gc}" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;0.75;0;0" keyTimes="0;0.6;0.64;0.68;1" dur="4.4s" repeatCount="indefinite"/>'
            f'<animate attributeName="x" values="600;624;592;600" dur="0.22s" repeatCount="indefinite"/>'
            f'</rect>'
        )

    body = f'''
  <rect x="16" y="16" width="{w-32}" height="{h-32}" rx="18" fill="url(#lkbg)"/>
  <rect x="16" y="16" width="{w-32}" height="{h-32}" rx="18" fill="url(#lkdots)" opacity="0.5"/>
  <rect x="16" y="16" width="{w-32}" height="{h-32}" rx="18" fill="none" stroke="#1c2a44" stroke-width="1.5"/>
  <g stroke="#ff2e97" stroke-width="2.4" fill="none" opacity="0.85">
    <path d="M 38 52 L 38 36 L 54 36"/><path d="M {w-54} 36 L {w-38} 36 L {w-38} 52"/>
    <path d="M 38 {h-52} L 38 {h-36} L 54 {h-36}"/><path d="M {w-54} {h-36} L {w-38} {h-36} L {w-38} {h-52}"/>
  </g>
  <g clip-path="url(#lkclip)">
    <ellipse cx="{cx}" cy="{cy}" rx="330" ry="270" fill="url(#lkglow)">
      <animate attributeName="opacity" values="0.55;0.95;0.55" dur="3.2s" repeatCount="indefinite"/>
    </ellipse>
    {reticle}
    {waves}
  </g>
  <text x="560" y="120" font-family="{FONT}" font-size="15" letter-spacing="4" fill="#ff6b9d" opacity="0.9">ARC 02 — LOCK ON</text>
  <text x="558" y="218" font-family="{FONT}" font-weight="bold" font-size="84" letter-spacing="10" fill="#ff2e97" opacity="0.4" filter="url(#lksoft)">LOCK ON</text>
  <text x="558" y="218" font-family="{FONT}" font-weight="bold" font-size="84" letter-spacing="10" fill="url(#lktitle)">LOCK ON</text>
  <rect x="562" y="248" width="700" height="2.4" fill="url(#lkrule)">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite"/>
  </rect>
  <text x="562" y="296" font-family="{FONT}" font-size="21" letter-spacing="3" fill="#ffb3c6">AIM TRUE — 18+ REST APIs · 4 HACKATHONS · 12 CERTIFICATIONS</text>
  <text x="562" y="500" font-family="{FONT}" font-size="16" fill="#c9d1d9"><tspan fill="#ff2e97">&#8250;</tspan> target: <tspan fill="#7ee0ff">Java Backend &amp; Software Engineer roles</tspan> — locked</text>
  <text x="562" y="528" font-family="{FONT}" font-size="16" fill="#c9d1d9"><tspan fill="#ff2e97">&#8250;</tspan> position: <tspan fill="#7ee0ff">Pune</tspan> · open to hybrid &amp; on-site · joining: immediate</text>
'''

    svg = head + defs + body + glitch
    svg += B.img_block(data, iw, ih, ix, iy, "#ff2e97")
    svg += muzzle
    svg += f'''
  <rect x="16" y="16" width="{w-32}" height="{h-32}" fill="#ff0033" opacity="0">
    <animate attributeName="opacity" values="0;0;0.09;0;0;0.05;0" keyTimes="0;0.48;0.51;0.54;0.85;0.88;1" dur="6.2s" repeatCount="indefinite"/>
  </rect>'''
    svg += B.embers("lk", w, h - 40, 60, 12, ["#ff2e97", "#ff4d6d", "#ffd166"], 9) + B.glint("lk", w, h)
    svg += f'''
  <rect x="21" y="30" width="{w-42}" height="1.5" fill="#ff2e97" opacity="0.16">
    <animate attributeName="y" values="30;{h-32};30" dur="8.5s" repeatCount="indefinite"/>
  </rect>
</svg>'''
    B.write("hajime-lockon-banner.svg", svg)


if __name__ == "__main__":
    build_lockon_banner()
