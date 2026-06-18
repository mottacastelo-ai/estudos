# SQUAD — Portal Educacional 5º Ano
**Última atualização:** 2026-06-18

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
    │   ├── revisor-qualidade.md           ← Audita conformidade pedagógica + vazamento de resposta (3c)
    │   ├── qa-simulador.md               ← Valida runtime com Playwright mobile (7 checks)
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
| `qa-simulador` | Sonnet 4.6 | Valida tecnicamente atividades HTML no browser com Playwright (viewport 375×812  | — |
| `revisor-qualidade` | Haiku 4.5 | Audita terminologia, escopo, gamificação e mapa mental — retorna score JSON | — |

---

## Skills

| Skill | Serve para | Conteúdo principal |
|---|---|---|
| `skill-analise-escopo` | `analisador-pedagogico` | Critérios de divisão de temas, captura de páginas do livro, sugestão de personagem e tipos de atividade |
| `skill-gerar-hq-prompt` | `gerador-hq-prompt` | Arco narrativo das 4 páginas, regra de sem reticências (descrever tudo explicitamente), formato de painel |
| `skill-gerar-atividades-html` | `gerador-atividades` | Design system completo (fontes, CSS vars, responsividade), templates de código por tipo de atividade, mapa mental canônico |
| `skill-atualizar-index` | `atualizador-index` | 4 regiões do index.html, tabela de cores por disciplina, padrões HTML de sidebar e bloco de conteúdo. **Obrigatório:** adicionar entradas no `HREF_MAP` de `loadActivityStatus()` para cada novo arquivo HTML gerado (mapeamento `href → "theme_slug\|activity_type"`). |
| `skill-hq-imagens` | `gerador-hq-imagens` | Contrato Codex: campos do JSON de pedido, comportamento de polling (30s/30min), destinos de arquivo, responsabilidades do Codex (incluindo validação 1024×1536) |

---

## Pré-requisito — Codex Desktop

Antes de iniciar qualquer pipeline, Léo deve:
1. Abrir o **Codex Desktop**
2. Despausar (ativar) as **duas automações**:
   - **Gerar HQs pendentes** — processa `.claude/pending/hq-[slug].json`
   - **Gerar Portraits pendentes** — processa `.claude/pending/portraits-batch.json`

---

## Fluxo completo

```
Léo ativa as 2 automações no Codex Desktop
         │
         ▼
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
  → [slug]-portrait-prompt.md      → mapa-mental-[slug].html
                                   → [outros tipos].html
         └─────────────────────────────────┘
                        │
                        ▼
               [atualizador-index]
                 → index.html atualizado
                   (sidebar + bloco + contador + THEME_CATALOG)
                        │
                        ▼
         ┌────────┴──────────────────┐
         │                          │
[revisor-qualidade]         [qa-simulador]        ← paralelo
   → score JSON                → JSON 7 checks
   → problemas/severidade      → screenshots em falha
         │                          │
         └───────────┬──────────────┘
                     ▼
        [Orquestrador consolida — bloqueia se qualquer um reprovar]
                     │
                     ▼
             [gerador-hq-imagens]
               • escreve .claude/pending/hq-[slug].json
               • escreve .claude/pending/portraits-batch.json
               • Codex (HQ): gera folha de personagem + pg1-pg4
               • Codex (Portrait): usa folha → gera [slug]-hd.png
               • polling → detecta done/ → aciona colador-hq
               • detecta error/ → reporta a Léo
                        │
                 ┌───────┴───────┐
                 ▼               ▼
          [colador-hq]     Codex salva
            → hq-[slug]    [slug]-hd.png
              .png          em _landing/chars/
                 └───────┬───────┘
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
| `[NomePersonagem].png` (folha de personagem) | `Personagens\5o ano\` |
| `[slug]-portrait-prompt.md` | `estudos/_landing/chars/` |
| `[slug]-hd.png` (portrait gamificação) | `estudos/_landing/chars/` |

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

| Personagem | Descrição | Tema | Portrait |
|---|---|---|---|
| Prepo | Robô roxo — mascote geral | Preposições | `prepo-hd.png` |
| Bia | Menina 11 anos, cabelo cacheado preto, uniforme azul | Protagonista recorrente | — |
| Prof. Teatrão | Professor dramático, cachecol colorido | Texto Teatral | `chars/teatral-hd.png` |
| Verbão | Letra animada, 3 roupas: passado/presente/futuro | Tempos Verbais | `chars/tempos-verbais-hd.png` |
| Elinho | Letra ℓ animada, versões cowboy e surfista | Letra ℓ | `chars/letra-l-hd.png` |
| Zé e Das Graças | Fantoches | Variação Linguística | `chars/variacao-linguistica-hd.png` |
| ?, !, . | Pontuações animadas | Pontuação | `chars/pontuacao-hd.png` |
| Façã | Criatura verde, imperativo "FAÇA!" | Texto Instrucional | `chars/texto-instrucional-hd.png` |
| Toni | Onda sonora animada | Entonação | `chars/entonacao-hd.png` |
| Calco | Robô calculadora verde, display com smile | Multiplicação e Divisão | `chars/multiplicacao-divisao-hd.png` |
| Divi | Robô calculadora verde, display com ✓ | Múltiplos e Divisores | `chars/multiplos-divisores-criterios-hd.png` |
| Poli | Cubo 3D animado, F+V=A+2 | Poliedros, Prismas e Pirâmides | `chars/poliedros-prismas-piramides-hd.png` |
| Esfer | Esfera azul-esverdeada com meridianos | Corpos Redondos e Planificação | `chars/corpos-redondos-planificacao-hd.png` |
| Primo | Dígito "1" verde-escuro, coroa dourada, lupa | Primos e Fatoração | `chars/primos-compostos-fatoracao-hd.png` |
| Max & Min | Duo: robô-D grande + robô-M pequeno | mdc e mmc | `chars/mdc-mmc-problemas-hd.png` |
| Lixinho | Lixeira cilíndrica animada, tampa-chapéu | O Lixo que Produzimos | `chars/lixo-que-produzimos-hd.png` |
| Professora Ciência | Cientista, jaleco branco, cabelo grisalho | O Caminho do Lixo | `chars/caminho-do-lixo-hd.png` |
| Ciclão | Gota azul, boné escuro com badge CICLÃO | O Ciclo da Água | `chars/ciclo-da-agua-hd.png` |
| Gotinha | Gota azul, capacete amarelo (distinto do Ciclão) | Água, Cidades e Consumo | `chars/agua-cidades-consumo-hd.png` |
| Agro 4.0 | Robô agrícola amarelo/dourado com rodas | Tecnologia Agropecuária | `chars/tecnologia-agropecuaria-hd.png` |
| Prof. Geografina | Mulher ~45, pele morena, óculos amarelos redondos, colete patchwork | Diversidade Cultural + País de Contrastes | `chars/diversidade-cultural-hd.png` + `chars/pais-de-contrastes-hd.png` |
| Calê | Moeda/medalha dourada com coroa de louros | Diversos Calendários | `chars/calendarios-povos-hd.png` |
| Memo | Estela de pedra cinza-bege | Marcos de Memória | `chars/marcos-memoria-hd.png` |
| Timbre | Selo postal laranja com bordas picotadas | Zumbi e Imigrantes | `chars/memoria-negra-imigrantes-hd.png` |

> Caminhos de portrait são relativos a `_landing/`. Folhas de personagem em `Personagens\5o ano\`.
> Novos personagens devem ser **metáforas visuais do conceito central** do tema.

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
