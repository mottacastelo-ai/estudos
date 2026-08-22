from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math


ROOT = Path(r"C:\Users\wizar\OneDrive\Documentos\Projeto Estudos")
OUT_DIR = ROOT / "estudos" / "portugues" / "acentuacao-paroxitonas-proparoxitonas"

W, H = 1024, 1536
PURPLE = "#7C3AED"
LILAC = "#A78BFA"
BG = "#F3F0FF"
GOLD = "#F59E0B"
DARK_GOLD = "#D97706"
BLACK = "#111111"
WHITE = "#FFFFFF"
RED = "#DC2626"
NAVY = "#0B2F6B"
BLUE = "#1D4ED8"
SKIN = "#D99048"
HAIR = "#101010"


def font(size, bold=False):
    for name in ("arialbd.ttf" if bold else "arial.ttf",
                 "calibrib.ttf" if bold else "calibri.ttf",
                 "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def size(draw, text, ft):
    b = draw.textbbox((0, 0), text, font=ft)
    return b[2] - b[0], b[3] - b[1]


def wrap(draw, text, ft, width):
    lines, line = [], ""
    for word in text.split():
        trial = word if not line else line + " " + word
        if size(draw, trial, ft)[0] <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def title(draw, text):
    draw.rectangle((0, 0, W, 76), fill=PURPLE)
    ft = font(29, True)
    tw, th = size(draw, text, ft)
    draw.text(((W - tw) / 2, 20), text, font=ft, fill=WHITE)


def panel(draw, box):
    draw.rounded_rectangle(box, radius=8, fill=BG, outline=BLACK, width=3)
    classroom(draw, box)


def classroom(draw, box):
    x1, y1, x2, y2 = box
    draw.rectangle((x1 + 3, y1 + 3, x2 - 3, y2 - 3), fill=BG)
    draw.rectangle((x1 + 30, y1 + 24, x2 - 30, y1 + 92), fill="#DBEAFE", outline=BLACK, width=2)
    draw.line((x1 + 30, y1 + 58, x2 - 30, y1 + 58), fill="#93C5FD", width=2)
    draw.line(((x1 + x2) // 2, y1 + 24, (x1 + x2) // 2, y1 + 92), fill="#93C5FD", width=2)
    draw.rounded_rectangle((x1 + 82, y1 + 80, x2 - 82, y2 - 54), radius=10, fill=WHITE, outline=PURPLE, width=4)
    draw.rectangle((x1 + 4, y2 - 55, x2 - 4, y2 - 4), fill="#DDD6FE")
    for x in (x1 + 90, x1 + 360, x1 + 680):
        draw.rounded_rectangle((x, y2 - 43, x + 145, y2 - 18), radius=7, fill="#C084FC", outline=BLACK, width=2)
        draw.line((x + 25, y2 - 18, x + 15, y2 - 4), fill=BLACK, width=2)
        draw.line((x + 118, y2 - 18, x + 130, y2 - 4), fill=BLACK, width=2)
    draw.rectangle((x2 - 128, y1 + 104, x2 - 82, y1 + 154), fill="#60A5FA", outline=BLACK, width=2)
    draw.rectangle((x2 - 118, y1 + 114, x2 - 92, y1 + 144), fill="#FDE68A", outline=BLACK, width=1)


def bubble(draw, box, speaker, text, tail=None, fs=18):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=22, fill=WHITE, outline=BLACK, width=2)
    if tail:
        tx, ty = tail
        if tx < (x1 + x2) / 2:
            pts = [(x1 + 42, y2 - 8), (x1 + 82, y2 - 8), tail]
        else:
            pts = [(x2 - 42, y2 - 8), (x2 - 82, y2 - 8), tail]
        draw.polygon(pts, fill=WHITE, outline=BLACK)
    f = font(fs)
    fb = font(fs, True)
    x = x1 + 15
    y = y1 + 10
    if speaker:
        label = speaker + ": "
        draw.text((x, y), label, font=fb, fill=PURPLE)
        x += size(draw, label, fb)[0]
    first_x = x
    lines = wrap(draw, text, f, x2 - first_x - 15)
    if lines and len(lines) > 1:
        rest = wrap(draw, " ".join(text.split()[len(lines[0].split()):]), f, x2 - x1 - 30)
        lines = [lines[0]] + rest
    for i, line in enumerate(lines):
        draw.text((first_x if i == 0 else x1 + 15, y), line, font=f, fill=BLACK)
        y += fs + 7


def board_text(draw, xy, parts, fs=30):
    x, y = xy
    for text, color, bold in parts:
        ft = font(fs, bold)
        draw.text((x, y), text, font=ft, fill=color)
        x += size(draw, text, ft)[0]


def flash(draw, cx, cy, r=45):
    pts = []
    for i in range(18):
        a = math.radians(i * 20)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    draw.polygon(pts, fill="#FDE68A", outline=GOLD)


def acentin(draw, cx, cy, s=1.0, mood="happy", arms="up", cape=False):
    if cape:
        draw.polygon([(cx - 15*s, cy - 10*s), (cx - 86*s, cy + 70*s), (cx - 4*s, cy + 78*s)], fill="#FBBF24", outline=BLACK)
    body = [(cx - 28*s, cy + 55*s), (cx + 6*s, cy - 72*s), (cx + 44*s, cy - 62*s), (cx + 5*s, cy + 72*s)]
    draw.polygon(body, fill=GOLD, outline=BLACK)
    draw.line(body + [body[0]], fill=BLACK, width=max(2, int(3*s)))
    hat = [(cx + 10*s, cy - 98*s), (cx + 68*s, cy - 126*s), (cx + 78*s, cy - 108*s), (cx + 18*s, cy - 82*s)]
    draw.polygon(hat, fill=DARK_GOLD, outline=BLACK)
    for ex in (-11, 19):
        draw.ellipse((cx + ex*s - 10*s, cy - 35*s, cx + ex*s + 10*s, cy - 10*s), fill=WHITE, outline=BLACK, width=2)
        draw.ellipse((cx + ex*s - 3*s, cy - 27*s, cx + ex*s + 5*s, cy - 15*s), fill=BLACK)
    if mood == "surprised":
        draw.ellipse((cx - 2*s, cy + 8*s, cx + 14*s, cy + 26*s), fill=BLACK)
    elif mood == "serious":
        draw.arc((cx - 3*s, cy + 10*s, cx + 26*s, cy + 34*s), 200, 340, fill=BLACK, width=max(2, int(2*s)))
    else:
        draw.arc((cx - 13*s, cy + 3*s, cx + 31*s, cy + 36*s), 10, 165, fill=BLACK, width=max(2, int(3*s)))
    if arms == "point":
        arms_xy = [(cx - 22*s, cy + 5*s, cx - 74*s, cy + 10*s), (cx + 34*s, cy + 0*s, cx + 92*s, cy - 15*s)]
    elif arms == "open":
        arms_xy = [(cx - 22*s, cy + 0*s, cx - 78*s, cy - 22*s), (cx + 33*s, cy + 0*s, cx + 88*s, cy - 22*s)]
    else:
        arms_xy = [(cx - 22*s, cy + 2*s, cx - 66*s, cy - 38*s), (cx + 33*s, cy + 2*s, cx + 74*s, cy - 38*s)]
    for ax1, ay1, ax2, ay2 in arms_xy:
        draw.line((ax1, ay1, ax2, ay2), fill=BLACK, width=max(2, int(4*s)))
        draw.ellipse((ax2 - 5*s, ay2 - 5*s, ax2 + 5*s, ay2 + 5*s), fill=BLACK)
    for lx in (-13, 21):
        draw.line((cx + lx*s, cy + 66*s, cx + (lx - 5)*s, cy + 104*s), fill=BLACK, width=max(2, int(4*s)))
        draw.ellipse((cx + (lx - 20)*s, cy + 100*s, cx + (lx + 12)*s, cy + 114*s), fill=WHITE, outline=BLACK, width=2)


def bia(draw, cx, cy, s=1.0, book=False, point=False):
    for a in range(0, 360, 18):
        hx = cx + math.cos(math.radians(a)) * 38*s
        hy = cy - 83*s + math.sin(math.radians(a)) * 30*s
        draw.ellipse((hx - 18*s, hy - 18*s, hx + 18*s, hy + 18*s), fill=HAIR, outline=BLACK)
    draw.ellipse((cx - 34*s, cy - 113*s, cx + 34*s, cy - 42*s), fill=SKIN, outline=BLACK, width=2)
    for ex in (-13, 13):
        draw.ellipse((cx + ex*s - 7*s, cy - 90*s, cx + ex*s + 7*s, cy - 74*s), fill=WHITE, outline=BLACK)
        draw.ellipse((cx + ex*s - 2*s, cy - 85*s, cx + ex*s + 3*s, cy - 77*s), fill=BLACK)
    draw.arc((cx - 13*s, cy - 73*s, cx + 17*s, cy - 51*s), 10, 170, fill=BLACK, width=2)
    draw.polygon([(cx - 44*s, cy - 35*s), (cx + 44*s, cy - 35*s), (cx + 34*s, cy + 44*s), (cx - 34*s, cy + 44*s)], fill=BLUE, outline=BLACK)
    draw.polygon([(cx - 23*s, cy - 35*s), (cx, cy - 11*s), (cx + 23*s, cy - 35*s)], fill=WHITE, outline=BLACK)
    draw.polygon([(cx - 47*s, cy + 44*s), (cx + 47*s, cy + 44*s), (cx + 32*s, cy + 91*s), (cx - 32*s, cy + 91*s)], fill=NAVY, outline=BLACK)
    if point:
        draw.line((cx + 40*s, cy - 18*s, cx + 84*s, cy - 55*s), fill=SKIN, width=max(3, int(7*s)))
        draw.ellipse((cx + 78*s, cy - 62*s, cx + 92*s, cy - 48*s), fill=SKIN, outline=BLACK)
        draw.line((cx - 40*s, cy - 18*s, cx - 70*s, cy + 14*s), fill=SKIN, width=max(3, int(7*s)))
    else:
        draw.line((cx - 42*s, cy - 18*s, cx - 75*s, cy + 18*s), fill=SKIN, width=max(3, int(7*s)))
        draw.line((cx + 42*s, cy - 18*s, cx + 75*s, cy + 18*s), fill=SKIN, width=max(3, int(7*s)))
    if book:
        draw.rounded_rectangle((cx - 45*s, cy - 12*s, cx + 45*s, cy + 48*s), radius=5, fill="#EF4444", outline=BLACK, width=2)
        draw.line((cx, cy - 12*s, cx, cy + 48*s), fill=WHITE, width=2)
    for lx in (-18, 18):
        draw.line((cx + lx*s, cy + 91*s, cx + lx*s, cy + 133*s), fill=SKIN, width=max(3, int(8*s)))
        draw.ellipse((cx + lx*s - 20*s, cy + 127*s, cx + lx*s + 22*s, cy + 144*s), fill=WHITE, outline=BLACK, width=2)


def prepo(draw, cx, cy, s=1.0, point=False):
    draw.rounded_rectangle((cx - 48*s, cy - 62*s, cx + 48*s, cy + 54*s), radius=int(28*s), fill=PURPLE, outline=BLACK, width=3)
    for ex in (-19, 19):
        draw.ellipse((cx + ex*s - 15*s, cy - 42*s, cx + ex*s + 15*s, cy - 12*s), fill=WHITE, outline=BLACK, width=2)
        draw.ellipse((cx + ex*s - 5*s, cy - 33*s, cx + ex*s + 5*s, cy - 18*s), fill=BLACK)
    draw.arc((cx - 17*s, cy - 17*s, cx + 24*s, cy + 18*s), 15, 160, fill=BLACK, width=3)
    draw.line((cx - 25*s, cy - 62*s, cx - 35*s, cy - 97*s), fill=BLACK, width=3)
    draw.line((cx + 25*s, cy - 62*s, cx + 35*s, cy - 97*s), fill=BLACK, width=3)
    draw.text((cx - 52*s, cy - 122*s), "D", font=font(max(14, int(27*s)), True), fill=PURPLE, stroke_width=2, stroke_fill=BLACK)
    draw.text((cx + 28*s, cy - 122*s), "E", font=font(max(14, int(27*s)), True), fill=PURPLE, stroke_width=2, stroke_fill=BLACK)
    draw.rounded_rectangle((cx - 42*s, cy + 8*s, cx + 42*s, cy + 38*s), radius=int(7*s), fill=WHITE, outline=BLACK, width=2)
    draw.text((cx - 28*s, cy + 11*s), "PREPO", font=font(max(12, int(15*s)), True), fill=BLACK)
    left = (cx - 86*s, cy - 34*s) if point else (cx - 84*s, cy - 22*s)
    draw.line((cx - 48*s, cy - 4*s, *left), fill=PURPLE, width=max(4, int(7*s)))
    draw.line((cx + 48*s, cy - 4*s, cx + 84*s, cy - 22*s), fill=PURPLE, width=max(4, int(7*s)))
    for lx in (-27, 27):
        draw.line((cx + lx*s, cy + 54*s, cx + lx*s, cy + 84*s), fill=PURPLE, width=max(4, int(7*s)))
        draw.ellipse((cx + lx*s - 19*s, cy + 78*s, cx + lx*s + 19*s, cy + 94*s), fill=PURPLE, outline=BLACK, width=2)


def page_base(text):
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    title(d, text)
    return im, d


def page1():
    im, d = page_base("TODA PALAVRA TEM UMA SÍLABA MAIS FORTE!")
    boxes = [(30, 96, 994, 430), (30, 455, 994, 700), (30, 725, 994, 970), (30, 995, 994, 1238), (30, 1262, 994, 1506)]
    for b in boxes:
        panel(d, b)
    d.rounded_rectangle((300, 296, 720, 386), radius=9, fill="#C4B5FD", outline=BLACK, width=2)
    d.rectangle((385, 248, 650, 315), fill="#2563EB", outline=BLACK, width=2)
    bia(d, 245, 326, .72)
    flash(d, 565, 256, 52)
    acentin(d, 565, 270, .63)
    bubble(d, (55, 116, 324, 178), "Bia", "Ei! Quem é você?!", (245, 230), 18)
    bubble(d, (615, 116, 965, 212), "Acentin", "Oi, Bia! Sou o Acentin! Vim te contar um segredo!", (575, 238), 17)
    board_text(d, (418, 512), [("AMIGO", BLACK, True)], 42)
    acentin(d, 162, 587, .58, "serious", "point")
    bia(d, 850, 625, .45)
    bubble(d, (255, 592, 948, 682), "Acentin", "Toda palavra tem uma sílaba mais forte. Ela se chama SÍLABA TÔNICA!", (180, 595), 18)
    board_text(d, (285, 780), [("A-", BLACK, False), ("MI", GOLD, True), ("-GO", BLACK, False)], 42)
    d.text((373, 746), "´", font=font(42, True), fill=GOLD)
    acentin(d, 386, 850, .52)
    bia(d, 835, 892, .46)
    bubble(d, (58, 852, 510, 952), "Acentin", "Em 'amigo', a sílaba forte é MI. Fala: a-MI-go!", (385, 883), 16)
    bubble(d, (535, 840, 962, 940), "Bia", "a-MI-go! Sai mais forte mesmo!", (832, 900), 17)
    board_text(d, (330, 1048), [("MÉ", GOLD, True), ("-DI-CO", BLACK, False)], 42)
    d.text((343, 1014), "´", font=font(42, True), fill=GOLD)
    bia(d, 136, 1170, .55, point=True)
    acentin(d, 850, 1163, .50)
    bubble(d, (205, 1132, 615, 1216), "Bia", "E em 'médico'? MÉ-di-co! O MÉ é mais forte!", (158, 1142), 16)
    bubble(d, (620, 1128, 965, 1228), "Acentin", "Isso! Mas nem toda sílaba tônica leva acento escrito!", (848, 1162), 16)
    acentin(d, 205, 1392, .78, "serious", "point")
    bia(d, 835, 1422, .56, book=True)
    bubble(d, (275, 1294, 835, 1385), "Acentin", "Nas próximas páginas eu ensino QUANDO usar o acento!", (225, 1360), 18)
    bubble(d, (520, 1400, 936, 1484), "Bia", "Já quero saber!", (835, 1438), 18)
    save(im, "hq-acentuacao-paroxitonas-proparoxitonas-pg1.png")


def page2():
    im, d = page_base("PAROXÍTONAS: A PENÚLTIMA SÍLABA É A MAIS FORTE")
    boxes = [(30, 96, 994, 418), (30, 442, 994, 682), (30, 706, 994, 968), (30, 992, 994, 1236), (30, 1260, 994, 1506)]
    for b in boxes:
        panel(d, b)
    board_text(d, (380, 155), [("A-", BLACK, False), ("MI", GOLD, True), ("-GO", BLACK, False)], 44)
    acentin(d, 190, 260, .76, "serious", "point")
    bia(d, 825, 312, .55)
    bubble(d, (245, 238, 715, 350), "Acentin", "Quando a sílaba tônica é a PENÚLTIMA, a palavra é PAROXÍTONA.", (205, 264), 17)
    bubble(d, (705, 118, 960, 188), "Bia", "Paroxítona? Que nome comprido!", (832, 250), 17)
    board_text(d, (170, 505), [("ME", GOLD, True), ("-sa   ", BLACK, False), ("QUEN", GOLD, True), ("-te   ", BLACK, False), ("a-", BLACK, False), ("MI", GOLD, True), ("-go", BLACK, False)], 34)
    acentin(d, 110, 575, .53, "happy", "point")
    bia(d, 862, 614, .48, book=True)
    bubble(d, (150, 572, 575, 660), "Acentin", "ME-sa, QUEN-te, a-MI-go. Todas paroxítonas!", (130, 575), 16)
    bubble(d, (595, 570, 955, 655), "Bia", "Mas nenhuma tem acento escrito!", (862, 612), 16)
    acentin(d, 150, 842, .62, "serious", "point")
    bia(d, 860, 898, .42, book=True)
    d.text((285, 735), "PAROXÍTONAS ACENTUADAS TERMINAM EM:", font=font(22, True), fill=PURPLE)
    d.text((270, 795), "L, R, N, X, PS, Ã, ÃS, ÃO, UM, UNS,", font=font(22, True), fill=PURPLE)
    d.text((270, 835), "I, IS, US ou DITONGO", font=font(22, True), fill=PURPLE)
    bubble(d, (56, 870, 404, 952), "Acentin", "A regra é: só levam acento quando terminam em:", (155, 846), 14)
    examples = [("NÍ-vel", "L"), ("BÔ-nus", "US"), ("re-VÓL-ver", "R"), ("JÚ-ri", "I"), ("TÓ-rax", "X")]
    x, y = 100, 1025
    for word, end in examples:
        d.text((x, y), word, font=font(28, True), fill=GOLD)
        d.text((x + size(d, word, font(28, True))[0] + 8, y + 4), "(" + end + ")", font=font(22, True), fill=RED)
        x += 180
    acentin(d, 835, 1136, .55, "happy", "point")
    bubble(d, (70, 1138, 548, 1225), "Acentin", "Nível (L), bônus (US), revólver (R)... por isso levam acento!", (820, 1140), 15)
    bubble(d, (570, 1140, 955, 1222), "Bia", "É a terminação que manda!", (852, 1160), 17)
    acentin(d, 130, 1390, .60)
    bia(d, 850, 1420, .55)
    bubble(d, (215, 1290, 945, 1385), "Acentin", "Paroxítona sem essa terminação? Sem acento! Igual 'amigo' e 'mesa'.", (145, 1370), 16)
    bubble(d, (300, 1400, 890, 1486), "Bia", "Agora só falta as proparoxítonas!", (850, 1430), 18)
    save(im, "hq-acentuacao-paroxitonas-proparoxitonas-pg2.png")


def page3():
    im, d = page_base("PROPAROXÍTONAS: TODAS LEVAM ACENTO!")
    boxes = [(30, 96, 994, 430), (30, 455, 994, 700), (30, 725, 994, 1015), (30, 1040, 994, 1255), (30, 1280, 994, 1506)]
    for b in boxes:
        panel(d, b)
    d.arc((870, 360, 938, 405), 180, 360, fill=BLACK, width=2)
    for x in range(880, 932, 12):
        d.ellipse((x, 374, x + 6, 380), fill=BLACK)
    board_text(d, (345, 150), [("MÉ", GOLD, True), ("-DI-CO", BLACK, False)], 48)
    d.text((360, 112), "´", font=font(42, True), fill=GOLD)
    acentin(d, 515, 270, .85, "happy", "open")
    bia(d, 145, 352, .45)
    bubble(d, (95, 330, 930, 410), "Acentin", "A sílaba tônica na ANTEPENÚLTIMA? A palavra é PROPAROXÍTONA!", (515, 330), 18)
    bia(d, 145, 620, .58)
    board_text(d, (420, 500), [("MÉ", GOLD, True), ("-di-co", BLACK, False)], 40)
    bubble(d, (240, 570, 820, 672), "Bia", "Contando do fim: co, di, MÉ. Terceira!", (160, 620), 17)
    acentin(d, 850, 620, .42)
    acentin(d, 510, 880, .95, "happy", "up", cape=True)
    d.rounded_rectangle((120, 750, 905, 835), radius=12, fill=PURPLE, outline=BLACK, width=3)
    d.text((150, 774), "TODAS as proparoxítonas levam acento. SEM EXCEÇÃO!", font=font(23, True), fill=WHITE)
    bubble(d, (245, 934, 785, 1000), "Acentin", "É a regra mais fácil do português!", (510, 920), 18)
    examples = ["TÊ-nis", "LÁ-gri-ma", "PÁS-sa-ro", "ÁR-vo-re", "MÉ-di-co", "HÍ-fen"]
    x, y = 125, 1076
    for word in examples:
        d.text((x, y), word, font=font(24, True), fill=GOLD)
        x += 245
        if x > 760:
            x = 115
            y += 42
    bia(d, 120, 1202, .45)
    acentin(d, 835, 1190, .45)
    bubble(d, (215, 1168, 725, 1244), "Bia", "Tênis, lágrima, pássaro, árvore, médico, hífen... TODAS com acento!", (125, 1185), 14)
    bubble(d, (735, 1168, 955, 1234), "Acentin", "Isso! Sem exceção!", (820, 1180), 15)
    prepo(d, 140, 1410, .55)
    bia(d, 720, 1435, .40)
    acentin(d, 880, 1420, .48)
    bubble(d, (235, 1308, 765, 1405), "Prepo", "Ei, Bia! Achei duas proparoxítonas no livro: 'médico' e 'álbum'!", (150, 1375), 15)
    bubble(d, (430, 1415, 945, 1490), "Acentin", "Proparoxítonas aparecem em todo lugar!", (880, 1425), 16)
    save(im, "hq-acentuacao-paroxitonas-proparoxitonas-pg3.png")


def page4():
    im, d = page_base("RESUMÃO DO ACENTIN")
    boxes = [(30, 96, 994, 400), (30, 425, 994, 735), (30, 760, 994, 1035), (30, 1060, 994, 1290), (30, 1315, 994, 1506)]
    for b in boxes:
        panel(d, b)
    d.line((512, 135, 512, 370), fill=BLACK, width=3)
    d.text((165, 135), "PAROXÍTONAS", font=font(27, True), fill=PURPLE)
    d.text((600, 135), "PROPAROXÍTONAS", font=font(25, True), fill=PURPLE)
    acentin(d, 512, 294, .60, "happy", "open")
    bia(d, 150, 336, .42)
    prepo(d, 875, 330, .38)
    bubble(d, (330, 305, 690, 382), "Acentin", "Vamos revisar tudo em uma tabela!", (512, 315), 17)
    d.text((86, 450), "PAROXÍTONA = penúltima sílaba tônica", font=font(22, True), fill=PURPLE)
    d.text((86, 505), "Sem acento: amigo, mesa, quente", font=font(20), fill=BLACK)
    d.text((86, 545), "Com acento: nível, revólver, vírus, júri", font=font(20), fill=BLACK)
    d.text((86, 585), "Terminações: L, R, US, I...", font=font(20), fill=BLACK)
    bia(d, 835, 665, .48, point=True)
    bubble(d, (100, 625, 745, 718), "Bia", "Paroxítona só leva acento se terminar naquelas letras!", (820, 650), 18)
    d.text((86, 785), "PROPAROXÍTONA = antepenúltima sílaba tônica", font=font(21, True), fill=PURPLE)
    d.text((86, 840), "TODAS levam acento (sem exceção!)", font=font(20, True), fill=BLACK)
    d.text((86, 882), "Ex: médico, lágrima, pássaro, árvore, hífen", font=font(20), fill=BLACK)
    prepo(d, 820, 955, .50, point=True)
    bubble(d, (95, 930, 700, 1018), "Prepo", "Proparoxítona sempre leva acento. Fácil!", (805, 950), 18)
    acentin(d, 155, 1198, .60, "serious", "point")
    d.ellipse((95, 1110, 150, 1165), outline=GOLD, width=5)
    d.line((142, 1158, 180, 1198), fill=GOLD, width=6)
    board_text(d, (365, 1108), [("A-", BLACK, False), ("ÇÚ", GOLD, True), ("-CAR", BLACK, False)], 42)
    d.text((426, 1070), "´", font=font(42, True), fill=GOLD)
    bubble(d, (230, 1148, 950, 1218), "Acentin", "Dica: ache a sílaba tônica. Depois conte do fim: última, penúltima, antepenúltima.", (160, 1195), 14)
    bubble(d, (230, 1222, 900, 1280), "Acentin", "Antepenúltima -> PROPAROXÍTONA -> sempre acento!", (160, 1210), 15)
    for i, word in enumerate(["médico", "amigo", "nível", "pássaro"]):
        d.text((90 + i * 205, 1328 + (i % 2) * 28), word, font=font(18, True), fill=GOLD if i % 2 == 0 else PURPLE)
    bia(d, 190, 1460, .32)
    acentin(d, 500, 1450, .43)
    prepo(d, 820, 1452, .30)
    bubble(d, (55, 1328, 360, 1388), "Acentin", "Agora você é um detetive das sílabas tônicas!", (500, 1432), 12)
    bubble(d, (365, 1328, 690, 1396), "Bia", "Obrigada, Acentin! Vou praticar em cada palavra!", (190, 1428), 12)
    bubble(d, (650, 1366, 965, 1428), "Prepo", "Bora praticar nas atividades!", (820, 1428), 15)
    save(im, "hq-acentuacao-paroxitonas-proparoxitonas-pg4.png")


def save(im, name):
    assert im.size == (1024, 1536), im.size
    path = OUT_DIR / name
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)
    with Image.open(path) as check:
        assert check.size == (1024, 1536), check.size
    print(f"{path}|1024x1536|{path.stat().st_size}")


if __name__ == "__main__":
    page1()
    page2()
    page3()
    page4()
