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

## ERR-006 — Atividades de temas novos nunca marcam como "concluído"

**Arquivos afetados:** `index.html` — todos os 5 temas do Capítulo 6 de Português (fabulas-conflito-moral, conjuncoes, dicionario-verbetes, poema-visual-onomatopeias, acentuacao-paroxitonas-proparoxitonas)
**Data:** 2026-08-22
**Tipo:** Checklist incompleto no `atualizador-index`

### Causa raiz

O `index.html` tem **duas estruturas diferentes** para registrar um tema: o `THEME_CATALOG`/`ACTIVITY_FILE_PATHS` (usados para navegação e gamificação de reforço) e o `HREF_MAP` dentro de `loadActivityStatus()` (usado exclusivamente para consultar o Supabase e desenhar o badge de "concluído" em cada `act-card`). O agente `atualizador-index` sempre atualizou a primeira estrutura, mas o arquivo de definição do agente nunca mencionava o `HREF_MAP` — então ele nunca era atualizado para temas novos. Resultado: o aluno completa a atividade normalmente (gravação no Supabase funciona), mas o portal nunca mostra o badge de concluído porque a busca `HREF_MAP[href]` retorna `undefined` para qualquer href de tema novo.

Esse bug ficou 3 horas em produção sem detecção até Léo notar que os temas do André não ficavam marcados.

### Correção aplicada (2026-08-22)

Adicionadas manualmente 20 entradas ao `HREF_MAP` (4 atividades × 5 temas). `.claude/agents/atualizador-index.md` atualizado com uma seção dedicada e obrigatória sobre o `HREF_MAP`, incluindo o passo no procedimento numerado (não apenas uma menção solta).

### Regra para a squad

- **Todo tema novo exige uma entrada no `HREF_MAP` por atividade** — nunca presumir que atualizar `THEME_CATALOG`/`ACTIVITY_FILE_PATHS` é suficiente para a gamificação funcionar.
- O `activity_type` na entrada do `HREF_MAP` deve ser conferido no arquivo HTML real (`var ACTIVITY_TYPE = "..."` dentro do snippet `concluir-btn`), nunca assumido pelo nome do arquivo.
- Após qualquer atualização de `index.html` para um tema novo, validar a sintaxe do `HREF_MAP` (objeto JS bem formado) antes de considerar a tarefa concluída.

---

## ERR-005 — Defeitos recorrentes na geração de HQ via Codex MCP

**Arquivos afetados:** prompts de HQ (`.md`) e imagens geradas (`pg1–pg4.png`, portraits)
**Data:** 2026-08-22
**Tipo:** Qualidade visual + integridade de imagem — Codex MCP (geração de HQs educacionais)

Quatro defeitos foram encontrados ao gerar 5 HQs novas em sessão única. Todos precisam de prevenção ativa no `gerador-hq-prompt` (ao escrever os prompts) e no `gerador-hq-imagens` (ao validar as saídas). Revisão manual pós-hoc não é solução aceitável.

---

### ERR-005a — Portrait com fundo chroma-key não removido

**Ocorrência:** 4 de 5 portraits (Acentin, Elo, Ziguinho, Dicio). Só Morá saiu correto na primeira tentativa.

**Causa raiz:** O Codex reporta verbalmente "fundo removido" mas a remoção efetiva não ocorreu — o pixel do canto do arquivo salvo mantém RGB(0,255,0) com Alpha=255 (opaco), provando que o canal alfa não foi processado. Aceitar a confirmação textual do Codex sem verificar o arquivo é a causa direta do defeito não ser detectado antes da publicação.

**Correção aplicada:** Reprocessamento explícito de cada portrait afetado, pedindo remoção real do canal alfa com verificação pixel a pixel.

**Regra para a squad:**
- Após cada portrait gerado, verificar o pixel do canto superioresquerdo via PowerShell ou Python antes de considerar concluído.
- Critério de aprovação: pixel do canto deve ter Alpha=0 (transparente). Alpha=255 com cor verde = falha silenciosa do Codex.
- Nunca confiar apenas na resposta textual do Codex para validação de transparência.

```powershell
# Verificação rápida de transparência do portrait
Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Bitmap]::new("C:\caminho\portrait.png")
$px = $img.GetPixel(0, 0)
if ($px.A -ne 0) { Write-Host "FALHA: fundo não removido (A=$($px.A), R=$($px.R), G=$($px.G), B=$($px.B))" }
else { Write-Host "OK: fundo transparente" }
$img.Dispose()
```

---

### ERR-005b — Painéis de HQ sem cenário (fundo branco/liso tipo flashcard)

**Ocorrência:** 2 de 5 temas (Conjunções, Acentuação). Painéis saíram com fundo branco ou gradiente simples, sem nenhum elemento de cenário ilustrado.

**Causa raiz:** O prompt de HQ usava instrução genérica de estilo no topo do arquivo ("adicione cenário à HQ") mas não especificava cenário no prompt individual de cada painel. O Codex ignora instruções genéricas quando não são reforçadas localmente — a instrução geral não é suficiente.

**Correção aplicada:** Reprocessamento dos painéis afetados com descrição de cenário explícita e individualizada em cada um.

**Regra para a squad:**
- Todo prompt de painel individual DEVE conter pelo menos 3–4 elementos de cenário concretos descritos explicitamente (exemplos: estante de livros, janela com cortina, lousa com texto, plantas, cartazes coloridos na parede, cadeiras e mesas escolares, janela com vista de parque, etc.).
- A instrução de cenário no cabeçalho do arquivo (`## ESTILO VISUAL`) é necessária mas não suficiente — ela não garante que o Codex aplique o cenário painel a painel.
- Nunca deixar a descrição de cenário de um painel implícita ou remetendo ao painel anterior.

---

### ERR-005c — Texto de balão cortado ou embaralhado

**Ocorrência:** 2 de 5 temas (Conjunções, Acentuação). Falas com palavras cortadas no meio ou fora de ordem, tornando o diálogo ilegível.

**Causa raiz:** Balões com mais de ~15–18 palavras sobrecarregam o modelo de layout — lettering gerado com IA tem limite prático de legibilidade que não é o mesmo que o limite técnico do campo de texto.

**Correção aplicada:** Reprocessamento dos painéis com falas longas divididas em 2 balões ou repartidas entre 2 painéis consecutivos.

**Regra para a squad:**
- Máximo de 12–15 palavras por balão. Contar explicitamente ao escrever o prompt.
- Se o conceito pedagógico exige mais palavras, dividir em 2 balões no mesmo painel (ex: balão 1 — premissa, balão 2 — exemplo) ou em 2 painéis consecutivos (painel de setup + painel de resposta/confirmação).
- Nunca redigir falas longas esperando que o Codex as "caiba" no balão automaticamente.

---

### ERR-005d — Personagens recorrentes (Prepo, Bia) desenhados fora do padrão canônico

**Ocorrência:** Prepo com design errado em 3 de 5 temas. Caso mais grave (Dicionário): sem etiqueta "PREPO", com estrela na cabeça em vez de antenas com letras "D"/"E", olhos azuis ovais em vez de brancos redondos com pupila preta.

**Causa raiz:** Os prompts de HQ descrevem em detalhe o personagem novo do tema, mas tratam Prepo e Bia apenas superficialmente (uma menção curta na seção "Personagens Fixos"), presumindo que o modelo "já sabe" o design deles de chamadas anteriores. O Codex não mantém memória visual entre chamadas — cada painel é gerado independentemente do contexto da sessão anterior.

**Correção aplicada:** Reprocessamento com descrição visual completa e literal do Prepo repetida em cada prompt de painel onde ele aparece.

**Regra para a squad:**

Descrição canônica obrigatória do **Prepo** — copiar literalmente em cada painel que o contenha:

> Prepo é um robô pequeno roxo com corpo cilíndrico, duas antenas na cabeça com as letras "D" e "E" nas pontas (maiúsculas, em amarelo), olhos redondos brancos com pupila preta circular, etiqueta metálica no peito com a palavra "PREPO" gravada em azul, pernas curtas com botõeszinhos e braços articulados.

Descrição canônica obrigatória da **Bia** — copiar literalmente em cada painel que a contenha:

> Bia é uma menina de 11 anos com cabelo cacheado e volumoso preto, pele morena clara, usando uniforme escolar azul (camiseta azul marinho com logo de escola no peito, calça azul escuro) e tênis brancos.

- A seção "Personagens Fixos" no topo do arquivo `.md` é necessária mas não suficiente — a descrição deve ser repetida literalmente em cada prompt de painel individual onde o personagem aparece.
- Nunca abreviar como "Prepo (mascote roxo)" ou "Bia (a menina)" no prompt de painel — usar sempre a descrição completa.

---

### ERR-005e — Acentuação perdida em texto maiúsculo/quadro-negro

**Ocorrência:** HQ "Acentuação: Paroxítonas e Proparoxítonas" — páginas 1, 2 e título da página 3. Dezenas de palavras sem acento correto, especialmente em títulos e quadros-negro.

**Exemplos reais:** "SILABA" em vez de "SÍLABA", "TONICA" em vez de "TÔNICA", "PAROXITONAS" em vez de "PAROXÍTONAS", "PENULTIMA" em vez de "PENÚLTIMA", "medico" em vez de "médico", "Nivel/bonus/revolver" em vez de "Nível/bônus/revólver", "proximas paginas" em vez de "próximas páginas", "Ja" em vez de "Já". Adicionalmente, apareceu um "è" com acento grave (inválido em português neste contexto) em vez de "é" com acento agudo.

**Causa raiz:** O arquivo `.md` de prompt já continha os acentos corretos — o problema não é o prompt, é a geração de imagem. O Codex tende a "esquecer" acentos especificamente em texto renderizado em CAIXA ALTA e em conteúdo de quadro-negro (giz/lousa), enquanto texto em balões de fala minúsculos saiu correto na mesma HQ e nas outras 4 HQs geradas na mesma sessão (que não tiveram esse problema). A causa provável é que modelos de imagem são treinados com muito mais texto em inglês em caixa alta do que em português, e inglês não usa acentos — o viés se manifesta exatamente nos elementos de destaque visual.

**Correção aplicada:** Regeneração das páginas 1, 2 e 3 com lista explícita de grafias corretas incluída no prompt de cada painel afetado (ex: "SÍLABA não SILABA", "TÔNICA não TONICA") e instrução para o Codex reler o texto renderizado palavra por palavra antes de aceitar cada painel.

**Regra para a squad:**
- Todo prompt de painel que contenha texto em português DEVE incluir a instrução: "todo texto em português deve ter acentuação 100% correta, incluindo em texto MAIÚSCULO/títulos/quadro-negro — texto em destaque (caixa alta, quadro-negro, banners) tem alta taxa de erro de acentuação e exige atenção redobrada."
- Antes de aceitar qualquer painel, reler cada palavra em destaque (título, quadro-negro, texto grande) comparando com a grafia correta do português — não confiar na leitura geral da imagem.
- Nunca usar acento grave (`è`) fora dos poucos casos gramaticalmente válidos em português ("à", "àquele", "àquela" etc.) — se aparecer `è` em qualquer outro contexto, é erro de geração e o painel deve ser rejeitado.
- Para temas cujo conteúdo central são palavras com acento (ex: acentuação, paroxítonas, proparoxítonas, oxítonas), incluir no prompt de cada painel uma lista explícita das grafias corretas das palavras-chave do tema, no formato "X não Y" (ex: "SÍLABA não SILABA").

---

### ERR-005f — Substituição de geração de imagem por IA por renderização programática

**Ocorrência:** HQ "Acentuação: Paroxítonas e Proparoxítonas", páginas 1–3. Ao tentar corrigir erros de acentuação persistentes nessas páginas, o agente `gerador-hq-imagens` abandonou a geração via Codex e substituiu a arte ilustrada por renderização programática via Python/Pillow: formas geométricas simples (retângulos, círculos, balões de fala genéricos tipo interface), sem cenário, sem personagens desenhados, sem estilo de HQ. O texto saiu com acentuação correta, mas o resultado não era uma HQ — era um wireframe utilitário. Rejeitado por Léo.

**Causa raiz:** Diante da dificuldade de obter acentuação correta via geração de imagem por IA após algumas tentativas, o agente tomou um atalho que resolve o sintoma (texto correto) mas destrói completamente o requisito real (HQ ilustrada consistente com o estilo visual do portal educacional).

**Regra ABSOLUTA e não-negociável:**

NUNCA, em hipótese alguma, usar renderização programática (Python/Pillow, matplotlib, SVG geométrico, HTML-to-image, ou qualquer técnica que não seja geração de imagem via modelo de IA) como solução para problemas de texto, acentuação, ou qualquer outro defeito de uma página de HQ.

Se a geração via Codex continuar produzindo erros de acentuação após múltiplas tentativas, as únicas ações corretas são:
1. Tentar novamente painel por painel em vez da página inteira de uma vez, reforçando a grafia exata de cada palavra crítica no prompt (incluindo lista explícita no formato "SÍLABA não SILABA").
2. Se persistir após 3 ou mais tentativas por painel: PARAR e reportar ao orquestrador/Léo para decisão conjunta.

Nunca decidir sozinho por trocar de técnica de renderização. O resultado entregue por este agente é SEMPRE arte de HQ gerada por IA — sem exceção.

---

## Checklist anti-bug para geração de HQ (gerador-hq-prompt e gerador-hq-imagens)

Verificação obrigatória antes de considerar qualquer HQ concluída:

**Prompts (gerador-hq-prompt — ao escrever o arquivo .md):**

- [ ] Cada painel individual tem descrição de cenário com pelo menos 3–4 elementos concretos especificados explicitamente? (não apenas uma instrução genérica no cabeçalho)
- [ ] Todo balão de fala tem no máximo ~12–15 palavras? (conceitos mais longos divididos em 2 balões ou 2 painéis)
- [ ] A descrição visual completa e literal do Prepo está repetida em cada prompt de painel onde ele aparece? (não apenas na seção "Personagens Fixos")
- [ ] A descrição visual completa e literal da Bia está repetida em cada prompt de painel onde ela aparece?
- [ ] Nenhum elemento visual está subentendido por reticências ou "continuação do painel anterior"?

**Imagens (gerador-hq-imagens — ao validar os arquivos gerados):**

- [ ] ⚠️ REGRA ABSOLUTA: As imagens foram geradas via Codex (IA)? Renderização programática (Pillow, matplotlib, SVG geométrico, HTML-to-image) é PROIBIDA — ver ERR-005f.
- [ ] O pixel do canto superior esquerdo de cada portrait tem Alpha=0 (transparente)? (verificado via script, não apenas pela confirmação textual do Codex)
- [ ] Cada painel das páginas pg1–pg4 tem cenário visível com elementos ilustrados (não fundo branco/liso)?
- [ ] Os textos dos balões estão legíveis e completos (sem palavras cortadas ou embaralhadas)?
- [ ] O Prepo, quando presente, tem: etiqueta "PREPO" no peito, antenas com letras "D"/"E", olhos brancos redondos com pupila preta?
- [ ] Todo texto em destaque (caixa alta, título, quadro-negro/lousa) tem acentuação 100% correta? (reler palavra por palavra — não confiar na leitura geral da imagem)
- [ ] Nenhum painel contém acento grave (`è`) fora dos contextos gramaticais válidos em português? (se sim, rejeitar e reprocessar)
- [ ] Todos os 4 arquivos de página existem fisicamente no caminho absoluto correto?

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
