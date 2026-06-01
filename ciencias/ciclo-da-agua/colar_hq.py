from PIL import Image
import os

slug = "ciclo-da-agua"
pasta = r"C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos\ciencias\ciclo-da-agua"

print("Validando dimensões das 4 páginas...")
print("-" * 60)

EXPECTED_W, EXPECTED_H = 1024, 1536
erros = []

for i in range(1, 5):
    path = os.path.join(pasta, f"hq-{slug}-pg{i}.png")
    img = Image.open(path)
    status = "OK" if (img.width == EXPECTED_W and img.height == EXPECTED_H) else "ERRO"
    print(f"pg{i}: {img.width}x{img.height}px — {status}")
    
    if img.width != EXPECTED_W or img.height != EXPECTED_H:
        erros.append(f"pg{i}: {img.width}x{img.height}px (esperado {EXPECTED_W}x{EXPECTED_H})")

print("-" * 60)

if erros:
    print("\nCOLAGEM ABORTADA — páginas com dimensão incorreta:")
    for erro in erros:
        print(f"  - {erro}")
    exit(1)

print("\nDimensões OK - Empilhando páginas...")

# Carregar as 4 páginas
arquivos = [f"hq-{slug}-pg{i}.png" for i in range(1, 5)]
imgs = [Image.open(os.path.join(pasta, f)).convert("RGB") for f in arquivos]

# Normalizar largura para a maior entre as 4
largura_max = max(img.width for img in imgs)
imgs_norm = []
for img in imgs:
    if img.width != largura_max:
        nova_altura = int(img.height * largura_max / img.width)
        img = img.resize((largura_max, nova_altura), Image.LANCZOS)
    imgs_norm.append(img)

# Empilhar verticalmente
altura_total = sum(img.height for img in imgs_norm)
canvas = Image.new("RGB", (largura_max, altura_total), (255, 255, 255))

y = 0
for img in imgs_norm:
    canvas.paste(img, (0, y))
    y += img.height

# Salvar
saida = os.path.join(pasta, f"hq-{slug}.png")
canvas.save(saida, "PNG", optimize=True)
print(f"Salvo: {saida}")
print(f"Dimensões finais: {largura_max}x{altura_total}px")
