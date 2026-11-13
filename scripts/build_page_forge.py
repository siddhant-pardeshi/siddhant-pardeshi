#!/usr/bin/env python3
"""Build the SIGNATURE page-forge animation: six robot cursors build a
mini profile preview live, one-shot SMIL timeline (refresh to replay).
Output: assets/svg/page-forge.svg — placed at the very top of the README."""
import os

FONT = "Cascadia Code, Consolas, 'JetBrains Mono', Menlo, monospace"
W, H = 1500, 520

CREW = [
    # name, color, start (offscreen), target (tip pos), glide begin
    ("SCOUT",   "#00e5ff", (-90, 640),  (150, 132), 0.9),
    ("TYPESET", "#ff2e97", (1590, -50), (170, 150), 1.1),
    ("LAYOUT",  "#bd5fff", (-90, -60),  (150, 226), 1.3),
    ("MOTION",  "#39ff14", (1590, 640), (620, 330),  1.5),
    ("QA",      "#ffd166", (-90, 640),  (150, 402),  1.7),
    ("DEPLOY",  "#00ffa3", (1590, 200), (900, 402),  1.9),
]


def cursor(name: str, color: str, start: tuple, target: tuple, begin: float) -> str:
    sx, sy = start
    tx, ty = target
    return f'''
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{begin}s" fill="freeze"/>
    <animate attributeName="opacity" to="0.3" dur="0.6s" begin="8.6s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" from="{sx} {sy}" to="{tx} {ty}"
      begin="{begin}s" dur="0.75s" fill="freeze" calcMode="spline" keySplines="0.3 0 0.2 1"/>
    <path d="M 0 0 L 0 16 L 4.4 12.6 L 7.4 19 L 10.4 17.6 L 7.4 11.6 L 12.6 11.6 Z"
          fill="{color}" stroke="#05070d" stroke-width="1"/>
    <g transform="translate(13,4)">
      <rect width="58" height="17" rx="8.5" fill="#0a0f1a" stroke="{color}" stroke-width="1"/>
      <text x="31" y="12" text-anchor="middle" font-family="{FONT}" font-size="9.5" letter-spacing="1" fill="{color}">{name}</text>
      <g transform="translate(8,-12)">
        <rect width="14" height="11" rx="3" fill="#0d1117" stroke="{color}" stroke-width="1"/>
        <circle cx="4.5" cy="5.5" r="1.7" fill="#7ee0ff">
          <animate attributeName="opacity" values="1;0.15;1" dur="1.4s" repeatCount="indefinite"/>
        </circle>
        <circle cx="9.5" cy="5.5" r="1.7" fill="#7ee0ff">
          <animate attributeName="opacity" values="0.15;1;0.15" dur="1.4s" repeatCount="indefinite"/>
        </circle>
        <line x1="7" y1="0" x2="7" y2="-4" stroke="{color}" stroke-width="1.2"/>
        <circle cx="7" cy="-5.4" r="1.9" fill="{color}">
          <animate attributeName="r" values="1.9;2.7;1.9" dur="1.8s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="1;0.4;1" dur="1.8s" repeatCount="indefinite"/>
        </circle>
      </g>
    </g>
  </g>'''


def wireframe(x: float, y: float, bw: float, bh: float, color: str, begin: float) -> str:
    corners = ""
    for cx, cy in ((x, y), (x + bw, y), (x, y + bh), (x + bw, y + bh)):
        corners += (f'<rect x="{cx-4}" y="{cy-4}" width="8" height="8" fill="{color}" opacity="0">'
                    f'<animate attributeName="opacity" from="0" to="1" dur="0.15s" begin="{begin+0.45:.2f}s" fill="freeze"/>'
                    f'</rect>')
    return (f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="10" pathLength="100" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-dasharray="100" stroke-dashoffset="100" opacity="0">'
            f'<animate attributeName="stroke-dashoffset" from="100" to="0" dur="0.5s" begin="{begin}s" fill="freeze"/>'
            f'<animate attributeName="opacity" from="0" to="0.9" dur="0.2s" begin="{begin}s" fill="freeze"/>'
            f'</rect>' + corners)


def clip_typing(cid: str, x: float, y: float, tw: float, begin: float, dur: float, text: str,
                size: float, fill: str, weight: str = "bold", spacing: str = "0") -> str:
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y-46}" width="0" height="{size+40}">'
            f'<animate attributeName="width" from="0" to="{tw}" begin="{begin}s" dur="{dur}s" fill="freeze"/>'
            f'</rect></clipPath>'
            f'<text x="{x}" y="{y}" clip-path="url(#{cid})" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{spacing}" fill="{fill}">{text}</text>')


def wipe_text(cid: str, x: float, y: float, tw: float, begin: float, dur: float, text: str,
              size: float, fill: str) -> str:
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y-40}" width="0" height="{size+30}">'
            f'<animate attributeName="width" from="0" to="{tw}" begin="{begin}s" dur="{dur}s" fill="freeze"/>'
            f'</rect></clipPath>'
            f'<text x="{x}" y="{y}" clip-path="url(#{cid})" font-family="{FONT}" font-size="{size}" '
            f'letter-spacing="1" fill="{fill}">{text}</text>')


def chip(cx: float, cy: float, cw: float, text: str, color: str, begin: float) -> str:
    return (f'<g transform="translate({cx},{cy})"><g opacity="0">'
            f'<animateTransform attributeName="transform" type="scale" values="0;1.18;1" keyTimes="0;0.7;1" '
            f'dur="0.45s" begin="{begin}s" fill="freeze"/>'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{begin}s" fill="freeze"/>'
            f'<rect x="{-cw//2}" y="-21" width="{cw}" height="42" rx="10" fill="#0a0f1a" stroke="{color}" stroke-width="1.6"/>'
            f'<text x="0" y="6" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="15" fill="{color}">{text}</text>'
            f'</g></g>')


def build() -> None:
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="Six robot cursors forge the profile live: wireframes, typing, pops and a deploy stamp">')
    defs = f'''<defs>
    <linearGradient id="pfbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0b1020"/><stop offset="0.55" stop-color="#0a0f1e"/><stop offset="1" stop-color="#05070d"/>
    </linearGradient>
    <linearGradient id="pfname" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#00e5ff"/><stop offset="0.5" stop-color="#7cc7ff"/><stop offset="1" stop-color="#c07bff"/>
    </linearGradient>
    <linearGradient id="pfglint" x1="0" y1="0" x2="0.3" y2="0">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#bfefff" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <filter id="pfsoft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="6"/></filter>
    <pattern id="pfdots" width="34" height="34" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#22304a"/></pattern>
  </defs>'''

    body = f'''
  <rect x="16" y="16" width="{W-32}" height="{H-32}" rx="18" fill="url(#pfbg)"/>
  <rect x="16" y="16" width="{W-32}" height="{H-32}" rx="18" fill="url(#pfdots)" opacity="0.5"/>
  <rect x="16" y="16" width="{W-32}" height="{H-32}" rx="18" fill="none" stroke="#1c2a44" stroke-width="1.5"/>
  <g stroke="#00e5ff" stroke-width="2.4" fill="none" opacity="0.85">
    <path d="M 38 52 L 38 36 L 54 36"/><path d="M {W-54} 36 L {W-38} 36 L {W-38} 52"/>
    <path d="M 38 {H-52} L 38 {H-36} L 54 {H-36}"/><path d="M {W-54} {H-36} L {W-38} {H-36} L {W-38} {H-52}"/>
  </g>

  <!-- boot loader -->
  <g opacity="1">
    <animate attributeName="opacity" from="1" to="0" dur="0.35s" begin="1.0s" fill="freeze"/>
    <text x="{W//2}" y="235" text-anchor="middle" font-family="{FONT}" font-size="16" letter-spacing="4" fill="#8b949e">BOOTING PROFILE FORGE — 6 CURSORS ONLINE</text>
    <rect x="{W//2-170}" y="252" width="340" height="9" rx="4.5" fill="#131c2e"/>
    <rect x="{W//2-170}" y="252" width="0" height="9" rx="4.5" fill="#00e5ff">
      <animate attributeName="width" from="0" to="340" dur="0.9s" fill="freeze"/>
    </rect>
    <text x="{W//2}" y="290" text-anchor="middle" font-family="{FONT}" font-size="13" fill="#4fd1c5">
      reading order · max 6 concurrent · refresh to replay
    </text>
  </g>

  <!-- beat 1+2: identity (Scout wireframe, Typeset types) -->
  {wireframe(140, 112, 520, 78, "#00e5ff", 1.8)}
  {clip_typing("pftype1", 162, 168, 470, 2.5, 1.0, "SIDDHANT PARDESHI", 36, "url(#pfname)")}
  <text x="672" y="168" font-family="{FONT}" font-size="13" fill="#5b8ba8" opacity="0">
    &#60;h1&#62;
    <animate attributeName="opacity" from="0" to="0.8" dur="0.3s" begin="2.3s" fill="freeze"/>
  </text>

  <!-- beat 3: subtitle (Layout wireframe, wipe) -->
  {wireframe(140, 208, 780, 56, "#bd5fff", 2.6)}
  {wipe_text("pfwipe1", 162, 246, 745, 3.3, 0.8, "SOFTWARE DEVELOPER — JAVA · SPRING BOOT · MYSQL · AWS · REACT", 17, "#8be9fd")}

  <!-- beat 4: stat chips (Motion pops) -->
  {chip(255, 330, 132, "GATE 2025 ✓", "#39ff14", 4.2)}
  {chip(525, 330, 148, "CGPA 8.13/10", "#00e5ff", 4.45)}
  {chip(812, 330, 156, "18+ REST APIs", "#ff2e97", 4.7)}

  <!-- beat 5: QA check (QA wireframe + type) -->
  {wireframe(140, 384, 640, 56, "#ffd166", 5.6)}
  {clip_typing("pftype2", 162, 422, 600, 6.2, 0.8, "✓ 74/74 checks passed — zero broken renders", 17, "#8affc1", "normal")}

  <!-- beat 6: deploy stamp (Deploy) -->
  <circle cx="1020" cy="412" r="20" fill="none" stroke="#00ffa3" stroke-width="2.5" opacity="0">
    <animate attributeName="r" values="20;96" dur="0.7s" begin="7.15s" repeatCount="1"/>
    <animate attributeName="opacity" values="0.85;0" dur="0.7s" begin="7.15s" repeatCount="1"/>
  </circle>
  <g transform="translate(1120,412) rotate(-6)"><g opacity="0">
    <animateTransform attributeName="transform" type="scale" values="0;1.22;1" keyTimes="0;0.7;1" dur="0.5s" begin="7.2s" fill="freeze"/>
    <animate attributeName="opacity" from="0" to="1" dur="0.18s" begin="7.2s" fill="freeze"/>
    <rect x="-118" y="-26" width="236" height="52" rx="10" fill="#05070d" stroke="#00ffa3" stroke-width="2.4"/>
    <text x="0" y="8" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="21" letter-spacing="3" fill="#00ffa3">DEPLOYED ✓ LIVE</text>
  </g></g>

  <!-- LIVE tag -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="8.6s" fill="freeze"/>
    <circle cx="{W-208}" cy="{H-34}" r="5" fill="#39ff14">
      <animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/>
    </circle>
    <text x="{W-194}" y="{H-30}" font-family="{FONT}" font-size="13" fill="#a7f3d0">LIVE — refresh to replay the forge</text>
  </g>

  <!-- glint + scan -->
  <rect x="-260" y="16" width="220" height="{H-32}" fill="url(#pfglint)">
    <animate attributeName="x" values="-260;{W}" dur="2.2s" begin="8.3s" repeatCount="1" fill="freeze"/>
  </rect>
  <rect x="17" y="30" width="{W-42}" height="1.5" fill="#00e5ff" opacity="0.14">
    <animate attributeName="y" values="30;{H-32};30" dur="10s" repeatCount="indefinite"/>
  </rect>'''

    crew = "".join(cursor(*c) for c in CREW)
    svg = head + defs + body + crew + "\n</svg>\n"

    import sys
    sys.stdout.write(svg)


if __name__ == "__main__":
    build()
