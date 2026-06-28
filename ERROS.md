# ERROS.md — Registro de Bugs Diagnosticados

Bugs já encontrados em produção. A squad deve consultar este arquivo antes de gerar atividades para não repetir os mesmos erros.

---

## ERR-001 — Botão "Concluir atividade" não aparecia em nenhuma atividade

**Arquivos afetados:** todos os ~120 HTMLs com `<!-- concluir-btn -->`
**Data:** 2026-06-13
**Tipo:** Arquitetural — snippet `concluir-btn`

### Causa raiz

O snippet usava exclusivamente um `MutationObserver` que só chamava `showBtn()` quando detectava um elemento com `id` ou `class` contendo `result`, `score` ou `gabarito` ficando visível. A grande maioria dos painéis de resultado usava nomes como `feedback-panel`, `resultado-area`, `gabarito-box` — que não batiam no regex — então o botão nunca aparecia.

Além disso, a maioria das atividades não setava `window.sabendoScore`, então o score gravado no banco seria `null`.

### Correção aplicada (2026-06-13)

Substituição arquitetural em todos os 120 arquivos:

1. **`Object.defineProperty` em `window.sabendoScore`** — qualquer `window.sabendoScore = X` em qualquer lugar da atividade agora dispara `showBtn()` automaticamente, sem depender de naming convention.
2. **MutationObserver mantido como fallback** com regex expandida: `result|score|gabarito|feedback|correc`.
3. **`window.sabendoScore` adicionado em 69 arquivos** que não tinham — calculado proporcional aos acertos no ponto correto (antes de exibir o resultado).
4. **CLAUDE.md atualizado** com o novo snippet canônico.

### Regra para a squad (pós-correção)

A atividade **DEVE** fazer `window.sabendoScore = pct` (número 0–100) no momento em que o resultado aparece. O setter dispara o botão automaticamente. Não é mais necessário seguir nenhuma convenção de id/class para o painel.

```js
// ✅ CORRETO — basta setar o score; o botão aparece automaticamente
var acertos = respostas.filter(function(r) { return r.correta; }).length;
window.sabendoScore = Math.round((acertos / total) * 100);
panel.style.display = 'block';   // id do painel não importa mais

// ❌ ERRADO (padrão antigo) — dependia do id/class do painel
var panel = document.getElementById('feedback-panel');
panel.style.display = 'block';   // botão nunca aparecia
```

Para criadores/wizards sem score: `window.sabendoScore = 100; document.dispatchEvent(new Event('sabendo:criador-done'));`

---

---

## ERR-002 — "Carta comum com acerto geral 0%" mesmo com respostas corretas

**Arquivos afetados:** atividades com botão "Ver gabarito" independente (antes de `window.sabendoScore` ser setado)
**Data:** 2026-06-15
**Tipo:** Race condition — MutationObserver vs. setter de score

### Causa raiz

O MutationObserver do snippet dispara `showBtn()` quando qualquer elemento com `id`/`class` contendo `result|score|gabarito|feedback|correc` fica visível. Callbacks de MO são microtasks — disparam DEPOIS da call stack síncrona atual.

O problema ocorria quando:
1. O aluno abre o gabarito via botão independente (ex: "Ver gabarito") — MO dispara
2. `window.sabendoScore` ainda não foi setado (null/undefined)
3. Versão antiga de `showBtn()` capturava `_capturedScore = null` e mostrava o botão
4. Quando o score era setado depois, o botão já estava visível → `_capturedScore` não era atualizado (anti-cheat)
5. Score `null` era gravado no banco → `calcRarity()` ignorava o null → `avg=0` → "carta comum 0%"

### Correção aplicada (2026-06-15)

**Fix global (100 arquivos via PowerShell):** null guard em `showBtn()`:

```javascript
// ANTES (bugado)
function showBtn() {
  if (btn.style.display === "none") {
    _capturedScore = (typeof window._sabendoScoreInternal === "number") ? Math.round(window._sabendoScoreInternal) : null;
    btn.style.display = "block";
  }
}

// DEPOIS (correto)
function showBtn() {
  if (typeof window._sabendoScoreInternal !== "number") return;
  if (btn.style.display === "none") {
    _capturedScore = Math.round(window._sabendoScoreInternal);
    btn.style.display = "block";
  }
}
```

O null guard garante que o botão nunca aparece antes do score estar disponível. O setter (`Object.defineProperty`) já chama `showBtn()` automaticamente quando `window.sabendoScore = pct` é executado.

**Fix per-arquivo (`rotulador-ciclo-da-agua.html`):** `window.sabendoScore = pct` estava em `updateScore()`, chamada a cada acerto parcial. Movido para `showFinal()` (100% ao completar) e para o toggle do gabarito (score atual como "desistência").

### Padrão seguro vs. inseguro

```javascript
// ✅ SEGURO — score setado ANTES do elemento gabarito aparecer
function revealGabarito() {
  window.sabendoScore = pct;  // setter dispara showBtn() AGORA
  elem.style.display = 'block';  // MO dispara depois, mas botão já visível → no-op
}

// ✅ SEGURO — score e gabarito setados na MESMA call stack síncrona
function checkAllDone() {
  if (done) {
    window.sabendoScore = pct;  // setter síncrono
    gabElem.classList.add('show');  // MO é microtask, vem depois → no-op
  }
}

// ❌ INSEGURO (sem null guard) — gabarito aparece em handler separado antes do score
document.getElementById('btn').addEventListener('click', function() {
  gabElem.classList.add('show');  // MO dispara → showBtn() → _capturedScore=null
  // score só é setado mais tarde, em outro evento
});

// ✅ SEGURO (com null guard) — mesmo cenário anterior, mas null guard bloqueia
// O MO dispara mas showBtn() retorna early porque score ainda não é number.
// Quando score é setado depois, o setter dispara showBtn() corretamente.
```

### Regra para a squad (pós-correção)

- Atividades com **gabarito independente** (botão "Ver gabarito" sem condição): sempre setar `window.sabendoScore` ANTES de mostrar o elemento gabarito.
- Atividades com **score incremental** (ex: arrastar, preencher): NÃO usar `window.sabendoScore = pct` em funções intermediárias — somente na função de conclusão final (e no toggle do gabarito como fallback de "desistência").
- O null guard no `showBtn()` é a última linha de defesa, mas não substitui a disciplina de setar o score no lugar certo.

---

## ERR-003 — Portal travado em modo retrato no tablet após instalação do PWA

**Arquivos afetados:** `manifest.json`
**Data:** 2026-06-18
**Tipo:** Configuração PWA — `orientation` incorreto

### Causa raiz

Durante a implementação do banner de instalação PWA (commit `c5171c7`), o campo `"orientation"` foi definido como `"portrait-primary"` no `manifest.json`. Esse valor instrui o sistema operacional a **travar o app em retrato permanentemente**, impedindo qualquer rotação no tablet do André.

### Correção aplicada (2026-06-18)

```json
// ANTES (bugado)
"orientation": "portrait-primary"

// DEPOIS (correto)
"orientation": "any"
```

O valor `"any"` permite rotação livre — retrato e paisagem — respeitando o bloqueio físico do dispositivo.

### Atenção pós-correção

- **Android (Chrome)**: o manifest é re-fetchado automaticamente a cada ~24h ou no próximo lançamento. A correção propaga sozinha — assim como o bug propagou sem reinstalar.
- **iOS (Safari)**: o manifest é cacheado no momento da instalação. Nesse caso sim é necessário desinstalar e reinstalar.

### Regra para a squad

O `manifest.json` **nunca deve ser alterado** sem revisar cada campo individualmente. O campo `orientation` deve permanecer `"any"` para apps educacionais com suporte a tablet.

---

## ERR-004 — `sabendoScore` acima de 100% em atividades

**Arquivos afetados:** `matematica/multiplos-divisores-criterios/complete-lacuna-multiplos-divisores-criterios.html`, `domino-multiplos-divisores-criterios.html`
**Data:** 2026-06-27
**Tipo:** Cálculo de score — dupla multiplicação por 100

### Causa raiz

Dois padrões de erro distintos, ambos resultando em scores salvos acima de 100 no banco (ex: 9000%), que se propagam para o display "Acerto: X%" na carta de gamificação.

**Padrão A — `pct` já é porcentagem, mas é multiplicado por 100 de novo:**
```javascript
// ❌ BUGADO
const pct = (totalScore / realMax) * 100;  // pct é 0–100
window.sabendoScore = Math.round(pct * 100); // salva até 10000

// ✅ CORRETO
window.sabendoScore = Math.round(pct); // pct já é 0–100
```

**Padrão B — score setado na função errada (progresso parcial em vez de resultado final):**
```javascript
// ❌ BUGADO — chamado a cada seção concluída, usa progresso (0/3, 1/3...) não acerto
function updateProgress() {
  const pct = (sectionsDone / 3) * 100;
  window.sabendoScore = Math.round(pct * 100); // duplo bug: timing + double-multiply
}

// ✅ CORRETO — score setado em showResult() com o acerto real
function showResult() {
  const pct = (totalScore / 22) * 100;
  window.sabendoScore = Math.round(pct);
}
```

### Regra para a squad

Antes de setar `window.sabendoScore`, checar:

1. **`pct` é fração (0–1)?** → usar `Math.round(pct * 100)`
2. **`pct` é porcentagem (0–100)?** → usar `Math.round(pct)` ou `pct` diretamente
3. **O setter está em `showResult()` / função de conclusão final?** → nunca em funções de progresso parcial

Regra de ouro: `window.sabendoScore` deve ser sempre um inteiro entre 0 e 100.

---

## Checklist anti-bug para `gerador-atividades`

Antes de finalizar qualquer arquivo HTML de atividade, verificar:

- [ ] A atividade chama `window.sabendoScore = pct` (0–100) antes de exibir o resultado? (se `pct` for fração 0–1, usar `Math.round(pct * 100)`; se já for 0–100, usar `Math.round(pct)` — nunca `Math.round(pct * 100)` quando pct já é porcentagem)
- [ ] Se houver botão "Ver gabarito" independente: `window.sabendoScore` é setado ANTES de mostrar o elemento?
- [ ] Se o score é incremental (acertos parciais): `window.sabendoScore` só é setado na conclusão final (não a cada acerto)?
- [ ] Para criadores: `window.sabendoScore = 100` + `document.dispatchEvent(new Event('sabendo:criador-done'))` na última etapa?
- [ ] Nenhuma `var` global usa nome proibido (`history`, `name`, `location`, `event`, `status`, `top`)?
- [ ] O snippet `<!-- concluir-btn -->` está presente antes de `</body>`?
- [ ] `DISCIPLINE`, `THEME_SLUG` e `ACTIVITY_TYPE` no snippet estão corretos?
- [ ] `totalActivities` no `GAMI_CONFIG` está correto para o tema?
- [ ] A cor do botão (`btn.style.cssText`) usa a cor primária da disciplina correta?
