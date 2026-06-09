# Contexto do Projeto Educacional — Portal sabendo.app
**Última atualização:** 2026-06-08

---

## Visão Geral

Portal web educacional (SPA) para o aprendizado do André (5º ano). Fundamentado em metodologia de aprendizagem ativa e estruturado na Pirâmide de Aprendizagem de Glasser: cada tema começa com uma HQ, avança por atividades de retrieval practice e culmina em tarefas de criação. Inclui sistema de gamificação completo com cartas colecionáveis e reforço adaptativo.

---

## Ecossistema sabendo.app

| Portal | URL | Repositório | Pasta local |
|---|---|---|---|
| Landing page | https://sabendo.app | `sabendo-landing` | `estudos\_landing\` (repo aninhado) |
| Portal André (5º ano) | https://andre.sabendo.app | `estudos` | `Projeto Estudos\estudos\` |
| Portal Lis (2º ano) | https://lis.sabendo.app | `estudos-2ano` | `Projeto Estudos\estudos-2ano\` |

**Deploy:** automático via hook Stop em `.claude/settings.json` → `.claude/deploy.ps1` → commit + push nos 3 repos se houver alterações.

### Fluxo de autenticação cross-domain

```
Usuário acessa sabendo.app (landing page)
         ↓
Login com email/senha → Supabase Auth
         ↓
Landing detecta profiles.portal do usuário
  • portal = "estudos"      → redireciona para andre.sabendo.app
  • portal = "estudos-2ano" → redireciona para lis.sabendo.app
         ↓
Tokens passados no hash da URL → portal processa via detectSessionInUrl: true
         ↓
Portal autentica localmente e exibe conteúdo personalizado
```

> Cada aluno tem seu próprio login e vê apenas seu progresso (streaks, cartas, reforços).

---

## Infraestrutura Técnica

### Hospedagem
- GitHub Pages (3 repos separados)
- Commit + push via GitHub Desktop — **manual**, ~30 segundos

### Supabase
- **Projeto:** `mmtrzxmitklpibfilbio.supabase.co`
- **Chave anon:** `sb_publishable_ZgA70ikD1XRgEhxzz7aKzQ_TNSAsxQ_`
- **Tabelas em uso:** `profiles`, `activity_log`, `streaks`, `cards`, `reinforcement_queue`
- **Autenticação cross-domain:** login na landing → detecta `profiles.portal` → redireciona com tokens no hash → portal processa via `detectSessionInUrl: true`

### Usuários
- `andre@sabendo.app` — portal: estudos, year: 5
- `lis@sabendo.app` — portal: estudos-2ano, year: 2

---

## Estado Atual — Disciplinas e Temas

**Total: 5 disciplinas · 25 temas · 107 atividades**

### 📝 Português — 8 temas

| Tema | Slug | Personagem | Portrait |
|---|---|---|---|
| Preposições | `preposicoes` | Prepo | `prepo-hd.png` |
| Texto Teatral | `teatral` | Prof. Teatrão | `chars/teatral-hd.png` |
| Tempos Verbais | `verbais` | Verbão | `chars/tempos-verbais-hd.png` |
| Letra ℓ e U | `letral` | Elinho | `chars/letra-l-hd.png` |
| Variação Linguística | `variacao` | Zé e Das Graças | `chars/variacao-linguistica-hd.png` |
| Pontuação | `pontuacao` | ? ! . | `chars/pontuacao-hd.png` |
| Texto Instrucional | `instrucional` | Façã | `chars/texto-instrucional-hd.png` |
| Entonação | `entonacao` | Toni | `chars/entonacao-hd.png` |

### 🔢 Matemática — 7 temas

| Tema | Slug | Personagem | Portrait |
|---|---|---|---|
| Tabuada | `tabuada` | Prepo | `prepo-hd.png` |
| Multiplicação e Divisão | `multiplicacao-divisao` | Calco | `chars/multiplicacao-divisao-hd.png` |
| Poliedros, Prismas e Pirâmides | `poliedros-prismas-piramides` | Poli | `chars/poliedros-prismas-piramides-hd.png` |
| Corpos Redondos e Planificação | `corpos-redondos-planificacao` | Esfer | `chars/corpos-redondos-planificacao-hd.png` |
| Múltiplos e Divisores | `multiplos-divisores-criterios` | Divi | `chars/multiplos-divisores-criterios-hd.png` |
| Primos e Fatoração | `primos-compostos-fatoracao` | Primo | `chars/primos-compostos-fatoracao-hd.png` |
| mdc e mmc | `mdc-mmc-problemas` | Max & Min | `chars/mdc-mmc-problemas-hd.png` |

### 🔬 Ciências — 4 temas

| Tema | Slug | Personagem | Portrait |
|---|---|---|---|
| O Lixo que Produzimos | `lixo-que-produzimos` | Lixinho | `chars/lixo-que-produzimos-hd.png` |
| O Caminho do Lixo | `caminho-do-lixo` | Professora Ciência | `chars/caminho-do-lixo-hd.png` |
| O Ciclo da Água | `ciclo-da-agua` | Ciclão | `chars/ciclo-da-agua-hd.png` |
| Água, Cidades e Consumo | `agua-cidades-consumo` | Gotinha | `chars/agua-cidades-consumo-hd.png` |

### 🌍 Geografia — 3 temas

| Tema | Slug | Personagem | Portrait |
|---|---|---|---|
| Diversidade Cultural | `diversidade-cultural` | Prof. Geografina | `chars/diversidade-cultural-hd.png` |
| País de Contrastes | `pais-de-contrastes` | Prof. Geografina | `chars/pais-de-contrastes-hd.png` |
| Tecnologia Agropecuária | `tecnologia-agropecuaria` | Agro 4.0 | `chars/tecnologia-agropecuaria-hd.png` |

### 📜 História — 3 temas

| Tema | Slug | Personagem | Portrait |
|---|---|---|---|
| Diversos Calendários | `calendarios-povos` | Calê | `chars/calendarios-povos-hd.png` |
| Marcos de Memória | `marcos-memoria` | Memo | `chars/marcos-memoria-hd.png` |
| Zumbi e Imigrantes | `memoria-negra-imigrantes` | Timbre | `chars/memoria-negra-imigrantes-hd.png` |

> Caminhos de portrait são relativos a `_landing/`.

---

## Gamificação

Sistema completo documentado em `referencias/GAMIFICACAO.md`. Resumo:

- **Reveal progressivo:** canvas pixelado (9 estágios) por tema, desbloqueado atividade a atividade
- **Cartas colecionáveis:** 6 raridades (Comum → Rara → Épica → Lend-Épica → Lendária → Revisional)
- **Reforço adaptativo:** atividades com score < 80% na 1ª tentativa entram em fila com `due_date + 5 dias`
- **Carta Revisional:** gerada ao resolver todos os reforços pendentes de um tema
- **Painel de coleção:** tela no portal exibindo todas as cartas obtidas por tema
- **Validação:** sistema completo testado e validado em Preposições (8 HTMLs com snippet "concluir-btn")
- **Próximo passo:** aplicar snippet nos demais 24 temas (padrão já definido, pronto para replicar)

---

## Sistema de Busca

Campo de busca na home do portal (`index.html`), implementado e em produção.

**Comportamento:**
- Busca por **nome de tema** — ex.: "Preposições", "Ciclo da Água"
- Busca por **número de página do livro** — ex.: "62" localiza o tema cuja HQ cobre as pp. 62–XX

**Como funciona a busca por pp.:**
O campo varre os atributos `data-pp` (ou equivalente) dos cards de tema no index. Os valores vêm da `hq-caption` de cada tema.

**Regra obrigatória (afeta geração de novos temas):**
> Toda `hq-caption` no `index.html` **DEVE conter** `pp. XX–YY` referenciando as páginas do livro didático cobertas pelo tema. Sem isso, o tema não aparece na busca por página.

Exemplo correto:
```html
<div class="hq-caption">
  <span>📖</span>
  <span>Prepo e as Preposições — 4 páginas · Personagens: Prepo, Bia · pp. 48–55</span>
</div>
```

**Cobertura atual:** nem todos os temas existentes têm pp. na caption. Temas futuros gerados pela skill **obrigatoriamente** incluirão pp. XX–YY.

---

## Paginação

O portal suporta paginação de resultados. Implementada e em produção para os temas que têm a marcação necessária. Temas futuros gerados pela skill devem incluir os atributos de paginação conforme o padrão do index.

---

## Visão Futura — Multi-usuário

**Não implementado ainda.** Visão de longo prazo:

- Qualquer responsável poderá cadastrar um aluno → portal personalizado em `[nome].sabendo.app`
- Cada aluno tem login próprio, conquistas próprias (cartas, streaks, reforços)
- `profiles.portal` controla para qual repo o aluno é redirecionado
- Estrutura técnica (Supabase + auth cross-domain) já suporta N usuários — é uma questão de provisionamento

---

## Estrutura de Arquivos

```
estudos/
├── index.html                    ← SPA principal
├── CLAUDE.md                     ← Orquestrador
├── SQUAD.md                      ← Arquitetura do squad multi-agente
├── CONTEUDO.md                   ← Inventário de temas e atividades
├── shared/
│   └── gamification.js           ← Sistema de gamificação (IIFE)
├── _landing/                     ← Repo aninhado (sabendo.app)
│   ├── prepo-hd.png
│   ├── chars/                    ← 23 portraits HD dos personagens
│   └── cartas/                   ← Fundos das cartas por tier
├── portugues/[slug]/
├── matematica/[slug]/
├── ciencias/[slug]/
├── historia/[slug]/
├── geografia/[slug]/
└── referencias/
    ├── GAMIFICACAO.md            ← Sistema de gamificação completo
    ├── CONTEXTO_PROJETO.md       ← Este arquivo
    ├── CONTEUDO.md               ← (legado — use CONTEUDO.md na raiz)
    ├── atividades-por-disciplina.md
    └── SKILL-portal-educacional-5ano.md
```

---

## Paleta de Cores por Disciplina

| Disciplina | disc | Primária | Clara | Bg |
|---|---|---|---|---|
| Português | `port` | `#7C3AED` | `#A78BFA` | `#F3F0FF` |
| Matemática | `mat` | `#059669` | `#34D399` | `#ECFDF5` |
| Ciências | `cien` | `#0284C7` | `#38BDF8` | `#F0F9FF` |
| História | `hist` | `#B45309` | `#F59E0B` | `#FFFBEB` |
| Geografia | `geo` | `#15803D` | `#4ADE80` | `#F0FDF4` |

---

## Convenção de Nomenclatura

```
Atividade HTML:       [tipo]-[slug].html
HQ imagem:            hq-[slug].png
Prompt HQ:            hq-[slug]-prompt.md
Portrait personagem:  _landing/chars/[slug]-hd.png
Folha personagem:     Personagens\5o ano\[Nome].png

Tipos de atividade: quiz / complete-lacuna / caca-erro / ordenacao / criador /
  classificador / transformador / flashcards / treino / batalha / domino /
  missao / frases / mapa-mental / detetive-nomes
```

---

## Fundamentação Pedagógica

| Pilar | Aplicação |
|---|---|
| Retrieval practice | Atividades de recuperação progressiva em cada tema |
| Aprendizagem multimídia | Integração de HQs, texto e atividades interativas |
| Pirâmide de Glasser | Progressão HQ → retrieval → aplicação → criação |
| Spaced repetition | Reforço adaptativo com `due_date + 5 dias` |
| Gamificação | Cartas colecionáveis, reveal progressivo, raridade por desempenho |

---

## Princípios Reitores

1. **Termos técnicos do livro são obrigatórios** — nome exato do livro, nunca apenas sinônimos coloquiais
2. **Proibido introduzir conteúdo fora do escopo** — só o que está nas fotos enviadas
3. **Variedade de tipos de atividade** — nenhum tipo se repete entre temas da mesma disciplina
4. **Documentação imediata** — toda mudança validada é documentada na mesma sessão
5. **Narrativa contínua** — personagens recorrentes facilitam imersão e transferência
