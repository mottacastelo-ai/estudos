from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap
import math


ROOT = Path(r"C:\Users\wizar\OneDrive\Documentos\Projeto Estudos")
OUT_DIR = ROOT / "estudos" / "portugues" / "acentuacao-paroxitonas-proparoxitonas"
CHAR_DIR = ROOT / "Personagens" / "5o ano"

PURPLE = "#7C3AED"
LILAC = "#A78BFA"
BG = "#F3F0FF"
GOLD = "#F59E0B"
DARK_GOLD = "#D97706"
BLACK = "#111111"
WHITE = "#FFFFFF"
RED = "#DC2626"
NAVY = "#0B3A78"
SKIN = "#D99048"
HAIR = "#101010"


def font(size, bold=False):
    names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


F = {s: font(s) for s in [14, 16, 18, 20, 22, 24, 26, 28, 30, 34, 40]}
FB = {s: font(s, True) for s in [14, 16, 18, 20, 22, 24, 26, 28, 30, 34, 40]}


def text_size(draw, txt, ft):
    box = draw.textbbox((0, 0), txt, font=ft)
    return box[2] - box[0], box[3] - box[1]


def wrap_lines(draw, text, ft, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = word if not line else f"{line} {word}"
        if text_size(draw, trial, ft)[0] <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def bubble(draw, box, text, tail=None, speaker=None, size=20):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=22, fill=WHITE, outline=BLACK, width=2)
    if tail:
        tx, ty = tail
        pts = [(x1 + 35, y2 - 8), (x1 + 78, y2 - 8), (tx, ty)]
        if tx > (x1 + x2) / 2:
            pts = [(x2 - 35, y2 - 8), (x2 - 78, y2 - 8), (tx, ty)]
        draw.polygon(pts, fill=WHITE, outline=BLACK)
    ft = font(size)
    fbold = font(size, True)
    y = y1 + 12
    if speaker:
        draw.text((x1 + 16, y), f"{speaker}: ", font=fbold, fill=PURPLE)
        prefix_w = text_size(draw, f"{speaker}: ", fbold)[0]
        first = True
        for ln in wrap_lines(draw, text, ft, x2 - x1 - 32 - (prefix_w if first else 0)):
            draw.text((x1 + 16 + (prefix_w if first else 0), y), ln, font=ft, fill=BLACK)
            y += size + 7
            first = False
    else:
        for ln in wrap_lines(draw, text, ft, x2 - x1 - 32):
            draw.text((x1 + 16, y), ln, font=ft, fill=BLACK)
            y += size + 7


def title(draw, text, width=1024):
    draw.rectangle((0, 0, width, 74), fill=PURPLE)
    tw, th = text_size(draw, text, FB[30])
    draw.text(((width - tw) / 2, 20), text, font=FB[30], fill=WHITE)


def panel(draw, box, fill=WHITE):
    draw.rounded_rectangle(box, radius=8, fill=fill, outline=BLACK, width=3)


def classroom(draw, box, board=False):
    x1, y1, x2, y2 = box
    draw.rectangle((x1 + 3, y1 + 3, x2 - 3, y2 - 3), fill=BG)
    draw.rectangle((x1 + 25, y1 + 25, x2 - 25, y1 + 82), fill="#DDEFFF", outline=BLACK, width=2)
    draw.line((x1 + 25, y1 + 54, x2 - 25, y1 + 54), fill=BLACK, width=1)
    draw.line(((x1 + x2) / 2, y1 + 25, (x1 + x2) / 2, y1 + 82), fill=BLACK, width=1)
    if board:
        draw.rounded_rectangle((x1 + 35, y1 + 45, x2 - 35, y2 - 45), radius=10, fill=WHITE, outline="#5B21B6", width=4)


def acentin(draw, cx, cy, scale=1.0, mood="happy", arms="up", cape=False):
    w, h = 50 * scale, 145 * scale
    pts = [
        (cx - w * 0.50, cy + h * 0.38),
        (cx + w * 0.05, cy - h * 0.50),
        (cx + w * 0.52, cy - h * 0.42),
        (cx - w * 0.05, cy + h * 0.50),
    ]
    if cape:
        draw.polygon([(cx - 18*scale, cy - 20*scale), (cx - 85*scale, cy + 65*scale), (cx - 10*scale, cy + 72*scale)], fill="#FBBF24", outline=BLACK)
    draw.polygon(pts, fill=GOLD, outline=BLACK)
    draw.line((pts[0], pts[1], pts[2], pts[3], pts[0]), fill=BLACK, width=max(2, int(3*scale)))
    hat = [(cx + 8*scale, cy - 84*scale), (cx + 62*scale, cy - 112*scale), (cx + 72*scale, cy - 94*scale), (cx + 16*scale, cy - 67*scale)]
    draw.polygon(hat, fill=DARK_GOLD, outline=BLACK)
    for ex in [-12, 18]:
        draw.ellipse((cx + ex*scale - 10*scale, cy - 28*scale, cx + ex*scale + 10*scale, cy - 5*scale), fill=WHITE, outline=BLACK, width=2)
        draw.ellipse((cx + ex*scale - 3*scale, cy - 21*scale, cx + ex*scale + 4*scale, cy - 9*scale), fill=BLACK)
    if mood == "surprised":
        draw.ellipse((cx - 3*scale, cy + 9*scale, cx + 13*scale, cy + 28*scale), fill=BLACK)
    elif mood == "serious":
        draw.arc((cx - 3*scale, cy + 10*scale, cx + 22*scale, cy + 35*scale), 200, 335, fill=BLACK, width=max(2, int(2*scale)))
        draw.line((cx - 24*scale, cy - 40*scale, cx - 3*scale, cy - 43*scale), fill=BLACK, width=2)
        draw.line((cx + 10*scale, cy - 45*scale, cx + 31*scale, cy - 38*scale), fill=BLACK, width=2)
    else:
        draw.arc((cx - 12*scale, cy + 3*scale, cx + 30*scale, cy + 35*scale), 10, 165, fill=BLACK, width=max(2, int(3*scale)))
    if arms == "up":
        arm_pts = [(cx - 26*scale, cy + 2*scale, cx - 66*scale, cy - 38*scale), (cx + 32*scale, cy + 5*scale, cx + 75*scale, cy - 36*scale)]
    elif arms == "point":
        arm_pts = [(cx - 25*scale, cy + 8*scale, cx - 70*scale, cy + 18*scale), (cx + 30*scale, cy + 0*scale, cx + 88*scale, cy - 12*scale)]
    else:
        arm_pts = [(cx - 27*scale, cy + 7*scale, cx - 72*scale, cy + 2*scale), (cx + 32*scale, cy + 6*scale, cx + 78*scale, cy + 13*scale)]
    for ax1, ay1, ax2, ay2 in arm_pts:
        draw.line((ax1, ay1, ax2, ay2), fill=BLACK, width=max(2, int(4*scale)))
        draw.ellipse((ax2 - 5*scale, ay2 - 5*scale, ax2 + 5*scale, ay2 + 5*scale), fill=BLACK)
    for lx in [-14, 20]:
        draw.line((cx + lx*scale, cy + 68*scale, cx + (lx-6)*scale, cy + 103*scale), fill=BLACK, width=max(2, int(4*scale)))
        draw.ellipse((cx + (lx-21)*scale, cy + 99*scale, cx + (lx+12)*scale, cy + 113*scale), fill=WHITE, outline=BLACK, width=2)


def bia(draw, cx, cy, scale=1.0, book=False, point=False):
    r = 40 * scale
    for a in range(0, 360, 22):
        hx = cx + math.cos(math.radians(a)) * r * 0.75
        hy = cy - 78*scale + math.sin(math.radians(a)) * r * 0.55
        draw.ellipse((hx-18*scale, hy-18*scale, hx+18*scale, hy+18*scale), fill=HAIR, outline=BLACK)
    draw.ellipse((cx - 34*scale, cy - 112*scale, cx + 34*scale, cy - 42*scale), fill=SKIN, outline=BLACK, width=2)
    for ex in [-13, 13]:
        draw.ellipse((cx+ex*scale-7*scale, cy-88*scale, cx+ex*scale+7*scale, cy-73*scale), fill=WHITE, outline=BLACK)
        draw.ellipse((cx+ex*scale-2*scale, cy-84*scale, cx+ex*scale+3*scale, cy-76*scale), fill=BLACK)
    draw.arc((cx - 12*scale, cy - 72*scale, cx + 16*scale, cy - 52*scale), 10, 170, fill=BLACK, width=2)
    draw.polygon([(cx - 42*scale, cy - 35*scale), (cx + 42*scale, cy - 35*scale), (cx + 35*scale, cy + 45*scale), (cx - 35*scale, cy + 45*scale)], fill=NAVY, outline=BLACK)
    draw.polygon([(cx - 22*scale, cy - 35*scale), (cx, cy - 12*scale), (cx + 22*scale, cy - 35*scale)], fill=WHITE, outline=BLACK)
    draw.polygon([(cx - 45*scale, cy + 45*scale), (cx + 45*scale, cy + 45*scale), (cx + 32*scale, cy + 88*scale), (cx - 32*scale, cy + 88*scale)], fill="#082F6C", outline=BLACK)
    if point:
        draw.line((cx + 38*scale, cy - 20*scale, cx + 80*scale, cy - 55*scale), fill=SKIN, width=max(3, int(8*scale)))
        draw.ellipse((cx + 75*scale, cy - 62*scale, cx + 90*scale, cy - 47*scale), fill=SKIN, outline=BLACK)
    else:
        draw.line((cx - 42*scale, cy - 18*scale, cx - 78*scale, cy + 20*scale), fill=SKIN, width=max(3, int(7*scale)))
        draw.line((cx + 42*scale, cy - 18*scale, cx + 78*scale, cy + 20*scale), fill=SKIN, width=max(3, int(7*scale)))
    if book:
        draw.rounded_rectangle((cx - 42*scale, cy - 15*scale, cx + 42*scale, cy + 42*scale), radius=5, fill="#2563EB", outline=BLACK, width=2)
        draw.line((cx, cy - 15*scale, cx, cy + 42*scale), fill=WHITE, width=2)
    for lx in [-18, 18]:
        draw.line((cx + lx*scale, cy + 88*scale, cx + lx*scale, cy + 132*scale), fill=SKIN, width=max(3, int(8*scale)))
        draw.ellipse((cx + lx*scale - 20*scale, cy + 126*scale, cx + lx*scale + 22*scale, cy + 143*scale), fill=WHITE, outline=BLACK, width=2)


def prepo(draw, cx, cy, scale=1.0, point=False):
    draw.rounded_rectangle((cx-50*scale, cy-65*scale, cx+50*scale, cy+55*scale), radius=int(30*scale), fill=PURPLE, outline=BLACK, width=3)
    draw.rounded_rectangle((cx-45*scale, cy+5*scale, cx+45*scale, cy+38*scale), radius=int(8*scale), fill=WHITE, outline=BLACK, width=2)
    draw.text((cx-30*scale, cy+9*scale), "PREPO", font=FB[int(18*scale) if scale >= 1 else 14], fill=BLACK)
    for ex in [-20, 20]:
        draw.ellipse((cx+ex*scale-16*scale, cy-44*scale, cx+ex*scale+16*scale, cy-12*scale), fill=WHITE, outline=BLACK, width=2)
        draw.ellipse((cx+ex*scale-5*scale, cy-34*scale, cx+ex*scale+6*scale, cy-18*scale), fill=BLACK)
    draw.arc((cx-18*scale, cy-16*scale, cx+25*scale, cy+18*scale), 15, 160, fill=BLACK, width=3)
    draw.line((cx-26*scale, cy-65*scale, cx-38*scale, cy-105*scale), fill=BLACK, width=3)
    draw.line((cx+26*scale, cy-65*scale, cx+38*scale, cy-105*scale), fill=BLACK, width=3)
    draw.text((cx-55*scale, cy-130*scale), "D", font=FB[28], fill=PURPLE, stroke_width=2, stroke_fill=BLACK)
    draw.text((cx+28*scale, cy-130*scale), "E", font=FB[28], fill=PURPLE, stroke_width=2, stroke_fill=BLACK)
    if point:
        draw.line((cx-48*scale, cy-5*scale, cx-88*scale, cy-35*scale), fill=PURPLE, width=max(4, int(8*scale)))
    else:
        draw.line((cx-48*scale, cy-5*scale, cx-88*scale, cy-25*scale), fill=PURPLE, width=max(4, int(8*scale)))
    draw.line((cx+48*scale, cy-5*scale, cx+88*scale, cy-25*scale), fill=PURPLE, width=max(4, int(8*scale)))
    for lx in [-28, 28]:
        draw.line((cx+lx*scale, cy+55*scale, cx+lx*scale, cy+84*scale), fill=PURPLE, width=max(4, int(8*scale)))
        draw.ellipse((cx+lx*scale-20*scale, cy+78*scale, cx+lx*scale+20*scale, cy+95*scale), fill=PURPLE, outline=BLACK, width=2)


def flash(draw, cx, cy, r=42):
    pts = []
    for i in range(16):
        a = math.radians(i * 22.5)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + math.cos(a)*rr, cy + math.sin(a)*rr))
    draw.polygon(pts, fill="#FDE68A", outline=GOLD)


def word_parts(draw, x, y, parts, size=28):
    cur = x
    for txt, color, bold in parts:
        ft = font(size, bold)
        draw.text((cur, y), txt, font=ft, fill=color)
        cur += text_size(draw, txt, ft)[0]


def sheet():
    im = Image.new("RGB", (1536, 1024), WHITE)
    d = ImageDraw.Draw(im)
    d.line((768, 40, 768, 984), fill="#DDDDDD", width=3)
    d.line((40, 512, 1496, 512), fill="#DDDDDD", width=3)
    flash(d, 330, 218, 78)
    acentin(d, 330, 238, 1.55, "happy", "up")
    d.text((205, 454), "ACENTIN — animado", font=FB[26], fill=BLACK)
    acentin(d, 1135, 245, 1.50, "serious", "point")
    d.line((1075, 260, 1028, 222), fill=BLACK, width=5)
    d.text((1002, 454), "ACENTIN — explicando", font=FB[26], fill=BLACK)
    acentin(d, 338, 715, 1.50, "surprised", "open")
    d.text((400, 596), "?", font=FB[40], fill=BLACK)
    d.text((208, 940), "ACENTIN — curioso", font=FB[26], fill=BLACK)
    bia(d, 1148, 700, 1.25, book=True)
    d.text((1040, 940), "BIA — apoio", font=FB[26], fill=BLACK)
    out = CHAR_DIR / "Acentin.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    assert im.size == (1536, 1024)
    im.save(out)


def draw_page_base(title_text):
    im = Image.new("RGB", (1024, 1536), WHITE)
    d = ImageDraw.Draw(im)
    title(d, title_text)
    return im, d


def page1():
    im, d = draw_page_base("TODA PALAVRA TEM UMA SÍLABA MAIS FORTE!")
    boxes = [(30, 95, 994, 430), (30, 455, 994, 700), (30, 725, 994, 970), (30, 995, 994, 1238), (30, 1262, 994, 1506)]
    for b in boxes:
        panel(d, b, BG); classroom(d, b)
    # p1
    x1,y1,x2,y2=boxes[0]
    d.rounded_rectangle((285, 280, 710, 390), radius=10, fill="#C4B5FD", outline=BLACK, width=2)
    d.rectangle((365, 235, 650, 294), fill="#2563EB", outline=BLACK, width=2)
    bia(d, 250, 305, .72, book=False)
    flash(d, 565, 245, 52); acentin(d, 565, 255, .65, "happy", "up")
    bubble(d, (55, 115, 325, 178), "Ei! Quem é você?!", (245,210), "Bia", 18)
    bubble(d, (625, 115, 965, 210), "Oi, Bia! Eu sou o Acentin! Vim te contar um segredo das palavras!", (580,235), "Acentin", 18)
    # p2
    x1,y1,x2,y2=boxes[1]
    d.rounded_rectangle((120, 520, 904, 645), radius=12, fill=WHITE, outline=PURPLE, width=3)
    acentin(d, 165, 575, .62, "serious", "point")
    d.line((200, 562, 285, 538), fill=BLACK, width=3)
    d.text((430, 520), "AMIGO", font=FB[40], fill=BLACK)
    bubble(d, (270, 595, 950, 685), "Toda palavra tem uma sílaba pronunciada com mais força. Ela se chama SÍLABA TÔNICA!", (190,585), "Acentin", 18)
    # p3
    x1,y1,x2,y2=boxes[2]
    word_parts(d, 285, 780, [("A-", BLACK, False), ("MI", GOLD, True), ("-GO", BLACK, False)], 40)
    d.text((372, 748), "´", font=FB[40], fill=GOLD)
    flash(d, 390, 825, 42); acentin(d, 390, 844, .52, "happy", "up")
    bubble(d, (60, 850, 510, 952), "Em 'amigo', a sílaba forte é MI. Fala comigo: a-MI-go!", (390,885), "Acentin", 17)
    bubble(d, (535, 840, 960, 940), "a-MI-go! É verdade, sai mais forte!", (650,900), "Bia", 17)
    # p4
    x1,y1,x2,y2=boxes[3]
    d.rounded_rectangle((80, 1035, 915, 1115), radius=12, fill=WHITE, outline=PURPLE, width=3)
    word_parts(d, 330, 1050, [("MÉ", GOLD, True), ("-DI-CO", BLACK, False)], 40)
    d.text((343, 1016), "´", font=FB[40], fill=GOLD)
    bia(d, 135, 1165, .55, point=True)
    acentin(d, 850, 1160, .50, "happy", "up")
    bubble(d, (205, 1132, 615, 1216), "E em 'médico'? MÉ-di-co! A sílaba forte é MÉ!", (155,1140), "Bia", 17)
    bubble(d, (620, 1128, 965, 1228), "Isso mesmo! Mas cuidado: nem toda sílaba tônica leva acento na escrita. Só algumas!", (850,1165), "Acentin", 16)
    # p5
    acentin(d, 205, 1393, .82, "serious", "point")
    bia(d, 835, 1420, .58, book=True)
    bubble(d, (275, 1292, 835, 1385), "Nas próximas páginas eu vou te ensinar QUANDO usar o acento. Vamos?", (225,1360), "Acentin", 18)
    bubble(d, (480, 1400, 935, 1486), "Vamos! Já quero saber!", (830,1435), "Bia", 18)
    save_page(im, OUT_DIR / "hq-acentuacao-paroxitonas-proparoxitonas-pg1.png")


def page2():
    im, d = draw_page_base("PAROXÍTONAS: A PENÚLTIMA SÍLABA É A MAIS FORTE")
    boxes = [(30,95,994,418),(30,442,994,682),(30,706,994,968),(30,992,994,1236),(30,1260,994,1506)]
    for b in boxes:
        panel(d,b,BG); classroom(d,b,board=True)
    # p1
    word_parts(d, 380, 160, [("A-",BLACK,False),("MI",GOLD,True),("-GO",BLACK,False)], 44)
    acentin(d, 190, 255, .78, "serious", "point"); bia(d, 820, 310, .55)
    bubble(d,(250,245,710,345),"Quando a sílaba tônica é a PENÚLTIMA, a palavra é chamada de PAROXÍTONA.",(210,260),"Acentin",17)
    bubble(d,(705,118,960,188),"Paroxítona? Que nome comprido!",(835,250),"Bia",17)
    # p2
    word_parts(d, 170, 508, [("ME",GOLD,True),("-sa   ",BLACK,False),("QUEN",GOLD,True),("-te   ",BLACK,False),("a-",BLACK,False),("MI",GOLD,True),("-go",BLACK,False)], 34)
    acentin(d, 110, 570, .55, "happy", "point"); bia(d, 865, 610, .50)
    bubble(d,(150,570,575,660),"Olha só: ME-sa, QUEN-te, a-MI-go. Todas paroxítonas!",(130,575),"Acentin",16)
    bubble(d,(595,570,955,655),"Mas nenhuma delas tem acento escrito!",(860,610),"Bia",16)
    # p3
    acentin(d, 150, 842, .65, "serious", "point")
    d.text((260,730),"A regra do livro é assim:",font=FB[24],fill=PURPLE)
    rule = "Paroxítonas só levam acento quando terminam em: L, R, N, X, PS, Ã, ÃS, ÃO, ÃOS, UM, UNS, OM, ONS, US, I, IS ou ditongo oral."
    bubble(d,(250,770,948,940),rule,None,None,18)
    bubble(d,(60,732,330,815),"Muito bem observado! A regra do livro é assim:",(155,830),"Acentin",15)
    # p4
    examples = [("NÍ-vel","L"),("BÔ-nus","US"),("re-VÓL-ver","R"),("JÚ-ri","I"),("a-do-RÁ-vel","L"),("TÓ-rax","X"),("FÓR-ceps","PS")]
    x,y=95,1025
    for i,(w,end) in enumerate(examples):
        d.text((x,y),w,font=FB[24],fill=GOLD)
        d.text((x+text_size(d,w,FB[24])[0]+5,y),end,font=FB[22],fill=RED)
        x += 230
        if i==3:
            x=95; y+=52
    acentin(d, 840,1135,.55,"happy","point")
    bubble(d,(70,1138,548,1225),"Nível termina em L, bônus em US, revólver em R... por isso levam acento!",(820,1140),"Acentin",15)
    bubble(d,(570,1140,955,1222),"Já entendi! É a terminação que manda!",(850,1160),"Bia",16)
    # p5
    acentin(d,130,1390,.62,"happy","up"); bia(d,850,1420,.55)
    bubble(d,(215,1290,945,1385),"Se a paroxítona NÃO termina numa dessas letras, ela fica sem acento — igual 'amigo', 'mesa', 'quente'.",(145,1370),"Acentin",16)
    bubble(d,(300,1400,890,1486),"Legal! Agora só falta as proparoxítonas!",(850,1430),"Bia",18)
    save_page(im, OUT_DIR / "hq-acentuacao-paroxitonas-proparoxitonas-pg2.png")


def page3():
    im, d = draw_page_base("PROPAROXÍTONAS: TODAS LEVAM ACENTO!")
    boxes = [(30,95,994,430),(30,455,994,700),(30,725,994,1015),(30,1040,994,1255),(30,1280,994,1506)]
    for b in boxes:
        panel(d,b,BG); classroom(d,b,board=True)
    word_parts(d, 345,150,[("MÉ",GOLD,True),("-DI-CO",BLACK,False)],48); d.text((360,112),"´",font=FB[40],fill=GOLD)
    acentin(d,515,270,.85,"happy","open")
    bubble(d,(95,318,930,410),"Agora a melhor parte! Quando a sílaba tônica é a ANTEPENÚLTIMA, a palavra é PROPAROXÍTONA!",(515,330),"Acentin",18)
    bia(d,145,620,.58,point=False)
    d.text((420,500),"MÉ-di-co",font=FB[40],fill=GOLD)
    bubble(d,(240,570,820,672),"Antepenúltima... deixa eu ver: co (última), di (penúltima), MÉ (antepenúltima). É a terceira contando do fim!",(160,620),"Bia",16)
    bubble(d,(820,520,965,588),"Exatamente!",(720,610),"Acentin",16)
    acentin(d,510,880,.95,"happy","up",cape=True)
    bubble(d,(120,748,905,835),"TODAS as palavras proparoxítonas são acentuadas. SEM EXCEÇÃO!",None,None,22)
    bubble(d,(245,934,785,1000),"É a regra mais fácil da língua portuguesa!",(510,920),"Acentin",18)
    examples=["TÊ-nis","LÁ-gri-ma","PÁS-sa-ro","me-MÓ-ria","ÁR-vo-re","MÉ-di-co","FÊ-nix"]
    x,y=92,1085
    for w in examples:
        d.text((x,y),w,font=FB[26],fill=GOLD)
        x += 220
        if x>780:
            x=92; y+=55
    bia(d,120,1202,.45)
    bubble(d,(215,1148,725,1238),"Tênis, lágrima, pássaro, memória, árvore, médico, fênix... TODAS têm acento!",(125,1185),"Bia",15)
    bubble(d,(735,1150,955,1222),"Isso! Sem exceção!",(820,1180),"Acentin",16)
    prepo(d,140,1410,.55); acentin(d,835,1420,.55,"happy","up")
    bubble(d,(235,1308,765,1405),"Ei, Bia! Achei uma tira do Laerte com duas proparoxítonas: 'médico' e 'álbum'!",(150,1375),"Prepo",15)
    bubble(d,(430,1415,945,1490),"Perfeito! Proparoxítonas aparecem em tudo quanto é lugar!",(830,1425),"Acentin",16)
    save_page(im, OUT_DIR / "hq-acentuacao-paroxitonas-proparoxitonas-pg3.png")


def page4():
    im, d = draw_page_base("RESUMÃO DO ACENTIN")
    boxes = [(30,95,994,400),(30,425,994,735),(30,760,994,1035),(30,1060,994,1290),(30,1315,994,1506)]
    for b in boxes:
        panel(d,b,BG)
        d.rounded_rectangle((65, b[1] + 45, 959, b[3] - 45), radius=8, fill=WHITE, outline=PURPLE, width=4)
    d.line((512,135,512,370),fill=BLACK,width=3)
    d.text((165,135),"PAROXÍTONAS",font=FB[28],fill=PURPLE)
    d.text((610,135),"PROPAROXÍTONAS",font=FB[26],fill=PURPLE)
    acentin(d,512,292,.62,"happy","open"); bia(d,150,335,.42); prepo(d,875,330,.38)
    bubble(d,(330,305,690,382),"Vamos revisar tudo em uma tabela!",(512,315),"Acentin",17)
    d.rectangle((80, 445, 610, 488), fill=WHITE)
    d.text((85,448),"PAROXÍTONA = penúltima sílaba tônica",font=FB[22],fill=PURPLE)
    d.text((85,505),"Sem acento: amigo, mesa, quente",font=F[20],fill=BLACK)
    txt="Com acento: nível, revólver, pólen, tórax, bíceps, júri, vírus, bônus."
    d.text((85,545),txt,font=font(19),fill=BLACK)
    d.text((85,590),"Terminações: L, R, N, X, PS, I, IS, US, ÃO(S), UM/UNS, OM/ONS, Ã/ÃS, ditongo",font=F[16],fill=BLACK)
    bia(d,835,665,.48,point=True)
    bubble(d,(100,625,745,718),"Paroxítona só leva acento se terminar naquelas letras específicas!",(820,650),"Bia",18)
    d.rectangle((80, 775, 690, 818), fill=WHITE)
    d.text((85,778),"PROPAROXÍTONA = antepenúltima sílaba tônica",font=FB[22],fill=PURPLE)
    d.text((85,835),"Regra: TODAS levam acento (sem exceção!)",font=FB[20],fill=BLACK)
    d.text((85,880),"Exemplos: médico, lágrima, pássaro, memória, árvore, tênis, fênix, hífen.",font=font(19),fill=BLACK)
    prepo(d,820,955,.50,point=True)
    bubble(d,(95,930,700,1018),"E proparoxítona sempre leva acento. Fácil!",(805,950),"Prepo",18)
    acentin(d,155,1198,.62,"serious","point")
    d.ellipse((95,1110,150,1165),outline=GOLD,width=5); d.line((142,1158,180,1198),fill=GOLD,width=6)
    word_parts(d, 365,1108,[("A-",BLACK,False),("ÇÚ",GOLD,True),("-CAR",BLACK,False)],42); d.text((426,1070),"´",font=FB[40],fill=GOLD)
    bubble(d,(230,1156,950,1210),"Dica do Acentin: primeiro descubra qual é a sílaba tônica. Depois conte de trás pra frente: última, penúltima, antepenúltima.",(160,1195),"Acentin",13)
    bubble(d,(230,1215,950,1282),"Se for a antepenúltima → PROPAROXÍTONA → SEMPRE acento! Se for a penúltima → PAROXÍTONA → só se terminar nas letras da regra.",(160,1210),"Acentin",12)
    words=["médico","amigo","nível","pássaro","quente","bônus"]
    for i,w in enumerate(words):
        d.text((80+i*150,1332+(i%2)*35),w,font=FB[18],fill=PURPLE if i%2 else GOLD)
    acentin(d,500,1430,.55,"happy","up"); bia(d,260,1450,.40); prepo(d,750,1450,.38)
    bubble(d,(55,1375,390,1450),"Agora você é um detetive das sílabas tônicas!",(500,1420),"Acentin",14)
    bubble(d,(365,1340,695,1406),"Obrigada, Acentin! Vou treinar em cada palavra que ler!",(275,1430),"Bia",14)
    bubble(d,(620,1410,965,1488),"Bora praticar nas atividades!",(750,1435),"Prepo",16)
    save_page(im, OUT_DIR / "hq-acentuacao-paroxitonas-proparoxitonas-pg4.png")


def save_page(im, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    assert im.size == (1024, 1536), im.size
    im.save(path)


if __name__ == "__main__":
    sheet()
    page1()
    page2()
    page3()
    page4()
    targets = [
        CHAR_DIR / "Acentin.png",
        OUT_DIR / "hq-acentuacao-paroxitonas-proparoxitonas-pg1.png",
        OUT_DIR / "hq-acentuacao-paroxitonas-proparoxitonas-pg2.png",
        OUT_DIR / "hq-acentuacao-paroxitonas-proparoxitonas-pg3.png",
        OUT_DIR / "hq-acentuacao-paroxitonas-proparoxitonas-pg4.png",
    ]
    for p in targets:
        with Image.open(p) as im:
            print(f"{p}|{im.size[0]}x{im.size[1]}|{p.stat().st_size}")
