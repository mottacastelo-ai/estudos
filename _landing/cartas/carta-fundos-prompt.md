# PROMPTS — Fundos das Cartas Colecionáveis
## Portal Sabendo.app — 5º Ano
## Para: Codex Desktop (GPT Image Generation)

---

## ESPECIFICAÇÕES GERAIS (válidas para todos os fundos)

- **Dimensões:** 400 × 560 px
- **Proporção:** 5:7 (trading card padrão)
- **Área do personagem:** elipse/oval central superior (~240×280px, centro em 200,220) — deve ser VAZIA ou com fundo muito sutil, para o personagem ser colado depois
- **Estilo:** cartoon digital, traço bold, child-friendly, inspirado em cartas Pokémon / Yu-Gi-Oh para crianças
- **Fontes na arte:** nenhuma — texto será adicionado em código
- **Fundo de cada carta:** SEM personagem desenhado — apenas o frame, bordas, decorações e textura

---

## CARTA COMUM ⚪

**Arquivo destino:** `carta-fundo-comum.png`

```
Create a collectible trading card background (400x560px) for a Brazilian elementary school educational app called "sabendo.app".

Style: clean digital cartoon, child-friendly, inspired by common Pokémon cards.

Design:
- Outer border: thin silver/light gray metallic frame (8px), slightly rounded corners (24px radius)
- Inner border: white with subtle gray shadow inset
- Card background texture: soft white/light gray gradient, very subtle paper texture, clean and simple
- Top area (character zone, ~240x280px centered at top half): plain white oval/rounded rectangle with very light gray border — this area must stay MOSTLY EMPTY for character insertion
- Bottom area: light gray banner with simple geometric pattern (dots or thin lines), space for text
- Corner decorations: small simple star or diamond shapes in silver/gray at each corner
- Subtle watermark pattern in background: very faint repeated small stars or dots
- Overall feeling: clean, simple, accessible — "entry level" card

Color palette: white, light gray (#E5E7EB), silver (#9CA3AF), with very subtle warm undertones
No text, no characters, no numbers. Just the frame and decorative elements.
```

---

## CARTA RARA 🔵

**Arquivo destino:** `carta-fundo-rara.png`

```
Create a collectible trading card background (400x560px) for a Brazilian elementary school educational app called "sabendo.app".

Style: shiny digital cartoon, child-friendly, inspired by rare holographic Pokémon cards.

Design:
- Outer border: smooth blue metallic frame (10px), rounded corners (24px radius), with subtle inner glow
- Inner border: deep blue (#1D4ED8) to sky blue (#38BDF8) gradient border (4px)
- Card background: cool blue gradient (top: #DBEAFE, bottom: #EFF6FF) with faint holographic shimmer pattern (diagonal rainbow lines, very subtle, 10% opacity)
- Top area (character zone, ~240x280px centered at top half): soft blue-tinted oval with gentle inner glow — MOSTLY EMPTY for character
- Bottom area: deep blue banner (#1E40AF) with light-colored geometric circuit/star pattern, space for card name text
- Corner decorations: crystalline blue diamond shapes with small sparkles
- Background texture: subtle hexagonal grid or crystalline pattern in blue tones
- Radial glow effect from card center: very soft, light blue
- Overall feeling: cool, shiny, "you earned something special"

Color palette: blues (#DBEAFE, #93C5FD, #2563EB, #1D4ED8), white highlights, silver metallic accents
No text, no characters, no numbers. Just the frame and decorative elements.
```

---

## CARTA ÉPICA 🟣

**Arquivo destino:** `carta-fundo-epica.png`

```
Create a collectible trading card background (400x560px) for a Brazilian elementary school educational app called "sabendo.app".

Style: powerful digital cartoon with energy effects, child-friendly but dramatic, inspired by epic-tier Pokémon EX cards.

Design:
- Outer border: thick purple metallic frame (12px), rounded corners (24px radius), glowing purple inner light (#7C3AED)
- Inner border: dual-tone purple (#5B21B6 to #A78BFA) gradient frame (5px) with subtle shimmer
- Card background: rich purple gradient (top: #2D1B69, bottom: #4C1D95) with magical particle/star field (tiny white dots scattered, some with small cross-sparkle shapes)
- Top area (character zone, ~240x280px): glowing oval, purple-tinted dark background with bright purple edge glow — character will be placed here
- Bottom area: dark purple banner (#1E1B4B) with glowing rune-like decorative pattern or constellation lines in light purple, space for card name
- Corner decorations: ornate crystalline purple gems with radiating light beams (4 corners)
- Background effects: wisps of magical purple energy/smoke floating from bottom, very stylized
- Faint lightning bolt or energy crack patterns in deep purple
- Overall feeling: powerful, magical, "this is something rare and special" — still child-friendly

Color palette: deep purples (#1E1B4B, #4C1D95, #7C3AED), light purples (#A78BFA, #C4B5FD), white sparkles
No text, no characters, no numbers. Just the frame and decorative elements.
```

---

## CARTA LENDÁRIA 🌟

**Arquivo destino:** `carta-fundo-lendaria.png`

```
Create a LEGENDARY collectible trading card background (400x560px) for a Brazilian elementary school educational app called "sabendo.app". This is the rarest, most prestigious card tier.

Style: breathtaking digital illustration with fire, gold and celestial effects — still child-friendly and colorful (NOT dark or scary), inspired by ultra-rare Pokémon VMAX and secret rare cards.

Design:
- Outer border: thick ornate GOLD frame (14px), highly detailed with engraved pattern, rounded corners (24px radius) — the gold should look 3D, embossed, with bright highlights
- Inner border: gradient gold-to-orange (#F59E0B to #FCD34D) with inner rainbow iridescent shimmer (holographic sheen, subtle)
- Card background: dramatic warm gradient (top: #1C0A00, blending to deep red/orange at bottom: #7C2D12) with:
  - Bright golden radial burst from center (sunburst/star rays) in gold and amber
  - Floating embers and sparkles (tiny glowing dots and star shapes) throughout
  - Subtle flame wisps rising from bottom edge in orange/gold
  - Faint constellation or celestial map pattern in deep amber
- Top area (character zone, ~240x280px): glowing golden oval with intense warm light emanating from edges — character will be placed here; background inside oval should be bright warm gold/amber glow
- Bottom area: deep burgundy/gold banner with ornate gold filigree decoration and royal pattern, space for card name
- Corner decorations: elaborate golden crown or star motifs with radiating beams, jewels, very ornate
- Background sheen: holographic rainbow shimmer overlay at ~15% opacity across entire card
- Overall feeling: legendary, epic achievement, "you are the best" — warm, golden, celebratory — like winning a championship

Color palette: gold (#F59E0B, #FCD34D, #B45309), deep reds/oranges (#7C2D12, #9A3412), bright white-gold highlights
No text, no characters, no numbers. Just the frame and decorative elements.
```

---

## ORDEM DE GERAÇÃO

1. `carta-fundo-comum.png`
2. `carta-fundo-rara.png`
3. `carta-fundo-epica.png`
4. `carta-fundo-lendaria.png`

Salvar todas em: `_landing/cartas/`

---

## NOTAS PARA COMPOSIÇÃO (código)

Após geração, cada carta final será montada em código (HTML Canvas ou CSS) com:
1. Fundo gerado aqui
2. Personagem PNG transparente centralizado na zona oval superior
3. Nome do personagem + tema (texto dinâmico)
4. Badge de raridade (ícone + label)
5. Acerto geral (% score)
6. Logo sabendo.app

**Dimensão da zona do personagem:** ~240×280px, centrada horizontalmente, topo em y=40px.
