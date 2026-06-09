# Sistema de Gamificação — Portal sabendo.app (André 5º ano)
**Última atualização:** 2026-06-08

---

## Visão geral

Sistema de 2 camadas por tema:
1. **Reveal progressivo do personagem** — canvas pixelado que se revela a cada atividade concluída pela primeira vez
2. **Reveal cinematográfico da carta** — dispara ao completar todas as atividades (ou ao melhorar a raridade em retry)

> ⚠️ O sistema de "peças" foi descartado. Não existe mais. Não referenciar.

---

## Arquivo principal

`estudos/shared/gamification.js` — módulo IIFE, expõe `window.SabendoGamification.run()`

### GAMI_CONFIG por atividade

```javascript
var GAMI_CONFIG = {
  characterName:   "Prepo",
  characterEmoji:  "🤖",              // fallback se img ausente
  characterImg:    "prepo-hd.png",    // relativo a _landing/
  themeLabel:      "Preposições · Português",
  totalActivities: 8,
  activityType:    "quiz",            // tipo desta atividade (ex: quiz, complete-lacuna, mapa-mental)
  primaryColor:    "#7C3AED",
  lightColor:      "#A78BFA",
  bgColor:         "#F3F0FF",
  glowRgb:         "124,58,237",
  backUrl:         "../../index.html#theme-port-preposicoes",
  // assetBase:    "../../"  (opcional; default "../../")
};
```

> `activityType` é obrigatório para o sistema de reforço adaptativo.
> `characterImg` é relativo a `_landing/` — portraits ficam em `_landing/chars/[slug]-hd.png`.

---

## Camada 1 — Reveal progressivo do personagem

### Estágios (STAGES_8 para temas com 8 atividades)

| Stage | pixelSize | gray% | bright% | Descrição |
|---|---|---|---|---|
| 0 | 42 | 100 | 38 | Bloqueado |
| 1 | 38 | 100 | 42 | Quase nada... |
| 2 | 34 | 100 | 46 | Algo está se formando... |
| 3 | 30 | 95  | 50 | Uma figura misteriosa! |
| 4 | 26 | 88  | 55 | Tomando forma... |
| 5 | 20 | 78  | 61 | Quem será? |
| 6 | 13 | 55  | 72 | Quase lá! |
| 7 |  4 | 15  | 90 | Só falta um toque... |
| 8 |  1 |  0  | 100 | Revelado! |

Curva exponencial (`pow(t, 3.2)`) via `getStages(n)` para temas com N ≠ 8.

### Lógica de progresso

- `fetchProgress()` conta entradas `is_first_attempt = true` no `activity_log` → `completedCount`
- `stageIndex = min(completedCount, totalActivities)`
- `prevStageIndex = isFirstAttempt ? stageIndex - 1 : stageIndex` (retry não avança estágio)

### Animação do modal (showCharModal)

- Canvas 200×240px com `renderPixelated()` (offscreen canvas + `ctx.filter` para grayscale/brightness)
- `requestAnimationFrame` interpolando pixelSize, gray, bright por 700ms (1500ms nos 2 últimos stages)
- **Efeitos na primeira tentativa:**
  - Flash: overlay roxo translúcido (opacity .48), fade-in → fade-out
  - Scan-line: barra de luz varrendo de cima para baixo
  - Wrap-pop: canvas escala para 1.06× e retorna (pulse)
- Retry: renderiza estágio atual direto, sem animação

### Path da imagem

`../../_landing/[characterImg]` (ex: `../../_landing/chars/tempos-verbais-hd.png`)

> ⚠️ Requer `.nojekyll` na raiz do repo — sem ele, GitHub Pages ignora `_landing/` e o canvas fica branco. O `.nojekyll` já existe desde 2026-06-06.

---

## Camada 2 — Reveal cinematográfico da carta

### Quando dispara

- **Primeira conclusão** do tema (prevRarity = null)
- **Raridade melhorou** em retry (ex: Comum → Rara)
- NÃO dispara se o aluno refez atividades sem melhorar a raridade

### Cálculo de raridade (calcRarity)

Lógica: **melhor score por tipo de atividade** (cada `activity_type` tem um "slot")

```
best = { quiz: max_score, complete-lacuna: max_score, ... }
avg = média dos best values
```

| Raridade | Condição |
|---|---|
| ⚪ Comum | avg < 70% |
| 🔵 Rara | avg 70–89% |
| 🟣 Épica | avg ≥ 90% |
| 🌟 Lendária | TODOS os registros com `is_first_attempt=true` E `score=100` |

> **Lendária é exclusiva da 1ª tentativa perfeita.** Se qualquer retry existe na tabela, `allPerfect` falha e Lendária nunca mais é atingível para aquele tema.

### Melhora por repetição

- Aluno refaz só as atividades que foi mal → "slot" atualizado com o melhor score
- Retry na mesma sessão NÃO altera o score salvo (`_capturedScore` travado no primeiro `showBtn()`)
- Retry em nova sessão salva novo score com `is_first_attempt = false` → melhora o slot

### Sequência de animação (showReveal)

Backdrop escurece → "NOVA CARTA OBTIDA" letra a letra → carta entra com spring → flash (tier) → partículas burst → carta flutua → nome do tier → "toque para continuar"

### REVEAL_TIERS

| Tier | Flash | Shockwave | Raios | Partículas |
|---|---|---|---|---|
| `comum` | — | — | — | 28 círculos cinza |
| `rara` | — | — | — | 45 sparks azuis |
| `epica` | — | ✓ | — | 60 círculos roxos |
| `lendepica` | roxo/dourado | ✓ (double) | — | 75 mixed arco-íris |
| `lendaria` | branco | — | 14 raios dourados | 95 estrelas 4 pontas + double burst |
| `revisional` | verde | — | — | confetti verde/branco |

### Fundos das cartas

`_landing/cartas/carta-fundo-[tier].png`

Tiers ativos: `comum`, `rara`, `epica`, `lend-epica`, `lendaria`, `revisional`

Tiers criados para uso futuro (condições não definidas): `super`, `secreta`, `super-secreta`, `holistica`, `morango`, `preporiana`, `pessego`, `abacaxi`, `kiwi`, `maca`, `uva`, `melancia`, `banana`

---

## Snippet `<!-- concluir-btn -->` nas atividades

Padrão aplicado em todos os HTMLs de atividade (exceto `mapa-mental` e `tabuada`):

```javascript
var _capturedScore = null;
function showBtn() {
  if (btn.style.display === "none") {
    // Primeira vez: trava o score (anti-cheat)
    _capturedScore = (typeof window.sabendoScore === "number") ? Math.round(window.sabendoScore) : null;
    btn.style.display = "block";
  } else if (_capturedScore !== null) {
    // Retry na mesma sessão: avisa que a nota está travada
    btn.textContent = "✓ Nota desta sessão: " + _capturedScore + "% · Concluir";
    btn.style.background = "linear-gradient(135deg,#059669,#34D399)";
  }
}
```

- `window.sabendoScore` deve ser setado pela atividade quando o resultado aparece (0–100)
- MutationObserver detecta quando elemento com id/class contendo "result/score/gabarito" fica visível
- Ao clicar em Concluir: verifica `is_first_attempt`, insere em `activity_log`, atualiza `streaks`, chama `SabendoGamification.run()`
- Botão "← [Tema]" fixo desktop (top:16px left:16px), fluxo normal mobile (≤640px)

---

## THEME_CATALOG — wiring de personagens

No `index.html` (linha ~2308), cada tema tem `charImg` e `charName` que alimentam a carta:

```javascript
{ disc:'port', slug:'preposicoes', ..., charName:'Prepo', charImg:'prepo-hd.png' }
{ disc:'port', slug:'teatral',     ..., charName:'Prof. Teatrão', charImg:'chars/teatral-hd.png' }
```

`charImg` é relativo a `_landing/`. Prepo usa `prepo-hd.png` (raiz); todos os outros usam `chars/[slug]-hd.png`.

---

## Sistema de Reforço Adaptativo ("Para reforçar")

**Objetivo:** identificar conceitos não sedimentados na 1ª tentativa e reapresentá-los após intervalo de tempo.

> Independente da carta — o aluno pode ter melhorado a carta por retry, mas o reforço persiste porque o diagnóstico é feito pela 1ª tentativa.

### Regras de disparo

- **Fonte:** `activity_log` com `is_first_attempt = true` e `score < 80%`
- **Elegíveis:** todos os tipos EXCETO `mapa-mental`
- **Gatilho:** ao concluir **todas** as atividades de um tema pela primeira vez
- **Intervalo:** `due_date = completed_at + 5 dias`

### Schema da tabela `reinforcement_queue`

```sql
CREATE TABLE reinforcement_queue (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         uuid REFERENCES auth.users NOT NULL,
  theme_slug      text NOT NULL,
  activity_type   text NOT NULL,
  first_score     int NOT NULL,
  triggered_at    timestamptz NOT NULL DEFAULT now(),
  due_date        timestamptz NOT NULL,
  resolved_at     timestamptz,
  UNIQUE (user_id, theme_slug, activity_type)
);
```

### Lógica de resolução

- Item resolvido quando: nova sessão + `score >= 80%` + `due_date <= now()`
- Se refizer antes do `due_date`: NÃO conta (memória ainda fresca)
- Ao resolver **todos** os itens de um tema: dispara reveal da **Carta Revisional**

### UX — Bloco "⚡ Para reforçar"

Visível no painel quando `due_date <= now()` e `resolved_at IS NULL`:

```
⚡ Para reforçar
  Preposições · Português
    › Quiz — sua nota na 1ª vez: 65%            [Refazer]
    › Complete Lacuna — sua nota na 1ª vez: 72%  [Refazer]
```

Ordenado por `first_score ASC`. Itens futuros (`due_date > hoje`) não aparecem.

---

## Tabelas Supabase

| Tabela | Papel |
|---|---|
| `activity_log` | Fonte de verdade — score, is_first_attempt, activity_type, theme_slug |
| `cards` | Carta salva por tema (upsert ao completar ou melhorar raridade) |
| `streaks` | Dias seguidos e total de atividades |
| `reinforcement_queue` | Fila de reforço adaptativo (RLS ativa) |
| `profiles` | user_id, portal, year |
| `pieces` | Legada — não usada |

---

## Painel de Coleção de Cartas

Tela no portal que exibe todas as cartas obtidas pelo aluno, organizadas por tema. Implementada e em produção.

- Cada carta mostra o personagem, nome do tema, raridade e data de obtenção
- Acessível a partir do portal principal

---

## Roadmap

| Status | Item |
|---|---|
| ✅ | Reveal progressivo do personagem (canvas pixelado, 9 estágios) |
| ✅ | Reveal cinematográfico da carta (5 tiers de raridade + revisional) |
| ✅ | Cálculo de raridade por melhor score por tipo |
| ✅ | Reforço adaptativo V1 (tabela + populate + resolve + Carta Revisional) |
| ✅ | THEME_CATALOG com charImg para todos os 25 temas |
| ✅ | 23 portraits HD em `_landing/chars/` |
| ✅ | Bloco "Para reforçar" no portal |
| ✅ | Tela de coleção de cartas no portal |
| ✅ | Gamificação validada em produção (piloto: Preposições — snippet em todos os 8 HTMLs) |
| ⏳ | Snippet "concluir-btn" nos demais 24 temas (pronto para implantação) |
| ⏳ | Condição de disparo para Lend-Épica |
| ⏳ | Reforço V2 — atividade diferente sobre o mesmo conceito |
