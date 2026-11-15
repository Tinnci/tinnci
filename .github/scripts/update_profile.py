import datetime
import json
import os
import urllib.request
from collections import Counter
from html import escape

USERNAME = "Tinnci"
OUT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(OUT_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

PALETTE = ["#FFD93D", "#FF6B6B", "#6BCB77", "#4D96FF"]

FEATURED_REPOS = [
    ("PecoFence", "RUST", "#FF6B6B", "Open-source Stardock Fences alternative for Win 11 — glass fences, live folders, tabs, Peek."),
    ("ha-tcl-udp-ac", "PYTHON", "#FFD93D", "Home Assistant integration for TCL air conditioners with local UDP & TCL+ cloud fallback."),
    ("anshin", "KOTLIN", "#FFD93D", "Medicine reminder Android app — Jetpack Compose, Material 3, MVVM, Hilt, Room."),
    ("meegle-cli", "GO", "#6BCB77", "Terminal-first CLI for Meegle (Lark Project) work items, schedules, and data."),
    ("zectrix-note4-platform", "C++", "#4D96FF", "Open firmware platform for the black-and-white Zectrix Note 4 e-paper device."),
    ("tinnci.github.io", "NEO-BRUTAL LAB", "#FF6B6B", "Personal digital garden built with React, Vite, Pele diagrams & Knowledge Graph."),
]

TECH_STACK = [
    ("RUST", "#FF6B6B"),
    ("TYPESCRIPT", "#4D96FF"),
    ("GO", "#6BCB77"),
    ("PYTHON", "#FFD93D"),
    ("C++", "#4D96FF"),
    ("KOTLIN", "#FFD93D"),
    ("FLUTTER", "#4D96FF"),
    ("REACT", "#6BCB77"),
    ("DOCKER", "#4D96FF"),
    ("LINUX", "#FFD93D"),
]


def gh_get(url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "tinnci-profile-bot"})
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_github_stats():
    user = gh_get(f"https://api.github.com/users/{USERNAME}")
    repos = []
    page = 1
    while True:
        batch = gh_get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner&page={page}")
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    repos = [r for r in repos if not r.get("private")]
    own = [r for r in repos if not r.get("fork")]
    stars = sum(r.get("stargazers_count", 0) for r in own)
    lang_counts = Counter(r["language"] for r in own if r.get("language"))
    top_langs = lang_counts.most_common(5)
    created = datetime.datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
    years = max(1, (datetime.datetime.now(datetime.timezone.utc) - created).days // 365)

    return {
        "public_repos": user.get("public_repos", len(repos)),
        "own_repos": len(own),
        "forks": len(repos) - len(own),
        "stars": stars,
        "followers": user.get("followers", 0),
        "following": user.get("following", 0),
        "years": years,
        "joined": created.strftime("%b %Y").upper(),
        "top_langs": top_langs,
        "repo_stars": {r["name"]: r.get("stargazers_count", 0) for r in repos},
    }


def wrap_lines(text: str, max_chars: int = 44, max_lines: int = 2):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        cand = f"{cur} {w}".strip()
        if len(cand) <= max_chars:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w
            if len(lines) == max_lines - 1:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines and len(" ".join(words)) > len(" ".join(lines)):
        if len(lines[-1]) > max_chars - 3:
            lines[-1] = lines[-1][: max_chars - 3] + "..."
        elif not lines[-1].endswith("..."):
            lines[-1] += "..."
    return lines


def render_header_svg():
    marquee_text = "RUST // TYPESCRIPT // GO // PYTHON // KOTLIN // FLUTTER // WIN32 // SHANGHAI // "
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="840" height="152" viewBox="0 0 840 152" role="img" aria-label="Hi, I'm Tinnci">
  <defs>
    <clipPath id="marqueeClip">
      <rect x="4" y="106" width="822" height="34" />
    </clipPath>
  </defs>

  <!-- Hard shadow + Main Hero Bento -->
  <rect x="12" y="12" width="822" height="136" fill="#000000" />
  <rect x="4" y="4" width="822" height="136" fill="#FFD93D" stroke="#000000" stroke-width="4" />

  <!-- Top-right corner accent tag -->
  <rect x="654" y="20" width="160" height="28" fill="#000000" />
  <g>
    <rect x="650" y="16" width="160" height="28" fill="#FF6B6B" stroke="#000000" stroke-width="3" />
    <circle cx="668" cy="30" r="5" fill="#111111">
      <animate attributeName="opacity" values="1;0.2;1" dur="1.4s" repeatCount="indefinite" />
    </circle>
    <text x="738" y="34" text-anchor="middle" font-family="'Consolas', 'Courier New', monospace" font-weight="900" font-size="11" fill="#111111" letter-spacing="1">ONLINE // DEV</text>
    <animateTransform attributeName="transform" type="translate" values="0 0;-1.5 -1.5;0 0;0 0" keyTimes="0;0.08;0.16;1" dur="5s" repeatCount="indefinite" />
  </g>

  <!-- Main Headline -->
  <text x="28" y="76" font-family="'Segoe UI', system-ui, -apple-system, sans-serif" font-weight="900" font-size="52" fill="#111111" letter-spacing="-1.5">HI, I'M TINNCI</text>
  <rect x="406" y="34" width="22" height="44" fill="#111111">
    <animate attributeName="opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite" />
  </rect>

  <!-- Bottom Marquee Strip (inspired by tinnci.github.io WindMarquee) -->
  <rect x="4" y="106" width="822" height="34" fill="#111111" stroke="#000000" stroke-width="3" />
  <g clip-path="url(#marqueeClip)">
    <g>
      <text x="16" y="128" font-family="'Consolas', 'Courier New', monospace" font-weight="900" font-size="13" fill="#FFD93D" letter-spacing="1.2">{escape(marquee_text * 3)}</text>
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-620 0" dur="14s" repeatCount="indefinite" />
    </g>
  </g>
</svg>
"""
    with open(os.path.join(OUT_DIR, "header.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)


def render_activity_svg(stats):
    top_langs = stats["top_langs"]
    max_cnt = max((c for _, c in top_langs), default=1)
    bar_colors = ["#FFD93D", "#FF6B6B", "#4D96FF", "#6BCB77", "#111111"]

    lang_rows = []
    for idx, (lang, cnt) in enumerate(top_langs):
        y_text = 72 + idx * 38
        y_rect = 58 + idx * 38
        w = max(12, int(230 * (cnt / max_cnt)))
        color = bar_colors[idx % len(bar_colors)]
        lang_rows.append(
            f'  <text x="440" y="{y_text}" class="lang">{escape(lang.upper()[:9])}</text>\n'
            f'  <rect x="520" y="{y_rect}" width="230" height="18" fill="#E5E5E5" stroke="#000000" stroke-width="2" />\n'
            f'  <rect x="520" y="{y_rect}" width="0" height="18" fill="{color}" stroke="#000000" stroke-width="2">\n'
            f'    <animate attributeName="width" from="0" to="{w}" dur="0.8s" begin="{idx * 0.1:.1f}s" fill="freeze" />\n'
            f'  </rect>\n'
            f'  <text x="766" y="{y_text}" class="cnt">{cnt}</text>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="840" height="270" viewBox="0 0 840 270" role="img" aria-label="Tinnci GitHub Activity Bento">
  <defs>
    <style>
      .num {{ font: 900 34px 'Segoe UI', system-ui, -apple-system, sans-serif; fill: #111111; }}
      .lbl {{ font: 800 11px 'Segoe UI', system-ui, -apple-system, sans-serif; fill: #111111; letter-spacing: 0.08em; }}
      .sub {{ font: 700 10px 'Consolas', 'Courier New', monospace; fill: #111111; opacity: 0.85; }}
      .lang {{ font: 800 12px 'Consolas', 'Courier New', monospace; fill: #111111; }}
      .cnt {{ font: 800 12px 'Consolas', 'Courier New', monospace; fill: #111111; }}
    </style>
  </defs>

  <rect x="10" y="10" width="190" height="115" fill="#000000" />
  <g>
    <rect x="4" y="4" width="190" height="115" fill="#FFD93D" stroke="#000000" stroke-width="3" />
    <rect x="174" y="14" width="8" height="8" fill="#111111">
      <animate attributeName="opacity" values="1;0.25;1" dur="2.4s" begin="0s" repeatCount="indefinite" />
    </rect>
    <text x="20" y="48" class="num">{stats['public_repos']}</text>
    <text x="20" y="74" class="lbl">PUBLIC REPOS</text>
    <text x="20" y="96" class="sub">{stats['own_repos']} ORIGINAL // {stats['forks']} FORKS</text>
    <animateTransform attributeName="transform" type="translate" values="0 0;-1.5 -1.5;0 0;0 0" keyTimes="0;0.08;0.16;1" dur="6s" begin="0s" repeatCount="indefinite" />
  </g>

  <rect x="218" y="10" width="190" height="115" fill="#000000" />
  <g>
    <rect x="212" y="4" width="190" height="115" fill="#FF6B6B" stroke="#000000" stroke-width="3" />
    <rect x="382" y="14" width="8" height="8" fill="#111111">
      <animate attributeName="opacity" values="1;0.25;1" dur="2.4s" begin="0.6s" repeatCount="indefinite" />
    </rect>
    <text x="228" y="48" class="num">{stats['stars']}</text>
    <text x="228" y="74" class="lbl">TOTAL STARS</text>
    <text x="228" y="96" class="sub">OWNED REPOSITORIES</text>
    <animateTransform attributeName="transform" type="translate" values="0 0;-1.5 -1.5;0 0;0 0" keyTimes="0;0.08;0.16;1" dur="6s" begin="1.5s" repeatCount="indefinite" />
  </g>

  <rect x="10" y="143" width="190" height="115" fill="#000000" />
  <g>
    <rect x="4" y="137" width="190" height="115" fill="#6BCB77" stroke="#000000" stroke-width="3" />
    <rect x="174" y="147" width="8" height="8" fill="#111111">
      <animate attributeName="opacity" values="1;0.25;1" dur="2.4s" begin="1.2s" repeatCount="indefinite" />
    </rect>
    <text x="20" y="181" class="num">{stats['followers']}</text>
    <text x="20" y="207" class="lbl">FOLLOWERS</text>
    <text x="20" y="229" class="sub">{stats['following']} FOLLOWING</text>
    <animateTransform attributeName="transform" type="translate" values="0 0;-1.5 -1.5;0 0;0 0" keyTimes="0;0.08;0.16;1" dur="6s" begin="3s" repeatCount="indefinite" />
  </g>

  <rect x="218" y="143" width="190" height="115" fill="#000000" />
  <g>
    <rect x="212" y="137" width="190" height="115" fill="#4D96FF" stroke="#000000" stroke-width="3" />
    <rect x="382" y="147" width="8" height="8" fill="#111111">
      <animate attributeName="opacity" values="1;0.25;1" dur="2.4s" begin="1.8s" repeatCount="indefinite" />
    </rect>
    <text x="228" y="181" class="num">{stats['years']} YRS</text>
    <text x="228" y="207" class="lbl">ON GITHUB</text>
    <text x="228" y="229" class="sub">JOINED {stats['joined']}</text>
    <animateTransform attributeName="transform" type="translate" values="0 0;-1.5 -1.5;0 0;0 0" keyTimes="0;0.08;0.16;1" dur="6s" begin="4.5s" repeatCount="indefinite" />
  </g>

  <rect x="428" y="10" width="402" height="248" fill="#000000" />
  <rect x="422" y="4" width="402" height="248" fill="#FAFAFA" stroke="#000000" stroke-width="3" />
  <rect x="422" y="4" width="402" height="38" fill="#111111" stroke="#000000" stroke-width="3" />
  <text x="438" y="28" font-family="'Consolas', 'Courier New', monospace" font-weight="900" font-size="13" fill="#FFD93D" letter-spacing="1">TOP LANGUAGES // OWN REPOS</text>
  <circle cx="802" cy="23" r="5" fill="#6BCB77">
    <animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite" />
  </circle>
{chr(10).join(lang_rows)}
</svg>
"""
    with open(os.path.join(OUT_DIR, "activity.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)


def render_stack_svg():
    cols = 5
    box_w, box_h = 152, 46
    gap_x, gap_y = 14, 14
    start_x, start_y = 4, 4
    items = []
    for i, (name, color) in enumerate(TECH_STACK):
        r, c = divmod(i, cols)
        x = start_x + c * (box_w + gap_x)
        y = start_y + r * (box_h + gap_y)
        items.append(
            f'  <rect x="{x + 5}" y="{y + 5}" width="{box_w}" height="{box_h}" fill="#000000" />\n'
            f'  <g>\n'
            f'    <rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" fill="{color}" stroke="#000000" stroke-width="3" />\n'
            f'    <text x="{x + box_w // 2}" y="{y + 28}" text-anchor="middle" font-family="\'Consolas\', \'Courier New\', monospace" font-weight="900" font-size="13" fill="#111111" letter-spacing="1">{escape(name)}</text>\n'
            f'    <animateTransform attributeName="transform" type="translate" values="0 0;-1.5 -1.5;0 0;0 0" keyTimes="0;0.06;0.12;1" dur="6s" begin="{i * 0.45:.2f}s" repeatCount="indefinite" />\n'
            f'  </g>'
        )

    total_w = start_x + cols * box_w + (cols - 1) * gap_x + 10
    total_h = start_y + 2 * box_h + gap_y + 10
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" viewBox="0 0 {total_w} {total_h}" role="img" aria-label="Tech Stack Bento">\n'
        + "\n".join(items)
        + "\n</svg>\n"
    )
    with open(os.path.join(ASSETS_DIR, "stack.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)


def render_project_card_svg(name: str, badge: str, color: str, desc: str, stars: int, idx: int = 0):
    lines = wrap_lines(desc, max_chars=44, max_lines=2)
    line1 = escape(lines[0]) if len(lines) > 0 else ""
    line2 = escape(lines[1]) if len(lines) > 1 else ""
    star_text = f"★ {stars}" if stars > 0 else "ACTIVE"
    slug = name.lower().replace(".", "-")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="408" height="126" viewBox="0 0 408 126" role="img" aria-label="{escape(name)}">
  <rect x="10" y="10" width="392" height="110" fill="#000000" />
  <g>
    <rect x="4" y="4" width="392" height="110" fill="#FAFAFA" stroke="#000000" stroke-width="3" />
    <rect x="4" y="4" width="392" height="36" fill="{color}" stroke="#000000" stroke-width="3" />
    <text x="18" y="27" font-family="'Segoe UI', system-ui, sans-serif" font-weight="900" font-size="16" fill="#111111">{escape(name)}</text>
    <rect x="274" y="11" width="110" height="22" fill="#111111" />
    <text x="329" y="26" text-anchor="middle" font-family="'Consolas', monospace" font-weight="800" font-size="10" fill="#FAFAFA">{escape(badge)}</text>
    <text x="18" y="64" font-family="'Segoe UI', system-ui, sans-serif" font-weight="600" font-size="12.5" fill="#111111">{line1}</text>
    <text x="18" y="83" font-family="'Segoe UI', system-ui, sans-serif" font-weight="600" font-size="12.5" fill="#111111">{line2}</text>
    <text x="18" y="102" font-family="'Consolas', monospace" font-weight="800" font-size="10.5" fill="#555555">GITHUB.COM/{USERNAME.upper()}/{escape(name.upper())}</text>
    <text x="370" y="102" text-anchor="end" font-family="'Consolas', monospace" font-weight="900" font-size="11" fill="#111111">{escape(star_text)}</text>
    <rect x="376" y="94" width="7" height="7" fill="{color}" stroke="#000000" stroke-width="1.5">
      <animate attributeName="opacity" values="1;0.25;1" dur="2.4s" begin="{idx * 0.4:.1f}s" repeatCount="indefinite" />
    </rect>
    <animateTransform attributeName="transform" type="translate" values="0 0;-1.5 -1.5;0 0;0 0" keyTimes="0;0.06;0.12;1" dur="7s" begin="{idx * 0.9:.1f}s" repeatCount="indefinite" />
  </g>
</svg>
"""
    path = os.path.join(ASSETS_DIR, f"project-{slug}.svg")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    return f"assets/project-{slug}.svg"


def render_section_title_svg(slug: str, num: str, title: str, color: str, tag: str, idx: int = 0):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="840" height="52" viewBox="0 0 840 52" role="img" aria-label="{escape(num)} {escape(title)}">
  <rect x="10" y="10" width="824" height="38" fill="#000000" />
  <g>
    <rect x="4" y="4" width="824" height="38" fill="#FAFAFA" stroke="#000000" stroke-width="3" />
    <rect x="4" y="4" width="64" height="38" fill="{color}" stroke="#000000" stroke-width="3" />
    <text x="36" y="29" text-anchor="middle" font-family="'Consolas', 'Courier New', monospace" font-weight="900" font-size="16" fill="#111111">{escape(num)}</text>
    <text x="84" y="29" font-family="'Segoe UI', system-ui, sans-serif" font-weight="900" font-size="16" fill="#111111" letter-spacing="1.2">{escape(title)}</text>
    <rect x="698" y="10" width="118" height="26" fill="#111111" />
    <rect x="707" y="20" width="6" height="6" fill="{color}">
      <animate attributeName="opacity" values="1;0.25;1" dur="2.2s" begin="{idx * 0.5:.1f}s" repeatCount="indefinite" />
    </rect>
    <text x="763" y="27" text-anchor="middle" font-family="'Consolas', 'Courier New', monospace" font-weight="800" font-size="11" fill="{color}" letter-spacing="0.8">{escape(tag)}</text>
    <animateTransform attributeName="transform" type="translate" values="0 0;-1.5 -1.5;0 0;0 0" keyTimes="0;0.05;0.10;1" dur="8s" begin="{idx * 1.2:.1f}s" repeatCount="indefinite" />
  </g>
</svg>
"""
    path = os.path.join(ASSETS_DIR, f"title-{slug}.svg")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    return f"assets/title-{slug}.svg"


def render_readme(project_cards, titles):
    rows = []
    for i in range(0, len(project_cards), 2):
        left_name, left_path = project_cards[i]
        left_cell = f'<td align="center"><a href="https://github.com/{USERNAME}/{left_name}"><img src="{left_path}" alt="{left_name}" /></a></td>'
        if i + 1 < len(project_cards):
            right_name, right_path = project_cards[i + 1]
            right_cell = f'<td align="center"><a href="https://github.com/{USERNAME}/{right_name}"><img src="{right_path}" alt="{right_name}" /></a></td>'
        else:
            right_cell = "<td></td>"
        rows.append(f"  <tr>\n    {left_cell}\n    {right_cell}\n  </tr>")

    readme = f"""<p align="center">
  <img src="header.svg" alt="Hi, I'm Tinnci" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/STUDENT_%26_SYSTEMS_BUILDER-FFD93D?style=for-the-badge&logoColor=000000" alt="Student & Systems Builder" />
  <img src="https://img.shields.io/badge/SHANGHAI%2C_CHINA-FF6B6B?style=for-the-badge&logoColor=000000" alt="Shanghai, China" />
  <a href="https://tinnci.github.io">
    <img src="https://img.shields.io/badge/BLOG_%2F_LAB-tinnci.github.io-6BCB77?style=for-the-badge&logo=safari&logoColor=000000" alt="Blog" />
  </a>
  <a href="mailto:luoyido@outlook.com">
    <img src="https://img.shields.io/badge/EMAIL-luoyido%40outlook.com-4D96FF?style=for-the-badge&logo=maildotru&logoColor=white" alt="Email" />
  </a>
</p>

<p align="center">
  <img src="{titles['projects']}" alt="01 // FEATURED PROJECTS" />
</p>

<table>
{chr(10).join(rows)}
</table>

<p align="center">
  <img src="{titles['stack']}" alt="02 // TECH STACK" />
</p>

<p align="center">
  <img src="assets/stack.svg" alt="Tech Stack Bento" />
</p>

<p align="center">
  <img src="{titles['activity']}" alt="03 // GITHUB ACTIVITY" />
</p>

<p align="center">
  <img src="activity.svg" alt="Tinnci's GitHub Activity" />
</p>
"""
    with open(os.path.join(OUT_DIR, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(readme)


def main():
    stats = fetch_github_stats()
    render_header_svg()
    render_activity_svg(stats)
    render_stack_svg()
    titles = {
        "projects": render_section_title_svg("projects", "01", "FEATURED PROJECTS", "#FF6B6B", f"{len(FEATURED_REPOS)} REPOS", 0),
        "stack": render_section_title_svg("stack", "02", "TECH STACK", "#FFD93D", f"{len(TECH_STACK)} TOOLS", 1),
        "activity": render_section_title_svg("activity", "03", "GITHUB ACTIVITY", "#6BCB77", "LIVE STATS", 2),
    }
    project_cards = []
    for idx, (name, badge, color, desc) in enumerate(FEATURED_REPOS):
        stars = stats["repo_stars"].get(name, 0)
        svg_path = render_project_card_svg(name, badge, color, desc, stars, idx)
        project_cards.append((name, svg_path))
    render_readme(project_cards, titles)
    print(f"Updated profile SVGs & README.md ({stats['public_repos']} repos, {stats['stars']} stars)")


if __name__ == "__main__":
    main()
