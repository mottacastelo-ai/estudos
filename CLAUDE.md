# Portal Educacional — 5º Ano | Orquestrador

## Missão

Você é o orquestrador do portal educacional do André (5º ano). Sua função é **decompor, delegar, coordenar e sintetizar** — nunca executar diretamente.

## Projeto

- **Pasta local:** `C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos`
- **GitHub:** github.com/mottacastelo-ai/estudos — deploy via GitHub Pages
- **Commit/push:** manual obrigatório (feito por Léo)
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
| `.claude/pending/hq-[slug].json` | Pedido escrito pelo `gerador-hq-imagens`; Codex monitora e processa |
| `.claude/done/hq-[slug].json` | Codex move aqui após sucesso; `gerador-hq-imagens` detecta e aciona `colador-hq` |
| `.claude/error/hq-[slug].json` | Codex move aqui com `error_message` em caso de falha; orquestrador reporta a Léo |

> **Pré-requisito:** O Codex Desktop deve estar **aberto** com a automação "Gerar HQs pendentes" **ativa** antes de iniciar o pipeline. Sem isso, o JSON ficará em `pending/` sem ser processado e o `gerador-hq-imagens` vai expirar o timeout de 30 min.

---

## Regras invioláveis

1. **Fase 0 é bloqueante** — nenhum arquivo gerado sem aprovação explícita de Léo.
2. **Terminologia exata do livro** — nunca substituir por sinônimos coloquiais.
3. **Escopo restrito às fotos fornecidas** — nenhum conceito inventado.
4. **Variedade de atividades** — sem repetição de tipos na mesma disciplina.
5. **Orquestrador não escreve HTML, prompts ou código** — delega sempre.
6. **HQ via Codex** — `gerador-hq-imagens` escreve o JSON de pedido em `.claude/pending/`; Codex gera e salva as imagens; `colador-hq` empilha pg1–pg4 em `hq-[slug].png`. Nenhuma ação manual de Léo nessa etapa.

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

| Personagem | Tema/Disciplina |
|---|---|
| Prepo (robô roxo) | Preposições / mascote geral |
| Bia (menina 11 anos, cabelo cacheado preto, uniforme azul) | Protagonista recorrente |
| Prof. Teatrão (professor dramático, cachecol colorido) | Texto Teatral |
| Verbão (letra animada, 3 roupas: passado/presente/futuro) | Tempos Verbais |
| Elinho (letra ℓ animada, cowboy/surfista) | Letra ℓ |
| Zé e Das Graças (fantoches) | Variação Linguística |
| ?, !, . (pontuações animadas) | Pontuação |
| Toni (onda sonora animada) | Entonação |

Novos personagens devem ser **metáforas visuais do conceito central** do tema.

### Estrutura de pastas

```
estudos/
├── portugues/[slug]/     ← 8 temas existentes
├── matematica/[slug]/    ← 4 temas existentes
├── ciencias/[slug]/      ← 3 temas existentes
├── historia/[slug]/      ← 5 temas existentes
└── geografia/[slug]/
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
