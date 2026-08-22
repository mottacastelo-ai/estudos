from __future__ import annotations

import math
import os
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


W, H = 1024, 1536
PURPLE = "#7C3AED"
LILAC = "#A78BFA"
BG = "#F3F0FF"
DARK_PURPLE = "#4C1D95"
GOLD = "#F5C518"
GOLD_DARK = "#E8B308"
GOLD_LIGHT = "#FFF7B0"
CREAM = "#FFF4CC"
BLACK = "#111111"
WHITE = "#FFFFFF"

ROOT = Path(r"C:\Users\wizar\OneDrive\Documentos\Projeto Estudos")
OUT_DIR = ROOT / "estudos" / "portugues" / "conjuncoes"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(fr"C:\Windows\Fonts\{name}", size)


F_TITLE = font("consolab.ttf", 36)
F_TEXT = font("comic.ttf", 23)
F_TEXT_B = font("comicbd.ttf", 23)
F_SMALL = font("comic.ttf", 18)
F_SMALL_B = font("comicbd.ttf", 18)
F_NOTE = font("comici.ttf", 18)
F_NOTE_B = font("comicz.ttf", 18)
F_BOARD = font("comicbd.ttf", 15)


def rounded(draw, box, fill, outline=BLACK, width=3, radius=14):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def title(draw, text):
    draw.rectangle((0, 0, W, 72), fill=PURPLE)
    draw.text((W // 2, 36), text, fill=WHITE, font=F_TITLE, anchor="mm")


def page_base(text):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    title(draw, text)
    return img, draw


def panel(draw, box, fill="#FFFFFF"):
    rounded(draw, box, fill=fill, outline=BLACK, width=3, radius=12)


def rich_tokens(text: str):
    parts = []
    i = 0
    while i < len(text):
        if text.startswith("[[", i):
            j = text.find("]]", i)
            parts.append((text[i + 2 : j], True))
            i = j + 2
        else:
            j = text.find("[[", i)
            if j < 0:
                j = len(text)
            parts.append((text[i:j], False))
            i = j
    toks = []
    for seg, hi in parts:
        for item in seg.replace("\n", " \n ").split(" "):
            if item == "":
                continue
            toks.append((item, hi))
    return toks


def draw_rich(draw, xy, text, max_w, base_font=F_TEXT, hi_font=F_TEXT_B, fill=BLACK, line_h=None):
    x, y = xy
    line_h = line_h or int(base_font.size * 1.35)
    cur = []
    cur_w = 0
    lines = []
    for tok, hi in rich_tokens(text):
        if tok == "\n":
            lines.append(cur)
            cur, cur_w = [], 0
            continue
        f = hi_font if hi else base_font
        tw = draw.textlength(tok + " ", font=f)
        if cur and cur_w + tw > max_w:
            lines.append(cur)
            cur, cur_w = [], 0
        cur.append((tok, hi))
        cur_w += tw
    if cur:
        lines.append(cur)
    for line in lines:
        xx = x
        for tok, hi in line:
            f = hi_font if hi else base_font
            if hi:
                draw.text((xx, y), tok + " ", fill=DARK_PURPLE, font=f, stroke_width=1, stroke_fill=GOLD)
            else:
                draw.text((xx, y), tok + " ", fill=fill, font=f)
            xx += draw.textlength(tok + " ", font=f)
        y += line_h
    return y


def speech(draw, box, text, tail=None, small=False):
    rounded(draw, box, WHITE, width=2, radius=18)
    if tail:
        x1, y1, x2, y2 = tail
        draw.line((x1, y1, x2, y2), fill=BLACK, width=3)
    f = F_SMALL if small else F_TEXT
    fb = F_SMALL_B if small else F_TEXT_B
    return draw_rich(draw, (box[0] + 14, box[1] + 12), text, box[2] - box[0] - 28, f, fb)


def caption(draw, box, text):
    rounded(draw, box, CREAM, width=2, radius=8)
    return draw_rich(draw, (box[0] + 12, box[1] + 10), text, box[2] - box[0] - 24, F_NOTE, F_NOTE_B)


def label(draw, xy, text, size=22, fill=DARK_PURPLE):
    draw.text(xy, text, fill=fill, font=font("comicbd.ttf", size), stroke_width=1, stroke_fill=GOLD)


def classroom(draw, box):
    x1, y1, x2, y2 = box
    draw.rectangle(box, fill="#FCFBFF")
    draw.rectangle((x1, y2 - 45, x2, y2), fill="#D9F99D")
    draw.rectangle((x1 + 20, y1 + 20, x2 - 20, y1 + 70), fill="#EDE9FE", outline=LILAC, width=2)
    draw.rectangle((x2 - 145, y1 + 20, x2 - 35, y1 + 88), fill="#BAE6FD", outline=BLACK, width=2)
    for i in range(3):
        draw.line((x2 - 130 + i * 35, y1 + 20, x2 - 130 + i * 35, y1 + 88), fill=WHITE, width=2)
    draw.ellipse((x2 - 95, y1 + 36, x2 - 70, y1 + 61), fill="#FDE68A")
    draw.rectangle((x1 + 35, y2 - 88, x1 + 190, y2 - 55), fill="#A78BFA", outline=BLACK, width=2)


def savanna(draw, box):
    x1, y1, x2, y2 = box
    draw.rectangle(box, fill="#CFFAFE")
    draw.rectangle((x1, y2 - 70, x2, y2), fill="#FDE68A")
    draw.ellipse((x2 - 120, y1 + 26, x2 - 55, y1 + 91), fill="#FACC15")
    draw.line((x1 + 90, y2 - 72, x1 + 105, y2 - 130), fill="#8B5A2B", width=9)
    draw.ellipse((x1 + 42, y2 - 170, x1 + 160, y2 - 95), fill="#86EFAC")


def playground(draw, box):
    x1, y1, x2, y2 = box
    draw.rectangle(box, fill="#BAE6FD")
    draw.rectangle((x1, y2 - 58, x2, y2), fill="#BBF7D0")
    draw.rectangle((x1 + 25, y2 - 95, x1 + 180, y2 - 78), fill="#A16207", outline=BLACK, width=2)
    draw.rectangle((x1 + 45, y2 - 78, x1 + 57, y2 - 35), fill="#854D0E")
    draw.rectangle((x1 + 148, y2 - 78, x1 + 160, y2 - 35), fill="#854D0E")
    draw.line((x2 - 95, y2 - 60, x2 - 75, y2 - 145), fill="#8B5A2B", width=12)
    draw.ellipse((x2 - 160, y2 - 205, x2 - 20, y2 - 110), fill="#86EFAC")


def elo(draw, cx, cy, s=1.0, mood="happy", glow=False):
    rx, ry = 34 * s, 56 * s
    if glow:
        for r in range(68, 38, -10):
            draw.ellipse((cx - r * s, cy - r * s, cx + r * s, cy + r * s), fill=GOLD_LIGHT)
    draw.line((cx - rx, cy + 5 * s, cx - 56 * s, cy + 35 * s), fill=GOLD_DARK, width=max(3, int(6 * s)))
    draw.line((cx + rx, cy + 5 * s, cx + 56 * s, cy + 35 * s), fill=GOLD_DARK, width=max(3, int(6 * s)))
    draw.ellipse((cx - 72 * s, cy + 25 * s, cx - 48 * s, cy + 50 * s), fill=WHITE, outline=BLACK, width=2)
    draw.ellipse((cx + 48 * s, cy + 25 * s, cx + 72 * s, cy + 50 * s), fill=WHITE, outline=BLACK, width=2)
    draw.line((cx - 18 * s, cy + ry - 4 * s, cx - 25 * s, cy + ry + 32 * s), fill=GOLD_DARK, width=max(3, int(6 * s)))
    draw.line((cx + 18 * s, cy + ry - 4 * s, cx + 25 * s, cy + ry + 32 * s), fill=GOLD_DARK, width=max(3, int(6 * s)))
    draw.ellipse((cx - 45 * s, cy + ry + 25 * s, cx - 12 * s, cy + ry + 45 * s), fill=WHITE, outline=BLACK, width=2)
    draw.ellipse((cx + 12 * s, cy + ry + 25 * s, cx + 45 * s, cy + ry + 45 * s), fill=WHITE, outline=BLACK, width=2)
    draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=GOLD, outline=BLACK, width=max(2, int(3 * s)))
    draw.ellipse((cx - 17 * s, cy - 31 * s, cx + 17 * s, cy + 38 * s), fill=BG, outline=GOLD_DARK, width=max(2, int(3 * s)))
    draw.arc((cx - rx + 8 * s, cy - ry + 8 * s, cx + rx - 8 * s, cy + ry - 8 * s), 210, 330, fill=GOLD_LIGHT, width=max(2, int(5 * s)))
    draw.ellipse((cx - 20 * s, cy - 40 * s, cx - 5 * s, cy - 22 * s), fill=WHITE, outline=BLACK, width=2)
    draw.ellipse((cx + 5 * s, cy - 40 * s, cx + 20 * s, cy - 22 * s), fill=WHITE, outline=BLACK, width=2)
    draw.ellipse((cx - 14 * s, cy - 34 * s, cx - 8 * s, cy - 27 * s), fill=BLACK)
    draw.ellipse((cx + 10 * s, cy - 34 * s, cx + 16 * s, cy - 27 * s), fill=BLACK)
    if mood == "surprised":
        draw.ellipse((cx - 8 * s, cy - 12 * s, cx + 8 * s, cy + 7 * s), fill="#7F1D1D")
        draw.text((cx, cy - 92 * s), "!", fill=GOLD, font=font("comicbd.ttf", int(42 * s)), anchor="mm", stroke_width=1, stroke_fill=BLACK)
    elif mood == "wink":
        draw.arc((cx - 12 * s, cy - 10 * s, cx + 12 * s, cy + 8 * s), 0, 180, fill=BLACK, width=2)
    else:
        draw.arc((cx - 18 * s, cy - 16 * s, cx + 18 * s, cy + 12 * s), 0, 180, fill=BLACK, width=max(2, int(3 * s)))


def bia(draw, cx, cy, s=1.0, pose="wave"):
    skin = "#A85F32"
    hair = "#15100B"
    shirt = "#0B3A78"
    shorts = "#164E8A"
    draw.ellipse((cx - 45 * s, cy - 124 * s, cx + 45 * s, cy - 44 * s), fill=hair, outline=BLACK, width=2)
    draw.ellipse((cx - 33 * s, cy - 108 * s, cx + 33 * s, cy - 45 * s), fill=skin, outline=BLACK, width=2)
    for dx in (-36, -24, 22, 35):
        draw.ellipse((cx + dx * s - 17 * s, cy - 120 * s, cx + dx * s + 17 * s, cy - 85 * s), fill=hair, outline=BLACK, width=1)
    draw.ellipse((cx - 18 * s, cy - 88 * s, cx - 4 * s, cy - 72 * s), fill=WHITE, outline=BLACK, width=1)
    draw.ellipse((cx + 6 * s, cy - 88 * s, cx + 20 * s, cy - 72 * s), fill=WHITE, outline=BLACK, width=1)
    draw.ellipse((cx - 12 * s, cy - 82 * s, cx - 7 * s, cy - 77 * s), fill=BLACK)
    draw.ellipse((cx + 12 * s, cy - 82 * s, cx + 17 * s, cy - 77 * s), fill=BLACK)
    draw.arc((cx - 18 * s, cy - 73 * s, cx + 18 * s, cy - 50 * s), 0, 180, fill=BLACK, width=2)
    draw.polygon([(cx - 39 * s, cy - 44 * s), (cx + 39 * s, cy - 44 * s), (cx + 50 * s, cy + 50 * s), (cx - 50 * s, cy + 50 * s)], fill=shirt, outline=BLACK)
    draw.polygon([(cx - 22 * s, cy - 44 * s), (cx, cy - 22 * s), (cx + 22 * s, cy - 44 * s)], fill=WHITE, outline=BLACK)
    draw.rectangle((cx - 45 * s, cy + 50 * s, cx + 45 * s, cy + 96 * s), fill=shorts, outline=BLACK, width=2)
    draw.line((cx - 25 * s, cy + 96 * s, cx - 32 * s, cy + 150 * s), fill=skin, width=max(6, int(10 * s)))
    draw.line((cx + 25 * s, cy + 96 * s, cx + 32 * s, cy + 150 * s), fill=skin, width=max(6, int(10 * s)))
    draw.ellipse((cx - 50 * s, cy + 145 * s, cx - 12 * s, cy + 165 * s), fill=WHITE, outline=BLACK, width=2)
    draw.ellipse((cx + 12 * s, cy + 145 * s, cx + 50 * s, cy + 165 * s), fill=WHITE, outline=BLACK, width=2)
    draw.line((cx - 44 * s, cy - 25 * s, cx - 74 * s, cy + 25 * s), fill=skin, width=max(5, int(8 * s)))
    if pose == "point":
        draw.line((cx + 43 * s, cy - 25 * s, cx + 85 * s, cy - 60 * s), fill=skin, width=max(5, int(8 * s)))
        draw.ellipse((cx + 78 * s, cy - 70 * s, cx + 95 * s, cy - 53 * s), fill=skin, outline=BLACK, width=1)
    elif pose == "hold":
        draw.line((cx + 43 * s, cy - 25 * s, cx + 78 * s, cy + 12 * s), fill=skin, width=max(5, int(8 * s)))
    else:
        draw.line((cx + 43 * s, cy - 25 * s, cx + 78 * s, cy - 65 * s), fill=skin, width=max(5, int(8 * s)))
        draw.ellipse((cx + 70 * s, cy - 80 * s, cx + 92 * s, cy - 58 * s), fill=skin, outline=BLACK, width=1)


def book(draw, box, color="#EF4444"):
    rounded(draw, box, color, outline=BLACK, width=2, radius=6)
    draw.line((box[0] + 8, box[1], box[0] + 8, box[3]), fill="#FEE2E2", width=3)


def page1():
    img, draw = page_base("PÁGINA 1 — O ELO QUE JUNTA AS PALAVRAS")
    boxes = [(20, 90, 500, 385), (524, 90, 1004, 385), (20, 405, 500, 700), (524, 405, 1004, 700), (20, 720, 1004, 1516)]
    for b in boxes:
        panel(draw, b)
        classroom(draw, b)
    bia(draw, 150, 300, .72, "hold"); book(draw, (205, 270, 360, 335))
    draw.text((245, 175), "O mosquito mergulhou.", font=F_SMALL_B, fill=BLACK, anchor="mm")
    draw.text((252, 212), "O mosquito mordeu o nariz do leão.", font=F_SMALL_B, fill=BLACK, anchor="mm")
    speech(draw, (35, 100, 360, 165), "Como eu junto essas duas frases sem ficar estranho?", small=True)
    draw.text((700, 170), "TCHIN!", font=F_TITLE, fill=GOLD, stroke_width=2, stroke_fill=GOLD_DARK, anchor="mm")
    elo(draw, 760, 260, 1.15, glow=True)
    speech(draw, (545, 92, 984, 168), "Oi! Sou o Elo! Eu ligo palavras e frases — sou uma [[conjunção]]!", small=True)
    elo(draw, 135, 560, 1.15)
    draw.text((315, 548), "O mosquito mergulhou.", font=F_SMALL_B, fill=BLACK, anchor="mm")
    draw.text((315, 590), "O mosquito mordeu o nariz do leão.", font=F_SMALL_B, fill=BLACK, anchor="mm")
    speech(draw, (52, 420, 480, 505), "As [[conjunções]] organizam o texto e constroem o sentido! Cada uma cria uma relação diferente entre as ideias.", small=True)
    draw.text((725, 492), "O mosquito mergulhou", font=F_SMALL_B, fill=BLACK, anchor="mm")
    label(draw, (723, 520), "e", 36)
    draw.text((755, 568), "mordeu o nariz do leão.", font=F_SMALL_B, fill=BLACK, anchor="mm")
    elo(draw, 625, 600, 1.0, glow=True)
    speech(draw, (625, 420, 980, 500), "Aqui a conjunção [[e]] faz a [[soma de ações]]!", small=True)
    caption(draw, (40, 745, 665, 855), "As conjunções ligam palavras ou frases e estabelecem relações como adição, oposição, tempo, causa, condição, finalidade, comparação, entre outras.")
    bia(draw, 760, 1220, 1.45, "hold"); elo(draw, 665, 1045, .75, "wink")
    speech(draw, (48, 930, 540, 1025), "Que legal! Então tem várias conjunções diferentes?")
    speech(draw, (570, 875, 965, 945), "E cada uma tem sua função!", small=True)
    return img


def page2():
    img, draw = page_base("PÁGINA 2 — MAS, PORÉM, CONTUDO… TODOS BRIGAM!")
    boxes = [(20, 90, 500, 535), (524, 90, 1004, 535), (20, 555, 500, 920), (524, 555, 1004, 920), (20, 940, 500, 1516), (524, 940, 1004, 1516)]
    for i, b in enumerate(boxes):
        panel(draw, b)
        savanna(draw, b) if i == 1 else classroom(draw, b)
    bia(draw, 145, 390, .85, "point"); elo(draw, 325, 365, .75)
    speech(draw, (42, 110, 470, 225), "Elo, e essa aqui? 'O leão queria acertar o mosquito, [[mas]] arranhou o próprio focinho!'", small=True)
    draw.ellipse((650, 260, 850, 450), fill="#F97316", outline=BLACK, width=3)
    draw.ellipse((685, 295, 815, 430), fill="#FBBF24", outline=BLACK, width=3)
    draw.ellipse((714, 330, 735, 350), fill=WHITE, outline=BLACK); draw.ellipse((770, 330, 791, 350), fill=WHITE, outline=BLACK)
    draw.arc((720, 360, 790, 410), 0, 180, fill=BLACK, width=3)
    draw.line((790, 315, 870, 250), fill="#FBBF24", width=22)
    draw.ellipse((858, 238, 905, 278), fill="#FBBF24", outline=BLACK, width=2)
    draw.ellipse((865, 190, 880, 205), fill=BLACK); draw.line((872, 196, 900, 175), fill=BLACK, width=2)
    draw.text((610, 160), "PÁ!", font=F_TITLE, fill="#EF4444", stroke_width=2, stroke_fill=GOLD, anchor="mm")
    caption(draw, (545, 440, 980, 515), "O leão quis acertar o mosquito, [[mas]] arranhou o próprio focinho.")
    elo(draw, 125, 755, 1.0)
    label(draw, (260, 640), "mas", 42); draw.text((250, 715), "✊  ✊", font=F_TITLE, fill=GOLD, anchor="mm")
    speech(draw, (38, 575, 470, 675), "A conjunção [[mas]] cria uma relação de [[oposição]]! Uma ideia contraria a outra!", small=True)
    bia(draw, 700, 820, .72, "point")
    speech(draw, (545, 575, 965, 670), "Mas tem outras palavras que fazem a mesma coisa que 'mas'?", small=True)
    elo(draw, 95, 1195, .85, glow=True)
    cards = ["mas", "porém", "entretanto", "contudo"]
    for n, c in enumerate(cards):
        x = 150 + n * 82
        rounded(draw, (x, 1010, x + 78, 1065), WHITE, outline=PURPLE, width=3)
        label(draw, (x + 8, 1020), c, 18)
        if n < 3:
            draw.text((x + 86, 1025), "=", font=F_SMALL_B, fill=GOLD_DARK)
    speech(draw, (45, 1090, 480, 1215), "Todas essas são conjunções de [[oposição]]! Podem substituir uma pela outra sem mudar o sentido!", small=True)
    bia(draw, 635, 1365, .75, "hold"); elo(draw, 910, 1355, .62)
    book(draw, (650, 1120, 925, 1320), "#FDF2F8")
    draw_rich(draw, (668, 1145), "O leão atacou, [[mas]] errou.\nO leão atacou, [[porém]] errou.\nO leão atacou, [[contudo]] errou.", 240, F_SMALL, F_SMALL_B)
    caption(draw, (545, 955, 980, 1070), "'Mas', 'porém', 'entretanto' e 'contudo' são intercambiáveis: todas indicam [[oposição]].")
    return img


def page3():
    img, draw = page_base("PÁGINA 3 — ENQUANTO, SE, POIS, PARA…")
    boxes = [(20, 90, 500, 430), (524, 90, 1004, 430), (20, 450, 500, 875), (524, 450, 1004, 875), (20, 895, 1004, 1516)]
    for b in boxes:
        panel(draw, b); playground(draw, b)
    bia(draw, 155, 370, .70, "hold"); elo(draw, 235, 245, .52)
    book(draw, (185, 305, 285, 355), "#FACC15")
    draw.ellipse((335, 130, 390, 185), outline=BLACK, width=3); draw.line((362, 158, 362, 135), fill=BLACK, width=3); draw.line((362, 158, 382, 158), fill=BLACK, width=3)
    speech(draw, (38, 105, 270, 175), "Eu leio [[enquanto]] como a maçã!", small=True)
    speech(draw, (250, 205, 480, 325), "'[[Enquanto]]' é uma conjunção de [[tempo]]! Duas ações acontecendo ao mesmo tempo!", small=True)
    bia(draw, 660, 370, .68, "hold"); elo(draw, 890, 300, .55)
    draw.ellipse((690, 135, 800, 170), fill=WHITE, outline=LILAC, width=2)
    speech(draw, (545, 105, 790, 175), "[[Se]] chover, eu abro o guarda-chuva!", small=True)
    speech(draw, (730, 200, 985, 325), "'[[Se]]' cria uma [[condição]]! Uma coisa só acontece se a outra acontecer!", small=True)
    draw.rectangle((675, 268, 735, 278), fill=PURPLE); draw.arc((645, 232, 765, 292), 180, 360, fill=PURPLE, width=8)
    bia(draw, 120, 805, .65, "point"); elo(draw, 220, 665, .55)
    # Prepo cameo only here
    draw.ellipse((335, 620, 430, 735), fill=PURPLE, outline=BLACK, width=3)
    draw.ellipse((352, 646, 378, 672), fill=WHITE, outline=BLACK); draw.ellipse((390, 646, 416, 672), fill=WHITE, outline=BLACK)
    draw.arc((360, 680, 405, 710), 0, 180, fill=BLACK, width=3)
    draw.rectangle((360, 705, 405, 730), fill="#EDE9FE", outline=BLACK, width=2)
    draw.line((335, 680, 300, 720), fill="#9CA3AF", width=7); draw.line((430, 675, 465, 705), fill="#9CA3AF", width=7)
    draw.line((383, 620, 383, 590), fill="#9CA3AF", width=4); draw.ellipse((374, 575, 392, 593), fill=LILAC, outline=BLACK)
    draw.rectangle((445, 700, 480, 755), fill="#93C5FD", outline=BLACK, width=2)
    speech(draw, (38, 470, 350, 535), "Olha o Prepo regando as plantas!", small=True)
    speech(draw, (55, 545, 485, 635), "Ele está regando [[pois]] as plantas estão com sede! '[[Pois]]' é conjunção de [[explicação]] — mostra o motivo!", small=True)
    bia(draw, 645, 815, .72, "hold"); elo(draw, 875, 700, .70, glow=True)
    book(draw, (630, 655, 745, 720), "#FDE68A")
    speech(draw, (545, 470, 835, 555), "Eu trouxe o caderno [[para]] anotar todas as conjunções!", small=True)
    speech(draw, (690, 575, 985, 670), "Perfeito! '[[Para]]' indica [[finalidade]] — mostra o objetivo da ação!", small=True)
    cards = [("enquanto", "tempo"), ("se", "condição"), ("pois", "explicação"), ("para", "finalidade")]
    for i, (a, b) in enumerate(cards):
        x = 65 + i * 235
        rounded(draw, (x, 955, x + 190, 1095), GOLD_LIGHT, outline=GOLD_DARK, width=3)
        label(draw, (x + 18, 985), a, 24)
        draw.text((x + 86, 1035), "→", font=F_TITLE, fill=BLACK, anchor="mm")
        draw.text((x + 95, 1060), b, font=F_SMALL_B, fill=BLACK, anchor="mm")
    bia(draw, 390, 1370, .85, "point"); elo(draw, 580, 1295, .80)
    caption(draw, (50, 1120, 965, 1190), "Cada conjunção estabelece uma relação diferente entre as ideias do texto.")
    return img


def page4():
    img, draw = page_base("PÁGINA 4 — OU EU ESCOLHO, OU EU COMPARO!")
    boxes = [(20, 90, 500, 535), (524, 90, 1004, 535), (20, 555, 500, 920), (524, 555, 1004, 920), (20, 940, 500, 1230), (20, 1250, 1004, 1516)]
    for b in boxes:
        panel(draw, b); classroom(draw, b)
    bia(draw, 180, 430, .75, "hold"); elo(draw, 355, 330, .55)
    draw.ellipse((115, 260, 165, 330), fill="#7C2D12", outline=BLACK, width=2); draw.polygon([(120, 330), (160, 330), (140, 390)], fill="#F59E0B", outline=BLACK)
    draw.ellipse((225, 260, 275, 330), fill="#F9A8D4", outline=BLACK, width=2); draw.polygon([(230, 330), (270, 330), (250, 390)], fill="#F59E0B", outline=BLACK)
    speech(draw, (40, 110, 285, 185), "Vou de chocolate [[ou]] de morango?", small=True)
    speech(draw, (225, 190, 488, 325), "'[[Ou]]' é conjunção de [[alternância]]! Você escolhe entre uma coisa OU outra!", small=True)
    elo(draw, 625, 340, .70)
    book(draw, (690, 210, 965, 360), "#FDF2F8")
    draw_rich(draw, (705, 240), "O medo pode ter relação com a realidade… [[ou]] não!", 240, F_SMALL, F_SMALL_B)
    speech(draw, (545, 105, 945, 185), "Olha esse exemplo! '[[Ou]]' mostra duas possibilidades!", small=True)
    bia(draw, 150, 835, .68, "hold"); elo(draw, 405, 760, .55)
    book(draw, (82, 640, 150, 700), "#60A5FA"); book(draw, (205, 670, 255, 710), "#A78BFA")
    speech(draw, (38, 575, 350, 650), "Esse livro é grande [[como]] uma pizza!", small=True)
    speech(draw, (230, 665, 480, 790), "'[[Como]]' é conjunção de [[comparação]]! Compara uma coisa com outra!", small=True)
    draw.rectangle((550, 590, 980, 870), fill="#F8FAFC", outline=BLACK, width=3)
    draw.ellipse((700, 610, 840, 670), fill=PURPLE, outline=BLACK, width=2)
    draw.text((770, 640), "CONJUNÇÕES", font=F_SMALL_B, fill=WHITE, anchor="mm")
    items = [("adição / soma — e", 610, 700), ("oposição — mas/porém", 780, 700), ("tempo — enquanto", 600, 765), ("condição — se", 805, 765), ("explicação — pois", 605, 830), ("finalidade — para", 810, 830), ("alternância — ou", 660, 880), ("comparação — como", 850, 880)]
    for t, x, y in items:
        draw.line((770, 670, x + 45, y), fill=LILAC, width=3)
        rounded(draw, (x, y - 20, x + 145, y + 20), "#EDE9FE", outline=PURPLE, width=2, radius=10)
        draw.text((x + 72, y), t, font=F_BOARD, fill=BLACK, anchor="mm")
    bia(draw, 560, 1110, .52); elo(draw, 440, 1085, .60)
    speech(draw, (45, 960, 470, 1040), "Agora você sabe: as [[conjunções]] organizam o texto e criam sentidos!", small=True)
    speech(draw, (230, 1135, 490, 1205), "Cada elo, uma ideia diferente!", small=True)
    bia(draw, 250, 1450, .58); elo(draw, 470, 1390, .68, "wink")
    for i, word in enumerate(["e", "mas", "porém", "enquanto", "se", "pois", "para", "ou", "como"]):
        x = 560 + (i % 3) * 115
        y = 1300 + (i // 3) * 60
        label(draw, (x, y), word, 24)
    caption(draw, (420, 1388, 990, 1510), "As conjunções ligam palavras ou frases e estabelecem relações como adição, oposição, tempo, causa, condição, finalidade, comparação, entre outras.")
    speech(draw, (660, 1258, 930, 1325), "Até a próxima!", small=True)
    return img


def save(img: Image.Image, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
    if img.size != (1024, 1536):
        raise RuntimeError(f"Invalid size for {path}: {img.size}")


def main():
    save(page1(), OUT_DIR / "hq-conjuncoes-pg1.png")
    save(page2(), OUT_DIR / "hq-conjuncoes-pg2.png")
    save(page3(), OUT_DIR / "hq-conjuncoes-pg3.png")
    save(page4(), OUT_DIR / "hq-conjuncoes-pg4.png")
    for p in [
        ROOT / "Personagens" / "5o ano" / "Elo.png",
        OUT_DIR / "hq-conjuncoes-pg1.png",
        OUT_DIR / "hq-conjuncoes-pg2.png",
        OUT_DIR / "hq-conjuncoes-pg3.png",
        OUT_DIR / "hq-conjuncoes-pg4.png",
    ]:
        with Image.open(p) as im:
            print(f"{p}|{im.size[0]}x{im.size[1]}|{os.path.getsize(p)}")


if __name__ == "__main__":
    main()
