#!/usr/bin/env python3
"""news-23 b21 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
BLACK = (12, 12, 12)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
NAVY = (18, 42, 86)
TEAL = (14, 110, 105)
GOLD = (184, 134, 11)
GREY = (90, 90, 90)
LIGHT = (232, 228, 216)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"

def f_serif_b(sz): return ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", sz)
def f_serif(sz): return ImageFont.truetype(FD + "DejaVuSerif.ttf", sz)
def f_sans(sz): return ImageFont.truetype(FD + "DejaVuSans.ttf", sz)
def f_sans_b(sz): return ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", sz)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def hline(y, x0=14, x1=1010, fill=INK, w=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)

# ---------- masthead ----------
d.rectangle([0, 0, W, 52], fill=BLACK)
text(14, 6, "THE WORLD TODAY", f_serif_b(34), fill=(255, 255, 255))
text(1010, 14, "MONDAY  23 NOVEMBER 2026", f_sans_b(17), fill=(212, 175, 55), anchor="ra")

# ---------- kicker ----------
text(14, 58, "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
     f_serif(15), fill=DARKRED)

# ---------- number strip ----------
nums = [
    ("-3.3%", "KOSPI", RED),
    ("5.3", "US-CHINA POWER GAP", NAVY),
    ("11,762", "EBOLA CASES, DRC", (90, 90, 20)),
    ("$450M", "SKUBAL DEAL", (128, 0, 128)),
    ("$107.3B", "ANTHROPIC IPO", (160, 32, 160)),
]
cw = (1010 - 14) / 5
for i, (v, lab, col) in enumerate(nums):
    x = 14 + i * cw
    text(x + 2, 76, v, f_sans_b(30), fill=col)
    text(x + 2, 108, lab, f_sans_b(11), fill=INK)
hline(124, fill=INK, w=2)

# ---------- the day in numbers strip ----------
d.rectangle([14, 128, 1010, 146], fill=NAVY)
text(20, 131, "THE DAY IN NUMBERS", f_sans_b(11), fill=(255, 255, 255))
text(1010 - 6, 131, "-5.8% intraday low  \u00b7  165 missiles in a week  \u00b7  12,000 cleared  \u00b7  264 kg seized  \u00b7  2% tax backed",
     f_sans(11), fill=(255, 255, 255), anchor="ra")

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", (0, 128, 96)), ("AMERICAS 8", (18, 42, 86)),
           ("MIDDLE EAST 6", (128, 96, 0)), ("EUROPE 5", (0, 96, 96)),
           ("AFRICA 3", (96, 64, 96)), ("WORLD 2", (90, 90, 90))]
rw = (1010 - 14) / 6
for i, (lab, col) in enumerate(regions):
    x = 14 + i * rw
    d.rectangle([x, 150, x + rw - 2, 168], fill=col)
    text(x + rw / 2, 153, lab, f_sans_b(11), fill=(255, 255, 255), anchor="ma")

# ---------- hero scenes ----------
HX0, HY0 = 14, 174
HW = 322
HGAP = 8

# --- scene 1: Kospi chart ---
x0 = HX0
d.rectangle([x0, HY0, x0 + HW, HY0 + 128], fill=(10, 18, 46))
# skyline
import random
random.seed(7)
bx = x0 + 6
while bx < x0 + HW - 14:
    bw = random.randint(14, 26)
    bh = random.randint(18, 46)
    d.rectangle([bx, HY0 + 128 - bh, bx + bw, HY0 + 128], fill=(24, 40, 80))
    for wy in range(HY0 + 128 - bh + 5, HY0 + 122, 9):
        for wx in range(bx + 3, bx + bw - 3, 7):
            if random.random() < 0.5:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
    bx += bw + 3
# chart line
pts = [(x0 + 14 + i * 34, HY0 + 96 - i * 2 - (0 if i < 5 else (i - 4) * 9)) for i in range(9)]
pts = [(x0 + 14 + i * 34, HY0 + 40 + i * 7) for i in range(9)]
d.line(pts, fill=(255, 80, 60), width=3)
for px, py in pts:
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 200, 60), outline=(255, 80, 60))
text(x0 + 10, HY0 + 6, "-3.3%", f_sans_b(30), fill=(255, 80, 60))
d.rectangle([x0, HY0 + 128 - 20, x0 + HW, HY0 + 128], fill=BLACK)
text(x0 + 8, HY0 + 110, "KOSPI  4,708.54   \u00b7   -161 PTS", f_sans_b(11), fill=(255, 255, 255))

# --- scene 2: Guterres globe ---
x0 = HX0 + HW + HGAP
d.rectangle([x0, HY0, x0 + HW, HY0 + 128], fill=TEAL)
text(x0 + 10, HY0 + 8, "150 DELEGATES", f_sans_b(26), fill=(255, 214, 60))
text(x0 + 10, HY0 + 38, "BACK A RISK FRAMEWORK", f_sans_b(15), fill=(255, 255, 255))
# flags
for i, col in enumerate([(200, 40, 40), (40, 80, 200), (255, 200, 40)]):
    fx = x0 + 22 + i * 52
    d.line([(fx, HY0 + 66), (fx, HY0 + 118)], fill=(255, 255, 255), width=3)
    d.polygon([(fx, HY0 + 66), (fx + 34, HY0 + 74), (fx, HY0 + 82)], fill=col)
# podium
d.polygon([(x0 + 150, HY0 + 118), (x0 + 230, HY0 + 118), (x0 + 215, HY0 + 128), (x0 + 165, HY0 + 128)], fill=(120, 72, 20))
# globe
gx, gy, gr = x0 + 280, HY0 + 88, 34
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(170, 215, 235), outline=(255, 255, 255), width=2)
d.ellipse([gx - 20, gy - 24, gx + 2, gy - 4], fill=(90, 170, 90))
d.ellipse([gx - 4, gy + 6, gx + 22, gy + 26], fill=(90, 170, 90))
d.ellipse([gx - 26, gy + 4, gx - 10, gy + 18], fill=(90, 170, 90))
d.rectangle([x0, HY0 + 128 - 20, x0 + HW, HY0 + 128], fill=BLACK)
text(x0 + 8, HY0 + 110, "UN  \u00b7  BRIDGETOWN", f_sans_b(11), fill=(255, 255, 255))

# --- scene 3: power bars ---
x0 = HX0 + 2 * (HW + HGAP)
d.rectangle([x0, HY0, x0 + HW, HY0 + 128], fill=(255, 255, 255), outline=INK, width=1)
text(x0 + 10, HY0 + 6, "NARROWEST SINCE 2018", f_sans_b(13), fill=INK)
text(x0 + HW - 10, HY0 + 6, "GAP 5.3", f_sans_b(13), fill=GOLD, anchor="ra")
bars = [("US", 78.9, NAVY), ("CHINA", 73.6, RED), ("INDIA", 40.5, GOLD)]
bw = 62
base = HY0 + 112
for i, (lab, val, col) in enumerate(bars):
    bx = x0 + 30 + i * 96
    bh = val * 0.72
    text(bx + bw / 2, base - bh - 18, f"{val}", f_sans_b(15), fill=col, anchor="ma")
    d.rectangle([bx, base - bh, bx + bw, base], fill=col)
    text(bx + bw / 2, base + 4, lab, f_sans_b(11), fill=INK, anchor="ma")

# ---------- hero headlines + bodies ----------
heroes = [
    ("1  AI ROUT HITS ASIA",
     "Kospi -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE"),
    ("2  GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back the plan.",
     "UNITED NATIONS"),
    ("3  US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 - gap 5.3, narrowest since 2018. India third.",
     "LOWY INSTITUTE"),
]
hy = HY0 + 128 + 6
for i, (head, body, src) in enumerate(heroes):
    x0 = HX0 + i * (HW + HGAP)
    lines = wrap(head, f_sans_b(15), HW)
    yy = hy
    for ln in lines[:2]:
        text(x0, yy, ln, f_sans_b(15), fill=INK)
        yy += 18
    blines = wrap(body, f_sans(12), HW)
    for ln in blines[:3]:
        text(x0, yy, ln, f_sans(12), fill=(40, 40, 40))
        yy += 15
    text(x0, yy + 1, src, f_sans(10), fill=GREY)
    # REPORTED chip
    chip = "REPORTED"
    cw2 = d.textlength(chip, font=f_sans_b(9)) + 10
    d.rectangle([x0 + HW - cw2, yy, x0 + HW, yy + 14], fill=NAVY)
    text(x0 + HW - cw2 / 2, yy + 2, chip, f_sans_b(9), fill=(255, 255, 255), anchor="ma")

# ---------- more of the day: 10 cards ----------
CY = 396
text(14, CY - 20, "MORE OF THE DAY \u2014 10 STORIES", f_sans_b(14), fill=INK)
hline(CY - 4, fill=INK, w=2)
cards = [
    ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury chief wants to know of violations over China sales.", "Reuters", "REPORTED", NAVY),
    ("FBI", "FBI PROBES NCIC HACK", "Hackers hit the NCIC system used by police nationwide.", "AP", "REPORTED", NAVY),
    ("WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "President says strikes could resume in the New Year.", "Reuters", "REPORTED", NAVY),
    ("MARKETS", "US FUTURES JUMP 3%", "Holiday-week rally lifts Nasdaq futures as the AI rout cools.", "Bloomberg", "REPORTED", NAVY),
    ("SPORT", "SKUBAL'S $450M METS DEAL", "Two-time Cy Young winner signs nine years, largest ever for a pitcher.", "ESPN", "REPORTED", NAVY),
    ("SPORT", "TOM JACKSON DIES AT 75", "Broncos linebacker turned ESPN voice dies.", "ESPN", "REPORTED", NAVY),
    ("LEGAL", "STATES SUE SPACEX", "Ten states challenge AI safety claims.", "AP", "REPORTED", NAVY),
    ("TECH", "ANTHROPIC IPO: $107.3B", "Claude maker raises at $83 a share; debut closes $97.17.", "WSJ", "REPORTED", NAVY),
    ("EUROPE", "POLAND: 3 RUSSIAN MISSILES CROSSED AIRSPACE", "Kyiv says three Kh-101s crossed Polish airspace Friday.", "AP", "CLAIM", RED),
    ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "Intel claims Moscow built a satellite to carry a nuclear warhead.", "Reuters", "CLAIM", RED),
]
card_w = 196
card_h = 86
for idx, (cat, head, body, src, chip, chipcol) in enumerate(cards):
    r, c = divmod(idx, 5)
    x0 = 14 + c * (card_w + 4)
    y0 = CY + r * (card_h + 4)
    d.rectangle([x0, y0, x0 + card_w, y0 + card_h], fill=(255, 255, 255), outline=(180, 180, 180), width=1)
    d.rectangle([x0, y0, x0 + card_w, y0 + 16], fill=BLACK)
    text(x0 + 4, y0 + 2, cat, f_sans_b(9), fill=(255, 255, 255))
    text(x0 + card_w - 4, y0 + 2, str(idx + 4), f_sans_b(10), fill=(255, 255, 255), anchor="ra")
    yy = y0 + 20
    for ln in wrap(head, f_sans_b(11), card_w - 8)[:2]:
        text(x0 + 4, yy, ln, f_sans_b(11), fill=INK)
        yy += 13
    for ln in wrap(body, f_sans(10), card_w - 8)[:2]:
        text(x0 + 4, yy, ln, f_sans(10), fill=(40, 40, 40))
        yy += 12
    text(x0 + 4, y0 + card_h - 14, src, f_sans(9), fill=GREY)
    cw2 = d.textlength(chip, font=f_sans_b(8)) + 8
    d.rectangle([x0 + card_w - cw2 - 3, y0 + card_h - 15, x0 + card_w - 3, y0 + card_h - 3], fill=chipcol)
    text(x0 + card_w - 3 - cw2 / 2, y0 + card_h - 14, chip, f_sans_b(8), fill=(255, 255, 255), anchor="ma")

# ---------- map + also ----------
MY = 596
text(14, MY - 18, "WHERE IT HAPPENED", f_sans_b(14), fill=INK)
text(492, MY - 18, "ALSO ON MONDAY", f_sans_b(14), fill=INK)
hline(MY - 2, fill=INK, w=2)
mapx0, mapy0, mapx1, mapy1 = 14, MY + 4, 480, 810
d.rectangle([mapx0, mapy0, mapx1, mapy1], fill=(214, 232, 240), outline=(150, 150, 150), width=1)
# grid
for gx in range(mapx0 + 30, mapx1, 30):
    d.line([(gx, mapy0), (gx, mapy1)], fill=(190, 210, 222), width=1)
for gy in range(mapy0 + 26, mapy1, 26):
    d.line([(mapx0, gy), (mapx1, gy)], fill=(190, 210, 222), width=1)
# rough continents (relative coords inside map box)
def poly(pts, fill=(140, 190, 120)):
    d.polygon([(mapx0 + px, mapy0 + py) for px, py in pts], fill=fill)
poly([(28, 52), (90, 30), (150, 44), (168, 78), (140, 118), (96, 132), (52, 108), (22, 82)])       # N America
poly([(96, 140), (128, 136), (150, 168), (128, 205), (104, 178), (88, 158)])                       # S America
poly([(196, 66), (236, 56), (252, 78), (232, 96), (200, 92)])                                      # Europe
poly([(212, 108), (268, 100), (292, 128), (272, 178), (236, 196), (214, 150)])                    # Africa
poly([(262, 44), (330, 26), (420, 34), (448, 66), (420, 108), (352, 116), (300, 96), (272, 66)])  # Asia
poly([(392, 168), (436, 160), (448, 186), (412, 200), (388, 188)])                                # Australia
# pins 1-13 (spread to avoid overlap)
pins = [(398, 78), (88, 168), (372, 52), (118, 96), (146, 74), (296, 118),
        (104, 66), (58, 108), (84, 126), (108, 148), (238, 66), (266, 82), (300, 52)]
for i, (px, py) in enumerate(pins, start=1):
    d.ellipse([mapx0 + px - 9, mapy0 + py - 9, mapx0 + px + 9, mapy0 + py + 9], fill=RED, outline=(255, 255, 255), width=1)
    text(mapx0 + px, mapy0 + py - 7, str(i), f_sans_b(10), fill=(255, 255, 255), anchor="ma")
text(14, 812, "Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing \u00b7 4 Washington \u00b7 5 New York \u00b7 6 Tehran \u00b7 7 Chicago \u00b7 8 San Francisco",
     f_sans(10), fill=GREY)
text(14, 826, "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 Kyiv \u00b7 13 Moscow", f_sans(10), fill=GREY)

# ALSO list (18 items, 2 columns x 9)
also = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: the day after pact rejected",
    "18. Benghazi: UN demands port probe",
    "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike",
    "21. West Bank settler attacks",
    "22. Iran war: no deal in sight",
    "23. Lebanon seizes 264 kg explosives",
    "24. Bahrain: strike hits plant, 2 hurt",
    "25. Sudan: defences down drones",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
for i, item in enumerate(also):
    col, row = divmod(i, 9)
    ax = 492 + col * 262
    ay = MY + 6 + row * 24
    # split number and rest for bold number
    num, rest = item.split(". ", 1)
    text(ax, ay, num + ".", f_sans_b(11), fill=INK)
    for ln in wrap(rest, f_sans(11), 262 - 26)[:1]:
        text(ax + 26, ay, ln, f_sans(11), fill=INK)

# ---------- DATE CHECK ----------
DY0, DY1 = 848, 936
d.rectangle([14, DY0, 1010, DY1], outline=RED, width=3)
text(24, DY0 + 6, "DATE CHECK", f_sans_b(15), fill=RED)
text(150, DY0 + 8, "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", f_sans_b(11), fill=INK)
text(24, DY0 + 30, "LEFT OUT \u2014 NOT 23 NOV: Democrats reach 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo Isidro captured (22 Nov) \u00b7",
     f_sans(11), fill=INK)
text(24, DY0 + 46, "EU-Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar ruling (19 Nov)",
     f_sans(11), fill=INK)
text(24, DY0 + 66, "NOT YET: Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
     f_sans(11), fill=INK)

# ---------- sources + chips ----------
text(14, 944, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
     f_sans(10), fill=GREY)
text(14, 960, "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, not independently confirmed \u00b7 ONGOING = still developing",
     f_sans(10), fill=GREY)

# ---------- footer ----------
d.rectangle([0, 984, W, H], fill=BLACK)
text(W // 2, 994, "Scenes are drawn illustrations, not photographs.  \u00b7  THE WORLD TODAY \u2014 Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions",
     f_sans_b(12), fill=(212, 175, 55), anchor="ma")

img.save("entry.png")
print("saved entry.png", img.size)
