# Portrait HD — Xis
## Tema: Os Quatro Sons da Letra X (e o CH) · Português 5º ano
## Destino: `_landing/chars/sons-x-ch-hd.png`

---

## INSTRUÇÕES PARA O CODEX

1. Léo fornece imagem de referência da folha de personagens do Xis (gerada antes, em `Personagens\5o ano\Xis.png`)
2. Use a referência **apenas para identidade visual** — não copie a folha completa nem as 4 poses
3. Gere um portrait novo, isolado, com UMA pose unificadora que mostre o Xis equilibrando todos os 4 chapéus
4. Remova o fundo chroma-key verde com a ferramenta local
5. Salve em `_landing/chars/sons-x-ch-hd.png`

---

## PROMPT

```
Generate a NEW full-body character portrait of "Xis",
a character from a Brazilian 5th-grade educational comic book about
the four different sounds of the letter X in Portuguese.

USE THE REFERENCE IMAGE (character sheet) only to maintain visual identity.
DO NOT reproduce the character sheet layout. Create a fresh, clean, isolated pose.

CHARACTER IDENTITY (from reference):
- Xis IS the capital letter X brought to life — two diagonal bars crossing
  in the middle forming the classic X shape
- Body color: vibrant purple #7C3AED with thick dark purple outline #4C1D95
- Two big round white eyes with black pupils placed on the two upper arms of the X
- Thin expressive black eyebrows, wide expressive mouth at the central crossing
- Short light-purple #A78BFA arms emerging from the side arms of the X, with
  white four-fingered hands
- Short dark-purple legs from the lower arms, with rounded black shoes
- Personality: theatrical, dramatic stage actor — loves presenting words like
  he is on a Broadway show

THE FOUR HATS (each represents a sound):
- Blue taxi-driver cap #2563EB with white band labeled "TÁXI" → sound /ks/ (táxi)
- Purple magician's top hat #7C3AED with golden #FCD34D band + small yellow
  stars → sound /sh/ (lixo, same as CH digraph)
- Green modern cap #16A34A with yellow #FCD34D side stripe → sound /z/ (exemplo)
- Orange wrinkled scholar hat #EA580C with thin white band → sound /ss/ (auxílio)

ISOLATION RULES — mandatory:
- No background scenery
- No speech bubbles
- No text or labels
- No other characters
- No props beyond the four hats

BACKGROUND: solid chroma-key green #00ff00, completely uniform.
IMPORTANT: do NOT use green #00ff00 on any part of the character
(the green cap is #16A34A — clearly a different green).

POSE: Xis stands centered in a confident theatrical pose with arms wide open
like a magician about to perform. He wears the PURPLE MAGICIAN HAT on his head
(this is his signature/most iconic hat). The OTHER THREE HATS float in a circular
arc around him: the BLUE TAXI CAP to his upper-left, the GREEN MODERN CAP to
his upper-right, and the ORANGE SCHOLAR HAT centered above his head. Small
sparkles and stars around him suggest magic/showmanship.
Big confident smile, expressive eyes looking forward.
Full body visible from head to feet.
Character centered, occupying approximately 85% of the frame height.

STYLE:
- Vibrant Brazilian children's educational comic book style
- Bold outlines, clean cel-shading, bright saturated colors
- Exaggerated, expressive, slightly cartoonish proportions
- Theatrical lighting — soft warm spotlight from above

OUTPUT: PNG, canvas exactly 1024×1024 px.
After generation: remove chroma-key background, save as sons-x-ch-hd.png
```

---

## CHECKLIST PÓS-GERAÇÃO

- [ ] Fundo removido (transparente)
- [ ] Personagem centralizado, corpo inteiro visível
- [ ] Canvas 1024×1024
- [ ] Os 4 chapéus visíveis (1 na cabeça + 3 flutuando)
- [ ] Cores dos chapéus corretas (azul/roxo/verde/laranja)
- [ ] Nenhum artefato de fundo verde restante no personagem
- [ ] Arquivo salvo em `_landing/chars/sons-x-ch-hd.png`

---

## NOTAS

- A pose unificadora com o chapéu roxo na cabeça + 3 chapéus flutuando comunica
  imediatamente "este personagem tem MÚLTIPLOS sons" — funciona como tooltip
  visual no portal
- O verde do chapéu (#16A34A) é diferente do chroma-key (#00ff00); se a remoção
  de fundo apagar parte do chapéu verde, refazer com chroma-key magenta #FF00FF
  como alternativa
- Personagem usa a paleta primária de Português (#7C3AED) — coerente com a cor
  da disciplina no portal
