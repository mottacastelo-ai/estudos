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
         ↓ (ambos concluídos)
[atualizador-index] → index.html atualizado
         ↓
[revisor-qualidade] → relatório de conformidade
         ↓
[gerador-hq-imagens] → escreve .claude/pending/hq-[slug].json → aguarda Codex processar
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

---

## Regras invioláveis

1. **Fase 0 é bloqueante** — nenhum arquivo gerado sem aprovação explícita de Léo.
2. **Terminologia exata do livro** — nunca substituir por sinônimos coloquiais.
3. **Escopo restrito às fotos fornecidas** — nenhum conceito inventado.
4. **Variedade de atividades** — sem repetição de tipos na mesma disciplina.
5. **Orquestrador não escreve HTML, prompts ou código** — delega sempre.
6. **HQ via Codex** — `gerador-hq-imagens` escreve o JSON de pedido em `.claude/pending/`; Codex gera e salva as imagens; `colador-hq` empilha pg1–pg4 em `hq-[slug].png`. Nenhuma ação manual de Léo nessa etapa.
7. **Documentação imediata** — toda mudança validada (novo recurso, nova regra, nova convenção) deve ser registrada nos docs do repositório na mesma sessão em que foi aprovada. Nenhuma melhoria fica apenas na memória do Claude.

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

> Caminhos de portrait são relativos a `_landing/`. Folhas de personagens em `Personagens\5o ano\`.
> Novos personagens devem ser **metáforas visuais do conceito central** do tema.

### Estrutura de pastas

```
estudos/
├── portugues/[slug]/     ← 12 temas
├── matematica/[slug]/    ← 7 temas
├── ciencias/[slug]/      ← 4 temas
├── historia/[slug]/      ← 3 temas
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

---

## Agentes disponíveis

| Agente | Responsabilidade |
|---|---|
| `analisador-pedagogico` | Analisa fotos, extrai conceitos, propõe estrutura de temas |
| `gerador-hq-prompt` | Cria `hq-[slug]-prompt.md` com prompts para o Codex |
| `gerador-atividades` | Cria arquivos HTML das atividades interativas |
| `atualizador-index` | Atualiza `index.html` para registrar o novo tema |
| `revisor-qualidade` | Audita arquivos gerados e reporta conformidade pedagógica |
| `gerador-hq-imagens` | Escreve JSON de pedido em `.claude/pending/`; faz polling até Codex confirmar em `.claude/done/` |
| `colador-hq` | Empilha pg1–pg4 em `hq-[slug].png` pronto para o index |
| `atualizador-docs` | Regenera `CONTEUDO.md` e atualiza tabela de agentes do `SQUAD.md` |
