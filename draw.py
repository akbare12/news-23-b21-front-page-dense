#!/usr/bin/env python3
"""Draw THE WORLD TODAY — Monday 23 November 2026 front page (1024x1024)."""
import os
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (178, 34, 34)
NAVY = (13, 27, 62)
GREEN = (31, 122, 60)
AMBER = (176, 124, 0)
BLUE = (31, 78, 156)
GREY = (90, 90, 90)

FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    # split on plain spaces only: U+00A0 inside a token keeps it unbreakable
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, lh, max_lines=None):
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def chip(d, x, y, label, color):
    f = font(SANS_B, 8)
    w = d.textlength(label, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=color)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


def hero_scene_kospi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    rnd = random.Random(7)
    bx = x + 6
    while bx < x + w - 20:
        bw = rnd.randint(18, 34)
        bh = rnd.randint(28, 62)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(24, 44, 92))
        for _ in range(6):
            wx = bx + rnd.randint(3, max(4, bw - 6))
            wy = y + h - bh + rnd.randint(4, max(5, bh - 8))
            d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 4
    pts = [(x + 14, y + 34), (x + 70, y + 52), (x + 130, y + 44),
           (x + 190, y + 72), (x + 250, y + 84), (x + 310, y + 108)]
    d.line(pts, fill=(255, 80, 80), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255))
    d.text((x + 10, y + 6), "intraday -5.8%", font=font(SANS_B, 11), fill=(255, 255, 255))
    f = font(SANS_B, 30)
    d.text((x + w - d.textlength("-3.3%", font=f) - 8, y + 4), "-3.3%",
           font=f, fill=(255, 90, 90))


def hero_scene_guterres(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    cx, cy, r = x + 78, y + 68, 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(126, 180, 226))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(255, 255, 255))
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(255, 255, 255))
    rnd = random.Random(11)
    nodes = [(x + 180 + rnd.randint(0, 130), y + 18 + rnd.randint(0, 90)) for _ in range(9)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            d.line([nodes[i], nodes[j]], fill=(140, 170, 220), width=1)
    for nx, ny in nodes:
        d.ellipse([nx - 4, ny - 4, nx + 4, ny + 4], fill=(255, 214, 90))
    d.polygon([(x + w - 58, y + h), (x + w - 46, y + h - 34),
               (x + w - 26, y + h - 34), (x + w - 14, y + h)], fill=(8, 14, 36))
    d.ellipse([x + w - 44, y + h - 62, x + w - 28, y + h - 46], fill=(8, 14, 36))
    d.rectangle([x + w - 52, y + h - 46, x + w - 20, y + h - 34], fill=(8, 14, 36))
    tag = "150 DELEGATES"
    f = font(SANS_B, 11)
    tw = d.textlength(tag, font=f) + 12
    d.rectangle([x + 8, y + 8, x + 8 + tw, y + 26], fill=(255, 214, 90))
    d.text((x + 14, y + 10), tag, font=f, fill=(17, 17, 17))


def hero_scene_power(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(242, 237, 224))
    d.text((x + 10, y + 8), "ASIA POWER INDEX 2026",
           font=font(SANS_B, 13), fill=INK)
    rows = [("US", 78.9, (31, 78, 156)), ("CHINA", 73.6, (178, 34, 34)),
            ("INDIA 3rd", 40.5, (120, 120, 120))]
    yy = y + 34
    for name, val, col in rows:
        d.text((x + 10, yy), name, font=font(SANS_B, 11), fill=INK)
        bx = x + 92
        bw = int((w - 150) * val / 100.0)
        d.rectangle([bx, yy + 1, bx + bw, yy + 15], fill=col)
        d.text((bx + bw + 6, yy), str(val), font=font(SANS_B, 11), fill=INK)
        yy += 26
    d.text((x + 10, yy + 2), "GAP 5.3 — narrowest since 2018",
           font=font(SANS_B, 12), fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=RED)

    # masthead
    f_mast = font(SERIF_B, 52)
    d.text((10, 12), "THE WORLD TODAY", font=f_mast, fill=INK)
    f_r = font(SANS_B, 15)
    d.text((W - 10 - d.textlength("31 STORIES", font=f_r), 16),
           "31 STORIES", font=f_r, fill=INK)
    f_r2 = font(SANS_B, 12)
    d.text((W - 10 - d.textlength("6 REGIONS", font=f_r2), 38),
           "6 REGIONS", font=f_r2, fill=GREY)

    # date line
    d.line([10, 76, W - 10, 76], fill=INK, width=2)
    d.text((10, 82), "MONDAY 23 NOVEMBER 2026", font=font(SANS_B, 19), fill=RED)
    f_k = font(SANS_B, 11)
    kick = "AI ROUT  ·  AI RULES  ·  POWER SHIFT"
    d.text((W - 10 - d.textlength(kick, font=f_k), 88), kick, font=f_k, fill=GREY)

    # number strip
    nums = [("-3.3%", "KOSPI"), ("5.3", "US-CHINA GAP"), ("11,762", "EBOLA CASES"),
            ("10T WON", "SEOUL FUND"), ("$450M", "SKUBAL DEAL"), ("$107.3B", "ANTHROPIC IPO")]
    cw = (W - 20) / 6.0
    y0 = 112
    d.rectangle([10, y0, W - 10, y0 + 44], outline=INK, width=1)
    for i, (num, lab) in enumerate(nums):
        cx = 10 + i * cw
        if i:
            d.line([cx, y0, cx, y0 + 44], fill=INK, width=1)
        fn = font(SANS_B, 26)
        d.text((cx + (cw - d.textlength(num, font=fn)) / 2, y0 + 2),
               num, font=fn, fill=RED)
        fl = font(SANS_B, 9)
        d.text((cx + (cw - d.textlength(lab, font=fl)) / 2, y0 + 31),
               lab, font=fl, fill=INK)

    # region bar
    regions = [("NORTH AMERICA 8", 8, (31, 78, 156)),
               ("EUROPE 6", 6, (198, 93, 18)),
               ("MIDDLE EAST 6", 6, (123, 45, 142)),
               ("ASIA-PACIFIC 6", 6, (15, 122, 109)),
               ("AFRICA 3", 3, (138, 90, 43)),
               ("WORLD 2", 2, (102, 102, 102))]
    y0 = 162
    x = 10
    fr = font(SANS_B, 11)
    for name, n, col in regions:
        seg = (W - 20) * n / 31.0
        d.rectangle([x, y0, x + seg, y0 + 22], fill=col)
        d.text((x + (seg - d.textlength(name, font=fr)) / 2, y0 + 5),
               name, font=fr, fill=(255, 255, 255))
        x += seg

    # UTC strip
    y0 = 190
    d.rectangle([10, y0, W - 10, y0 + 20], fill=NAVY)
    utc = ("THE DAY IN UTC   ~00:00 ASIA OPENS · 06:30 KOSPI -3.3% · "
           "~09:00 SEOUL FUND · 14:30 WALL ST +3% · ~16:00 GUTERRES · "
           "~21:00 FBI HACK (~ = APPROX.)")
    uf = 11
    while d.textlength(utc, font=font(SANS_B, uf)) > 990 and uf > 8:
        uf -= 1
    d.text((16, y0 + 4), utc, font=font(SANS_B, uf), fill=(255, 255, 255))

    # heroes
    heroes = [
        ("#1  ASIA-PACIFIC · MARKETS", "AI ROUT HITS ASIA",
         "Kospi closes 4,708.54, sheds 161 pts. Samsung -3.1%, SK Hynix -2.5%.",
         "Source: Yonhap · Korea JoongAng", "REPORTED", GREEN, hero_scene_kospi),
        ("#2  WORLD · UNITED NATIONS", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges global AI safety rules at Bridgetown; "
         "150 delegates back a risk framework.",
         "Source: UN News · Reuters", "REPORTED", GREEN, hero_scene_guterres),
        ("#3  WORLD · POWER", "US LEAD OVER CHINA AT RECORD LOW",
         "Gap 5.3 narrowest since 2018. US diplomatic influence -6 to 76.7. "
         "India third at 40.5.",
         "Source: Lowy Institute", "REPORTED", GREEN, hero_scene_power),
    ]
    hx = [10, 350, 690]
    hw = 324
    y0 = 216
    for (kick, head, body, src, lab, col, scene), x in zip(heroes, hx):
        scene(d, x, y0, hw, 128)
        yy = y0 + 134
        d.text((x, yy), kick, font=font(SANS_B, 10), fill=RED)
        yy += 15
        lines = wrap(d, head, font(SANS_B, 17), hw)
        yy = text_block(d, x, yy, lines, font(SANS_B, 17), INK, 20, max_lines=2)
        yy += 2
        blines = wrap(d, body, font(SANS, 11), hw)
        yy = text_block(d, x, yy, blines, font(SANS, 11), INK, 13, max_lines=2)
        yy += 3
        d.text((x, yy), src, font=font(SANS, 9), fill=GREY)
        chip(d, x + hw - 62, yy - 1, lab, col)

    # small cards 5x2
    cards = [
        ("#4", "SPORT · US", "Skubal signs $450M Mets deal",
         "Two-time Cy Young winner, nine years — the largest ever for a pitcher.",
         "ESPN", "REPORTED", GREEN, (31, 78, 156)),
        ("#5", "TECH · US", "Anthropic IPO: $107.3B, largest ever",
         "Claude maker raised at $83 a share on 19 Nov; debut close $97.17.",
         "Bloomberg", "REPORTED", GREEN, (31, 78, 156)),
        ("#6", "EUROPE · WAR", "Poland: 3 Russian missiles crossed airspace",
         "Kyiv: three Kh-101 missiles entered Poland; Tusk calls it provocation.",
         "AP", "CLAIM", AMBER, (198, 93, 18)),
        ("#7", "EUROPE · SECURITY", "Intel warns of Russian nuclear satellite",
         "Satellite built to carry a nuclear warhead; launch possible next month.",
         "Bloomberg", "CLAIM", AMBER, (198, 93, 18)),
        ("#8", "EUROPE · ECONOMY", "Paris: 100+ back 2% billionaire tax",
         "Economists, politicians, unions rally behind France's 2% wealth tax.",
         "AFP", "REPORTED", GREEN, (198, 93, 18)),
        ("#9", "EUROPE · UK", "Manchester: 12,000 cleared after scare",
         "Substance scare empties arena district; no casualties reported.",
         "AP", "REPORTED", GREEN, (198, 93, 18)),
        ("#10", "EUROPE · WAR", "Zelenskyy: 165 Russian missiles in a week",
         "Kyiv says Moscow fired 165 missiles in seven days as US delays Patriots.",
         "Kyiv", "CLAIM", AMBER, (198, 93, 18)),
        ("#11", "WORLD · CLIMATE", "COP31: the day after",
         "194 nations reject the Antalya pact; Guterres 'profoundly frustrated'.",
         "CNN", "REPORTED", GREEN, (102, 102, 102)),
        ("#12", "AFRICA · LIBYA", "Benghazi: UN demands probe of port attacks",
         "Drones hit two Russian ships; UN calls for an investigation.",
         "UN News", "CLAIM", AMBER, (138, 90, 43)),
        ("#13", "MIDDLE EAST · ISRAEL", "Israel unity talks resume",
         "Likud and Gantz's Yashar return to the table after Sunday's stall.",
         "Reuters", "ONGOING", BLUE, (123, 45, 142)),
    ]
    y0 = 456
    cw2, ch2 = 200, 92
    for i, (num, kick, head, body, src, lab, col, scol) in enumerate(cards):
        r, c = divmod(i, 5)
        x = 10 + c * (cw2 + 3)
        y = y0 + r * (ch2 + 4)
        d.rectangle([x, y, x + cw2, y + ch2], outline=(160, 150, 130), width=1, fill=(255, 255, 255))
        d.rectangle([x, y, x + cw2, y + 16], fill=scol)
        d.text((x + 4, y + 3), num, font=font(SANS_B, 9), fill=(255, 255, 255))
        d.text((x + 30, y + 3), kick, font=font(SANS_B, 8), fill=(255, 255, 255))
        yy = y + 19
        hlines = wrap(d, head, font(SANS_B, 11), cw2 - 8)
        yy = text_block(d, x + 4, yy, hlines, font(SANS_B, 11), INK, 13, max_lines=2)
        blines = wrap(d, body, font(SANS, 9), cw2 - 8)
        yy = text_block(d, x + 4, yy, blines, font(SANS, 9), INK, 11, max_lines=2)
        d.text((x + 4, y + ch2 - 14), src, font=font(SANS, 8), fill=GREY)
        chip(d, x + cw2 - 58, y + ch2 - 15, lab, col)

    # map + ALSO
    y0 = 652
    d.text((10, y0), "THE WORLD — WHERE IT HAPPENED",
           font=font(SANS_B, 13), fill=RED)
    mx, my, mw, mh = 10, y0 + 20, 500, 240
    d.rectangle([mx, my, mx + mw, my + mh], fill=(223, 233, 239),
                outline=(160, 150, 130), width=1)
    for gx in range(mx + 50, mx + mw, 50):
        d.line([gx, my, gx, my + mh], fill=(200, 214, 224), width=1)
    for gy in range(my + 40, my + mh, 40):
        d.line([mx, gy, mx + mw, gy], fill=(200, 214, 224), width=1)
    land = (232, 220, 192)
    edge = (184, 169, 127)
    na = [(18, 60), (38, 27), (78, 19), (118, 25), (138, 44), (128, 69),
          (108, 79), (98, 107), (78, 126), (53, 117), (33, 93), (14, 79)]
    gl = [(143, 15), (163, 10), (173, 25), (158, 34)]
    sa = [(103, 145), (128, 140), (148, 155), (143, 193), (128, 226),
          (113, 212), (103, 174)]
    eu = [(233, 54), (258, 35), (283, 40), (293, 59), (278, 73),
          (258, 69), (243, 78), (233, 69)]
    af = [(233, 93), (268, 88), (293, 98), (303, 126), (288, 169),
          (263, 193), (248, 164), (233, 126)]
    asia = [(298, 40), (338, 26), (388, 30), (428, 45), (458, 59),
            (468, 88), (438, 107), (408, 98), (388, 117), (358, 102),
            (328, 88), (308, 69)]
    au = [(428, 179), (463, 174), (478, 188), (458, 207), (433, 198)]
    for poly in (na, gl, sa, eu, af, asia, au):
        pts = [(mx + px, my + py) for px, py in poly]
        d.polygon(pts, fill=land, outline=edge)
    for ix, iy in [(408, 126), (424, 136), (438, 122)]:
        d.ellipse([mx + ix - 5, my + iy - 3, mx + ix + 5, my + iy + 3],
                  fill=land, outline=edge)
    d.text((mx + mw - 118, my + 4), "PIN = STORY NUMBER",
           font=font(SANS_B, 9), fill=GREY)
    d.text((mx + 4, my + mh - 12), "N ↑", font=font(SANS_B, 9), fill=GREY)

    def pin(lon, lat, n, claim=False, dx=0, dy=0):
        px = mx + (lon + 180.0) / 360.0 * mw + dx
        py = my + (90.0 - lat) / 180.0 * mh + dy
        col = (217, 138, 0) if claim else (178, 34, 34)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col, outline=(255, 255, 255), width=1)
        f = font(SANS_B, 8)
        s = str(n)
        d.text((px - d.textlength(s, font=f) / 2, py - 5), s, font=f, fill=(255, 255, 255))

    pin(126.9, 37.5, 1)
    pin(-59.6, 13.1, 2, dx=-18)
    pin(151.2, -33.9, 3)
    pin(-74.0, 40.7, 4)
    pin(-122.4, 37.8, 5)
    pin(19.0, 52.0, 6, claim=True)
    pin(37.6, 55.7, 7, claim=True, dx=8, dy=-6)
    pin(2.35, 48.85, 8)
    pin(-2.24, 53.48, 9, dx=-6, dy=-6)
    pin(30.5, 50.45, 10, claim=True)
    pin(30.7, 36.9, 11, dx=-8)
    pin(20.1, 32.1, 12, claim=True, dx=-6)
    pin(35.2, 31.8, 13, dy=-9)
    pin(34.5, 31.5, 14, dx=8, dy=7)
    pin(35.2, 32.0, 15, dx=-11, dy=8)
    pin(51.4, 35.7, 16)
    pin(35.5, 33.9, 17, dx=9, dy=-8)
    pin(50.6, 26.2, 18)
    pin(32.5, 15.5, 19)
    pin(30.0, 1.5, 20)
    pin(90.4, 23.8, 21)
    pin(126.9, 37.5, 22, dx=11, dy=9)
    pin(126.9, 37.5, 23, dx=-11, dy=9)
    pin(116.4, 39.9, 24, dx=-10, dy=-8)
    pin(126.9, 37.5, 25, dx=11, dy=-9)
    pin(-77.0, 38.9, 26, dx=-11, dy=9)
    pin(-77.0, 38.9, 27, dx=11, dy=9)
    pin(-80.0, 26.8, 28)
    pin(-74.0, 40.7, 29, dx=11, dy=-9)
    pin(-105.0, 39.7, 30)
    pin(-97.2, 25.9, 31)

    # ALSO list — two columns
    d.text((522, y0), "ALSO ON MONDAY — 18 MORE STORIES",
           font=font(SANS_B, 13), fill=RED)
    also_cols = [
        (522, [("MIDDLE EAST", (123, 45, 142), [
            ("14", "Gaza: two killed in Israeli strike"),
            ("15", "West Bank settler attacks hit villages"),
            ("16", "Iran war: no deal in sight"),
            ("17", "Lebanon seizes 264 kg of explosives"),
            ("18", "Bahrain: Iranian strike hits plant")]),
            ("AFRICA", (138, 90, 43), [
            ("19", "Sudan drones downed over Khartoum"),
            ("20", "DRC: fighting traps Ebola teams")])]),
        (772, [("ASIA-PACIFIC", (15, 122, 109), [
            ("21", "Bangladesh: Hasina jailed if she returns"),
            ("22", "Seoul minister quits over AI exam chaos"),
            ("23", "SK Telecom -7.3% as Anthropic hype cools"),
            ("24", "China eases margin rules to calm rout"),
            ("25", "Seoul readies 10T-won stabilisation fund")]),
            ("NORTH AMERICA", (31, 78, 156), [
            ("26", "Bessent demands Nvidia answers"),
            ("27", "FBI probes hack of police database"),
            ("28", "Trump: Iran strikes may resume"),
            ("29", "US futures jump 3% holiday week"),
            ("30", "Tom Jackson dies at 75"),
            ("31", "States sue SpaceX over AI safety claims")])]),
    ]
    f_h = font(SANS_B, 11)
    f_i = font(SANS, 10)
    for ax, groups in also_cols:
        yy = y0 + 20
        for name, col, items in groups:
            d.text((ax, yy), name, font=f_h, fill=col)
            yy += 15
            for n, t in items:
                d.text((ax, yy), n, font=font(SANS_B, 10), fill=RED)
                d.text((ax + 22, yy), t, font=f_i, fill=INK)
                yy += 13

    # DATE CHECK
    y0 = 920
    d.rectangle([10, y0, W - 10, y0 + 48], outline=RED, width=2, fill=(255, 240, 238))
    d.text((16, y0 + 4), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
    d.text((16 + 92, y0 + 5),
           "Every story above happened or was first reported on Monday 23 November 2026.",
           font=font(SANS_B, 10), fill=INK)
    d.text((W - 10 - d.textlength("WIRES READ UP TO 23:00 UTC", font=font(SANS_B, 9)), y0 + 5),
           "WIRES READ UP TO 23:00 UTC", font=font(SANS_B, 9), fill=GREY)
    d.text((16, y0 + 19),
           "LEFT OUT (not 23 Nov): Dems reach 258 (22 Nov) · Sparta II fire (22 Nov) · El Chapo captured (22 Nov) · EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov)",
           font=font(SANS, 9), fill=INK)
    d.text((16, y0 + 32),
           "NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff.",
           font=font(SANS, 9), fill=INK)

    # footer
    y0 = 976
    d.text((10, y0),
           "SOURCES: AP · Reuters · Bloomberg · AFP · CNN · ESPN · UN News · WHO · Kyiv · Lowy Institute · Korea JoongAng · Morningstar",
           font=font(SANS, 9), fill=GREY)
    d.text((10, y0 + 12),
           "CONFIRMED = 2+ outlets · REPORTED = carried by a named source · CLAIM = one side alleges · ONGOING = developing · Red pin = reported · Amber pin = claim (unverified)",
           font=font(SANS, 9), fill=GREY)
    d.text((10, y0 + 24), "THE WORLD TODAY · 23 NOV 2026",
           font=font(SANS_B, 9), fill=INK)
    d.text((W - 10 - d.textlength("Scenes are drawn illustrations, not photographs.", font=font(SANS, 9)), y0 + 24),
           "Scenes are drawn illustrations, not photographs.", font=font(SANS, 9), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
