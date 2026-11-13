#!/usr/bin/env python3
"""Generates every SVG in assets/ locally. No third-party image services.
Static art needs nothing; stats/activity/projects use the GitHub API (GITHUB_TOKEN optional)."""
import html, json, os, urllib.request

USER = "nashihab"
REPOS = ["site", "hex-gen", "nashihab.github.io", "AutoFileOrganizer"]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

BGD, PAN, DIM, TX, MU = "#04060c", "#08111f", "#12305a", "#d6ecff", "#6b7fa3"
C, V, M, G, A = "#2ee6ff", "#8b7bff", "#ff4fd8", "#3dffa0", "#ffb347"
FONT = "JetBrains Mono, SFMono-Regular, Consolas, Menlo, monospace"
esc = html.escape


def wrap(w, h, body, defs="", ruler=False):
    base = (f'<radialGradient id="bgg" cx=".8" cy=".25" r="1.1"><stop offset="0" stop-color="#0b1a36"/><stop offset="1" stop-color="{BGD}"/></radialGradient>'
            f'<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#0d1c36" stroke-width="1"/></pattern>'
            f'<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".2"/></pattern>'
            f'<linearGradient id="neon" x1="0" x2="1"><stop offset="0" stop-color="{C}"/><stop offset="1" stop-color="{V}"/></linearGradient>'
            f'<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    rl = ""
    if ruler:
        rl = (f'<path d="' + "".join(f"M{x} 0 v{9 if x % 100 == 0 else 5}" for x in range(20, w, 20)) +
              "".join(f"M0 {y} h{9 if y % 100 == 0 else 5}" for y in range(20, h, 20)) + f'" stroke="{DIM}" stroke-width="1"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">'
            f'<defs>{base}{defs}</defs>'
            f'<rect width="{w}" height="{h}" rx="14" fill="url(#bgg)"/><rect width="{w}" height="{h}" rx="14" fill="url(#grid)" opacity=".6"/>'
            f'{rl}{body}<rect width="{w}" height="{h}" rx="14" fill="url(#scan)"/>'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="#12305a"/></svg>')


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name)


def track(points):
    return (";".join(f"{t:.4f}" for t, _ in points), ";".join(str(v) for _, v in points))


def chamfer(x, y, w, h, c=14):
    return f"M{x+c} {y} H{x+w} V{y+h-c} L{x+w-c} {y+h} H{x} V{y+c} Z"


def pulse(d, color, delay=0, dur=3, width=2.5):
    return (f'<path d="{d}" fill="none" stroke="{DIM}" stroke-width="{width-.5}"/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" pathLength="100" stroke-dasharray="9 91" '
            f'stroke-linecap="round" filter="url(#glow)"><animate attributeName="stroke-dashoffset" values="100;0" '
            f'dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></path>')


# ================================================================ HERO
def htree(cx, cy, S):
    halves = [S / 4, S / 4, S / 8, S / 8, S / 16, S / 16]
    segs, pts = [], [(cx, cy)]
    for t, h in enumerate(halves):
        new = []
        for (px, py) in pts:
            for s in (-1, 1):
                q = (px + s * h, py) if t % 2 == 0 else (px, py + s * h)
                segs.append((t + 1, px, py, q[0], q[1]))
                new.append(q)
        pts = new
    return segs, pts


def hero():
    W, H = 900, 420
    dx, dy, ds = 520, 40, 340          # die
    cx, cy, S = dx + ds / 2, dy + ds / 2, 320
    defs = (f'<pattern id="rows" width="8" height="6" patternUnits="userSpaceOnUse"><path d="M0 5.5H8" stroke="#0e2548" stroke-width="1"/></pattern>'
            f'<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0V6" stroke="#18457f" stroke-width="1"/></pattern>'
            f'<linearGradient id="sweep" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{C}" stop-opacity="0"/><stop offset="1" stop-color="{C}" stop-opacity=".13"/></linearGradient>')
    b = ""
    # ---- die
    b += f'<path d="{chamfer(dx, dy, ds, ds, 18)}" fill="#050c1a" stroke="{C}" stroke-width="1.6" filter="url(#glow)"/>'
    b += f'<path d="{chamfer(dx, dy, ds, ds, 18)}" fill="url(#rows)"/>'
    for mx, my, mw, mh in ((dx + 20, dy + 20, 96, 64), (dx + 226, dy + 258, 96, 64), (dx + 20, dy + 262, 64, 58)):
        b += f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" fill="#07162c"/><rect x="{mx}" y="{my}" width="{mw}" height="{mh}" fill="url(#hatch)" opacity=".5" stroke="#1b4c8c"/>'
    for k in range(7):
        b += f'<path d="M{cx-120+40*k} {dy+4} V{dy+ds-4}" stroke="{A}" stroke-opacity=".16" stroke-width="3"/>'
    b += '<path d="' + "".join(f"M{dx+20+i*20} {dy} v-7 M{dx+20+i*20} {dy+ds} v7 M{dx} {dy+20+i*20} h-7 M{dx+ds} {dy+20+i*20} h7" for i in range(16)) + f'" stroke="{C}" stroke-opacity=".45"/>'
    # ---- clock tree
    segs, sinks = htree(cx, cy, S)
    T, slot = 4.6, 0.34
    base = f"M{cx} {dy} V{cy}" + "".join(f" M{x1} {y1} L{x2} {y2}" for _, x1, y1, x2, y2 in segs)
    b += f'<path d="{base}" fill="none" stroke="#17406f" stroke-width="1.6"/>'
    cols = [C, C, "#57b8ff", V, V, M]
    widths = [3.4, 3, 2.6, 2.2, 1.8, 1.6]
    b += '<g filter="url(#glow)">'
    allsegs = [(0, cx, dy, cx, cy)] + segs
    for tier, x1, y1, x2, y2 in allsegs:
        a, bb = tier * slot / T, (tier + 1) * slot / T
        ko, vo = track([(0, 0), (a, 0), (a + .001, 1), (.74, 1), (.9, 0), (1, 0)])
        kd, vd = track([(0, 100), (a, 100), (bb, 0), (1, 0)])
        col = "#ffffff" if tier == 0 else cols[tier - 1]
        w = 3.6 if tier == 0 else widths[tier - 1]
        b += (f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{col}" stroke-width="{w}" pathLength="100" stroke-dasharray="100 100" stroke-linecap="round">'
              f'<animate attributeName="stroke-dashoffset" dur="{T}s" repeatCount="indefinite" keyTimes="{kd}" values="{vd}"/>'
              f'<animate attributeName="stroke-opacity" dur="{T}s" repeatCount="indefinite" keyTimes="{ko}" values="{vo}"/></path>')
    b += "</g>"
    e = 7 * slot / T
    ks, vs = track([(0, .3), (e, .3), (e + .001, 1), (e + .07, .3), (1, .3)])
    for (sx, sy) in sinks:
        b += (f'<rect x="{sx-3.5}" y="{sy-3.5}" width="7" height="7" fill="#06142b" stroke="{M}" stroke-width="1.2">'
              f'<animate attributeName="stroke-opacity" dur="{T}s" repeatCount="indefinite" keyTimes="{ks}" values="{vs}"/></rect>')
    b += (f'<circle cx="{cx}" cy="{cy}" r="5" fill="{BGD}" stroke="#fff" stroke-width="2" filter="url(#glow)"/>'
          f'<text x="{cx+8}" y="{dy-10}" font-size="10" fill="{C}" letter-spacing="2">CLK</text>'
          f'<text x="{dx+ds}" y="{dy+ds+22}" text-anchor="end" font-size="10" fill="{MU}" letter-spacing="2">CTS · H-TREE · 64 SINKS</text>')
    # ---- left column
    b += (f'<circle cx="54" cy="62" r="4" fill="{G}" filter="url(#glow)"><animate attributeName="opacity" values="1;.25;1" dur="1.8s" repeatCount="indefinite"/></circle>'
          f'<text x="68" y="66" font-size="12" fill="{C}" letter-spacing="4">ASIC PHYSICAL DESIGN ENGINEER</text>')
    b += f'<text x="48" y="140" font-size="58" font-weight="700" fill="#ffffff">Nahid Ahmed</text>'
    b += f'<text x="48" y="202" font-size="58" font-weight="700" fill="url(#neon)" filter="url(#glow)">Shihab</text>'
    b += f'<text x="50" y="232" font-size="14" fill="{MU}" letter-spacing="4">@NASHIHAB</text>'
    b += f'<rect x="48" y="256" width="430" height="46" rx="8" fill="{PAN}" stroke="{DIM}"/><text x="64" y="285" font-size="18" font-weight="700" fill="{M}">&gt;</text>'
    lines = ["ASIC Physical Design Engineer", "PnR | CTS | MMMC | Timing", "Embedded Systems | IoT | Robotics",
             "VLSI | Automation | Hardware", "RTL -> GDSII"]
    N, dur = len(lines), len(lines) * 2.8
    for i, t in enumerate(lines):
        a, bb, c = i / N, i / N + .45 / N, (i + 1) / N
        wl, ch = len(t) * 11 + 6, 11
        k, v = track([(0, 0), (a, 0), (bb, wl), (c - .0001, wl), (c, 0), (1, 0)])
        defs += f'<clipPath id="c{i}"><rect x="88" y="262" height="34" width="0"><animate attributeName="width" dur="{dur}s" repeatCount="indefinite" keyTimes="{k}" values="{v}"/></rect></clipPath>'
        b += f'<text x="88" y="285" font-size="18" fill="{TX}" clip-path="url(#c{i})">{esc(t)}</text>'
        kx, vx = track([(0, 88), (a, 88), (bb, 88 + wl), (c - .0001, 88 + wl), (c, 88), (1, 88)])
        ko, vo = track([(0, 0), (a, 0), (a + .0001, 1), (c - .0001, 1), (c, 0), (1, 0)])
        b += (f'<rect y="269" width="9" height="20" fill="{C}" x="88" filter="url(#glow)"><animate attributeName="x" dur="{dur}s" repeatCount="indefinite" keyTimes="{kx}" values="{vx}"/>'
              f'<animate attributeName="opacity" dur="{dur}s" repeatCount="indefinite" keyTimes="{ko}" values="{vo}"/></rect>')
    x = 48
    for t in ["PnR", "CTS", "MMMC", "STA", "PV", "GDSII"]:
        w = len(t) * 8 + 22
        b += f'<rect x="{x}" y="326" width="{w}" height="26" rx="13" fill="none" stroke="{C}" stroke-opacity=".55"/><text x="{x+w/2}" y="343" text-anchor="middle" font-size="11" fill="{TX}">{t}</text>'
        x += w + 8
    b += f'<text x="50" y="392" font-size="10" fill="{MU}" letter-spacing="3">CIRCUITS. SILICON. CODE. REPEAT.</text>'
    b += f'<rect width="{W}" height="70" fill="url(#sweep)"><animate attributeName="y" values="-70;{H}" dur="6s" repeatCount="indefinite"/></rect>'
    write("hero.svg", wrap(W, H, b, defs, ruler=True))


# ================================================================ SECTION HEADERS
def section(fname, idx, title, sub, col):
    W, H = 900, 64
    ticks = "".join(f"M{x} 54 v{6 if x % 100 == 24 else 3}" for x in range(24, W - 23, 20))
    b = (f'<rect x="24" y="14" width="34" height="30" fill="none" stroke="{col}" stroke-width="1.5" filter="url(#glow)"/>'
         f'<text x="41" y="35" text-anchor="middle" font-size="14" font-weight="700" fill="{col}">{idx}</text>'
         f'<text x="74" y="36" font-size="19" font-weight="700" fill="{TX}" letter-spacing="5">{esc(title)}</text>'
         f'<text x="{W-24}" y="34" text-anchor="end" font-size="11" fill="{MU}" letter-spacing="2">{esc(sub)}</text>'
         f'<path d="M24 54 H{W-24}" stroke="{DIM}" stroke-width="1.5"/><path d="{ticks}" stroke="{DIM}"/>'
         f'<path d="M24 54 H{W-24}" stroke="{col}" stroke-width="2" pathLength="100" stroke-dasharray="5 95" stroke-linecap="round" filter="url(#glow)">'
         f'<animate attributeName="stroke-dashoffset" values="100;0" dur="3s" repeatCount="indefinite"/></path>')
    write(fname, wrap(W, H, b))


# ================================================================ DATASHEET
def datasheet():
    W, H = 900, 300
    rows = [("DOMAIN", "ASIC Physical Design"), ("FLOW", "RTL → NETLIST → FLOORPLAN → PLACEMENT → CTS"),
            ("", "→ ROUTING → SIGNOFF → GDSII"),
            ("IMPLEMENT", "PnR · CTS · MMMC"), ("SIGNOFF", "STA · PV · SDC"),
            ("AUTOMATION", "Python · Tcl · Shell · AI / ML"),
            ("SYSTEMS", "Embedded · IoT · Robotics"), ("SPACE", "Nano-satellite · UAV · UGV · ROV"),
            ("LEARNING", "Optoelectronics")]
    b = (f'<text x="32" y="36" font-size="11" fill="{C}" letter-spacing="4" font-weight="700">DATASHEET</text>'
         f'<text x="140" y="36" font-size="11" fill="{MU}" letter-spacing="2">NAHID AHMED SHIHAB  ·  PD-ENG  ·  REV 2026</text>'
         f'<path d="M32 46 H520" stroke="{C}" stroke-width="1.5"/>')
    y = 70
    for lab, val in rows:
        b += (f'<text x="32" y="{y}" font-size="10.5" fill="{A}" letter-spacing="2">{lab}</text>'
              f'<text x="150" y="{y}" font-size="12.5" fill="{TX}">{esc(val)}</text>')
        if lab or val.startswith("→"):
            pass
        b += f'<path d="M32 {y+9} H520" stroke="{DIM}" stroke-opacity=".7"/>'
        y += 26
    # chip with pins
    bx, by, bw = 670, 92, 120
    left = ["PnR", "CTS", "MMMC", "STA", "PV", "SDC"]
    right = ["Python", "Tcl", "Shell", "C++", "Verilog", "ESP32"]
    b += f'<rect x="{bx}" y="{by}" width="{bw}" height="{bw+20}" rx="8" fill="{PAN}" stroke="{C}" stroke-width="1.8" filter="url(#glow)"/>'
    for i in range(6):
        py = by + 18 + i * 22
        for side, lab in ((0, left[i]), (1, right[i])):
            x1, x2 = (bx - 24, bx) if side == 0 else (bx + bw, bx + bw + 24)
            d = f"M{x1} {py} H{x2}" if side == 0 else f"M{x1} {py} H{x2}"
            b += pulse(d, C if side == 0 else M, delay=(i * .35 + side * .15) % 3, dur=2.4, width=2)
            if side == 0:
                b += f'<text x="{x1-8}" y="{py+4}" text-anchor="end" font-size="11" fill="{TX}">{lab}</text><text x="{bx+8}" y="{py+3.5}" font-size="8" fill="{MU}">{i+1}</text>'
            else:
                b += f'<text x="{x2+8}" y="{py+4}" font-size="11" fill="{TX}">{lab}</text><text x="{bx+bw-8}" y="{py+3.5}" text-anchor="end" font-size="8" fill="{MU}">{12-i}</text>'
    b += f'<circle cx="{bx+12}" cy="{by+10}" r="3" fill="{C}"/>'
    b += (f'<text x="{bx+bw/2}" y="{by+78}" text-anchor="middle" font-size="26" font-weight="700" fill="url(#neon)" filter="url(#glow)">PD</text>'
          f'<text x="{bx+bw/2}" y="{by+98}" text-anchor="middle" font-size="9" fill="{MU}" letter-spacing="3">ASIC</text>'
          f'<text x="{bx+bw/2}" y="{by+bw+44}" text-anchor="middle" font-size="9" fill="{MU}" letter-spacing="3">PIN-OUT · TOP VIEW</text>')
    write("datasheet.svg", wrap(W, H, b))


# ================================================================ FLOW
def flow():
    stages = ["RTL", "NETLIST", "FLOORPLAN", "PLACEMENT", "CTS", "ROUTING", "SIGNOFF", "GDSII"]
    cols = [C, C, "#57b8ff", V, V, M, G, G]
    W, H, bw, gap, y = 900, 150, 94, 16, 54
    x0 = (W - (len(stages) * bw + (len(stages) - 1) * gap)) / 2
    n, dur = len(stages), len(stages) * 0.9
    b = f'<path d="M{x0} {y+22} H{W-x0}" stroke="{DIM}" stroke-width="2"/>'
    for i, s in enumerate(stages):
        x, col = x0 + i * (bw + gap), cols[i]
        a, c = i / n, (i + 1) / n
        k, v = track([(0, .3), (a, .3), (a + .0001, 1), (c - .0001, 1), (c, .3), (1, .3)])
        b += (f'<path d="{chamfer(x, y, bw, 44, 10)}" fill="{PAN}" stroke="{col}" stroke-width="1.8" filter="url(#glow)">'
              f'<animate attributeName="stroke-opacity" dur="{dur}s" repeatCount="indefinite" keyTimes="{k}" values="{v}"/></path>'
              f'<text x="{x+bw/2}" y="{y+27}" text-anchor="middle" font-size="12" font-weight="700" fill="{TX}">{s}</text>'
              f'<text x="{x+6}" y="{y-9}" font-size="10" fill="{col}">0{i+1}</text>')
    b += f'<circle r="5" fill="#fff" filter="url(#glow)"><animateMotion dur="{dur}s" repeatCount="indefinite" path="M{x0} {y+22} H{W-x0}"/></circle>'
    b += f'<text x="{W/2}" y="{H-22}" text-anchor="middle" font-size="11" fill="{MU}" letter-spacing="3">TIMING CLOSURE · MMMC · SDC · STANDARD CELLS · PV</text>'
    write("flow.svg", wrap(W, H, b))


def smooth(pts):
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d


def closure():
    W, H = 900, 270
    vals = [-.62, -.43, -.31, -.22, -.15, -.095, -.055, -.025, -.008, 0, 0]
    x0, x1, yz, yb = 70, 510, 70, 210
    pts = [(x0 + i * (x1 - x0) / (len(vals) - 1), yz + (-v) / .7 * (yb - yz)) for i, v in enumerate(vals)]
    d = smooth(pts)
    defs = (f'<linearGradient id="cg" gradientUnits="userSpaceOnUse" x1="{x0}" x2="{x1}"><stop offset="0" stop-color="{M}"/><stop offset=".7" stop-color="{A}"/><stop offset="1" stop-color="{G}"/></linearGradient>')
    b = (f'<text x="28" y="34" font-size="12" font-weight="700" fill="{TX}" letter-spacing="3">WNS CONVERGENCE</text>'
         f'<text x="214" y="34" font-size="10" fill="{MU}" letter-spacing="2">ILLUSTRATIVE</text>')
    for v in (0, -.2, -.4, -.6):
        yy = yz + (-v) / .7 * (yb - yz)
        b += f'<path d="M{x0} {yy} H{x1}" stroke="{DIM}" stroke-dasharray="{"0" if v else "5 4"}" stroke-width="1"/><text x="{x0-8}" y="{yy+4}" text-anchor="end" font-size="10" fill="{MU}">{v:.1f}</text>'
    b += f'<path d="M{x0} {yz} H{x1}" stroke="{A}" stroke-dasharray="5 4" stroke-opacity=".8"/><text x="{x1+8}" y="{yz+4}" font-size="10" fill="{A}">0 ns</text>'
    for i in range(0, 11, 2):
        xx = x0 + i * (x1 - x0) / 10
        b += f'<path d="M{xx} {yb} v6" stroke="{DIM}"/><text x="{xx}" y="{yb+20}" text-anchor="middle" font-size="10" fill="{MU}">{i}</text>'
    b += f'<text x="{(x0+x1)/2}" y="{yb+40}" text-anchor="middle" font-size="10" fill="{MU}" letter-spacing="3">OPT ITERATION</text>'
    b += f'<path d="{d} L{x1} {yz} L{x0} {yz} Z" fill="{M}" fill-opacity=".07"/>'
    k, v = track([(0, 100), (.55, 0), (1, 0)])
    b += (f'<path d="{d}" fill="none" stroke="url(#cg)" stroke-width="3" pathLength="100" stroke-dasharray="100 100" stroke-linecap="round" filter="url(#glow)">'
          f'<animate attributeName="stroke-dashoffset" dur="8s" repeatCount="indefinite" keyTimes="{k}" values="{v}"/></path>')
    b += (f'<circle r="5" fill="#fff" filter="url(#glow)"><animateMotion dur="8s" repeatCount="indefinite" path="{d}" calcMode="linear" keyPoints="0;1;1" keyTimes="0;.55;1"/></circle>')
    # terminal
    tx, ty, tw, th = 560, 22, 320, 226
    b += f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="10" fill="#050b16" stroke="{DIM}"/><path d="M{tx} {ty+30} H{tx+tw}" stroke="{DIM}"/>'
    b += "".join(f'<circle cx="{tx+18+i*16}" cy="{ty+15}" r="4.5" fill="{c}" fill-opacity=".8"/>' for i, c in enumerate((M, A, G)))
    b += f'<text x="{tx+tw-14}" y="{ty+19}" text-anchor="end" font-size="10" fill="{MU}" letter-spacing="2">flow.log</text>'
    log = [("FLOORPLAN", "done"), ("PLACEMENT", "done"), ("CTS", "done"), ("ROUTING", "done"), ("SIGNOFF STA", "WNS 0.00")]
    T = 8
    for i, (nm, st) in enumerate(log):
        yy = ty + 60 + i * 28
        t0 = (i + 1) * .12
        ko, vo = track([(0, 0), (t0, 0), (t0 + .005, 1), (.93, 1), (1, 0)])
        an = f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="{ko}" values="{vo}"/>'
        b += (f'<text x="{tx+20}" y="{yy}" font-size="12" fill="{MU}" opacity="0">$ <tspan fill="{TX}">{nm}</tspan>{an}</text>'
              f'<text x="{tx+tw-20}" y="{yy}" text-anchor="end" font-size="12" fill="{C}" opacity="0">{st}{an}</text>')
    ko, vo = track([(0, 0), (.78, 0), (.785, 1), (.93, 1), (1, 0)])
    b += (f'<text x="{tx+20}" y="{ty+th-22}" font-size="13" font-weight="700" fill="{G}" filter="url(#glow)" opacity="0">TIMING CLOSED  ·  READY FOR GDSII'
          f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="{ko}" values="{vo}"/></text>')
    write("closure.svg", wrap(W, H, b, defs))


# ================================================================ STACK
def stack():
    rows = [("LANGUAGES", C, ["Python", "C++", "C", "Verilog", "JavaScript", "HTML", "CSS", "SCSS", "Tcl", "Shell"]),
            ("PHYSICAL DESIGN", M, ["IC Physical Design", "PnR", "CTS", "MMMC", "STA", "SDC", "GDSII"]),
            ("EMBEDDED / HW", V, ["Embedded C", "ESP32", "STM32", "Arduino", "Raspberry Pi", "Altium", "KiCad"]),
            ("TOOLS / AI", G, ["Linux", "Git", "VS Code", "MATLAB", "OpenCV", "ROS", "TensorFlow", "n8n"])]
    W, left, cw = 900, 196, 8.0
    b, y = "", 26
    for label, col, items in rows:
        b += f'<rect x="28" y="{y+5}" width="3" height="16" fill="{col}" filter="url(#glow)"/><text x="40" y="{y+18}" font-size="11" fill="{col}" letter-spacing="2" font-weight="700">{label}</text>'
        x = left
        for it in items:
            w = len(it) * cw + 24
            if x + w > W - 24:
                x, y = left, y + 36
            b += (f'<path d="{chamfer(x, y, w, 26, 7)}" fill="{PAN}" stroke="{col}" stroke-opacity=".65"/>'
                  f'<text x="{x+w/2}" y="{y+17}" text-anchor="middle" font-size="12" fill="{TX}">{esc(it)}</text>')
            x += w + 8
        y += 46
    write("stack.svg", wrap(W, y + 4, b))


# ================================================================ GITHUB DATA
def gh(path, graphql=None):
    h = {"User-Agent": "readme-gen", "Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        h["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    if graphql:
        req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": graphql}).encode(), headers=h)
    else:
        req = urllib.request.Request("https://api.github.com" + path, headers=h)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


LANG = {"Python": "#3572A5", "C++": "#f34b7d", "C": "#9aa4b2", "JavaScript": "#f1e05a", "HTML": "#e34c26", "CSS": "#8b7bff",
        "SCSS": "#c6538c", "Verilog": "#b2b7f8", "Shell": "#89e051", "Tcl": "#e4cc98", "TypeScript": "#3178c6"}


def stats():
    user, repos = None, []
    try:
        user, repos = gh(f"/users/{USER}"), gh(f"/users/{USER}/repos?per_page=100&type=owner")
    except Exception as e:
        print("stats: API unavailable, placeholder:", e)
    vals = [("FOLLOWERS", user["followers"] if user else "--", C), ("PUBLIC REPOS", user["public_repos"] if user else "--", V),
            ("STARS", sum(r["stargazers_count"] for r in repos) if user else "--", A)]
    langs = {}
    for r in repos:
        if not r["fork"] and r["language"]:
            langs[r["language"]] = langs.get(r["language"], 0) + 1
    W, H = 900, 210
    b = ""
    for i, (lab, val, col) in enumerate(vals):
        x = 20 + i * 295
        b += (f'<path d="{chamfer(x, 18, 270, 76)}" fill="{PAN}" stroke="{col}" stroke-opacity=".8" filter="url(#glow)"/>'
              f'<text x="{x+20}" y="64" font-size="32" font-weight="700" fill="{col}">{val}</text>'
              f'<text x="{x+20}" y="83" font-size="10" fill="{MU}" letter-spacing="3">{lab}</text>')
    b += f'<text x="24" y="128" font-size="10" fill="{MU}" letter-spacing="3">LANGUAGE MIX</text>'
    total = sum(langs.values())
    if total:
        x = 24
        b += '<clipPath id="bar"><rect x="24" y="138" width="852" height="12" rx="6"/></clipPath><g clip-path="url(#bar)">'
        for l, n in sorted(langs.items(), key=lambda kv: -kv[1]):
            w = 852 * n / total
            b += f'<rect x="{x}" y="138" width="{w}" height="12" fill="{LANG.get(l, MU)}"/>'; x += w
        b += "</g>"
        lx = 24
        for l, n in sorted(langs.items(), key=lambda kv: -kv[1])[:7]:
            b += f'<circle cx="{lx+5}" cy="178" r="5" fill="{LANG.get(l, MU)}"/><text x="{lx+16}" y="182" font-size="12" fill="{TX}">{esc(l)} {100*n/total:.0f}%</text>'
            lx += 40 + len(l) * 8 + 30
    else:
        b += f'<rect x="24" y="138" width="852" height="12" rx="6" fill="{DIM}"/><text x="24" y="178" font-size="12" fill="{MU}">live data appears after the first Action run</text>'
    write("stats.svg", wrap(W, H, b))


def activity():
    weeks, total = None, None
    q = f'{{ user(login:"{USER}") {{ contributionsCollection {{ contributionCalendar {{ totalContributions weeks {{ contributionDays {{ contributionCount }} }} }} }} }} }}'
    try:
        cal = gh("", q)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        weeks = [[d["contributionCount"] for d in w["contributionDays"]] for w in cal["weeks"]]
        total = cal["totalContributions"]
    except Exception as e:
        print("activity: unavailable, placeholder:", e)
    W, H, step, cell = 900, 190, 15, 11
    nw = len(weeks) if weeks else 53
    x0 = (W - nw * step) / 2
    levels = ["#0c1a31", "#0e4a63", "#118aa3", "#1fc4de", C]
    mx = max((max(w) for w in weeks), default=0) if weeks else 0
    b = (f'<text x="{x0}" y="34" font-size="12" font-weight="700" fill="{TX}" letter-spacing="3">CONTRIBUTION MATRIX</text>'
         f'<text x="{W-x0}" y="34" text-anchor="end" font-size="11" fill="{C}" letter-spacing="2">{"" if total is None else f"{total} IN THE LAST YEAR"}</text>')
    for wi in range(nw):
        for di in range(7):
            n = weeks[wi][di] if weeks and di < len(weeks[wi]) else 0
            lv = 0 if n == 0 or not mx else min(4, 1 + int(3.99 * n / mx))
            b += f'<rect x="{x0+wi*step}" y="{54+di*step}" width="{cell}" height="{cell}" rx="2" fill="{levels[lv]}"/>'
    if weeks is None:
        b += f'<text x="{W/2}" y="{H-14}" text-anchor="middle" font-size="11" fill="{MU}">syncs after the first Action run</text>'
    b += f'<rect x="{x0-46}" y="50" width="46" height="{7*step+4}" fill="{C}" opacity=".10"><animate attributeName="x" values="{x0-46};{x0+nw*step}" dur="4.5s" repeatCount="indefinite"/></rect>'
    write("activity.svg", wrap(W, H, b))


def projects():
    cards = []
    for name in REPOS:
        try:
            r = gh(f"/repos/{USER}/{name}")
            cards.append((name, r.get("description") or "", r.get("language") or "", r["stargazers_count"]))
        except Exception as e:
            print("projects: skipped", name, e)
            cards.append((name, "", "", None))
    W, cw, ch = 900, 418, 100
    H = 20 + ((len(cards) + 1) // 2) * (ch + 16) + 4
    b, colors = "", [C, V, M, G]
    for i, (n, d, l, s) in enumerate(cards):
        x, y, col = 20 + (i % 2) * (cw + 24), 20 + (i // 2) * (ch + 16), colors[i % 4]
        d = (d[:56] + "…") if len(d) > 56 else d
        b += (f'<a href="https://github.com/{USER}/{esc(n)}" target="_blank"><path d="{chamfer(x, y, cw, ch, 16)}" fill="{PAN}" stroke="{col}" stroke-opacity=".7"/>'
              f'<rect x="{x}" y="{y+22}" width="3" height="{ch-44}" fill="{col}" filter="url(#glow)"/>'
              f'<text x="{x+22}" y="{y+34}" font-size="16" font-weight="700" fill="{col}">{esc(n)}</text>'
              f'<text x="{x+cw-22}" y="{y+34}" text-anchor="end" font-size="16" fill="{col}">↗</text>'
              f'<text x="{x+22}" y="{y+58}" font-size="12" fill="{TX if d else MU}">{esc(d) if d else "github.com/" + USER + "/" + esc(n)}</text>')
        if l:
            b += f'<circle cx="{x+27}" cy="{y+82}" r="5" fill="{LANG.get(l, MU)}"/><text x="{x+38}" y="{y+86}" font-size="12" fill="{TX}">{esc(l)}</text>'
        if s is not None:
            b += f'<text x="{x+cw-22}" y="{y+86}" text-anchor="end" font-size="12" fill="{MU}">★ {s}</text>'
        b += "</a>"
    write("projects.svg", wrap(W, H, b))


def footer():
    W, H = 900, 96
    b = (f'<path d="M40 24 H{W-40}" stroke="{DIM}" stroke-width="1.5"/>'
         f'<path d="M40 24 H{W-40}" stroke="{C}" stroke-width="2" pathLength="100" stroke-dasharray="4 96" stroke-linecap="round" filter="url(#glow)"><animate attributeName="stroke-dashoffset" values="100;0" dur="3.4s" repeatCount="indefinite"/></path>'
         f'<text x="{W/2}" y="60" text-anchor="middle" font-size="14" font-weight="700" fill="url(#neon)" letter-spacing="7">CIRCUITS. SILICON. CODE. REPEAT.</text>'
         f'<text x="{W/2}" y="80" text-anchor="middle" font-size="10" fill="{MU}" letter-spacing="3">NAHID AHMED SHIHAB  ·  @NASHIHAB  ·  NASHIHAB.GITHUB.IO</text>')
    write("footer.svg", wrap(W, H, b))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    hero()
    section("h-profile.svg", "01", "PROFILE", "SPEC SHEET  ·  PD-ENG", C); datasheet()
    section("h-arsenal.svg", "02", "TECH ARSENAL", "LANGUAGES · TOOLS · HW", V); stack()
    section("h-flow.svg", "03", "IC PHYSICAL DESIGN", "RTL → GDSII", M); flow(); closure()
    section("h-projects.svg", "04", "MAKING STUFF", "JUST FOR HOBBY", A); projects()
    section("h-stats.svg", "05", "MOMENTUM", "LIVE · AUTO-REFRESHED", G); stats(); activity()
    footer()
