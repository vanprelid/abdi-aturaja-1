#!/usr/bin/env python3
"""Generator swimlane: spesifikasi JSON -> satu halaman HTML (SVG inline, tema terang/gelap).

Pemakaian:
    python3 swimlane.py spesifikasi.json keluaran.html

Format spesifikasi: lihat references/format-swimlane.md.
Script menghitung posisi kartu, merutekan garis siku lewat celah antar-kolom,
dan mencetak PERINGATAN bila teks terlalu panjang atau garis berisiko menembus kartu.
"""
import json
import sys
from html import escape as E

# ---------------------------------------------------------------- ukuran grid
LANE_X, TAB_W = 16, 168
COL0, PITCH, CW, CH = 212, 166, 150, 120
LTOP, LH, LGAP = 16, 150, 10

TITLE_PX, SUB_PX = 18.5, 15

SEMPIT = set("iljtfr.,:;'!|() ·-/")
LEBAR = set("mwMW@%")


def em_huruf(ch, tebal):
    """Perkiraan lebar satu huruf Plus Jakarta Sans dalam satuan em."""
    if ch in SEMPIT:
        w = 0.30
    elif ch in LEBAR:
        w = 0.86
    elif ch.isupper() or ch.isdigit():
        w = 0.66
    else:
        w = 0.55
    return w * (1.06 if tebal else 1.0)

WARNA = {  # (terang, gelap)
    "ink": ("#0F172A", "#475569"), "violet": ("#7C3AED", "#8B5CF6"), "blue": ("#2563EB", "#3B82F6"),
    "teal": ("#0D9488", "#14B8A6"), "amber": ("#B45309", "#D97706"), "rose": ("#BE123C", "#E11D48"),
    "green": ("#15803D", "#22C55E"), "orange": ("#C2410C", "#EA580C"),
}

ICON = {
    "person": '<circle cx="0" cy="-4" r="4"/><path d="M-7,8 a7,7 0 0 1 14,0"/>',
    "users": '<circle cx="-3" cy="-4" r="3.2"/><path d="M-9,7 a6,6 0 0 1 12,0"/><circle cx="5" cy="-3" r="2.6"/><path d="M4,2 a5,5 0 0 1 6,5"/>',
    "crown": '<path d="M-8,5 l-1,-10 l5,4 l4,-6 l4,6 l5,-4 l-1,10 z"/>',
    "chat": '<path d="M-8,-6 h16 v10 h-9 l-4,4 v-4 h-3 z"/>',
    "mail": '<rect x="-8" y="-6" width="16" height="12" rx="1.5"/><path d="M-8,-5 l8,6 l8,-6"/>',
    "hub": '<circle cx="0" cy="0" r="3"/><circle cx="-7" cy="-6" r="2"/><circle cx="7" cy="-6" r="2"/><circle cx="0" cy="8" r="2"/><path d="M-2,-2 L-5.5,-4.8 M2,-2 L5.5,-4.8 M0,3 V6"/>',
    "tool": '<path d="M5,-8 a5,5 0 0 0 -6,6 l-7,7 l3,3 l7,-7 a5,5 0 0 0 6,-6 l-3,3 l-3,-3 z"/>',
    "branch": '<circle cx="-5" cy="-7" r="2.2"/><circle cx="-5" cy="7" r="2.2"/><circle cx="6" cy="-3" r="2.2"/><path d="M-5,-4.8 V4.8 M6,-0.8 c0,5 -11,3 -11,6"/>',
    "check": '<path d="M0,-9 l7,3 v5 c0,5 -3,8 -7,10 c-4,-2 -7,-5 -7,-10 v-5 z"/><path d="M-3.5,0 l2.5,2.5 l4.5,-5"/>',
    "rocket": '<path d="M0,-9 c4,3 5,8 3,13 h-6 c-2,-5 -1,-10 3,-13 z"/><path d="M-3,4 l-3,4 M3,4 l3,4"/><circle cx="0" cy="-2" r="1.6"/>',
    "store": '<rect x="-8" y="-7" width="16" height="11" rx="1.5"/><path d="M-3,8 h6 M0,4 v4"/>',
    "laptop": '<rect x="-7" y="-6" width="14" height="9" rx="1"/><path d="M-9,6 h18"/>',
    "server": '<rect x="-7" y="-8" width="14" height="7" rx="1.5"/><rect x="-7" y="1" width="14" height="7" rx="1.5"/><path d="M-4,-4.5 h1 M-4,4.5 h1"/>',
    "cloud": '<path d="M-6,6 a4,4 0 0 1 0,-8 a6,6 0 0 1 11,-1 a4,4 0 0 1 1,9 z"/>',
    "doc": '<path d="M-6,-9 h8 l4,4 v14 h-12 z"/><path d="M-3,-1 h6 M-3,3 h6"/>',
    "database": '<ellipse cx="0" cy="-6" rx="7" ry="3"/><path d="M-7,-6 v12 c0,4 14,4 14,0 v-12 M-7,0 c0,4 14,4 14,0"/>',
    "lock": '<rect x="-7" y="-2" width="14" height="10" rx="2"/><path d="M-4,-2 v-3 a4,4 0 0 1 8,0 v3"/>',
    "chart": '<path d="M-8,8 h16 M-5,8 v-6 M0,8 v-12 M5,8 v-9"/>',
    "phone": '<rect x="-5" y="-9" width="10" height="18" rx="2"/><path d="M-1.5,6 h3"/>',
    "globe": '<circle cx="0" cy="0" r="8"/><ellipse cx="0" cy="0" rx="3.5" ry="8"/><path d="M-8,0 h16"/>',
    "flag": '<path d="M-6,9 v-18 M-6,-8 h12 l-3,4 l3,4 h-12"/>',
    "search": '<circle cx="-2" cy="-2" r="6"/><path d="M2.5,2.5 l5,5"/>',
    "bell": '<path d="M-6,4 v-4 a6,6 0 0 1 12,0 v4 l2,2 h-16 z"/><path d="M-2,8 a2,2 0 0 0 4,0"/>',
    "gear": '<circle cx="0" cy="0" r="3.5"/><path d="M0,-9 v3 M0,6 v3 M-9,0 h3 M6,0 h3 M-6.4,-6.4 l2.1,2.1 M4.3,4.3 l2.1,2.1 M-6.4,6.4 l2.1,-2.1 M4.3,-4.3 l2.1,-2.1"/>',
    "spark": '<path d="M0,-9 l2.5,6.5 l6.5,2.5 l-6.5,2.5 l-2.5,6.5 l-2.5,-6.5 l-6.5,-2.5 l6.5,-2.5 z"/>',
}

JENIS_GARIS = {  # jenis: (kelas garis, marker, teks legenda)
    "alur": ("lA", "mA", "alur kerja"),
    "rilis": ("lR", "mR", "jalur rilis / hasil akhir"),
    "manual": ("lM", "mM", "langkah manual yang bermasalah"),
    "info": ("lD", "mD", "notifikasi · baca-saja"),
}

peringatan = []


def warn(msg):
    peringatan.append(msg)


def lebar_teks(t, px, tebal=False):
    return sum(em_huruf(c, tebal) for c in t) * px


def main(spec_path, out_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    lanes = spec["jalur"]
    lane_idx = {l["id"]: i for i, l in enumerate(lanes)}
    steps = spec["langkah"]
    side = spec.get("sampingan", [])

    def ly(i):
        return LTOP + i * (LH + LGAP)

    def cx(c):
        return COL0 + (c - 1) * PITCH

    def cy(l):
        return ly(l) + (LH - CH) / 2

    right = max([cx(s["kolom"]) + CW for s in steps]
                + [cx(s["kolom"]) + CW + (s.get("lebar_kolom", 1) - 1) * PITCH for s in side])
    W = int(right + 20)
    H = ly(len(lanes)) + 6

    if len(steps) > 12:
        warn(f"{len(steps)} kartu utama; anggaran ≤ 12. Pertimbangkan memecah bagan.")

    pos = {}
    occupied = {}
    for s in steps:
        li = lane_idx[s["jalur"]]
        pos[s["id"]] = (cx(s["kolom"]), cy(li), li, s["kolom"])
        key = (li, s["kolom"])
        if key in occupied:
            warn(f"Kartu '{s['id']}' dan '{occupied[key]}' menempati jalur+kolom yang sama.")
        occupied[key] = s["id"]
        if lebar_teks(s["judul"], TITLE_PX, True) > CW - 24:
            warn(f"Judul '{s['judul']}' kemungkinan meluber dari kartu; persingkat.")
        ket = s.get("ket", [])
        if len(ket) > 2:
            warn(f"Kartu '{s['id']}' punya {len(ket)} baris keterangan; maksimal 2.")
        for line in ket:
            if lebar_teks(line, SUB_PX) > CW - 24:
                warn(f"Keterangan '{line}' ({len(line)} huruf) kemungkinan meluber; persingkat (± 16 huruf).")
        if len(s.get("penanda", [])) > 1:
            warn(f"Kartu '{s['id']}' punya {len(s['penanda'])} penanda; anggaran ≤ 1 per kartu.")

    o = []
    a = o.append

    def icon(x, y, name, cls, r=17):
        if name not in ICON:
            warn(f"Ikon '{name}' tidak dikenal; tersedia: {', '.join(sorted(ICON))}.")
            name = "spark"
        a(f'<circle cx="{x}" cy="{y}" r="{r}" class="ic {cls}"/><g transform="translate({x},{y})" class="ig">{ICON[name]}</g>')

    def pbadge(x, y, t, cls="pb"):
        w = 14 + 7.2 * len(t)
        a(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="19" rx="9.5" class="{cls}"/>'
          f'<text x="{x + w / 2:.1f}" y="{y + 13.5}" class="pbt{"w" if cls == "pbw" else ""}" text-anchor="middle">{E(t)}</text>')
        return w

    aria = spec.get("aria", spec.get("judul", "Bagan swimlane"))
    a(f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{E(aria)}">')
    a('<defs><filter id="sh" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="2" stdDeviation="3" class="shc"/></filter>')
    for k, c in [("mA", "fA"), ("mR", "fR"), ("mM", "fM"), ("mD", "fD")]:
        a(f'<marker id="{k}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,1 L9,5 L0,9 z" class="{c}"/></marker>')
    a('</defs>')

    # jalur
    for i, l in enumerate(lanes):
        y = ly(i)
        k = f"w{i}"
        a(f'<rect x="{LANE_X}" y="{y}" width="{W - 2 * LANE_X}" height="{LH}" rx="14" class="lane"/>')
        a(f'<rect x="{LANE_X}" y="{y}" width="{TAB_W}" height="{LH}" rx="14" class="tab" style="fill:var(--{k})"/>')
        icon(LANE_X + 30, y + 32, l.get("ikon", "spark"), "tabic", 15)
        a(f'<text x="{LANE_X + 54}" y="{y + 37}" class="tabt">{E(l["nama"])}</text>')
        if l.get("sub"):
            if lebar_teks(l["sub"], 12) > TAB_W - 30:
                warn(f"Sub jalur '{l['sub']}' terlalu panjang untuk tab.")
            a(f'<text x="{LANE_X + 18}" y="{y + 68}" class="tabs">{E(l["sub"])}</text>')
        bx = LANE_X + 18
        for p in l.get("penanda", []):
            bx += pbadge(bx, y + LH - 34, p, "pbw") + 5

    # garis
    edges = spec.get("garis")
    if edges is None:
        ordered = sorted(steps, key=lambda s: s["kolom"])
        edges = [{"dari": x["id"], "ke": y["id"], "jenis": "alur"} for x, y in zip(ordered, ordered[1:])]
    side_from = {s["dari"] for s in side if s.get("dari")}
    used = set()

    def card_hits(lane, c_from, c_to):
        return [sid for (li, c), sid in occupied.items() if li == lane and c_from < c < c_to]

    for e in edges:
        if e["dari"] not in pos or e["ke"] not in pos:
            warn(f"Garis {e['dari']} → {e['ke']} merujuk kartu yang tidak ada.")
            continue
        x1, y1, l1, c1 = pos[e["dari"]]
        x2, y2, l2, c2 = pos[e["ke"]]
        jenis = e.get("jenis", "alur")
        cls, mk, _ = JENIS_GARIS[jenis]
        used.add(jenis)
        dy = 14 if e["dari"] in side_from else 0
        sx, sy, ex, ey = x1 + CW, y1 + CH / 2 + dy, x2, y2 + CH / 2
        if c2 <= c1:
            warn(f"Garis {e['dari']} → {e['ke']} mundur/sekolom; generator hanya merutekan ke kanan. Gambar ulang aktornya di kolom baru.")
            continue
        if l1 == l2:
            hits = card_hits(l1, c1, c2)
            if hits:
                warn(f"Garis {e['dari']} → {e['ke']} menembus kartu {hits}.")
            d = f"M{sx},{sy} H{ex - 2}"
            lx, lyy, anc = (sx + ex) / 2, sy - 8, "middle"
        else:
            hits = card_hits(l1, c1, c2) if c2 - c1 > 1 else []
            if hits:
                warn(f"Garis {e['dari']} → {e['ke']} melintas di jalur asal dan menembus kartu {hits}.")
            mx = ex - (PITCH - CW) / 2
            r = 8
            s = 1 if ey > sy else -1
            d = (f"M{sx},{sy} H{mx - r} Q{mx},{sy} {mx},{sy + s * r} V{ey - s * r} "
                 f"Q{mx},{ey} {mx + r},{ey} H{ex - 2}")
            lx, lyy, anc = mx + 8, (sy + ey) / 2 + 4, "start"
        a(f'<path d="{d}" class="ln {cls}" marker-end="url(#{mk})"/>')
        if e.get("label"):
            a(f'<text x="{lx}" y="{lyy}" class="ll" text-anchor="{anc}">{E(e["label"])}</text>')

    # kartu sampingan (garis putus-putus dari kartu sejalur)
    for s in side:
        li = lane_idx[s["jalur"]]
        span = s.get("lebar_kolom", 1)
        gx, gy = cx(s["kolom"]) + 10, cy(li) + 10
        gw = CW + (span - 1) * PITCH - 10
        if s.get("dari"):
            x1, y1, l1, _ = pos[s["dari"]]
            if l1 != li:
                warn(f"Sampingan '{s['judul']}' harus sejalur dengan kartu asalnya.")
            else:
                jenis = s.get("jenis", "manual")
                cls, mk, _ = JENIS_GARIS[jenis]
                used.add(jenis)
                a(f'<path d="M{x1 + CW},{y1 + 30} H{gx - 4}" class="ln {cls}" marker-end="url(#{mk})"/>')
        a(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{CH - 20}" rx="12" class="ghost"/>')
        a(f'<text x="{gx + 16}" y="{gy + 30}" class="gt">{E(s["judul"])}</text>')
        for j, line in enumerate(s.get("ket", [])[:2]):
            a(f'<text x="{gx + 16}" y="{gy + 52 + j * 18}" class="gs">{E(line)}</text>')
        bx = gx + gw - 6
        for p in reversed(s.get("penanda", [])):
            w = 14 + 7.2 * len(p)
            bx -= w
            pbadge(bx, gy - 9, p)
            bx -= 4

    # kartu utama
    for s in steps:
        x, y, li, c = pos[s["id"]]
        a(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="12" class="card" filter="url(#sh)"/>')
        icon(x + 28, y + 28, s.get("ikon", "spark"), f"c{li}")
        if s.get("nomor", True):
            a(f'<text x="{x + CW - 14}" y="{y + 33}" class="no" text-anchor="end">{c:02d}</text>')
        a(f'<text x="{x + 14}" y="{y + 72}" class="ct">{E(s["judul"])}</text>')
        for j, line in enumerate(s.get("ket", [])[:2]):
            a(f'<text x="{x + 14}" y="{y + 93 + j * 17}" class="cs">{E(line)}</text>')
        bx = x + CW - 8
        for p in reversed(s.get("penanda", [])):
            w = 14 + 7.2 * len(p)
            bx -= w
            pbadge(bx, y - 9, p)
            bx -= 4
    a('</svg>')
    svg = "\n".join(o)

    # ------------------------------------------------------------ HTML di sekitar SVG
    def tok(mode):
        return "".join(f"--w{i}:{WARNA.get(l.get('warna', 'blue'), WARNA['blue'])[mode]};" for i, l in enumerate(lanes))

    lane_cls = "".join(f".c{i}{{fill:var(--w{i})}}" for i in range(len(lanes)))
    has_badge = any(s.get("penanda") for s in steps + side) or any(l.get("penanda") for l in lanes)
    leg = []
    for j in ["alur", "rilis", "manual", "info"]:
        if j in used:
            leg.append(f'<span><i class="g-{j}"></i>{E(spec.get("legenda", {}).get(j, JENIS_GARIS[j][2]))}</span>')
    if has_badge:
        leg.append(f'<span><em><span class="pill">P1</span></em>{E(spec.get("legenda", {}).get("penanda", "penanda masalah"))}</span>')
    daftar = spec.get("daftar_penanda")
    daftar_html = ""
    if daftar:
        items = "".join(f'<div><b>{E(d["kode"])}</b>{E(d["teks"])}</div>' for d in daftar["isi"])
        daftar_html = f'<div><h2>{E(daftar.get("judul", "Penanda"))}</h2><div class="probs">{items}</div></div>'
    below = ""
    if leg or daftar_html:
        solo = "" if daftar_html else " solo"
        below = (f'<div class="below{solo}"><div><h2>Cara membaca</h2><div class="legend">{"".join(leg)}</div></div>'
                 f'{daftar_html}</div>')
    siklus = spec.get("siklus")
    siklus_html = ""
    if siklus:
        parts = []
        n = len(siklus["langkah"])
        for i, t in enumerate(siklus["langkah"]):
            hl = " hl" if i == n - 1 and siklus.get("sorot_terakhir", True) else ""
            parts.append(f'<span class="c{hl}">{E(t)}</span>')
        siklus_html = (f'<div class="cycle"><span>{E(siklus.get("pengantar", ""))}</span>'
                       + '<span class="ar">→</span>'.join(parts) + '</div>')
    scope = ""
    if spec.get("lingkup"):
        lj = spec["lingkup"]
        scope = f'<div class="scope"><b>{E(lj.get("judul", ""))}</b> {E(lj.get("isi", ""))}</div>'

    html = TEMPLATE
    for k, v in {
        "__TITLE__": E(spec.get("judul", "Bagan")),
        "__EYEBROW__": E(spec.get("eyebrow", "")),
        "__DESC__": E(spec.get("deskripsi", "")),
        "__SCOPE__": scope,
        "__LIGHT__": tok(0), "__DARK__": tok(1), "__LANECLS__": lane_cls,
        "__SVG__": svg, "__BELOW__": below, "__CYCLE__": siklus_html,
        "__SOURCE__": E(spec.get("sumber", "")),
    }.items():
        html = html.replace(k, v)
    open(out_path, "w", encoding="utf-8").write(html)
    print(f"Ditulis: {out_path}  ({len(steps)} kartu, {len(lanes)} jalur, lebar {W}px)")
    for p in peringatan:
        print("PERINGATAN:", p)


TEMPLATE = """<meta charset="utf-8">
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap">
<style>
/* Swimlane: jalur mendatar = siapa/di mana, kolom = urutan; garis siku hanya di celah antar-kolom */
:root{
  --bg:#EEF1F6; --paper:#FFFFFF; --lane:#F5F7FA; --card:#FFFFFF; --ink:#0F172A; --muted:#64748B;
  --flow:#334155; --rel:#16A34A; --bad:#E11D48; --shadow:rgba(15,23,42,.10); --accent:#2563EB;
  __LIGHT__
  --f-ui:"Plus Jakarta Sans","Segoe UI",system-ui,sans-serif;
  --f-mono:"JetBrains Mono",ui-monospace,Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#080C16; --paper:#0F1522; --lane:#161E2E; --card:#1C2638; --ink:#EEF2F8; --muted:#94A3B8;
  --flow:#CBD5E1; --rel:#4ADE80; --bad:#FB7185; --shadow:rgba(0,0,0,.45); --accent:#60A5FA;
  __DARK__ color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#080C16; --paper:#0F1522; --lane:#161E2E; --card:#1C2638; --ink:#EEF2F8; --muted:#94A3B8;
  --flow:#CBD5E1; --rel:#4ADE80; --bad:#FB7185; --shadow:rgba(0,0,0,.45); --accent:#60A5FA;
  __DARK__ color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--f-ui);font-size:14px;line-height:1.5}
.wrap{max-width:1780px;margin:0 auto;padding-inline:24px;padding-block:28px 36px}
header{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:14px 40px;margin-bottom:18px}
.eyebrow{font-family:var(--f-mono);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:600}
h1{font-weight:800;font-size:clamp(26px,3.6vw,44px);line-height:1.05;letter-spacing:-.02em;margin:4px 0 0;text-wrap:balance}
header p{margin:8px 0 0;color:var(--muted);max-width:64ch;font-size:15px}
.scope{font-size:13px;color:var(--muted);max-width:400px;border-left:3px solid var(--accent);padding-left:14px}
.scope b{color:var(--ink);font-weight:700}
figure{margin:0;background:var(--paper);border-radius:20px;padding:18px;box-shadow:0 1px 2px var(--shadow),0 12px 32px -12px var(--shadow)}
.scroll{overflow-x:auto}
svg{display:block;width:100%;height:auto;min-width:1000px;font-family:var(--f-ui)}
.below{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.6fr);gap:28px;margin-top:18px;padding:4px 6px 0}
.below h2{font-size:12px;font-family:var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 10px;font-weight:600}
.legend{display:grid;gap:9px;font-size:13.5px}
.below.solo{grid-template-columns:1fr}
.below.solo .legend{display:flex;flex-wrap:wrap;gap:10px 28px}
.hint{display:none;font-size:12.5px;color:var(--muted);margin:0 0 8px}
@media (max-width:900px){.hint{display:block}}
.legend span{display:flex;align-items:center;gap:12px}
.legend i{flex:none;width:40px;height:0;border-top:2.5px solid var(--flow)}
.legend i.g-rilis{border-color:var(--rel);border-top-width:3px}
.legend i.g-manual{border-color:var(--bad);border-top-style:dashed}
.legend i.g-info{border-color:var(--muted);border-top-style:dotted}
.legend em{font-style:normal;flex:none;width:40px;text-align:center}
.pill{font-family:var(--f-mono);font-size:11px;font-weight:600;background:var(--bad);color:#fff;border-radius:999px;padding:1px 8px}
.probs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px 28px;font-size:13.5px}
.probs div{display:grid;grid-template-columns:44px 1fr;align-items:baseline}
.probs b{font-family:var(--f-mono);font-size:12px;color:var(--bad);font-weight:600}
.cycle{margin-top:16px;display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:13px;color:var(--muted)}
.cycle .c{background:var(--paper);border-radius:999px;padding:5px 14px;color:var(--ink);font-weight:500;box-shadow:0 1px 2px var(--shadow)}
.cycle .c.hl{background:var(--ink);color:var(--paper)}
footer{margin-top:14px;font-size:12px;color:var(--muted)}
@media (max-width:900px){.below{grid-template-columns:1fr}.probs{grid-template-columns:1fr}}
@media (max-width:700px){.wrap{padding-inline:16px}figure{padding:10px;border-radius:14px}}
.lane{fill:var(--lane)}
.tabic{fill:rgba(255,255,255,.18)}
.tabt{fill:#fff;font-size:16px;font-weight:700}
.tabs{fill:rgba(255,255,255,.85);font-size:13px;font-weight:500}
.card{fill:var(--card)}
.shc{flood-color:var(--shadow);flood-opacity:1}
__LANECLS__
.ig{fill:none;stroke:#fff;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.no{font-family:var(--f-mono);font-size:13px;font-weight:600;fill:var(--muted)}
.ct{font-size:18.5px;font-weight:700;fill:var(--ink)}
.cs{font-size:15px;fill:var(--muted);font-weight:500}
.ghost{fill:none;stroke:var(--muted);stroke-width:1.5;stroke-dasharray:5 5}
.gt{font-size:16px;font-weight:700;fill:var(--ink)}
.gs{font-size:14px;fill:var(--muted);font-weight:500}
.ll{font-size:13.5px;font-weight:600;fill:var(--ink);paint-order:stroke;stroke:var(--lane);stroke-width:4px;stroke-linejoin:round}
.ln{fill:none;stroke-linecap:round}
.lA{stroke:var(--flow);stroke-width:2}
.lR{stroke:var(--rel);stroke-width:3}
.lM{stroke:var(--bad);stroke-width:2;stroke-dasharray:6 5;animation:dash 1s linear infinite}
.lD{stroke:var(--muted);stroke-width:1.8;stroke-dasharray:2 5}
@keyframes dash{to{stroke-dashoffset:-22}}
@media (prefers-reduced-motion:reduce){.lM{animation:none}}
.fA{fill:var(--flow)}.fR{fill:var(--rel)}.fM{fill:var(--bad)}.fD{fill:var(--muted)}
.pb{fill:var(--bad)}.pbw{fill:#fff}
.pbt{font-family:var(--f-mono);font-size:11px;font-weight:600;fill:#fff}
.pbtw{font-family:var(--f-mono);font-size:11px;font-weight:600;fill:#BE123C}
</style>

<div class="wrap">
<header>
  <div>
    <span class="eyebrow">__EYEBROW__</span>
    <h1>__TITLE__</h1>
    <p>__DESC__</p>
  </div>
  __SCOPE__
</header>
<figure>
<p class="hint">Geser bagan ke samping untuk melihat semua langkah →</p>
<div class="scroll">
__SVG__
</div>
__BELOW__
</figure>
__CYCLE__
<footer>__SOURCE__</footer>
</div>
"""

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
