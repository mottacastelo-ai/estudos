# PROMPT — Sprite Sheet de Peças do Prepo
## Para: Codex Desktop (GPT Image Generation)
## Output esperado: `prepo-pecas-sheet.png` → salvar em `_landing/`

---

## OBJETIVO

Gerar um **sprite sheet 4×4** com as 16 partes isoladas do robô Prepo.
Cada célula contém UMA parte do corpo do Prepo, no mesmo estilo da imagem canônica.
O resultado será usado no portal educacional para animar a "montagem" do personagem.

---

## REFERÊNCIA VISUAL OBRIGATÓRIA

Usar a imagem canônica do Prepo que está na pasta de personagens (`Prepo.png`).
O Prepo é um robô arredondado, roxo/azul escuro, cartunesco, com:
- Corpo redondo volumoso com placa "PREPO" no centro
- Dois olhos redondos com brilho
- Antenas nas laterais do topo da cabeça
- Braços curtos e expressivos erguidos
- Pernas curtas com base larga
- Traço bold cartoon, iluminação suave, estilo amigável para crianças

---

## LAYOUT DO SPRITE SHEET

**Dimensões totais:** 800 × 800 px  
**Grade:** 4 colunas × 4 linhas = 16 células  
**Tamanho de cada célula:** 200 × 200 px  
**Fundo:** branco (#FFFFFF)  
**Separação entre células:** linha cinza claro fina (1px, #E5E7EB) — opcional  

### Ordem das células (esquerda→direita, cima→baixo):

```
Linha 1: [Antena D]    [Antena E]    [Conector D]   [Conector E]
Linha 2: [Topo cabeça] [Face]        [Olho D]       [Olho E]
Linha 3: [Boca]        [Ombros]      [Corpo]        [Placa PREPO]
Linha 4: [Braço D]     [Braço E]     [Perna D]      [Perna E]
```

---

## ESPECIFICAÇÕES POR PARTE

Cada parte deve:
- Estar **centralizada** na sua célula de 200×200px
- Ter **fundo branco** na célula (sem transparência necessária)
- Ocupar ~60–75% da célula (não muito pequena, não cortada)
- Ser fiel ao estilo canônico (mesma cor, traço, volumetria)
- Parecer uma **peça de robô recortada** — como se fosse uma placa de alumínio ou peça de encaixe
- Ter uma **borda roxa sutil** ou contorno que a distingue como peça isolada (opcional mas recomendado)
- Pequena **sombra projetada** para dar profundidade de peça 3D (shadow: bottom-right, suave)

### Descrição de cada peça:

**Antena D** (linha 1, col 1)
Antena direita do Prepo — haste fina roxa com bolinha na ponta, levemente curvada. Parte superior da cabeça.

**Antena E** (linha 1, col 2)  
Antena esquerda — espelho da Antena D.

**Conector D** (linha 1, col 3)  
Conector lateral direito da cabeça — pequena estrutura arredondada roxa que conecta a cabeça ao corpo. Vista lateral.

**Conector E** (linha 1, col 4)  
Espelho do Conector D, lado esquerdo.

**Topo cabeça** (linha 2, col 1)  
Parte superior da cabeça redonda do Prepo — meia-esfera roxa escura com textura metálica suave. Onde as antenas se encaixam.

**Face** (linha 2, col 2)  
Painel frontal da cabeça — placa roxa/cinza com a área dos olhos e boca (os olhos e boca aparecem como encaixes/buracos nesta peça).

**Olho D** (linha 2, col 3)  
Olho direito do Prepo — esfera arredondada branca com íris roxa e brilho. Parece uma lente de câmera robótica.

**Olho E** (linha 2, col 4)  
Espelho do Olho D.

**Boca** (linha 3, col 1)  
Boca do Prepo — painel retangular levemente arredondado com linha de "smile" roxa/escura. Peça de encaixe frontal.

**Ombros** (linha 3, col 2)  
Peça de ombros — estrutura em "T" roxa que conecta a cabeça ao corpo e aos braços. Formato de shoulder pad robótico.

**Corpo** (linha 3, col 3)  
Torso principal do Prepo — a grande esfera central roxa com textura volumosa. Sem a placa PREPO (ela é separada).

**Placa PREPO** (linha 3, col 4)  
Placa retangular brilhante com o texto "PREPO" em letras brancas bold, estilo plaquinha de identificação robótica. Bordas arredondadas, fundo roxo escuro.

**Braço D** (linha 4, col 1)  
Braço direito do Prepo — estrutura curta arredondada, posição levantada/expressiva como no canônico. Sem mão separada (a garra/ponta faz parte).

**Braço E** (linha 4, col 2)  
Espelho do Braço D.

**Perna D** (linha 4, col 3)  
Perna direita — estrutura curta roxa com base larga e estável. Vista frontal.

**Perna E** (linha 4, col 4)  
Espelho da Perna D.

---

## PROMPT PARA COLAR NO CODEX

```
Create a clean 800x800px sprite sheet with a 4x4 grid (16 cells, each 200x200px) on a white background.
Each cell contains one isolated body part of "Prepo", a friendly purple cartoon robot mascot for a Brazilian elementary school educational portal.

Reference the Prepo.png canonical image for style consistency. Prepo has: rounded purple/dark-indigo body, white round eyes with purple irises, short expressive arms raised up, short wide legs, a "PREPO" nameplate on the chest, two thin antennas on top, and a bold cartoon style with soft shading.

Grid layout (left to right, top to bottom):
Row 1: Right Antenna, Left Antenna, Right Side Connector, Left Side Connector
Row 2: Top of Head (dome), Face Panel, Right Eye, Left Eye
Row 3: Mouth Panel, Shoulder Piece, Main Body Sphere, PREPO Nameplate
Row 4: Right Arm, Left Arm, Right Leg, Left Leg

Each part must:
- Be centered in its 200x200 cell
- Fill about 65% of the cell (not cropped, not too small)
- Match Prepo's exact color palette (deep purple #1e1b4b to #7C3AED, white accents)
- Look like a removable robot panel/piece with a subtle purple outline and soft drop shadow
- White cell background (#FFFFFF)
- Optional: thin light gray divider lines between cells

Style: Bold cartoon, flat shading with highlights, child-friendly, same art style as canonical Prepo. No text labels needed inside cells.
```

---

## INSTRUÇÕES DE USO

1. Abra a imagem canônica `Prepo.png` como referência visual na sessão do Codex
2. Cole o prompt acima
3. Se o resultado não bater com o estilo canônico, peça regeneração com: *"Keep exact same art style as the Prepo reference, more consistent colors"*
4. Salve o output como `prepo-pecas-sheet.png` na pasta `_landing/`

---

## COORDENADAS NO CÓDIGO (para uso no portal)

Após gerar a imagem, as coordenadas de cada peça no sprite (origem top-left da célula):

| ID   | Nome          | x  | y   | w   | h   |
|------|---------------|-----|-----|-----|-----|
| p1   | Antena D      | 0   | 0   | 200 | 200 |
| p2   | Antena E      | 200 | 0   | 200 | 200 |
| p3   | Conector D    | 400 | 0   | 200 | 200 |
| p4   | Conector E    | 600 | 0   | 200 | 200 |
| p5   | Topo cabeça   | 0   | 200 | 200 | 200 |
| p6   | Face          | 200 | 200 | 200 | 200 |
| p7   | Olho D        | 400 | 200 | 200 | 200 |
| p8   | Olho E        | 600 | 200 | 200 | 200 |
| p9   | Boca          | 0   | 400 | 200 | 200 |
| p10  | Ombros        | 200 | 400 | 200 | 200 |
| p11  | Corpo         | 400 | 400 | 200 | 200 |
| p12  | Placa PREPO   | 600 | 400 | 200 | 200 |
| p13  | Braço D       | 0   | 600 | 200 | 200 |
| p14  | Braço E       | 200 | 600 | 200 | 200 |
| p15  | Perna D       | 400 | 600 | 200 | 200 |
| p16  | Perna E       | 600 | 600 | 200 | 200 |
