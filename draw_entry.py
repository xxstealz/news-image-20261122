#!/usr/bin/env python3
"""Draw 'The Daily Globe' — dense edition, Sunday 22 November 2026.

Fresh rewrite for the densify round of news-image-20261122: the same
masthead and COP31 lead, then a 6x6 grid of compact story cards —
37 verified stories in all, 12 of them with a small illustrated strip.
Pure PIL, no network, no random input, no timestamps: the same run
always writes the same bytes.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
CW = W - 2 * MARGIN  # 968

PAPER = (247, 242, 231)
INK = (26, 26, 26)
MUTED = (107, 98, 87)
RED = (179, 39, 30)
NAVY = (31, 58, 95)
WHITE = (255, 255, 255)
SKY = (196, 216, 232)
SEA = (38, 84, 124)
GREEN = (46, 107, 52)
ORANGE = (201, 106, 27)
TEAL = (31, 107, 107)
PURPLE = (91, 58, 142)
GOLD = (138, 109, 27)
SLATE = (74, 85, 104)
BROWN = (122, 74, 33)
MAGENTA = (142, 58, 91)
GRASS = (58, 128, 58)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 56)
F_DATE = font("DejaVuSans.ttf", 17)
F_FOOT = font("DejaVuSans.ttf", 11)
F_LEAD = font("DejaVuSerif-Bold.ttf", 40)
F_LEAD_TAG = font("DejaVuSans-Bold.ttf", 11)
F_LEAD_SUB = font("DejaVuSans.ttf", 16)
F_HEAD = font("DejaVuSans-Bold.ttf", 11)
F_SUB = font("DejaVuSans.ttf", 9)
F_TAG = font("DejaVuSans-Bold.ttf", 8)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---- wide pictogram strips: small scenes for the illustrated cards ----
# Each draws into a (x, y, w, h) box, roughly 134x28.

def strip_ship(d, x, y, w, h):
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    d.polygon([(x + w * 0.06, y + h * 0.62), (x + w * 0.94, y + h * 0.62),
               (x + w * 0.86, y + h * 0.88), (x + w * 0.14, y + h * 0.88)],
              fill=(70, 74, 80))
    d.rectangle([x + w * 0.42, y + h * 0.38, x + w * 0.58, y + h * 0.62],
                fill=(70, 74, 80))
    d.polygon([(x + w * 0.44, y + h * 0.38), (x + w * 0.51, y + h * 0.06),
               (x + w * 0.58, y + h * 0.38)], fill=(232, 110, 24))
    for cx, cy, r in [(0.51, 0.04, 4), (0.60, 0.10, 5), (0.44, 0.12, 4)]:
        d.ellipse([x + w * cx - r, y + h * cy - r, x + w * cx + r, y + h * cy + r],
                  fill=(90, 90, 90))


def strip_missile(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # missile streaking down-left to up-right
    d.polygon([(x + w * 0.30, y + h * 0.55), (x + w * 0.62, y + h * 0.30),
               (x + w * 0.70, y + h * 0.42), (x + w * 0.38, y + h * 0.67)],
              fill=(200, 200, 200))
    d.polygon([(x + w * 0.62, y + h * 0.30), (x + w * 0.72, y + h * 0.18),
               (x + w * 0.70, y + h * 0.42)], fill=RED)
    d.line([x + w * 0.30, y + h * 0.55, x + w * 0.06, y + h * 0.80],
           fill=(232, 180, 60), width=3)
    d.line([x + w * 0.30, y + h * 0.55, x + w * 0.12, y + h * 0.62],
           fill=(232, 180, 60), width=2)
    d.ellipse([x + w * 0.84, y + h * 0.62, x + w * 0.92, y + h * 0.78], fill=RED)
    d.text((x + w * 0.80, y + h * 0.10), "KH-101", font=F_TAG, fill=INK)


def strip_tanker(d, x, y, w, h):
    d.rectangle([x, y + h * 0.66, x + w, y + h], fill=SEA)
    d.rectangle([x + w * 0.04, y + h * 0.44, x + w * 0.96, y + h * 0.72],
                fill=(120, 60, 40))
    d.rectangle([x + w * 0.78, y + h * 0.14, x + w * 0.92, y + h * 0.44],
                fill=(240, 240, 240))
    for i, cx in enumerate([0.14, 0.30, 0.46, 0.62]):
        d.rectangle([x + w * cx, y + h * 0.24, x + w * (cx + 0.12), y + h * 0.44],
                    fill=(40, 90, 140) if i % 2 else (200, 160, 40))
    d.polygon([(x + w * 0.52, y + h * 0.44), (x + w * 0.56, y + h * 0.16),
               (x + w * 0.60, y + h * 0.44)], fill=(232, 110, 24))
    d.ellipse([x + w * 0.56 - 3, y + h * 0.10 - 3, x + w * 0.56 + 3, y + h * 0.10 + 3],
              fill=(90, 90, 90))


def strip_ball(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=GRASS)
    d.line([x, y + h * 0.5, x + w, y + h * 0.5], fill=WHITE, width=2)
    d.ellipse([x + w * 0.42, y + h * 0.08, x + w * 0.58, y + h * 0.92],
              outline=WHITE, width=2)
    cx, cy, r = x + w * 0.76, y + h * 0.50, 10
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=INK, width=1)
    d.polygon([(cx - 3, cy - 5), (cx + 3, cy - 5), (cx + 5, cy), (cx, cy + 5),
               (cx - 5, cy)], fill=INK)
    d.rectangle([x + w * 0.04, y + h * 0.20, x + w * 0.10, y + h * 0.80],
                outline=WHITE, width=2)


def strip_car(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 210, 210))
    d.rectangle([x, y + h * 0.58, x + w, y + h * 0.86], fill=(60, 60, 60))
    for i in range(8):
        d.rectangle([x + i * w / 8, y + h * 0.68, x + (i + 0.5) * w / 8,
                     y + h * 0.76], fill=(240, 200, 40))
    # low F1 silhouette
    d.polygon([(x + w * 0.18, y + h * 0.58), (x + w * 0.82, y + h * 0.58),
               (x + w * 0.88, y + h * 0.44), (x + w * 0.62, y + h * 0.40),
               (x + w * 0.52, y + h * 0.28), (x + w * 0.40, y + h * 0.28),
               (x + w * 0.34, y + h * 0.40), (x + w * 0.12, y + h * 0.44)],
              fill=RED)
    for cx in (0.28, 0.72):
        d.ellipse([x + w * cx - 7, y + h * 0.52 - 7, x + w * cx + 7, y + h * 0.52 + 7],
                  fill=INK)
    for i in range(4):
        for j in range(2):
            if (i + j) % 2 == 0:
                d.rectangle([x + w * 0.90 + i * 4, y + h * 0.08 + j * 4,
                             x + w * 0.90 + (i + 1) * 4, y + h * 0.08 + (j + 1) * 4],
                            fill=INK)


def strip_hoop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 150, 96))
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(120, 80, 40))
    d.rectangle([x + w * 0.78, y + h * 0.10, x + w * 0.92, y + h * 0.55],
                fill=WHITE, outline=INK, width=1)
    d.ellipse([x + w * 0.82, y + h * 0.50, x + w * 0.88, y + h * 0.62],
              outline=RED, width=2)
    cx, cy, r = x + w * 0.30, y + h * 0.50, 11
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 110, 24), outline=INK, width=1)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=INK, width=1)
    d.line([cx - r, cy, cx + r, cy], fill=INK, width=1)
    d.line([cx, cy - r, cx, cy + r], fill=INK, width=1)


def strip_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 130, 150))
    for cx, cy, r in [(0.30, 0.30, 14), (0.48, 0.24, 17), (0.66, 0.32, 13),
                      (0.80, 0.28, 10)]:
        d.ellipse([x + w * cx - r, y + h * cy - r, x + w * cx + r, y + h * cy + r],
                  fill=(52, 58, 66))
    d.polygon([(x + w * 0.55, y + h * 0.45), (x + w * 0.50, y + h * 0.70),
               (x + w * 0.58, y + h * 0.70), (x + w * 0.52, y + h * 0.95)],
              fill=(232, 200, 40))
    for px in (0.18, 0.32, 0.46, 0.70, 0.84):
        d.line([x + w * px, y + h * 0.58, x + w * (px - 0.03), y + h * 0.78],
               fill=(180, 200, 230), width=2)


def strip_boat(d, x, y, w, h):
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=SEA)
    d.line([x, y + h * 0.70, x + w, y + h * 0.70], fill=(120, 180, 220), width=2)
    d.line([x + w * 0.1, y + h * 0.85, x + w * 0.9, y + h * 0.85],
           fill=(120, 180, 220), width=2)
    d.polygon([(x + w * 0.20, y + h * 0.60), (x + w * 0.80, y + h * 0.60),
               (x + w * 0.72, y + h * 0.82), (x + w * 0.28, y + h * 0.82)],
              fill=(122, 74, 33))
    for cx in (0.35, 0.48, 0.61):
        d.ellipse([x + w * cx - 4, y + h * 0.34 - 4, x + w * cx + 4, y + h * 0.34 + 4],
                  fill=(52, 58, 66))
        d.rectangle([x + w * cx - 5, y + h * 0.38, x + w * cx + 5, y + h * 0.60],
                    fill=(52, 58, 66))


def strip_clapper(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 30))
    d.rectangle([x + w * 0.30, y + h * 0.30, x + w * 0.70, y + h * 0.88],
                fill=WHITE, outline=INK, width=1)
    for i in range(4):
        if i % 2 == 0:
            d.polygon([(x + w * (0.30 + i * 0.10), y + h * 0.30),
                       (x + w * (0.36 + i * 0.10), y + h * 0.30),
                       (x + w * (0.30 + i * 0.10), y + h * 0.08),
                       (x + w * (0.24 + i * 0.10), y + h * 0.08)], fill=INK)
    d.rectangle([x + w * 0.36, y + h * 0.55, x + w * 0.64, y + h * 0.60],
                fill=INK)
    d.rectangle([x + w * 0.36, y + h * 0.68, x + w * 0.56, y + h * 0.73],
                fill=INK)
    d.text((x + w * 0.76, y + h * 0.55), "$120M", font=F_TAG, fill=(232, 200, 40))


def strip_bank(d, x, y, w, h):
    d.rectangle([x, y + h * 0.82, x + w, y + h * 0.92], fill=(120, 116, 110))
    d.polygon([(x + w * 0.15, y + h * 0.42), (x + w * 0.50, y + h * 0.18),
               (x + w * 0.85, y + h * 0.42)], fill=(90, 96, 104))
    for i in range(4):
        cx = x + w * (0.24 + i * 0.17)
        d.rectangle([cx - 4, y + h * 0.42, cx + 4, y + h * 0.82],
                    fill=(200, 196, 188))
    d.text((x + w * 0.86, y + h * 0.10), "1.5%", font=F_TAG, fill=RED)


def strip_virus(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 230, 220))
    cx, cy = x + w * 0.30, y + h * 0.50
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([cx + 10 * math.cos(a), cy + 10 * math.sin(a),
                cx + 16 * math.cos(a), cy + 16 * math.sin(a)], fill=RED, width=2)
        d.ellipse([cx + 16 * math.cos(a) - 2, cy + 16 * math.sin(a) - 2,
                   cx + 16 * math.cos(a) + 2, cy + 16 * math.sin(a) + 2], fill=RED)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(150, 40, 40))
    d.text((x + w * 0.52, y + h * 0.32), "EBOLA", font=F_TAG, fill=INK)
    d.text((x + w * 0.52, y + h * 0.58), "11,000+", font=F_TAG, fill=RED)


def strip_trophy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 220, 160))
    cx = x + w * 0.30
    d.polygon([(cx - 12, y + h * 0.10), (cx + 12, y + h * 0.10),
               (cx + 8, y + h * 0.55), (cx - 8, y + h * 0.55)], fill=(212, 175, 55))
    d.arc([cx - 22, y + h * 0.12, cx - 6, y + h * 0.48], 90, 270, fill=(212, 175, 55),
          width=3)
    d.arc([cx + 6, y + h * 0.12, cx + 22, y + h * 0.48], 270, 90, fill=(212, 175, 55),
          width=3)
    d.rectangle([cx - 3, y + h * 0.55, cx + 3, y + h * 0.72], fill=(212, 175, 55))
    d.rectangle([cx - 14, y + h * 0.72, cx + 14, y + h * 0.86], fill=(212, 175, 55))
    d.text((x + w * 0.52, y + h * 0.30), "CHAMPIONS", font=F_TAG, fill=INK)
    d.text((x + w * 0.52, y + h * 0.58), "2-1", font=F_TAG, fill=RED)


# ---- lead illustration: cracked globe, pale sun, red NO DEAL slash ----

def pic_globe_lead(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    cx, cy, r = x + w * 0.42, y + h * 0.58, h * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 120, 180), outline=INK, width=3)
    d.ellipse([cx - r * 0.55, cy - r * 0.60, cx - r * 0.05, cy - r * 0.10], fill=GREEN)
    d.ellipse([cx + r * 0.10, cy + r * 0.05, cx + r * 0.65, cy + r * 0.55], fill=GREEN)
    d.ellipse([cx - r * 0.75, cy + r * 0.25, cx - r * 0.35, cy + r * 0.60], fill=GREEN)
    crack = [(cx - r * 0.45, cy - r * 0.95), (cx - r * 0.15, cy - r * 0.45),
             (cx - r * 0.45, cy - r * 0.05), (cx - r * 0.05, cy + r * 0.35),
             (cx - r * 0.30, cy + r * 0.75), (cx + r * 0.05, cy + r * 0.95)]
    d.line(crack, fill=RED, width=5, joint="curve")
    sx, sy = x + w * 0.84, y + h * 0.20
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([sx + 22 * math.cos(a), sy + 22 * math.sin(a),
                sx + 34 * math.cos(a), sy + 34 * math.sin(a)], fill=(232, 180, 60),
               width=4)
    d.ellipse([sx - 18, sy - 18, sx + 18, sy + 18], fill=(232, 180, 60), outline=INK,
              width=2)
    d.rectangle([x + w * 0.55, y + h * 0.78, x + w * 0.98, y + h * 0.94], fill=RED)
    d.text((x + w * 0.55 + 8, y + h * 0.78 + 4), "NO DEAL", font=F_HEAD, fill=WHITE)


# ---- compact story card ----

def story_card(d, x, y, w, h, color, tag, headline, sub, strip=None):
    """One compact card: coloured accent bar, tag, headline, body lines,
    and for illustrated cards a pictogram strip at the bottom."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=WHITE, outline=INK, width=1)
    d.rectangle([x, y, x + 3, y + h - 1], fill=color)
    tx = x + 10
    tw = w - 20
    d.text((tx, y + 6), tag, font=F_TAG, fill=color)
    head_lines = wrap(d, headline, F_HEAD, tw)[:3]
    ly = y + 19
    for ln in head_lines:
        d.text((tx, ly), ln, font=F_HEAD, fill=INK)
        ly += 13
    if strip:
        # Body sits right under the headline so the pictogram strip at the
        # bottom can never cover it; strip cards all have <=2-line heads.
        sy = ly + 2
        max_lines = 1 if len(head_lines) >= 3 else 2
    else:
        sy = y + 60
        max_lines = 4
    for ln in wrap(d, sub, F_SUB, tw)[:max_lines]:
        d.text((tx, sy), ln, font=F_SUB, fill=MUTED)
        sy += 11
    if strip:
        strip(d, tx, y + h - 34, tw, 28)


# ---- layout ----

def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.text((MARGIN, 12), "THE DAILY GLOBE", font=F_MAST, fill=INK)
    d.text((MARGIN, 74), "SUNDAY, 22 NOVEMBER 2026  \u2022  WORLD NEWS IN ONE PAGE",
           font=F_DATE, fill=INK)
    src = "Sources: Reuters \u2022 AP \u2022 AFP \u2022 FIFA \u2022 LiveScore"
    sw = d.textlength(src, font=F_FOOT)
    d.text((W - MARGIN - sw, 78), src, font=F_FOOT, fill=MUTED)
    d.rectangle([MARGIN, 100, W - MARGIN, 103], fill=INK)
    d.rectangle([MARGIN, 107, W - MARGIN, 109], fill=INK)

    # lead: COP31
    lx, ly, lw, lh = MARGIN, 116, CW, 166
    d.rectangle([lx, ly, lx + lw - 1, ly + lh - 1], fill=WHITE, outline=INK, width=2)
    pic_globe_lead(d, lx + lw - 250, ly + 8, 242, lh - 16)
    tx = lx + 16
    d.text((tx, ly + 10), "CLIMATE  \u2022  ANTALYA, TURKEY", font=F_LEAD_TAG, fill=GREEN)
    d.text((tx, ly + 30), "COP31", font=F_LEAD, fill=RED)
    d.text((tx, ly + 72), "COLLAPSES", font=F_LEAD, fill=INK)
    sub = ("No climate deal: nearly 200 nations leave Antalya without a pact "
           "after two weeks of talks and two days of overtime.")
    sy = ly + 122
    for ln in wrap(d, sub, F_LEAD_SUB, lw - 280):
        d.text((tx, sy), ln, font=F_LEAD_SUB, fill=INK)
        sy += 20

    # grid: 6 columns x 6 rows = 36 cards (+ lead = 37 stories)
    # (color, tag, headline, sub, strip)
    cards = [
        (RED, "CONFLICT \u2022 LIBYA", "WARSHIP SUNK IN BENGHAZI",
         "Sea drones sink the Russian corvette Merkury.", strip_ship),
        (NAVY, "EUROPE \u2022 POLAND", "POLAND: MISSILES WERE RUSSIAN",
         "All three objects were Russian Kh-101 missiles.", strip_missile),
        (RED, "CONFLICT \u2022 HORMUZ", "HORMUZ TANKERS ATTACKED",
         "Two tankers hit in the Gulf of Oman on Sunday.", strip_tanker),
        (GREEN, "SPORT \u2022 ENGLAND", "LIVERPOOL 4-0 MAN UTD",
         "Pochettino's debut ends in a rout at Anfield.", strip_ball),
        (GREEN, "SPORT \u2022 F1", "VERSTAPPEN WINS IN VEGAS",
         "35 lead changes in a wild Las Vegas GP.", strip_car),
        (GREEN, "SPORT \u2022 NBA", "WEMBANYAMA SCORES 50",
         "50 points, 19 boards in Spurs' 114-91 win.", strip_hoop),
        (RED, "UKRAINE \u2022 KYIV REGION", "14 MISSING NEAR KYIV",
         "Russian drone collapses a five-storey block in Dymer; 2 dead, "
         "9 evacuated.", None),
        (RED, "UKRAINE", "186 DRONES IN ONE NIGHT",
         "Ukraine says it downed 161 of 186 Russian drones in an overnight "
         "barrage.", None),
        (RED, "CONFLICT \u2022 BALTIC SEA", "SPARTA II TOWING BEGINS",
         "Towing starts Sunday after Saturday's strike; 16 crew evacuated, "
         "one hurt.", None),
        (ORANGE, "MIDDLE EAST \u2022 GAZA", "WCK: TRUCK VICTIMS NOT STAFF",
         "Founder Jose Andres: the three killed in a Gaza food-van strike "
         "were not WCK.", None),
        (GOLD, "MARKETS \u2022 SWITZERLAND", "SNB WATCHES INFLATION",
         "SNB flags second-round inflation risks.", strip_bank),
        (PURPLE, "CULTURE \u2022 FILM", "HUNGER GAMES OPENS AT $120M",
         "$120M domestic, $225M worldwide at the opening.", strip_clapper),
        (ORANGE, "WEST BANK", "SETTLER ARSON IN WEST BANK",
         "Cars torched in four villages near Ramallah; police open inquiry, "
         "rival calls it 'terrorism'.", None),
        (BROWN, "SUDAN", "DRONES HIT KHARTOUM",
         "Four killed as strikes hit homes and a UN building; army blames "
         "Ethiopia - unverified.", None),
        (NAVY, "EUROPE \u2022 ESPIONAGE", "POLAND: SECOND PLOT VS RAPPER",
         "Russia 'twice tried to kill' US-Ukrainian star Kyivstoner, "
         "Warsaw says.", None),
        (BROWN, "AFRICA \u2022 NIGERIA", "NIGERIA BOAT TOLL HITS 24",
         "Boat toll hits 24 in Bayelsa; 24 survivors found.", strip_boat),
        (MAGENTA, "AMERICAS \u2022 BRAZIL", "BRAZIL STORM TOLL RISES TO 5",
         "Supercell wrecks Tupancireta: 5 dead, 265 hurt.", strip_storm),
        (BROWN, "AFRICA \u2022 CONGO", "EBOLA FIGHTING TRAPS STAFF",
         "Clashes trap Ebola workers at an Ituri hospital.", strip_virus),
        (TEAL, "ASIA \u2022 INDONESIA", "FACTORY FIRE TOLL RISES",
         "3 dead, 37 missing after a blaze at a candy factory in Cikande.",
         None),
        (TEAL, "ASIA \u2022 SOUTH KOREA", "S. KOREA MINISTER QUITS",
         "Education chief Choi Kyo-jin resigns after AI-cheating measures "
         "chaos.", None),
        (BROWN, "AFRICA \u2022 S. AFRICA", "MLAMBO-NGCUKA MOURNED",
         "Flags at half-mast from Sunday; state funeral for the ex-UN "
         "Women chief, 28 Nov.", None),
        (SLATE, "ISRAEL \u2022 POLITICS", "EISENKOT COURTS LIKUD",
         "Israel's opposition leader invites Netanyahu's party to "
         "coalition talks.", None),
        (PURPLE, "SPACE", "MERCURY ARRIVAL - WITH A GLITCH",
         "BepiColombo reaches Mercury orbit after 8 years; ESA reports a "
         "thruster fault.", None),
        (GOLD, "ASIA \u2022 JAPAN", "SHURI CASTLE RISES AGAIN",
         "Okinawa celebrates the restored hall, seven years after fire "
         "destroyed it.", None),
        (GREEN, "SPORT \u2022 ITALY", "ATALANTA 4-4 INTER",
         "Esposito's hat-trick not enough as a stoppage-time penalty "
         "rescues Atalanta.", None),
        (GREEN, "SPORT \u2022 SPAIN", "BARCELONA 3-2 VILLARREAL",
         "Barca come back from two down to win on the road.", None),
        (GREEN, "SPORT \u2022 S. AMERICA", "BOCA WIN SUDAMERICANA",
         "Boca Juniors beat Atletico Mineiro 2-0 to lift the Copa "
         "Sudamericana.", None),
        (GREEN, "SPORT \u2022 ENGLAND", "NEWCASTLE 2-2 ARSENAL",
         "Madueke rescues a point for the leaders after Barnes and Thiaw "
         "turn it around.", None),
        (GREEN, "SPORT \u2022 SPAIN", "REAL MADRID 2-1 CELTA",
         "Bellingham and late Espi complete a comeback; Mbappe misses a "
         "penalty.", None),
        (GREEN, "SPORT \u2022 ITALY", "AC MILAN 5-1 FROSINONE",
         "Ramos ends his drought as Milan hit five at San Siro to go "
         "fourth.", None),
        (GREEN, "SPORT \u2022 FRANCE", "LE MANS 3-2 MARSEILLE",
         "Stoppage-time winner hands Le Mans a second Ligue 1 victory.",
         None),
        (GREEN, "SPORT \u2022 ITALY", "JUVENTUS 4-0 VENEZIA",
         "Four goals in 18 minutes mark Spalletti's 600th Serie A match.",
         None),
        (GREEN, "SPORT \u2022 U17 WC", "SAUDI ARABIA STUN FRANCE",
         "Alkahtani's 73rd-minute goal wins 1-0 at the U17 World Cup in "
         "Doha.", None),
        (GREEN, "SPORT \u2022 U17 WC", "EGYPT 2-0 QATAR",
         "Hosts Qatar beaten as Egypt win their U17 World Cup group game.",
         None),
        (GREEN, "SPORT \u2022 NWSL", "KC CURRENT WIN NWSL TITLE",
         "First NWSL crown: 2-1 over Washington Spirit.", strip_trophy),
        (MAGENTA, "EUROPE \u2022 PROTESTS", "YOUTH TAKE TO THE STREETS",
         "Cost-of-living protests in 400 cities across 20+ European "
         "countries.", None),
    ]
    assert len(cards) == 36, len(cards)
    col_w, row_h = 154, 112
    gx, gy = MARGIN, 290
    for i, (color, tag, head, sub, strip) in enumerate(cards):
        r, c = divmod(i, 6)
        story_card(d, gx + c * (col_w + 8), gy + r * (row_h + 7),
                   col_w, row_h, color, tag, head, sub, strip)

    # footer
    d.rectangle([MARGIN, 1002, W - MARGIN, 1003], fill=INK)
    d.text((MARGIN, 1007), "37 STORIES  \u2022  FIVE REGIONS  \u2022  ALL VERIFIED 22 NOVEMBER 2026",
           font=F_FOOT, fill=MUTED)
    right = "THE DAILY GLOBE"
    rw = d.textlength(right, font=F_FOOT)
    d.text((W - MARGIN - rw, 1007), right, font=F_FOOT, fill=MUTED)

    img.save(out_path, format="PNG")
    return out_path


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(target)
    print("wrote", target)
