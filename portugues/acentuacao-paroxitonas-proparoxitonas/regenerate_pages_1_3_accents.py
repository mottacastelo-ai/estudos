from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import re
import unicodedata


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


VISIBLE_TEXTS = {
    "pg1": [
        "TODA PALAVRA TEM UMA SÍLABA MAIS FORTE!",
        "Ei! Quem é você?!",
        "Oi, Bia! Eu sou o Acentin! Vim te contar um segredo das palavras!",
        "AMIGO",
        "Toda palavra tem uma sílaba pronunciada com mais força. Ela se chama SÍLABA TÔNICA!",
        "A-MI-GO",
        "Em 'amigo', a sílaba forte é MI. Fala comigo: a-MI-go!",
        "a-MI-go! É verdade, sai mais forte!",
        "MÉ-DI-CO",
        "E em 'médico'? MÉ-di-co! A sílaba forte é MÉ!",
        "Isso mesmo! Mas cuidado: nem toda sílaba tônica leva acento na escrita. Só algumas!",
        "Nas próximas páginas eu vou te ensinar QUANDO usar o acento. Vamos?",
        "Vamos! Já quero saber!",
    ],
    "pg2": [
        "PAROXÍTONAS: A PENÚLTIMA SÍLABA É A MAIS FORTE",
        "A-MI-GO",
        "Quando a sílaba tônica é a PENÚLTIMA, a palavra é chamada de PAROXÍTONA.",
        "Paroxítona? Que nome comprido!",
        "ME-sa",
        "QUEN-te",
        "a-MI-go",
        "Olha só: ME-sa, QUEN-te, a-MI-go. Todas paroxítonas!",
        "Mas nenhuma delas tem acento escrito!",
        "Paroxítonas só levam acento quando terminam em: L, R, N, X, PS, Ã, ÃS, ÃO, ÃOS, UM, UNS, OM, ONS, US, I, IS ou ditongo oral.",
        "Muito bem observado! A regra do livro é assim:",
        "NÍ-veL",
        "BÔ-nuS",
        "re-VÓL-veR",
        "JÚ-rI",
        "a-do-RÁ-veL",
        "TÓ-raX",
        "FÓR-cepS",
        "Nível termina em L, bônus em US, revólver em R... por isso levam acento!",
        "Já entendi! É a terminação que manda!",
        "Se a paroxítona NÃO termina numa dessas letras, ela fica sem acento - igual 'amigo', 'mesa', 'quente'.",
        "Legal! Agora só falta as proparoxítonas!",
    ],
    "pg3": [
        "PROPAROXÍTONAS: TODAS LEVAM ACENTO!",
        "MÉ-DI-CO",
        "Agora a melhor parte! Quando a sílaba tônica é a ANTEPENÚLTIMA, a palavra é PROPAROXÍTONA!",
        "Antepenúltima... deixa eu ver: co (última), di (penúltima), MÉ (antepenúltima). É a terceira contando do fim!",
        "Exatamente!",
        "TODAS as palavras proparoxítonas são acentuadas. SEM EXCEÇÃO!",
        "É a regra mais fácil da língua portuguesa!",
        "TÊ-nis",
        "LÁ-gri-ma",
        "PÁS-sa-ro",
        "me-MÓ-ria",
        "ÁR-vo-re",
        "MÉ-di-co",
        "HÍ-fen",
        "Tênis, lágrima, pássaro, memória, árvore, médico, hífen... TODAS têm acento!",
        "Isso! Sem exceção!",
        "Ei, Bia! Achei uma tira do Laerte com duas proparoxítonas: 'médico' e 'álbum'!",
        "Perfeito! Proparoxítonas aparecem em tudo quanto é lugar!",
    ],
}

FORBIDDEN = [
    "SILABA", "TONICA", "PAROXITONA", "PAROXITONAS", "PROPAROXITONA",
    "PROPAROXITONAS", "PENULTIMA", "ANTEPENULTIMA", "MEDICO", "NIVEL",
    "BONUS", "REVOLVER", "TERMINACAO", "TERMINACOES", "PROXIMAS",
    "PAGINAS", "JA", "JURI", "VIRUS", "EXCECAO", "LINGUA", "ALBUM",
]


def font(size, bold=False):
    names = (
        "arialbd.ttf" if bold else "arial.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    )
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def text_size(draw, text, ft):
    box = draw.textbbox((0, 0), text, font=ft)
    return box[2] - box[0], box[3] - box[1]


def strip_accents(text):
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def validate_texts(page_key):
    joined = "\n".join(VISIBLE_TEXTS[page_key])
    raw_upper = joined.upper()
    stripped = strip_accents(joined).upper()
    for bad in FORBIDDEN:
        pattern = r"(?<![A-Z])" + re.escape(bad) + r"(?![A-Z])"
        if re.search(pattern, raw_upper):
            raise ValueError(f"Texto sem acento encontrado em {page_key}: {bad}")
    required = [
        "SÍLABA", "TÔNICA", "PAROXÍTONA", "PROPAROXÍTONAS", "PENÚLTIMA",
        "ANTEPENÚLTIMA", "MÉDICO", "NÍVEL", "BÔNUS", "REVÓLVER",
        "TERMINAÇÃO", "PRÓXIMAS", "PÁGINAS", "JÁ", "JÚRI",
    ]
    # Only check terms that are expected on the current page.
    for word in required:
        base = strip_accents(word).upper()
        if base in stripped and word.upper() not in joined.upper():
            raise ValueError(f"Forma acentuada obrigatória ausente em {page_key}: {word}")


def wrap_text(draw, text, ft, max_width):
    lines, line = [], ""
    for word in text.split():
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


def fit_font(draw, text, max_width, max_size, min_size=12, bold=True):
    for size in range(max_size, min_size - 1, -1):
        ft = font(size, bold)
        if text_size(draw, text, ft)[0] <= max_width:
            return ft
    return font(min_size, bold)


def draw_title(draw, text):
    draw.rectangle((0, 0, W, 78), fill=PURPLE)
    ft = fit_font(draw, text, W - 42, 30, 20, True)
    tw, th = text_size(draw, text, ft)
    draw.text(((W - tw) / 2, 22), text, font=ft, fill=WHITE)


def panel(draw, box):
    draw.rounded_rectangle(box, radius=8, fill=BG, outline=BLACK, width=3)
    classroom(draw, box)


def classroom(draw, box):
    x1, y1, x2, y2 = box
    draw.rectangle((x1 + 3, y1 + 3, x2 - 3, y2 - 3), fill=BG)
    draw.rectangle((x1 + 26, y1 + 22, x2 - 26, y1 + 82), fill="#DBEAFE", outline=BLACK, width=2)
    draw.line((x1 + 26, y1 + 52, x2 - 26, y1 + 52), fill="#93C5FD", width=2)
    draw.line(((x1 + x2) / 2, y1 + 22, (x1 + x2) / 2, y1 + 82), fill="#93C5FD", width=2)
    draw.rounded_rectangle((x1 + 85, y1 + 75, x2 - 85, y2 - 56), radius=10, fill=WHITE, outline=PURPLE, width=4)
    draw.rectangle((x1 + 4, y2 - 55, x2 - 4, y2 - 4), fill="#DDD6FE")
    for x in (x1 + 95, x1 + 368, x1 + 684):
        draw.rounded_rectangle((x, y2 - 42, x + 135, y2 - 18), radius=7, fill="#C084FC", outline=BLACK, width=2)
        draw.line((x + 24, y2 - 18, x + 14, y2 - 4), fill=BLACK, width=2)
        draw.line((x + 110, y2 - 18, x + 122, y2 - 4), fill=BLACK, width=2)


def bubble(draw, box, speaker, text, tail=None, fs=17, fill=WHITE, outline=BLACK, text_fill=BLACK):
    x1, y1, x2, y2 = box
    if tail:
        tx, ty = tail
        if tx < (x1 + x2) / 2:
            pts = [(x1 + 42, y2 - 8), (x1 + 82, y2 - 8), tail]
        else:
            pts = [(x2 - 42, y2 - 8), (x2 - 82, y2 - 8), tail]
        draw.polygon(pts, fill=fill, outline=outline)
    draw.rounded_rectangle(box, radius=20, fill=fill, outline=outline, width=2)
    while fs > 10:
        ft = font(fs)
        fb = font(fs, True)
        prefix = f"{speaker}: " if speaker else ""
        first_width = x2 - x1 - 30 - (text_size(draw, prefix, fb)[0] if speaker else 0)
        lines = wrap_text(draw, text, ft, first_width)
        if lines:
            used_words = len(lines[0].split())
            rest = " ".join(text.split()[used_words:])
            if rest:
                lines = [lines[0]] + wrap_text(draw, rest, ft, x2 - x1 - 30)
        if y1 + 12 + len(lines) * (fs + 6) <= y2 - 8:
            break
        fs -= 1
    y = y1 + 10
    x = x1 + 15
    if speaker:
        draw.text((x, y), prefix, font=fb, fill=PURPLE if fill == WHITE else WHITE)
        x += text_size(draw, prefix, fb)[0]
    for i, line in enumerate(lines):
        draw.text((x if i == 0 else x1 + 15, y), line, font=ft, fill=text_fill)
        y += fs + 6


def board_text(draw, xy, parts, fs=34):
    x, y = xy
    for text, color, bold in parts:
        ft = font(fs, bold)
        draw.text((x, y), text, font=ft, fill=color)
        x += text_size(draw, text, ft)[0]


def flash(draw, cx, cy, r=42):
    pts = []
    for i in range(18):
        a = math.radians(i * 20)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    draw.polygon(pts, fill="#FDE68A", outline=GOLD)


def acentin(draw, cx, cy, s=1.0, mood="happy", arms="up", cape=False):
    if cape:
        draw.polygon([(cx - 16*s, cy - 10*s), (cx - 88*s, cy + 72*s), (cx - 4*s, cy + 78*s)], fill="#FBBF24", outline=BLACK)
    body = [(cx - 28*s, cy + 55*s), (cx + 6*s, cy - 72*s), (cx + 44*s, cy - 62*s), (cx + 5*s, cy + 72*s)]
    draw.polygon(body, fill=GOLD, outline=BLACK)
    draw.line(body + [body[0]], fill=BLACK, width=max(2, int(3*s)))
    hat = [(cx + 10*s, cy - 98*s), (cx + 68*s, cy - 126*s), (cx + 78*s, cy - 108*s), (cx + 18*s, cy - 82*s)]
    draw.polygon(hat, fill=DARK_GOLD, outline=BLACK)
    for ex in (-11, 19):
        draw.ellipse((cx + ex*s - 10*s, cy - 35*s, cx + ex*s + 10*s, cy - 10*s), fill=WHITE, outline=BLACK, width=2)
        draw.ellipse((cx + ex*s - 3*s, cy - 27*s, cx + ex*s + 5*s, cy - 15*s), fill=BLACK)
    if mood == "serious":
        draw.arc((cx - 4*s, cy + 10*s, cx + 26*s, cy + 34*s), 205, 340, fill=BLACK, width=max(2, int(2*s)))
    else:
        draw.arc((cx - 13*s, cy + 3*s, cx + 31*s, cy + 36*s), 10, 165, fill=BLACK, width=max(2, int(3*s)))
    if arms == "point":
        arms_xy = [(cx - 22*s, cy + 5*s, cx - 74*s, cy + 10*s), (cx + 34*s, cy, cx + 92*s, cy - 15*s)]
    elif arms == "open":
        arms_xy = [(cx - 22*s, cy, cx - 78*s, cy - 22*s), (cx + 33*s, cy, cx + 88*s, cy - 22*s)]
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


def prepo(draw, cx, cy, s=1.0):
    draw.rounded_rectangle((cx - 48*s, cy - 62*s, cx + 48*s, cy + 54*s), radius=int(28*s), fill=PURPLE, outline=BLACK, width=3)
    for ex in (-19, 19):
        draw.ellipse((cx + ex*s - 15*s, cy - 42*s, cx + ex*s + 15*s, cy - 12*s), fill=WHITE, outline=BLACK, width=2)
        draw.ellipse((cx + ex*s - 5*s, cy - 33*s, cx + ex*s + 5*s, cy - 18*s), fill=BLACK)
    draw.arc((cx - 17*s, cy - 17*s, cx + 24*s, cy + 18*s), 15, 160, fill=BLACK, width=3)
    draw.line((cx - 25*s, cy - 62*s, cx - 35*s, cy - 97*s), fill=BLACK, width=3)
    draw.line((cx + 25*s, cy - 62*s, cx + 35*s, cy - 97*s), fill=BLACK, width=3)
    draw.text((cx - 52*s, cy - 122*s), "D", font=font(max(14, int(27*s)), True), fill="#FACC15", stroke_width=2, stroke_fill=BLACK)
    draw.text((cx + 28*s, cy - 122*s), "E", font=font(max(14, int(27*s)), True), fill="#FACC15", stroke_width=2, stroke_fill=BLACK)
    draw.rounded_rectangle((cx - 42*s, cy + 8*s, cx + 42*s, cy + 38*s), radius=int(7*s), fill="#E5E7EB", outline=BLACK, width=2)
    draw.text((cx - 30*s, cy + 11*s), "PREPO", font=font(max(12, int(15*s)), True), fill=BLUE)
    draw.line((cx - 48*s, cy - 4*s, cx - 84*s, cy - 22*s), fill=PURPLE, width=max(4, int(7*s)))
    draw.line((cx + 48*s, cy - 4*s, cx + 84*s, cy - 22*s), fill=PURPLE, width=max(4, int(7*s)))
    for lx in (-27, 27):
        draw.line((cx + lx*s, cy + 54*s, cx + lx*s, cy + 84*s), fill=PURPLE, width=max(4, int(7*s)))
        draw.ellipse((cx + lx*s - 19*s, cy + 78*s, cx + lx*s + 19*s, cy + 94*s), fill=PURPLE, outline=BLACK, width=2)


def page_base(page_key):
    validate_texts(page_key)
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    draw_title(d, VISIBLE_TEXTS[page_key][0])
    return im, d


def page1():
    im, d = page_base("pg1")
    boxes = [(30, 96, 994, 430), (30, 455, 994, 700), (30, 725, 994, 970), (30, 995, 994, 1238), (30, 1262, 994, 1506)]
    for b in boxes:
        panel(d, b)
    d.rounded_rectangle((300, 298, 720, 386), radius=9, fill="#C4B5FD", outline=BLACK, width=2)
    d.rectangle((385, 248, 650, 316), fill="#2563EB", outline=BLACK, width=2)
    bia(d, 245, 326, .72)
    flash(d, 565, 256, 52)
    acentin(d, 565, 270, .63)
    bubble(d, (55, 116, 324, 178), "Bia", VISIBLE_TEXTS["pg1"][1], (245, 230), 18)
    bubble(d, (612, 116, 965, 224), "Acentin", VISIBLE_TEXTS["pg1"][2], (575, 238), 16)
    board_text(d, (418, 512), [("AMIGO", BLACK, True)], 42)
    acentin(d, 162, 587, .58, "serious", "point")
    bubble(d, (255, 592, 948, 684), "Acentin", VISIBLE_TEXTS["pg1"][4], (180, 595), 18)
    board_text(d, (285, 780), [("A-", BLACK, False), ("MI", GOLD, True), ("-GO", BLACK, False)], 42)
    d.text((373, 746), "´", font=font(42, True), fill=GOLD)
    flash(d, 386, 840, 36)
    acentin(d, 386, 850, .52)
    bia(d, 835, 892, .46)
    bubble(d, (58, 850, 516, 952), "Acentin", VISIBLE_TEXTS["pg1"][6], (385, 883), 16)
    bubble(d, (535, 840, 962, 940), "Bia", VISIBLE_TEXTS["pg1"][7], (832, 900), 16)
    board_text(d, (330, 1048), [("MÉ", GOLD, True), ("-DI-CO", BLACK, False)], 42)
    d.text((343, 1014), "´", font=font(42, True), fill=GOLD)
    bia(d, 136, 1170, .55, point=True)
    acentin(d, 850, 1163, .50)
    bubble(d, (205, 1132, 615, 1216), "Bia", VISIBLE_TEXTS["pg1"][9], (158, 1142), 15)
    bubble(d, (620, 1128, 965, 1228), "Acentin", VISIBLE_TEXTS["pg1"][10], (848, 1162), 14)
    acentin(d, 205, 1392, .78, "serious", "point")
    bia(d, 835, 1422, .56, book=True)
    bubble(d, (275, 1294, 835, 1392), "Acentin", VISIBLE_TEXTS["pg1"][11], (225, 1360), 17)
    bubble(d, (520, 1400, 936, 1484), "Bia", VISIBLE_TEXTS["pg1"][12], (835, 1438), 18)
    save(im, "hq-acentuacao-paroxitonas-proparoxitonas-pg1.png")


def page2():
    im, d = page_base("pg2")
    boxes = [(30, 96, 994, 418), (30, 442, 994, 682), (30, 706, 994, 968), (30, 992, 994, 1236), (30, 1260, 994, 1506)]
    for b in boxes:
        panel(d, b)
    board_text(d, (380, 155), [("A-", BLACK, False), ("MI", GOLD, True), ("-GO", BLACK, False)], 44)
    acentin(d, 190, 260, .76, "serious", "point")
    bia(d, 825, 312, .55)
    bubble(d, (245, 238, 715, 350), "Acentin", VISIBLE_TEXTS["pg2"][2], (205, 264), 16)
    bubble(d, (705, 118, 960, 188), "Bia", VISIBLE_TEXTS["pg2"][3], (832, 250), 16)
    board_text(d, (145, 505), [("ME", GOLD, True), ("-sa   ", BLACK, False), ("QUEN", GOLD, True), ("-te   ", BLACK, False), ("a-", BLACK, False), ("MI", GOLD, True), ("-go", BLACK, False)], 34)
    acentin(d, 110, 575, .53, "happy", "point")
    bia(d, 862, 614, .48, book=True)
    bubble(d, (150, 572, 575, 660), "Acentin", VISIBLE_TEXTS["pg2"][7], (130, 575), 15)
    bubble(d, (595, 570, 955, 655), "Bia", VISIBLE_TEXTS["pg2"][8], (862, 612), 16)
    acentin(d, 150, 842, .62, "serious", "point")
    d.text((282, 724), "REGRA DO LIVRO", font=font(24, True), fill=PURPLE)
    rule_lines = [
        "Paroxítonas só levam acento quando terminam em:",
        "L, R, N, X, PS, Ã, ÃS, ÃO, ÃOS, UM, UNS,",
        "OM, ONS, US, I, IS ou ditongo oral.",
    ]
    for i, line in enumerate(rule_lines):
        d.text((282, 760 + i * 38), line, font=font(21, True if i == 0 else False), fill=PURPLE)
    bubble(d, (56, 870, 404, 952), "Acentin", VISIBLE_TEXTS["pg2"][10], (155, 846), 14)
    examples = [("NÍ-veL", "L"), ("BÔ-nuS", "US"), ("re-VÓL-veR", "R"), ("JÚ-rI", "I"), ("a-do-RÁ-veL", "L"), ("TÓ-raX", "X"), ("FÓR-cepS", "PS")]
    x, y = 82, 1022
    for i, (word, end) in enumerate(examples):
        d.text((x, y), word, font=font(22, True), fill=GOLD)
        d.text((x + text_size(d, word, font(22, True))[0] + 5, y + 3), end, font=font(17, True), fill=RED)
        x += 225
        if i == 3:
            x = 82
            y += 45
    acentin(d, 835, 1136, .55, "happy", "point")
    bubble(d, (70, 1138, 548, 1225), "Acentin", VISIBLE_TEXTS["pg2"][18], (820, 1140), 14)
    bubble(d, (570, 1140, 955, 1222), "Bia", VISIBLE_TEXTS["pg2"][19], (852, 1160), 16)
    acentin(d, 130, 1390, .60)
    bia(d, 850, 1420, .55)
    bubble(d, (215, 1290, 945, 1388), "Acentin", VISIBLE_TEXTS["pg2"][20], (145, 1370), 15)
    bubble(d, (300, 1400, 890, 1486), "Bia", VISIBLE_TEXTS["pg2"][21], (850, 1430), 18)
    save(im, "hq-acentuacao-paroxitonas-proparoxitonas-pg2.png")


def page3():
    im, d = page_base("pg3")
    boxes = [(30, 96, 994, 430), (30, 455, 994, 700), (30, 725, 994, 1015), (30, 1040, 994, 1255), (30, 1280, 994, 1506)]
    for b in boxes:
        panel(d, b)
    d.arc((870, 360, 938, 405), 180, 360, fill=BLACK, width=2)
    for x in range(880, 932, 12):
        d.ellipse((x, 374, x + 6, 380), fill=BLACK)
    board_text(d, (345, 150), [("MÉ", GOLD, True), ("-DI-CO", BLACK, False)], 48)
    d.text((360, 112), "´", font=font(42, True), fill=GOLD)
    flash(d, 374, 207, 42)
    acentin(d, 515, 270, .85, "happy", "open")
    bubble(d, (88, 310, 938, 414), "Acentin", VISIBLE_TEXTS["pg3"][2], None, 16)
    bia(d, 145, 620, .58)
    board_text(d, (420, 500), [("MÉ", GOLD, True), ("-di-co", BLACK, False)], 40)
    bubble(d, (240, 560, 820, 680), "Bia", VISIBLE_TEXTS["pg3"][3], (160, 620), 15)
    acentin(d, 850, 620, .42)
    bubble(d, (812, 520, 962, 592), "Acentin", VISIBLE_TEXTS["pg3"][4], (850, 620), 15)
    acentin(d, 510, 880, .95, "happy", "up", cape=True)
    bubble(d, (110, 748, 915, 835), None, VISIBLE_TEXTS["pg3"][5], None, 20, fill=PURPLE, outline=BLACK, text_fill=WHITE)
    bubble(d, (245, 934, 785, 1000), "Acentin", VISIBLE_TEXTS["pg3"][6], (510, 920), 17)
    examples = ["TÊ-nis", "LÁ-gri-ma", "PÁS-sa-ro", "me-MÓ-ria", "ÁR-vo-re", "MÉ-di-co", "HÍ-fen"]
    x, y = 95, 1076
    for word in examples:
        d.text((x, y), word, font=font(23, True), fill=GOLD)
        x += 225
        if x > 780:
            x = 95
            y += 42
    bia(d, 120, 1202, .45)
    acentin(d, 835, 1190, .45)
    bubble(d, (215, 1154, 724, 1246), "Bia", VISIBLE_TEXTS["pg3"][14], None, 13)
    bubble(d, (735, 1162, 955, 1238), "Acentin", VISIBLE_TEXTS["pg3"][15], None, 14)
    prepo(d, 140, 1410, .55)
    bia(d, 720, 1435, .40)
    acentin(d, 880, 1420, .48)
    bubble(d, (235, 1300, 765, 1408), "Prepo", VISIBLE_TEXTS["pg3"][16], None, 14)
    bubble(d, (430, 1415, 945, 1492), "Acentin", VISIBLE_TEXTS["pg3"][17], None, 14)
    save(im, "hq-acentuacao-paroxitonas-proparoxitonas-pg3.png")


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
