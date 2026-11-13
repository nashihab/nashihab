#!/usr/bin/env python3
"""Generates every SVG in assets/ locally. No third-party image services.
Static art needs nothing; stats/projects use the GitHub API (GITHUB_TOKEN optional)."""
import html, json, os, urllib.request

USER = "nashihab"
REPOS = ["site", "hex-gen", "nashihab.github.io", "AutoFileOrganizer"]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

BGD, PAN, DIM, TX, MU = "#05070d", "#0a1224", "#14315a", "#cfe8ff", "#6b7fa3"
C, M, V, G = "#00e5ff", "#ff2bd6", "#8a5cff", "#39ff88"
FONT = "JetBrains Mono, SFMono-Regular, Consolas, Menlo, monospace"
esc = html.escape


def wrap(w, h, body, defs=""):
    base = (f'<radialGradient id="bgg" cx=".75" cy=".3" r="1"><stop offset="0" stop-color="#0b1730"/><stop offset="1" stop-color="{BGD}"/></radialGradient>'
            f'<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#0f1f3a" stroke-width="1"/></pattern>'
            f'<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".28"/></pattern>'
            f'<linearGradient id="neon" x1="0" x2="1"><stop offset="0" stop-color="{C}"/><stop offset=".55" stop-color="{V}"/><stop offset="1" stop-color="{M}"/></linearGradient>'
            f'<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">'
            f'<defs>{base}{defs}</defs>'
            f'<rect width="{w}" height="{h}" rx="14" fill="url(#bgg)"/><rect width="{w}" height="{h}" rx="14" fill="url(#grid)" opacity=".55"/>'
            f'{body}<rect width="{w}" height="{h}" rx="14" fill="url(#scan)"/>'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="#12305a"/></svg>')


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name)


def track(points):
    return (";".join(f"{t:.4f}" for t, _ in points), ";".join(str(v) for _, v in points))


def chamfer(x, y, w, h, c=14):
    return f"M{x+c} {y} H{x+w} V{y+h-c} L{x+w-c} {y+h} H{x} V{y+c} Z"


def brackets(w, h, col=C, l=22, m=10):
    d = (f"M{m} {m+l} V{m} H{m+l} M{w-m-l} {m} H{w-m} V{m+l} "
         f"M{w-m} {h-m-l} V{h-m} H{w-m-l} M{m+l} {h-m} H{m} V{h-m-l}")
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2" filter="url(#glow)" opacity=".9"/>'


def trace(d, color, delay=0, dur=3):
    return (f'<path d="{d}" fill="none" stroke="{DIM}" stroke-width="2"/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" pathLength="100" stroke-dasharray="9 91" '
            f'stroke-linecap="round" filter="url(#glow)"><animate attributeName="stroke-dashoffset" values="100;0" '
            f'dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></path>')


# ---------------------------------------------------------------- banner
def banner():
    W, H = 900, 320
    lines = ["ASIC Physical Design Engineer", "PnR | CTS | MMMC | Timing",
             "Embedded Systems | IoT | Robotics", "VLSI | Automation | Hardware", "RTL -> GDSII"]
    N, slot = len(lines), 2.8
    dur = N * slot
    defs = (f'<linearGradient id="sweep" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{C}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{C}" stop-opacity=".18"/></linearGradient>')
    b = brackets(W, H)
    # circuit traces + chip
    b += trace("M520 85 H600 L640 125 H700", C, 0) + trace("M520 170 H700", M, .6) + trace("M520 255 H600 L640 215 H700", G, 1.2)
    b += trace("M890 130 H860 L840 150 H820", V, .3) + trace("M890 215 H860 L840 195 H820", C, 1.5)
    b += trace("M735 22 V110", M, .9) + trace("M785 40 V110", C, 2) + trace("M735 298 V230", G, .2) + trace("M785 298 V230", V, 1.1)
    b += f'<rect x="700" y="110" width="120" height="120" rx="10" fill="{PAN}" stroke="{C}" stroke-width="2" filter="url(#glow)"/>'
    for i in range(5):
        p = 718 + i * 20
        b += (f'<path d="M{p} 110 v-8 M{p} 230 v8 M700 {p-598} h-8 M820 {p-598} h8" stroke="{C}" stroke-width="2" opacity=".7"/>')
    b += (f'<rect x="725" y="135" width="70" height="70" rx="6" fill="none" stroke="{M}" stroke-width="1.5">'
          f'<animate attributeName="opacity" values=".3;1;.3" dur="2.4s" repeatCount="indefinite"/></rect>'
          f'<text x="760" y="177" text-anchor="middle" font-size="16" font-weight="700" fill="{C}" filter="url(#glow)">ASIC</text>'
          f'<text x="760" y="195" text-anchor="middle" font-size="9" fill="{MU}">RTL→GDSII</text>')
    # status
    b += (f'<text x="50" y="52" font-size="12" fill="{MU}" letter-spacing="2">SYS://NASHIHAB</text>'
          f'<circle cx="200" cy="48" r="4" fill="{G}" filter="url(#glow)"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>'
          f'<text x="212" y="52" font-size="12" fill="{G}" letter-spacing="2">ONLINE</text>')
    # name with glitch layers
    for col, dx in ((M, "0;0;-3;3;0;0"), (C, "0;0;3;-3;0;0")):
        b += (f'<text x="50" y="125" font-size="42" font-weight="700" fill="{col}" opacity=".55"><animate attributeName="x" values="{ "; ".join(str(50+int(v)) for v in dx.split(";")) }" '
              f'keyTimes="0;.9;.92;.94;.96;1" dur="5s" repeatCount="indefinite"/>Nahid Ahmed Shihab</text>')
    b += f'<text x="50" y="125" font-size="42" font-weight="700" fill="url(#neon)" filter="url(#glow)">Nahid Ahmed Shihab</text>'
    b += f'<text x="52" y="156" font-size="14" fill="{MU}" letter-spacing="3">@NASHIHAB  //  CIRCUITS. SILICON. CODE. REPEAT.</text>'
    # typed line
    for i, t in enumerate(lines):
        a, bb, c = i / N, i / N + .45 / N, (i + 1) / N
        wl = len(t) * 12.9 + 40
        k, v = track([(0, 0), (a, 0), (bb, wl), (c - .0001, wl), (c, 0), (1, 0)])
        defs += (f'<clipPath id="c{i}"><rect x="50" y="205" height="44" width="0"><animate attributeName="width" dur="{dur}s" '
                 f'repeatCount="indefinite" keyTimes="{k}" values="{v}"/></rect></clipPath>')
        b += (f'<text x="50" y="235" font-size="21" fill="{TX}" clip-path="url(#c{i})"><tspan fill="{M}">&gt;</tspan> {esc(t)}</text>')
        cw = (len(t) + 2) * 12.9 + 14
        kx, vx = track([(0, 50), (a, 50), (bb, 50 + cw), (c - .0001, 50 + cw), (c, 50), (1, 50)])
        ko, vo = track([(0, 0), (a, 0), (a + .0001, 1), (c - .0001, 1), (c, 0), (1, 0)])
        b += (f'<rect y="217" width="10" height="22" fill="{C}" x="50" filter="url(#glow)"><animate attributeName="x" dur="{dur}s" repeatCount="indefinite" keyTimes="{kx}" values="{vx}"/>'
              f'<animate attributeName="opacity" dur="{dur}s" repeatCount="indefinite" keyTimes="{ko}" values="{vo}"/></rect>')
    b += (f'<rect width="{W}" height="60" fill="url(#sweep)"><animate attributeName="y" values="-60;{H}" dur="5s" repeatCount="indefinite"/></rect>')
    write("banner.svg", wrap(W, H, b, defs))


# ---------------------------------------------------------------- section headers
def section(fname, title, color):
    W, H = 900, 56
    tw = len(title) * 13 + 40
    b = (f'<text x="24" y="35" font-size="18" font-weight="700" fill="{M}">//</text>'
         f'<text x="52" y="35" font-size="18" font-weight="700" fill="{color}" letter-spacing="4" filter="url(#glow)">{esc(title)}</text>'
         f'<path d="M{52+tw} 28 H{W-30}" stroke="{DIM}" stroke-width="2"/>'
         f'<path d="M{52+tw} 28 H{W-30}" stroke="{color}" stroke-width="2" pathLength="100" stroke-dasharray="6 94" filter="url(#glow)">'
         f'<animate attributeName="stroke-dashoffset" values="100;0" dur="2.6s" repeatCount="indefinite"/></path>'
         f'<path d="M{W-30} 22 l6 6 l-6 6 l-6 -6 Z" fill="{color}" filter="url(#glow)"/>')
    write(fname, wrap(W, H, b))


# ---------------------------------------------------------------- pillars
def pillars():
    W, H = 900, 170
    cards = [("ASIC PHYSICAL DESIGN", "PnR · CTS", "MMMC · STA · PV", C, "chip"),
             ("EMBEDDED SYSTEMS", "Firmware · Hardware", "IoT · Control", M, "gear"),
             ("SPACE & ROBOTICS", "Nano-satellite", "UAV · UGV · ROV", V, "orbit"),
             ("AUTOMATION", "Python · Tcl", "Shell · AI / ML", G, "term")]
    b = ""
    for i, (t, l1, l2, col, ic) in enumerate(cards):
        x, y, w, h = 20 + i * 220, 20, 200, 130
        b += (f'<path d="{chamfer(x, y, w, h)}" fill="{PAN}" stroke="{col}" stroke-width="1.5" filter="url(#glow)">'
              f'<animate attributeName="stroke-opacity" values=".45;1;.45" dur="3s" begin="{i*.5}s" repeatCount="indefinite"/></path>')
        cx, cy = x + 34, y + 38
        if ic == "chip":
            b += f'<rect x="{cx-12}" y="{cy-12}" width="24" height="24" rx="3" fill="none" stroke="{col}" stroke-width="2"/><rect x="{cx-5}" y="{cy-5}" width="10" height="10" fill="{col}"/>'
            b += "".join(f'<path d="M{cx+o} {cy-12} v-6 M{cx+o} {cy+12} v6 M{cx-12} {cy+o} h-6 M{cx+12} {cy+o} h6" stroke="{col}" stroke-width="2"/>' for o in (-6, 6))
        elif ic == "gear":
            b += (f'<g><circle cx="{cx}" cy="{cy}" r="13" fill="none" stroke="{col}" stroke-width="5" stroke-dasharray="6 5.1"/>'
                  f'<circle cx="{cx}" cy="{cy}" r="7" fill="none" stroke="{col}" stroke-width="2"/>'
                  f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="8s" repeatCount="indefinite"/></g>')
        elif ic == "orbit":
            b += (f'<circle cx="{cx}" cy="{cy}" r="5" fill="{col}"/><ellipse cx="{cx}" cy="{cy}" rx="17" ry="7" fill="none" stroke="{col}" stroke-width="1.5"/>'
                  f'<g><circle cx="{cx+17}" cy="{cy}" r="3" fill="{TX}"/><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="4s" repeatCount="indefinite"/></g>')
        else:
            b += (f'<rect x="{cx-16}" y="{cy-13}" width="32" height="26" rx="3" fill="none" stroke="{col}" stroke-width="2"/>'
                  f'<text x="{cx-10}" y="{cy+6}" font-size="15" font-weight="700" fill="{col}">&gt;_</text>')
        b += (f'<text x="{x+20}" y="{y+80}" font-size="12.5" font-weight="700" fill="{col}" letter-spacing="1">{esc(t)}</text>'
              f'<text x="{x+20}" y="{y+100}" font-size="12" fill="{TX}">{esc(l1)}</text><text x="{x+20}" y="{y+117}" font-size="12" fill="{MU}">{esc(l2)}</text>')
    write("pillars.svg", wrap(W, H, b))


# ---------------------------------------------------------------- stack
def stack():
    rows = [("LANGUAGES", C, ["Python", "C++", "C", "Verilog", "JavaScript", "HTML", "CSS", "SCSS", "Tcl", "Shell"]),
            ("PHYSICAL DESIGN", M, ["IC Physical Design", "PnR", "CTS", "MMMC", "STA", "SDC", "GDSII"]),
            ("EMBEDDED / HW", V, ["Embedded C", "ESP32", "STM32", "Arduino", "Raspberry Pi", "Altium", "KiCad"]),
            ("TOOLS / AI", G, ["Linux", "Git", "VS Code", "MATLAB", "OpenCV", "ROS", "TensorFlow", "n8n"])]
    W, left, cw = 900, 190, 8.0
    b, y = "", 26
    for label, col, items in rows:
        b += f'<text x="28" y="{y+17}" font-size="12" fill="{col}" letter-spacing="2" font-weight="700">{label}</text>'
        x = left
        for it in items:
            w = len(it) * cw + 24
            if x + w > W - 24:
                x, y = left, y + 36
            b += (f'<path d="{chamfer(x, y, w, 26, 7)}" fill="{PAN}" stroke="{col}" stroke-opacity=".7"/>'
                  f'<text x="{x+w/2}" y="{y+17}" text-anchor="middle" font-size="12" fill="{TX}">{esc(it)}</text>')
            x += w + 8
        y += 46
    write("stack.svg", wrap(W, y + 4, b))


# ---------------------------------------------------------------- flow
def flow():
    stages = ["RTL", "NETLIST", "FLOORPLAN", "PLACEMENT", "CTS", "ROUTING", "SIGNOFF", "GDSII"]
    cols = [C, C, V, V, M, M, G, G]
    W, H, bw, gap, y = 900, 170, 94, 16, 60
    x0 = (W - (len(stages) * bw + (len(stages) - 1) * gap)) / 2
    n, dur = len(stages), len(stages) * 0.9
    b = f'<text x="{W/2}" y="30" text-anchor="middle" font-size="12" fill="{MU}" letter-spacing="2">TIMING CLOSURE · MMMC · SDC · STANDARD CELLS · PV</text>'
    b += f'<path d="M{x0} {y+22} H{W-x0}" stroke="{DIM}" stroke-width="2"/>'
    for i, s in enumerate(stages):
        x, col = x0 + i * (bw + gap), cols[i]
        a, c = i / n, (i + 1) / n
        k, v = track([(0, .35), (a, .35), (a + .0001, 1), (c - .0001, 1), (c, .35), (1, .35)])
        b += (f'<path d="{chamfer(x, y, bw, 44, 10)}" fill="{PAN}" stroke="{col}" stroke-width="1.8" filter="url(#glow)">'
              f'<animate attributeName="stroke-opacity" dur="{dur}s" repeatCount="indefinite" keyTimes="{k}" values="{v}"/></path>'
              f'<text x="{x+bw/2}" y="{y+27}" text-anchor="middle" font-size="12" font-weight="700" fill="{TX}">{s}</text>'
              f'<text x="{x+6}" y="{y-8}" font-size="10" fill="{col}">0{i+1}</text>')
    b += (f'<circle r="5" fill="{TX}" filter="url(#glow)"><animateMotion dur="{dur}s" repeatCount="indefinite" path="M{x0} {y+22} H{W-x0}"/></circle>')
    b += f'<text x="{W/2}" y="{H-24}" text-anchor="middle" font-size="14" font-weight="700" fill="url(#neon)" letter-spacing="6">RTL  →  GDSII</text>'
    write("flow.svg", wrap(W, H, b))


# ---------------------------------------------------------------- GitHub API
def api(path):
    h = {"User-Agent": "readme-gen", "Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        h["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urllib.request.urlopen(urllib.request.Request("https://api.github.com" + path, headers=h), timeout=20) as r:
        return json.load(r)


LANG = {"Python": "#3572A5", "C++": "#f34b7d", "C": "#9aa4b2", "JavaScript": "#f1e05a", "HTML": "#e34c26", "CSS": "#8a5cff",
        "SCSS": "#c6538c", "Verilog": "#b2b7f8", "Shell": "#89e051", "Tcl": "#e4cc98", "TypeScript": "#3178c6"}


def stats():
    user, repos = None, []
    try:
        user, repos = api(f"/users/{USER}"), api(f"/users/{USER}/repos?per_page=100&type=owner")
    except Exception as e:
        print("stats: API unavailable, writing placeholder:", e)
    vals = [("FOLLOWERS", user["followers"] if user else "--", C), ("PUBLIC REPOS", user["public_repos"] if user else "--", M),
            ("STARS", sum(r["stargazers_count"] for r in repos) if user else "--", G)]
    langs = {}
    for r in repos:
        if not r["fork"] and r["language"]:
            langs[r["language"]] = langs.get(r["language"], 0) + 1
    W, H = 900, 220
    b = ""
    for i, (lab, val, col) in enumerate(vals):
        x = 20 + i * 295
        b += (f'<path d="{chamfer(x, 20, 270, 78)}" fill="{PAN}" stroke="{col}" stroke-opacity=".8" filter="url(#glow)"/>'
              f'<text x="{x+20}" y="68" font-size="34" font-weight="700" fill="{col}" filter="url(#glow)">{val}</text>'
              f'<text x="{x+20}" y="88" font-size="11" fill="{MU}" letter-spacing="3">{lab}</text>')
    b += f'<text x="24" y="132" font-size="12" fill="{MU}" letter-spacing="3">LANGUAGE MIX</text>'
    total = sum(langs.values())
    if total:
        x = 24
        b += '<clipPath id="bar"><rect x="24" y="142" width="852" height="12" rx="6"/></clipPath><g clip-path="url(#bar)">'
        for l, n in sorted(langs.items(), key=lambda kv: -kv[1]):
            w = 852 * n / total
            b += f'<rect x="{x}" y="142" width="{w}" height="12" fill="{LANG.get(l, MU)}"/>'; x += w
        b += "</g>"
        lx = 24
        for l, n in sorted(langs.items(), key=lambda kv: -kv[1])[:7]:
            b += (f'<circle cx="{lx+5}" cy="184" r="5" fill="{LANG.get(l, MU)}"/><text x="{lx+16}" y="188" font-size="12" fill="{TX}">{esc(l)} {100*n/total:.0f}%</text>')
            lx += 40 + len(l) * 8 + 30
    else:
        b += f'<rect x="24" y="142" width="852" height="12" rx="6" fill="{DIM}"/><text x="24" y="184" font-size="12" fill="{MU}">live data appears after the first Action run</text>'
    write("stats.svg", wrap(W, H, b))


def projects():
    cards = []
    for name in REPOS:
        try:
            r = api(f"/repos/{USER}/{name}")
            cards.append((name, r.get("description") or "", r.get("language") or "", r["stargazers_count"]))
        except Exception as e:
            print("projects: skipped", name, e)
            cards.append((name, "", "", None))
    W, cw, ch = 900, 418, 100
    rows = (len(cards) + 1) // 2
    H = 20 + rows * (ch + 16) + 4
    b, colors = "", [C, M, V, G]
    for i, (n, d, l, s) in enumerate(cards):
        x, y, col = 20 + (i % 2) * (cw + 24), 20 + (i // 2) * (ch + 16), colors[i % 4]
        d = (d[:56] + "…") if len(d) > 56 else d
        b += (f'<a href="https://github.com/{USER}/{esc(n)}" target="_blank"><path d="{chamfer(x, y, cw, ch, 16)}" fill="{PAN}" stroke="{col}" stroke-opacity=".8" filter="url(#glow)"/>'
              f'<text x="{x+20}" y="{y+34}" font-size="16" font-weight="700" fill="{col}">{esc(n)}</text>'
              f'<text x="{x+20}" y="{y+58}" font-size="12" fill="{TX if d else MU}">{esc(d) if d else "github.com/" + USER + "/" + esc(n)}</text>')
        if l:
            b += f'<circle cx="{x+25}" cy="{y+82}" r="5" fill="{LANG.get(l, MU)}"/><text x="{x+36}" y="{y+86}" font-size="12" fill="{TX}">{esc(l)}</text>'
        if s is not None:
            b += f'<text x="{x+cw-20}" y="{y+86}" text-anchor="end" font-size="12" fill="{MU}">★ {s}</text>'
        b += "</a>"
    write("projects.svg", wrap(W, H, b))


def footer():
    W, H = 900, 90
    b = (f'<path d="M40 26 H{W-40}" stroke="{DIM}" stroke-width="2"/>'
         f'<path d="M40 26 H{W-40}" stroke="{C}" stroke-width="2" pathLength="100" stroke-dasharray="5 95" filter="url(#glow)"><animate attributeName="stroke-dashoffset" values="100;0" dur="3s" repeatCount="indefinite"/></path>'
         f'<text x="{W/2}" y="62" text-anchor="middle" font-size="14" font-weight="700" fill="url(#neon)" letter-spacing="6">CIRCUITS. SILICON. CODE. REPEAT.</text>'
         f'<rect x="{W/2+232}" y="49" width="9" height="16" fill="{C}"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>')
    write("footer.svg", wrap(W, H, b))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    banner(); pillars()
    section("h-arsenal.svg", "TECH ARSENAL", C); stack()
    section("h-flow.svg", "IC PHYSICAL DESIGN", M); flow()
    section("h-projects.svg", "MAKING STUFF // JUST FOR HOBBY", V); projects()
    section("h-stats.svg", "MOMENTUM", G); stats()
    footer()
