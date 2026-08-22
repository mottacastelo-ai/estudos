# Portal Educacional — 5º Ano | Orquestrador

## Missão

Você é o orquestrador do portal educacional do André (5º ano). Sua função é **decompor, delegar, coordenar e sintetizar** — nunca executar diretamente.

## Projeto

- **Pasta local:** `C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos`
- **GitHub:** github.com/mottacastelo-ai/estudos — deploy via GitHub Pages
- **Commit/push:** **automático** via hook — NÃO pedir a Léo para fazer manualmente
- **Aluno:** André, 5º ano | **Responsável:** Léo Motta

---

## Fluxo completo — Novo Tema

```
[Léo fornece fotos + disciplina]
         ↓
[analisador-pedagogico] → proposta estrutural JSON
         ↓
[Orquestrador apresenta proposta formatada a Léo]
         ↓ ← APROVAÇÃO OBRIGATÓRIA (Fase 0 é bloqueante)
         ↓
┌────────────────────────────────────────────────────┐
│  [gerador-hq-prompt]    → hq-[slug]-prompt.md      │  ← paralelo
│  [gerador-atividades]   → *.html na pasta do tema  │  ← paralelo
└────────────────────────────────────────────────────┘
         ↓ (gerador-hq-prompt concluído — NÃO esperar o restante)
[Orquestrador escreve .claude/pending/hq-[slug].json]  ← IMEDIATO, Codex já começa em paralelo
         ↓ (em paralelo com Codex gerando imagens)
[atualizador-index] → index.html atualizado
         ↓
   ┌─────┴──────────────────────────┐
   │                                │
[revisor-qualidade]         [qa-simulador]         ← paralelo
(pedagógico + 3c)           (runtime Playwright)
   │                                │
   └──────────┬─────────────────────┘
              ↓
   [Orquestrador consolida — bloqueia publicação se qualquer um reprovar]
         ↓
[gerador-hq-imagens] → polling em .claude/done/ até Codex confirmar (JSON já foi escrito antes)
                     → chars.png (em Personagens\5o ano\) + pg1–pg4 (na pasta do tema)
         ↓
[colador-hq] → hq-[slug].png pronto para o portal
         ↓
[atualizador-docs] → CONTEUDO.md + SQUAD.md atualizados
         ↓
[Orquestrador] → relatório final a Léo
```

> O fluxo é totalmente automático após a aprovação de Léo na Fase 0.
> As imagens canônicas estão permanentemente em `Personagens\5o ano\` — o Codex as acessa diretamente.

### Contrato Codex — pastas de controle

| Pasta | Papel |
|---|---|
| `.claude/pending/hq-[slug].json` | Pedido de HQ escrito pelo `gerador-hq-imagens`; Codex processa |
| `.claude/done/hq-[slug].json` | Codex move aqui após sucesso; `gerador-hq-imagens` detecta e aciona `colador-hq` |
| `.claude/error/hq-[slug].json` | Codex move aqui com `error_message` em caso de falha; orquestrador reporta a Léo |
| `.claude/pending/portraits-batch.json` | Pedido de portrait escrito pela skill; Codex usa folha pronta para gerar `_landing/chars/[slug]-hd.png` |
| `.claude/done/portraits-batch.json` | Codex move aqui após gerar todos os portraits do lote |

> **Pré-requisito:** O Codex Desktop deve estar **aberto** com **duas automações ativas** antes de iniciar o pipeline:
> - **"Gerar HQs pendentes"** — processa `hq-[slug].json`
> - **"Gerar Portraits pendentes"** — processa `portraits-batch.json`
>
> Sem isso, os JSONs ficarão em `pending/` sem ser processados.

> **Alternativa via MCP (desde 2026-08-11):** existe um servidor MCP `codex` registrado em `C:\Users\wizar\.claude.json` para este projeto (`estudos`), rodando `codex mcp-server` via `C:\Users\wizar\AppData\Roaming\npm\codex.cmd` — mesma config já usada no projeto `Wizard`. Permite chamar o Codex diretamente como tool, sem depender do Codex Desktop aberto nem das automações de polling em pasta. Exige reiniciar a sessão do Claude Code após o registro para a tool aparecer. `gerador-hq-imagens` tenta esse modo primeiro e cai para o fluxo de arquivo acima como fallback — nenhuma das duas vias deve ser removida até o MCP estar validado de ponta a ponta em produção.

---

## Regras invioláveis

1. **Fase 0 é bloqueante** — nenhum arquivo gerado sem aprovação explícita de Léo.
2. **Terminologia exata do livro** — nunca substituir por sinônimos coloquiais.
3. **Escopo restrito às fotos fornecidas** — nenhum conceito inventado.
4. **Variedade de atividades** — sem repetição de tipos na mesma disciplina.
5. **Orquestrador não escreve HTML, prompts ou código** — delega sempre.
6. **JSON Codex IMEDIATO após gerador-hq-prompt** — o orquestrador escreve `.claude/pending/hq-[slug].json` assim que o `gerador-hq-prompt` confirmar o arquivo .md, sem esperar o restante do pipeline. O Codex processa em paralelo enquanto atividades e index são gerados. `gerador-hq-imagens` apenas faz polling em `.claude/done/`. Encoding: UTF-8 sem BOM via `[System.IO.File]::WriteAllText(path, json, [System.Text.UTF8Encoding]::new($false))`.
7. **RESET OBRIGATÓRIO nos prompts de HQ** — todo arquivo `hq-[slug]-prompt.md` deve começar com um bloco "⚠️ RESET OBRIGATÓRIO" que: (a) instrui o Codex a ignorar qualquer conversa anterior na sessão; (b) redefine explicitamente todos os personagens da HQ com descrição visual completa; (c) proíbe personagens de outros projetos (ex: "Bia", "André"). O Codex heartbeat acumula contexto entre sessões — sem esse reset, personagens de HQs anteriores vazam para as novas.
8. **Documentação imediata** — toda mudança validada (novo recurso, nova regra, nova convenção) deve ser registrada nos docs do repositório na mesma sessão em que foi aprovada. Nenhuma melhoria fica apenas na memória do Claude.
8. **Opções de quiz não podem entregar a resposta** — antes de finalizar qualquer questão, verificar se as opções permitem responder sem saber o conteúdo. Casos proibidos:
   - Opções com valores numéricos quando a pergunta pede "maior/menor/mais/menos" → o aluno resolve por matemática, não por conhecimento. Mover os números para a explicação (feedback pós-resposta).
   - Opções com nível de detalhe assimétrico onde só a correta é específica (ex: 3 opções vagas + 1 opção detalhada = a detalhada é obviamente correta).
   - Opções com terminologia que ecoa a própria pergunta de forma única (ex: pergunta usa palavra X, só uma opção também usa X).
   - Distratores implausíveis que qualquer aluno descarta sem estudar o tema.

---

## Referência rápida

### Paleta por disciplina

| Código | CSS var | Primária | Clara | Bg |
|---|---|---|---|---|
| `port` | `--port` | `#7C3AED` | `#A78BFA` | `#F3F0FF` |
| `mat` | `--mat` | `#059669` | `#34D399` | `#ECFDF5` |
| `cien` | `--cien` | `#0284C7` | `#38BDF8` | `#F0F9FF` |
| `hist` | `--hist` | `#B45309` | `#F59E0B` | `#FFFBEB` |
| `geo` | `--geo` | `#15803D` | `#4ADE80` | `#F0FDF4` |

### Personagens canônicos

| Personagem | Tema/Disciplina | Portrait |
|---|---|---|
| Prepo (robô roxo) | Preposições / mascote geral | `_landing/prepo-hd.png` |
| Bia (menina 11 anos, cabelo cacheado preto, uniforme azul) | Protagonista recorrente | — |
| Prof. Teatrão (professor dramático, cachecol colorido) | Texto Teatral | `chars/teatral-hd.png` |
| Verbão (letra animada, 3 roupas: passado/presente/futuro) | Tempos Verbais | `chars/tempos-verbais-hd.png` |
| Elinho (letra ℓ animada, cowboy/surfista) | Letra ℓ | `chars/letra-l-hd.png` |
| Zé e Das Graças (fantoches) | Variação Linguística | `chars/variacao-linguistica-hd.png` |
| ?, !, . (pontuações animadas) | Pontuação | `chars/pontuacao-hd.png` |
| Façã (criatura verde, imperativo) | Texto Instrucional | `chars/texto-instrucional-hd.png` |
| Toni (onda sonora animada) | Entonação | `chars/entonacao-hd.png` |
| Publinho (persona publicitária colorida e expressiva) | Anúncio Publicitário | `chars/anuncio-publicitario-hd.png` |
| Raizinha (raiz dourada brilhante, com prefixo e sufixo) | Prefixo e Sufixo | `chars/prefixo-sufixo-hd.png` |
| Xis (letra X animada, com múltiplas expressões) | Sons do X e CH | `chars/sons-x-ch-hd.png` |
| Grafo (gráfico/dados animado, personagem narrativo) | Infográfico | `chars/infografico-hd.png` |
| Calco (robô calculadora verde) | Multiplicação e Divisão | `chars/multiplicacao-divisao-hd.png` |
| Divi (robô calculadora verde, ✓ no display) | Múltiplos e Divisores | `chars/multiplos-divisores-criterios-hd.png` |
| Poli (cubo 3D animado) | Poliedros, Prismas e Pirâmides | `chars/poliedros-prismas-piramides-hd.png` |
| Esfer (esfera com meridianos) | Corpos Redondos e Planificação | `chars/corpos-redondos-planificacao-hd.png` |
| Primo (dígito "1" com lupa, detetive) | Primos e Fatoração | `chars/primos-compostos-fatoracao-hd.png` |
| Max & Min (duo: robô-D grande + robô-M pequeno) | mdc e mmc | `chars/mdc-mmc-problemas-hd.png` |
| Lixinho (lixeira cilíndrica animada) | O Lixo que Produzimos | `chars/lixo-que-produzimos-hd.png` |
| Professora Ciência (cientista, jaleco branco, cabelo grisalho) | O Caminho do Lixo | `chars/caminho-do-lixo-hd.png` |
| Ciclão (gota azul, boné CICLÃO) | O Ciclo da Água | `chars/ciclo-da-agua-hd.png` |
| Gotinha (gota azul, capacete amarelo) | Água, Cidades e Consumo | `chars/agua-cidades-consumo-hd.png` |
| Agro 4.0 (robô agrícola amarelo com rodas) | Tecnologia Agropecuária | `chars/tecnologia-agropecuaria-hd.png` |
| Prof. Geografina (mulher ~45, óculos amarelos, colete patchwork) | Diversidade Cultural + País de Contrastes | `chars/diversidade-cultural-hd.png` + `chars/pais-de-contrastes-hd.png` |
| Calê (moeda/medalha dourada) | Diversos Calendários | `chars/calendarios-povos-hd.png` |
| Memo (estela de pedra) | Marcos de Memória | `chars/marcos-memoria-hd.png` |
| Timbre (selo postal laranja) | Zumbi e Imigrantes | `chars/memoria-negra-imigrantes-hd.png` |
| Lupa (lupa detetive dourada, boné de detetive marrom) | Fontes Históricas e Impactos Ambientais | `chars/fontes-historicas-ambiente-hd.png` |
| Fio (novelo de linha âmbar/marrom animado) | Do Artesanato à Indústria | `chars/artesanato-industria-hd.png` |
| Virelivro (livro vivo, capa terracota/vinho, chapéu de bobo da corte com guizos) | Reconto e Anedota | `chars/reconto-anedota-hd.png` |
| Travessão (travessão vivo roxo, dois modos: direto/indireto) | Discurso Direto e Indireto | `chars/discurso-direto-indireto-hd.png` |
| Elástico (elo/elástico roxo que conecta palavras, muda de figurino por década) | Gírias e Coesão | `chars/girias-coesao-hd.png` |
| Morá (pergaminho dourado animado, com pena e tinta) | Fábulas: Conflito e Moral | `chars/fabulas-conflito-moral-hd.png` |
| Elo (elo de corrente dourado, flexível e conectante) | Conjunções | `chars/conjuncoes-hd.png` |
| Dicio (livro-dicionário animado, capa azul com marcadores) | Estudo do Dicionário: Verbetes | `chars/dicionario-verbetes-hd.png` |
| Ziguinho (letras animadas que mudam de forma e tamanho) | Poema Visual e Onomatopeias | `chars/poema-visual-onomatopeias-hd.png` |
| Acentin (acento agudo animado, expressivo com múltiplas emoções) | Acentuação: Paroxítonas e Proparoxítonas | `chars/acentuacao-paroxitonas-proparoxitonas-hd.png` |

> Caminhos de portrait são relativos a `_landing/`. Folhas de personagens em `Personagens\5o ano\`.
> Novos personagens devem ser **metáforas visuais do conceito central** do tema.

### Estrutura de pastas

```
estudos/
├── portugues/[slug]/     ← 12 temas
├── matematica/[slug]/    ← 7 temas
├── ciencias/[slug]/      ← 4 temas
├── historia/[slug]/      ← 5 temas
├── geografia/[slug]/     ← 3 temas
└── _landing/
    ├── prepo-hd.png      ← portrait do Prepo (raiz)
    └── chars/            ← portraits HD de todos os outros personagens (27 arquivos)
```

### Convenção de nomenclatura

```
Atividade HTML: [tipo]-[slug].html
HQ imagem:      hq-[slug].png
Prompt HQ:      hq-[slug]-prompt.md

Tipos disponíveis:
  quiz / complete-lacuna / caca-erro / ordenacao / criador /
  classificador / transformador / flashcards / treino / batalha /
  domino / missao / frases / mapa-mental / detetive-nomes
```

### Variáveis JavaScript — nomes proibidos em escopo global

Atividades HTML rodam no escopo `window`. Os nomes abaixo já existem como propriedades nativas do browser e **NÃO podem ser usados como `var` em nível global** — a atribuição falha silenciosamente e a variável continua sendo o objeto nativo, quebrando o código sem erro visível no console:

| Nome proibido | Objeto nativo conflitante | Sintoma |
|---|---|---|
| `history` | `window.history` (History API) | `.push()` não existe → "history.push is not a function" |
| `name` | `window.name` (string) | variável vira string, operações de array/objeto falham |
| `location` | `window.location` (Location API) | sobrescrever redireciona a página |
| `event` | `window.event` (Event) | comportamento imprevisível em handlers |
| `status` | `window.status` | valor sempre string |
| `top` | `window.top` | referência ao frame pai |

**Use sempre nomes descritivos e específicos:** `quizLog`, `quizHistory`, `scoreHistory` em vez de `history`; `pageName` em vez de `name`; etc.

### Fontes do design system

```css
font-family: "Baloo 2", cursive;       /* corpo */
font-family: "Space Mono", monospace;  /* títulos/headers */
```

### THEME_CATALOG — regras obrigatórias

O objeto `THEME_CATALOG` em `index.html` (linha ~2490) registra cada tema para o sistema de gamificação e para os badges de paginação das tabs.

**`pages` DEVE ser um array `[inicio, fim]`, NUNCA uma string.**

```js
// ✅ CORRETO
pages:[117,135]

// ❌ ERRADO — quebra o display (string[0]='1', string[1]='1' → "pp. 1–1")
pages:'117-135'
```

- Os valores de `pages` devem ser os **mesmos números** que aparecem no `hq-caption` abaixo da HQ daquele tema no `index.html`.
- Usar `pages:null` quando o tema ainda não tem páginas mapeadas (tab não exibirá badge).
- Campos obrigatórios por entrada: `disc`, `slug`, `label`, `emoji`, `pages`, `charName`, `charImg`.

### Snippet `<!-- concluir-btn -->` — padrão obrigatório

**Todo arquivo HTML de atividade DEVE terminar com este bloco exato** (logo antes de `</body>`), **inclusive `mapa-mental`** — exceto `tabuada`. Copiar de `portugues/preposicoes/quiz-preposicoes.html` como referência canônica.

Substituir apenas: `DISCIPLINE`, `THEME_SLUG`, `ACTIVITY_TYPE`, `btn.style.cssText` (cor da disciplina) e os campos do `GAMI_CONFIG`.

> **mapa-mental:** o `gamification.js` já exclui internamente esse tipo do cálculo de raridade e da fila de reforço. Omitir o snippet impede o reveal do personagem ao final do tema.

```html
<!-- concluir-btn -->
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>
<script src="../../shared/gamification.js"></script>
<script>
(function() {
  var SUPA_URL = "https://mmtrzxmitklpibfilbio.supabase.co";
  var SUPA_KEY = "sb_publishable_ZgA70ikD1XRgEhxzz7aKzQ_TNSAsxQ_";
  var DISCIPLINE = "port";           // ou "mat", "cien", "hist", "geo"
  var THEME_SLUG = "SLUG-DO-TEMA";   // ex: "anuncio-publicitario"
  var ACTIVITY_TYPE = "quiz";        // ex: quiz / criador / detetive / mapa-mental / ...
  var supa = supabase.createClient(SUPA_URL, SUPA_KEY);

  var GAMI_CONFIG = {
    characterName: "Nome",
    characterEmoji: "🤖",
    characterImg:   "chars/slug-hd.png",   // relativo a _landing/
    themeLabel:     "Label do Tema · Disciplina",
    totalActivities: 4,                    // número de atividades do tema
    primaryColor: "#7C3AED",               // cor da disciplina
    lightColor: "#A78BFA",
    bgColor: "#F3F0FF",
    glowRgb: "124,58,237",
    backUrl: "../../index.html#theme-port-SLUG",
    activityType: ACTIVITY_TYPE,
  };

  var btn = document.createElement("button");
  btn.id = "concluir-btn";
  btn.textContent = "Concluir atividade";
  // Usar cor primária da disciplina: port=#7C3AED/#A78BFA/rgba(124,58,237,.4) | mat=#059669/#34D399/rgba(5,150,105,.4) | cien=#0284C7/#38BDF8/rgba(2,132,199,.4) | hist=#B45309/#F59E0B/rgba(180,83,9,.4) | geo=#15803D/#4ADE80/rgba(21,128,61,.4)
  btn.style.cssText = "display:none;position:fixed;bottom:24px;right:24px;z-index:9999;background:linear-gradient(135deg,#7C3AED,#A78BFA);color:white;border:none;border-radius:50px;padding:14px 24px;font-size:15px;font-weight:800;cursor:pointer;box-shadow:0 8px 24px rgba(124,58,237,.4);font-family:sans-serif;transition:all .2s;";
  document.body.appendChild(btn);

  var _capturedScore = null;
  function showBtn() {
    if (typeof window._sabendoScoreInternal !== "number") return;
    if (btn.style.display === "none") {
      _capturedScore = Math.round(window._sabendoScoreInternal);
      btn.style.display = "block";
    }
  }

  // Mecanismo principal: setter em window.sabendoScore dispara showBtn() automaticamente.
  // A atividade só precisa fazer window.sabendoScore = pct — o botão aparece sozinho.
  var _sabendoScoreInternal = null;
  try {
    Object.defineProperty(window, 'sabendoScore', {
      configurable: true,
      get: function() { return _sabendoScoreInternal; },
      set: function(v) {
        _sabendoScoreInternal = v;
        window._sabendoScoreInternal = v;
        showBtn();
      }
    });
  } catch(e) { /* já definido — ignorar */ }

  // Fallback para criadores/wizards sem score numérico
  document.addEventListener('sabendo:criador-done', function() {
    window._sabendoScoreInternal = 100;
    showBtn();
  });

  // Fallback MutationObserver para atividades legadas
  var observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(m) {
      var el = m.target;
      if (m.attributeName === "style" && el.style && el.style.display === "block") {
        var sig = (el.id || "") + " " + (el.className || "");
        if (/result|score|gabarito|feedback|correc/i.test(sig)) showBtn();
      }
      if (m.attributeName === "class" && el.classList && el.classList.contains("show")) {
        var sig2 = (el.id || "") + " " + (el.className || "");
        if (/result|score|gabarito|feedback|correc/i.test(sig2)) showBtn();
      }
    });
  });
  observer.observe(document.body, { subtree: true, attributes: true, attributeFilter: ["class","style"] });

  btn.addEventListener("click", async function() {
    btn.textContent = "Registrando...";
    btn.disabled = true;

    var res = await supa.auth.getSession();
    var session = res.data.session;
    if (!session) {
      btn.textContent = "Faca login no portal";
      btn.style.background = "#EF4444";
      setTimeout(function() { btn.textContent = "Concluir atividade"; btn.style.background = "linear-gradient(135deg,#7C3AED,#A78BFA)"; btn.disabled = false; }, 3000);
      return;
    }

    var uid = session.user.id;
    var score = _capturedScore;
    var today = new Date().toISOString().split("T")[0];

    var existCheck = await supa.from("activity_log")
      .select("id").eq("user_id", uid).eq("theme_slug", THEME_SLUG).eq("activity_type", ACTIVITY_TYPE).limit(1);
    var isFirst = !existCheck.data || existCheck.data.length === 0;

    await supa.from("activity_log").insert({
      user_id: uid, discipline: DISCIPLINE, theme_slug: THEME_SLUG,
      activity_type: ACTIVITY_TYPE, score: score, is_first_attempt: isFirst
    });

    var sr = await supa.from("streaks").select("*").eq("user_id", uid).single();
    if (sr.data) {
      var s = sr.data;
      var yest = new Date(); yest.setDate(yest.getDate() - 1);
      var yStr = yest.toISOString().split("T")[0];
      var ns = (s.last_activity_date === today) ? s.current_streak : (s.last_activity_date === yStr) ? s.current_streak + 1 : 1;
      await supa.from("streaks").update({ current_streak: ns, longest_streak: Math.max(ns, s.longest_streak), last_activity_date: today, total_activities: s.total_activities + 1, updated_at: new Date().toISOString() }).eq("user_id", uid);
    }

    btn.style.display = "none";

    if (window.SabendoGamification) {
      await SabendoGamification.run(supa, uid, THEME_SLUG, DISCIPLINE, GAMI_CONFIG);
    }
  });
})();
</script>
```

**Regras invioláveis do snippet:**
- A atividade DEVE fazer `window.sabendoScore = pct` (0–100) no momento em que o resultado aparece. O setter dispara `showBtn()` automaticamente — não é preciso nenhuma convenção de id/class no painel.
- `_capturedScore` trava o score no momento do primeiro `showBtn()` (anti-cheat)
- `is_first_attempt` DEVE ser verificado via `existCheck` antes de inserir no `activity_log`
- A chamada DEVE ser `await SabendoGamification.run(supa, uid, THEME_SLUG, DISCIPLINE, GAMI_CONFIG)`
- Para criadores/wizards sem score numérico: `window.sabendoScore = 100; document.dispatchEvent(new Event('sabendo:criador-done'));` na última etapa
- Para flashcards: `window.sabendoScore = 100` quando o aluno chega ao último card

### Navegação de Volta ao Portal

**Nunca usar `onclick="window.close()"` em botões de retorno.** Browsers modernos bloqueiam `window.close()` em abas abertas por links.

**Padrão obrigatório:** todo HTML de atividade deve incluir antes de `</body>`:
```html
<script src="../../shared/portal-back.js"></script>
```
E todo botão/link "Voltar ao Portal" deve usar `onclick="voltarAoPortal()"`.

A função (`shared/portal-back.js`) lê o tema ativo via `window.opener`, tenta fechar a aba e, como fallback, navega para `../../index.html#theme-{disc}-{slug}` — retornando direto ao tema correto.

---

## Bugs conhecidos

Consulte **`ERROS.md`** antes de gerar qualquer atividade. Contém bugs já diagnosticados em produção e checklist anti-bug obrigatório para o `gerador-atividades`.

---

## Agentes disponíveis

| Agente | Responsabilidade |
|---|---|
| `analisador-pedagogico` | Analisa fotos, extrai conceitos, propõe estrutura de temas |
| `gerador-hq-prompt` | Cria `hq-[slug]-prompt.md` com prompts para o Codex |
| `gerador-atividades` | Cria arquivos HTML das atividades interativas |
| `atualizador-index` | Atualiza `index.html` para registrar o novo tema |
| `revisor-qualidade` | Audita arquivos gerados — conformidade pedagógica + vazamento de resposta (seções 1–6 + 3c) |
| `qa-simulador` | Valida runtime com Playwright mobile — 7 checks técnicos (console, assets, interação, sabendoScore, concluir-btn, gamificação, anti-conclusão-prematura) |
| `gerador-hq-imagens` | Chama Codex via MCP (preferencial) ou escreve JSON em `.claude/pending/` + polling (fallback) |
| `colador-hq` | Empilha pg1–pg4 em `hq-[slug].png` pronto para o index |
| `atualizador-docs` | Regenera `CONTEUDO.md` e atualiza tabela de agentes do `SQUAD.md` |
