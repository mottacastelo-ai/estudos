"""
Corta prepo-hd.png (300x450 RGBA) em 16 peças transparentes.
Cada peça é um PNG 200x240 com só aquela região visível.
Quando stacked no stage 200x240, formam o Prepo perfeito.
"""
from PIL import Image
import os

BASE = r'C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos'

# Carrega original (300x450, RGBA)
orig = Image.open(os.path.join(BASE, '_landing', 'prepo-hd.png')).convert('RGBA')

# object-fit: contain → cabe por altura: 160x240, centralizado em 200x240
SCALED_W, SCALED_H = 160, 240
CANVAS_W, CANVAS_H = 200, 240
OFFSET_X = (CANVAS_W - SCALED_W) // 2   # = 20px

scaled = orig.resize((SCALED_W, SCALED_H), Image.LANCZOS)

# Canvas completo do Prepo (200x240, transparente) — a referência
full = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
full.paste(scaled, (OFFSET_X, 0))
full.save(os.path.join(BASE, '_landing', 'prepo-stage.png'))   # debug

# ─── Regiões (em coordenadas 200x240) ───────────────────────────────────────
#  Cada região define um retângulo; peças podem se sobrepor — OK para montagem.
#  PAD: margem extra ao redor de cada região para evitar borda abrupta.
PAD = 4

REGIONS = [
    ('p1',  'Antena D',     40,   0,  80,  36),
    ('p2',  'Antena E',    118,   0, 158,  36),
    ('p3',  'Conector E',   16,  24,  60,  62),
    ('p4',  'Conector D',  140,  24, 184,  62),
    ('p5',  'Topo cabeca',  36,  18, 164,  65),
    ('p6',  'Face',         36,  52, 164, 102),
    ('p7',  'Olho E',       46,  54,  90,  96),
    ('p8',  'Olho D',      110,  54, 154,  96),
    ('p9',  'Boca',         62,  86, 138, 112),
    ('p10', 'Ombros',       34, 100, 166, 138),
    ('p11', 'Corpo',        38, 128, 162, 178),
    ('p12', 'Placa PREPO',  54, 152, 146, 190),
    ('p13', 'Braco E',       2, 106,  52, 172),
    ('p14', 'Braco D',     148, 106, 198, 172),
    ('p15', 'Perna E',      44, 172,  98, 240),
    ('p16', 'Perna D',     102, 172, 156, 240),
]

out_dir = os.path.join(BASE, '_landing', 'prepo-pieces')
os.makedirs(out_dir, exist_ok=True)

for pid, name, x1, y1, x2, y2 in REGIONS:
    # Aplica padding (clampado nas bordas do canvas)
    px1 = max(0,        x1 - PAD)
    py1 = max(0,        y1 - PAD)
    px2 = min(CANVAS_W, x2 + PAD)
    py2 = min(CANVAS_H, y2 + PAD)

    # Peça: canvas 200x240, só a região tem pixels, resto transparente
    piece = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    region_img = full.crop((px1, py1, px2, py2))
    piece.paste(region_img, (px1, py1))

    out_path = os.path.join(out_dir, f'piece-{pid}.png')
    piece.save(out_path)
    print(f'[OK] {pid:4s} {name:15s}  {px1},{py1} - {px2},{py2}  ({px2-px1}x{py2-py1}px)')

print(f'\n{len(REGIONS)} pecas salvas em _landing/prepo-pieces/')
print(f'prepo-stage.png = referencia do Prepo em 200x240')
