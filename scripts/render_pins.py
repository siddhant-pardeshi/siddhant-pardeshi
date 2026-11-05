#!/usr/bin/env python3
"""Render self-hosted repo pin cards (neon HUD style) from the GitHub REST API.

No third-party service involved: cards are written to assets/pins/ and committed
by the cards workflow, so they are served by GitHub itself and never fail.
"""
import html
import json
import os
import textwrap
import urllib.request

PINS = [p.strip() for p in os.environ.get(
    "PINS",
    "siddhant-pardeshi/BankNest,siddhant-pardeshi/BloodDonation-Management,Arya-jannawar/MetroMind",
).split(",") if p.strip()]
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = "assets/pins"
FONT = "Cascadia Code, Consolas, 'JetBrains Mono', Menlo, monospace"

LANG_COLORS = {
    "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "Java": "#b07219",
    "Python": "#3572A5", "C": "#555555", "C++": "#f34b7d", "C#": "#178600",
    "HTML": "#e34c26", "CSS": "#563d7c", "Shell": "#89e051", "Go": "#00ADD8",
    "Kotlin": "#A97BFF", "SQL": "#e38c00",
}


def fetch(repo: str) -> dict:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}",
        headers={
            "User-Agent": "pins-renderer",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def render(repo: str, data: dict) -> str:
    owner, name = repo.split("/", 1)
    lang = data.get("language") or "Code"
    lang_color = LANG_COLORS.get(lang, "#8b949e")
    stars = data.get("stargazers_count", 0)
    forks = data.get("forks_count", 0)
    desc = data.get("description") or "No description provided."
    wrapped = textwrap.wrap(desc, 50)
    lines = wrapped[:3]
    if len(wrapped) > 3:
        lines[2] = lines[2].rstrip(" .,;") + "…"

    def star_path(cx: float, cy: float, r: float, fill: str) -> str:
        import math
        pts = []
        for i in range(10):
            rad = r if i % 2 == 0 else r * 0.45
            a = -math.pi / 2 + i * math.pi / 5
            pts.append(f"{cx + rad * math.cos(a):.1f},{cy + rad * math.sin(a):.1f}")
        return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'

    desc_svg = "".join(
        f'<text x="24" y="{96 + i * 19}" font-family="{FONT}" font-size="12.5" fill="#8b949e">{esc(line)}</text>'
        for i, line in enumerate(lines)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="200" viewBox="0 0 420 200" role="img" aria-label="{esc(repo)}: {esc(desc)}">
  <rect x="1.5" y="1.5" width="417" height="197" rx="12" fill="#0d1117" stroke="#22d3ee" stroke-width="1.4"/>
  <text x="24" y="42" font-family="{FONT}" font-size="12" fill="#8b949e">{esc(owner)}</text>
  <text x="24" y="66" font-family="{FONT}" font-weight="bold" font-size="17" fill="#7cc7ff">{esc(name[:32])}</text>
  {desc_svg}
  <line x1="20" y1="156" x2="400" y2="156" stroke="#1c2a44" stroke-width="1.2"/>
  <circle cx="28" cy="177" r="6" fill="{lang_color}"/>
  <text x="40" y="181" font-family="{FONT}" font-size="13" fill="#c9d1d9">{esc(lang)}</text>
  {star_path(316, 176, 8, "#ffd166")}
  <text x="330" y="181" font-family="{FONT}" font-size="13" fill="#c9d1d9">{stars}</text>
  <text x="368" y="181" font-family="{FONT}" font-size="13" fill="#5b8ba8">⑂ {forks}</text>
</svg>'''


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for repo in PINS:
        data = fetch(repo)
        path = os.path.join(OUT, repo.split("/", 1)[1] + ".svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(repo, data))
        print(f"rendered {path} ({data.get('stargazers_count', 0)} stars)")


if __name__ == "__main__":
    main()
