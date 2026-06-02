# SQUAD — Portal Educacional 5º Ano
**Última atualização:** 2026-06-02

---

## Visão geral

Squad multi-agente que automatiza a criação completa de novos temas para o portal educacional do André (5º ano). Um único comando de Léo desencadeia todo o pipeline — da análise das fotos do livro até a HQ colada pronta para o portal.

---

## Arquitetura de arquivos

```
estudos/
├── CLAUDE.md                              ← Orquestrador (lido automaticamente pelo Claude Code)
├── SQUAD.md                               ← Este arquivo
└── .claude/
    ├── agents/
    │   ├── analisador-pedagogico.md       ← Fase 0: análise de fotos
    │   ├── gerador-hq-prompt.md           ← Cria hq-[slug]-prompt.md
    │   ├── gerador-atividades.md          ← Cria HTMLs das atividades
    │   ├── atualizador-index.md           ← Registra tema no index.html
    │   ├── revisor-qualidade.md           ← Audita conformidade pedagógica
    │   ├── gerador-hq-imagens.md          ← Escreve pedido em pending/; polling em done/
    │   └── colador-hq.md                  ← Empilha pg1–pg4 em hq-[slug].png
    ├── skills/
    │   ├── skill-analise-escopo.md        ← Procedimento da Fase 0
    │   ├── skill-gerar-hq-prompt.md       ← Padrões narrativos da HQ
    │   ├── skill-gerar-atividades-html.md ← Design system + templates de código
    │   ├── skill-atualizar-index.md       ← Padrões HTML do index.html
    │   └── skill-hq-imagens.md            ← Contrato Codex: campos JSON, polling, erros
    ├── pending/                           ← Pedidos de HQ aguardando Codex
    ├── done/                              ← JSONs de HQs processadas com sucesso
    └── error/                             ← JSONs de HQs com falha + error_message
```

---

## Agentes

| Agente | Modelo | Responsabilidade | Usa skill |
|---|---|---|---|
| `analisador-pedagogico` | Sonnet 4.6 | Analisa fotos do livro, extrai conceitos e páginas, propõe estrutura de temas (Fase 0) | `skill-analise-escopo` |
| `atualizador-docs` | Haiku 4.5 | Regenera referencias/CONTEUDO.md (via index.html) e tabela de agentes do SQUAD.md | — |
| `atualizador-index` | Sonnet 4.6 | Adiciona o tema na sidebar, bloco de conteúdo e contador do index.html | `skill-atualizar-index` |
| `colador-hq` | Haiku 4.5 | Empilha pg1–pg4 verticalmente com Pillow → `hq-[slug].png` | — |
| `gerador-atividades` | Sonnet 4.6 | Cria HTMLs das atividades interativas (quiz, mapa mental, etc.) | `skill-gerar-atividades-html` |
| `gerador-hq-imagens` | Sonnet 4.6 | Escreve JSON de pedido em `.claude/pending/`; polling até Codex confirmar em `.claude/done/` | `skill-hq-imagens` |
| `gerador-hq-prompt` | **Opus 4.7** | Cria `hq-[slug]-prompt.md` com narrativa de 4 páginas + folha de personagens | `skill-gerar-hq-prompt` |
| `revisor-qualidade` | Haiku 4.5 | Audita terminologia, escopo, gamificação e mapa mental — retorna score JSON | — |

---

## Skills

| Skill | Serve para | Conteúdo principal |
|---|---|---|
| `skill-analise-escopo` | `analisador-pedagogico` | Critérios de divisão de temas, captura de páginas do livro, sugestão de personagem e tipos de atividade |
| `skill-gerar-hq-prompt` | `gerador-hq-prompt` | Arco narrativo das 4 páginas, regra de sem reticências (descrever tudo explicitamente), formato de painel |
| `skill-gerar-atividades-html` | `gerador-atividades` | Design system completo (fontes, CSS vars, responsividade), templates de código por tipo de atividade, mapa mental canônico |
| `skill-atualizar-index` | `atualizador-index` | 4 regiões do index.html, tabela de cores por disciplina, padrões HTML de sidebar e bloco de conteúdo |
| `skill-hq-imagens` | `gerador-hq-imagens` | Contrato Codex: campos do JSON de pedido, comportamento de polling (30s/30min), destinos de arquivo, responsabilidades do Codex (incluindo validação 1024×1536) |

---

## Fluxo completo

```
Léo fornece fotos + disciplina
         │
         ▼
[analisador-pedagogico]
  • lê fotos, extrai termos técnicos exatos do livro
  • identifica páginas (ex.: pp. 45–52)
  • propõe divisão em temas + personagem + tipos de atividade
  • retorna JSON + proposta formatada para Léo
         │
         ▼
Orquestrador apresenta proposta a Léo
         │
    ◄────┤ APROVAÇÃO OBRIGATÓRIA (Fase 0 — bloqueante)
         │
         ├─────────────────────────────────┐
         ▼                                 ▼
[gerador-hq-prompt]              [gerador-atividades]
  → hq-[slug]-prompt.md            → quiz-[slug].html
                                   → mapa-mental-[slug].html
                                   → [outros tipos].html
         └─────────────────────────────────┘
                        │
                        ▼
               [atualizador-index]
                 → index.html atualizado
                   (sidebar + bloco + contador + pp. XX–YY)
                        │
                        ▼
              [revisor-qualidade]
                 → score JSON
                 → lista de problemas por severidade
                        │
                        ▼
             [gerador-hq-imagens]
               • escreve .claude/pending/hq-[slug].json
               • polling a cada 30s por até 30min
               • Codex gera e salva pg1–pg4 + chars (1024×1536)
               • detecta done/ → aciona colador-hq
               • detecta error/ → reporta a Léo
                        │
                        ▼
                [colador-hq]
                  • valida dimensões das 4 páginas
                  • empilha verticalmente com Pillow
                  → hq-[slug].png na pasta do tema
                        │
                        ▼
           Orquestrador → relatório final a Léo
```

---

## Destinos de arquivo por tipo

| Arquivo | Destino |
|---|---|
| `hq-[slug]-prompt.md` | `estudos/[disciplina]/[slug]/` |
| `[tipo]-[slug].html` | `estudos/[disciplina]/[slug]/` |
| `hq-[slug]-pg1..4.png` | `estudos/[disciplina]/[slug]/` |
| `hq-[slug].png` (colagem final) | `estudos/[disciplina]/[slug]/` |
| `[NomePersonagem].png` (chars) | `C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\Personagens\5o ano\` |

---

## Regras invioláveis

| # | Regra |
|---|---|
| 1 | **Fase 0 é bloqueante** — nenhum arquivo gerado sem aprovação explícita de Léo |
| 2 | **Terminologia exata do livro** — nunca substituir por sinônimos coloquiais |
| 3 | **Escopo restrito às fotos** — nenhum conceito inventado |
| 4 | **Variedade de atividades** — nenhum tipo se repete entre temas da mesma disciplina |
| 5 | **Orquestrador não executa** — sempre delega aos agentes |
| 6 | **Sem reticências nos prompts de HQ** — tudo descrito explicitamente, nada subentendido |
| 7 | **Validar dimensão 1024×1536 antes de salvar** — nunca salvar thumbnail de comparação |
| 8 | **Mapa mental segue o canônico** — adaptar `historia/diversidade-cultural/mapa-mental-diversidade-cultural.html` |
| 9 | **Responsivo obrigatório** — notebook é principal, celular deve ser plenamente navegável |

---

## Paleta de cores por disciplina

| Disciplina | disc | Primária | Clara | Bg | Dark |
|---|---|---|---|---|---|
| Português | `port` | `#7C3AED` | `#A78BFA` | `#F3F0FF` | `#4C1D95` |
| Matemática | `mat` | `#059669` | `#34D399` | `#ECFDF5` | `#064E3B` |
| Ciências | `cien` | `#0284C7` | `#38BDF8` | `#F0F9FF` | `#075985` |
| História | `hist` | `#B45309` | `#F59E0B` | `#FFFBEB` | `#78350F` |
| Geografia | `geo` | `#15803D` | `#4ADE80` | `#F0FDF4` | `#14532D` |

---

## Personagens canônicos

| Personagem | Descrição | Tema |
|---|---|---|
| Prepo | Robô roxo — mascote geral | Preposições |
| Bia | Menina 11 anos, cabelo cacheado preto, uniforme azul | Protagonista recorrente |
| Prof. Teatrão | Professor dramático, cachecol colorido | Texto Teatral |
| Verbão | Letra animada, 3 roupas: passado/presente/futuro | Tempos Verbais |
| Elinho | Letra ℓ animada, versões cowboy e surfista | Letra ℓ |
| Zé e Das Graças | Fantoches | Variação Linguística |
| ?, !, . | Pontuações animadas | Pontuação |
| Toni | Onda sonora animada | Entonação |

Novos personagens devem ser **metáforas visuais do conceito central** do tema.

---

## Como alterar o squad

| O que alterar | Arquivo |
|---|---|
| Ordem do fluxo, regras globais, personagens, paleta | `CLAUDE.md` |
| O que um agente faz, seu modelo, seu output JSON | `.claude/agents/[agente].md` |
| Procedimento detalhado de uma etapa | `.claude/skills/skill-[nome].md` |
| Adicionar agente novo | Criar `.claude/agents/[novo].md` + registrar em `CLAUDE.md` + atualizar este arquivo |
| Remover agente | Deletar o `.md` + remover do `CLAUDE.md` + atualizar este arquivo |

---

## Como acionar

Abra o Claude Code com a pasta `estudos/` como diretório de trabalho:

```bash
cd "C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos"
claude
```

O `CLAUDE.md` é carregado automaticamente. Para iniciar o pipeline completo:

> "Tenho fotos novas de [Disciplina] sobre [assunto]. Quero criar um novo tema."
