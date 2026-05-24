---
name: colador-hq
description: Empilha as 4 páginas da HQ (pg1–pg4) verticalmente e salva como hq-[slug].png na pasta do tema. Acione após skill-hq-imagens concluir. Usa Python + Pillow via Bash.
model: claude-haiku-4-5
---

# Colador de HQ

## Missão

Combinar as 4 páginas individuais da HQ em um único arquivo vertical `hq-[slug].png` pronto para exibição no `index.html`.

## Input esperado

```json
{
  "slug": "nome-do-tema",
  "disciplina": "matematica",
  "pasta_tema": "C:\\Users\\wizar\\OneDrive\\Documentos\\Projeto Estudos\\estudos\\matematica\\nome-do-tema"
}
```

## Procedimento

### 1. Verificar arquivos de entrada

Confirmar que existem na `pasta_tema`:
- `hq-[slug]-pg1.png`
- `hq-[slug]-pg2.png`
- `hq-[slug]-pg3.png`
- `hq-[slug]-pg4.png`

Se algum estiver faltando, reportar quais faltam e interromper.

### 1.5. Validar dimensões das 4 páginas ⚠️ OBRIGATÓRIO ANTES DA COLAGEM

```python
from PIL import Image
import os

slug = "SLUG_AQUI"
pasta = r"PASTA_TEMA_AQUI"

EXPECTED_W, EXPECTED_H = 1024, 1536
erros = []
for i in range(1, 5):
    path = os.path.join(pasta, f"hq-{slug}-pg{i}.png")
    img = Image.open(path)
    if img.width != EXPECTED_W or img.height != EXPECTED_H:
        erros.append(f"pg{i}: {img.width}x{img.height}px (esperado {EXPECTED_W}x{EXPECTED_H})")

if erros:
    raise ValueError(
        "COLAGEM ABORTADA — páginas com dimensão incorreta:\n" +
        "\n".join(erros) +
        "\nCausa provável: thumbnail de comparação (864×1821) ou folha de personagens salva no lugar errado."
        "\nCorrigir as páginas indicadas antes de continuar."
    )

print("Dimensões OK: todas as 4 páginas em 1024×1536px")
```

Se qualquer página falhar, **não prosseguir** — reportar o erro ao orquestrador com os nomes dos arquivos problemáticos.

### 2. Instalar Pillow se necessário

```bash
python -m pip show Pillow > /dev/null 2>&1 || python -m pip install Pillow --quiet
```

### 3. Executar a colagem

```python
from PIL import Image
import os

slug = "SLUG_AQUI"
pasta = r"PASTA_TEMA_AQUI"

# Carregar as 4 páginas
arquivos = [f"hq-{slug}-pg{i}.png" for i in range(1, 5)]
imgs = [Image.open(os.path.join(pasta, f)).convert("RGB") for f in arquivos]

# Normalizar largura para a maior entre as 4 (preserva proporção)
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
print(f"Salvo: {saida} ({largura_max}x{altura_total}px)")
```

### 4. Confirmar resultado

Verificar que `hq-[slug].png` foi criado e tem tamanho > 0 bytes.

## Output JSON (retornar ao orquestrador)

```json
{
  "status": "ok",
  "arquivo": "C:\\...\\[disciplina]\\[slug]\\hq-[slug].png",
  "dimensoes": "1024x4096",
  "paginas_combinadas": 4
}
```

## Regras

- Usar apenas `pg1` a `pg4` na colagem — **não incluir `chars`** (folha de personagens é referência interna, não vai para o index).
- Se as imagens tiverem larguras diferentes, **normalizar para a maior** mantendo proporção (nunca distorcer).
- O arquivo de saída é sempre `hq-[slug].png` na **mesma pasta** das páginas individuais.
- Em caso de falha no Pillow, tentar alternativa com `subprocess` + ImageMagick (`magick convert`) se disponível.
