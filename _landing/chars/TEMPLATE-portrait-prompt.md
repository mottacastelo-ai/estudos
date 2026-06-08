# Template Padrão — Portrait HD de Personagem
## Portal Educacional 5º Ano · sabendo.app

> Copie este template para cada novo personagem.
> Preencha as seções marcadas com [PREENCHER].
> Lições aprendidas com Professor Teatrão incorporadas.

---

## INSTRUÇÕES PARA O CODEX

1. Léo fornece imagem de referência do quadrinho com o personagem
2. Use a referência **apenas para identidade visual** — não copie a cena
3. Gere um portrait novo, isolado, conforme prompt abaixo
4. Remova o fundo chroma-key verde com a ferramenta local
5. Salve em `_landing/chars/[SLUG]-hd.png`

---

## PROMPT PADRÃO

```
Generate a NEW full-body character portrait of "[NOME DO PERSONAGEM]", 
a character from a Brazilian 5th-grade educational comic book.

USE THE REFERENCE IMAGE only to maintain visual identity. 
DO NOT reproduce the comic panel scene. Create a fresh, clean, isolated pose.

CHARACTER IDENTITY (extracted from reference):
[DESCREVER: cabelo, expressão, roupa, elemento mais marcante, estilo geral]

ISOLATION RULES — mandatory:
- No background scenery
- No speech bubbles
- No text or labels
- No other characters
- No props or background objects

BACKGROUND: solid chroma-key green #00ff00, completely uniform.
IMPORTANT: do NOT use green #00ff00 on any part of the character.

POSE: create a new expressive pose that reflects the character's personality.
Full body visible from head to feet.
Character centered, occupying approximately 85% of the frame height.

STYLE:
- Vibrant Brazilian children's educational comic book style
- Bold outlines, clean cel-shading, bright saturated colors
- Exaggerated, expressive, slightly cartoonish proportions

OUTPUT: PNG, canvas exactly 1024×1024 px.
After generation: remove chroma-key background, save as [SLUG]-hd.png
```

---

## CHECKLIST PÓS-GERAÇÃO

- [ ] Fundo removido (transparente)
- [ ] Personagem centralizado, corpo inteiro visível
- [ ] Canvas 1024×1024 (ou maior se necessário — mínimo é 1024)
- [ ] Nenhum artefato de fundo verde restante
- [ ] Arquivo salvo em `_landing/chars/[SLUG]-hd.png`

---

## LIÇÕES APRENDIDAS (Professor Teatrão — 07/06/2026)

1. **"Use a referência apenas para identidade"** — não pedir para copiar o painel evita que o modelo tente reproduzir a cena completa com balões e cenário
2. **Fundo chroma-key verde #00ff00** em vez de "transparent background" — ferramentas de geração não produzem transparência nativa; o fluxo correto é gerar em verde e remover localmente
3. **Personagem isolado explicitamente** — listar tudo que NÃO deve aparecer (cenário, balões, texto, outros personagens)
4. **Canvas exatamente 1024×1024** — "mínimo" permite variações; se precisar tamanho exato, especificar "canvas final exatamente 1024×1024"
5. **Pose nova autorizada** — dar liberdade de pose melhora muito o resultado visual
