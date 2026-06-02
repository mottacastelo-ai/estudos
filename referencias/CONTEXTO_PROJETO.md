# Contexto do Projeto Educacional — Portal Interativo de Aprendizagem

**Última atualização:** 2026-05-22 (baseado no estado atual do repositório GitHub)

---

## Visão Geral

Portal web educacional construído como aplicação de página única (SPA) para o aprendizado do André (5º ano). Fundamentado em metodologia de aprendizagem ativa (Roediger & Karpicke, 2006; Mayer, 2009) e estruturado na Pirâmide de Aprendizagem de Glasser: cada tema começa com uma HQ, avança por atividades de retrieval practice e culmina em tarefas de criação.

- **Repositório:** [github.com/mottacastelo-ai/estudos](https://github.com/mottacastelo-ai/estudos)
- **Pasta local:** `C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos`
- **Potencial futuro:** Adaptação comercial para público mais amplo

---

## Ecossistema sabendo.app

| Portal | URL | Repositório |
|---|---|---|
| Landing page | https://sabendo.app | sabendo-landing |
| Portal André (5º ano) | https://andre.sabendo.app | estudos |
| Portal Lis (2º ano) | https://lis.sabendo.app | estudos-2ano-lis |

---

## Infraestrutura Técnica

### Hospedagem & Deploy
- **Repositório & Hospedagem:** GitHub Pages
- **Workflow de deploy:**
  1. Editar arquivos localmente
  2. Commit + push via GitHub Desktop (**manual**, ~30 segundos)
  3. GitHub Pages publica automaticamente após o push
- **⚠️ Nota:** o processo **não é inteiramente automático** — commit e push são passos manuais obrigatórios

> O `README.md` no repositório ainda menciona Netlify, mas o deploy é feito exclusivamente via **GitHub Pages**.

### Estrutura de Arquivos

Os arquivos estão organizados em **subdiretórios por disciplina** (mudança em relação ao estado inicial, quando tudo ficava na raiz):

```
estudos/
├── index.html                  ← SPA principal
├── README.md                   ← documentação (desatualizada em relação ao estado real)
├── canonicas_ref.html          ← referência visual de personagens canônicos
├── versao canonica Bia.png
├── versao canonica Bia com fundo.png
├── versao canonica prepo.png
├── portugues/
│   ├── preposicoes/
│   ├── texto-teatral/
│   ├── tempos-verbais/
│   ├── letra-l/
│   ├── variacao-linguistica/
│   ├── pontuacao/
│   ├── entonacao/
│   └── texto-instrucional/
├── matematica/
│   ├── tabuada/
│   ├── multiplicacao-divisao/
│   ├── corpos-redondos-planificacao/
│   └── poliedros-prismas-piramides/
├── ciencias/
│   ├── caminho-do-lixo/
│   ├── lixo-que-produzimos/
│   └── tecnologia-agropecuaria/
├── historia/
│   ├── pais-de-contrastes/
│   ├── diversidade-cultural/
│   ├── marcos-memoria/
│   ├── memoria-negra-imigrantes/
│   └── calendarios-povos/
└── referencias/
    └── (arquivos de referência do projeto: temas-existentes.md, etc.)
```

Dentro de cada subdiretório de tema ficam: HQ (`.png`), atividades (`.html`) e prompt HQ (`.md`).

---

## Estado Atual — Disciplinas e Temas

### 📝 Português — 8 temas

| Tema | Slug | Personagem(ns) principal(is) |
|---|---|---|
| Preposições | `preposicoes` | Prepo (robô roxo) |
| Texto Teatral | `texto-teatral` | Prof. Teatrão |
| Tempos Verbais | `tempos-verbais` | Verbão |
| Letra ℓ e U | `letra-l` | Elinho |
| Variação Linguística | `variacao-linguistica` | Zé e Das Graças |
| Pontuação Expressiva | `pontuacao` | ?, !, . (personagens pontuação) |
| Entonação | `entonacao` | Toni (onda sonora animada) |
| Texto Instrucional | `texto-instrucional` | — |

### 🔢 Matemática — 4 temas

| Tema | Slug |
|---|---|
| Tabuada | `tabuada` |
| Multiplicação e Divisão | `multiplicacao-divisao` |
| Corpos Redondos e Planificação | `corpos-redondos-planificacao` |
| Poliedros: Prismas e Pirâmides | `poliedros-prismas-piramides` |

### 🔬 Ciências — 3 temas

| Tema | Slug |
|---|---|
| Caminho do Lixo | `caminho-do-lixo` |
| O Lixo que Produzimos | `lixo-que-produzimos` |
| Tecnologia Agropecuária | `tecnologia-agropecuaria` |

### 📜 História — 5 temas

| Tema | Slug |
|---|---|
| País de Contrastes | `pais-de-contrastes` |
| Diversidade Cultural | `diversidade-cultural` |
| Marcos e Memória | `marcos-memoria` |
| Memória Negra e Imigrantes | `memoria-negra-imigrantes` |
| Calendários dos Povos | `calendarios-povos` |

**Total atual: 4 disciplinas · 20 temas**

---

## Personagens Recorrentes das HQs

| Personagem | Descrição |
|---|---|
| **Prepo** | Robô roxo — mascote do portal; aparece em múltiplos temas |
| **Bia** | Menina de 11 anos, cabelo cacheado preto, uniforme azul; protagonista frequente |
| **Prof. Teatrão** | Professor dramático com cachecol colorido (Texto Teatral) |
| **Verbão** | Letra animada com 3 versões de roupa: passado/presente/futuro (Tempos Verbais) |
| **Elinho** | Letra ℓ animada, versões cowboy e surfista (Letra ℓ e U) |
| **Zé e Das Graças** | Fantoches para variação linguística (Variação Linguística) |
| **?, !, .** | Pontuações animadas: ? azul/curioso, ! vermelho-laranja/musculoso, . cinza/calmo |
| **Toni** | Onda sonora animada (Entonação) |

Cada novo tema pode introduzir um personagem adicional que seja metáfora visual do conteúdo.

---

## Paleta de Cores por Disciplina

| Disciplina | Código CSS | Cor primária | Cor clara | Bg |
|---|---|---|---|---|
| Português | `port` | `#7C3AED` | `#A78BFA` | `#F3F0FF` |
| Matemática | `mat` | `#059669` | `#34D399` | `#ECFDF5` |
| Ciências | `cien` | `#0284C7` | `#38BDF8` | `#F0F9FF` |
| História | `hist` | `#B45309` | `#F59E0B` | `#FFFBEB` |
| Geografia | `geo` | `#15803D` | `#4ADE80` | `#F0FDF4` |

---

## Fundamentação Pedagógica

| Pilar | Referência | Aplicação |
|---|---|---|
| Retrieval practice | Roediger & Karpicke (2006) | Atividades de recuperação progressiva em cada tema |
| Aprendizagem multimídia | Mayer (2009) | Integração de HQs, texto e atividades interativas |
| Pirâmide de Glasser | — | Progressão HQ → retrieval → aplicação → criação |
| Spaced repetition | — | Sistema Leitner nos flashcards da tabuada |
| Gamificação | Plass, Homer & Kinzer (2015) | Pontuação, medalhas e feedback imediato |

**Sequência obrigatória por tema:** prompt HQ → geração das imagens (Léo no ChatGPT) → colagem → atividades HTML → atualização do `index.html`

---

## Convenção de Nomenclatura

```
Arquivos de atividade:  [tipo]-[slug-do-tema].html
Arquivo HQ:             hq-[slug-do-tema].png
Prompt HQ:              hq-[slug-do-tema]-prompt.md

Tipos reconhecidos: quiz / complete-lacuna / caca-erro / ordenacao / criador /
classificador / transformador / flashcards / treino / batalha / domino /
missao / frases / mapa-mental
```

---

## Princípios Reitores

1. **Termos técnicos do livro são obrigatórios** — usar o nome exato do livro (ex.: "pretérito perfeito", não só "passado"). O André precisa reconhecer o termo na prova.
2. **Proibido introduzir conteúdo fora do escopo das fotos** — nenhum conceito que não esteja nas fotos enviadas pode aparecer nas atividades.
3. **Variedade de tipos de atividade** — nenhum tipo deve se repetir entre temas da mesma disciplina.
4. **Qualidade sobre quantidade** — preferir temas bem construídos a muitos temas superficiais.
5. **Narrativa contínua** — personagens recorrentes facilitam imersão e transferência de aprendizagem.

---

## Workflow de Entrega (Cowork)

- **Cowork** edita `index.html` diretamente e salva todos os arquivos na pasta da disciplina correspondente (`portugues/`, `matematica/`, etc.) — **sem subpastas adicionais dentro do tema, sem ZIPs**
- O arquivo `hq-[slug].png` **não é colocado pelo Cowork** — Léo o copia manualmente para a pasta do tema após baixar da colagem
- Fallback Claude.ai: ZIP com `index.html` completo já atualizado + todos os arquivos de atividade

---

## Decisões de Design (sessão 2026-06-02)

- **Home hero:** gradiente neutro dark slate — não vinculado a uma disciplina específica
- **act-cards:** todas as 5 disciplinas têm `border-top: 4px solid var(--[disc]-color)` para identidade visual consistente
- **disc-home-cards:** fundo colorido leve com gradiente + borda lateral da cor da disciplina
- **Linguagem motivacional:** "Por onde vai hoje?", "Missões e desafios", saudação pessoal ao André
- **Ícones disc-home-cards:** 52px
- **Transições de tela:** fade 150ms
- **Favicon:** emoji 🎓 como SVG inline

---

## Arquitetura Futura Planejada

| Componente | Detalhes |
|---|---|
| Autenticação | Supabase Auth |
| Banco de dados | Supabase (PostgreSQL) |
| Tabelas previstas | `profiles`, `activity_log`, `streaks` |
| Estado atual | localStorage como base — sem login |
| Migração | Supabase entra quando o login for implementado |

---

## Contato & Manutenção

- **Responsável:** Léo Motta
- **Repositório:** github.com/mottacastelo-ai/estudos
- **Pasta local:** `C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos`
