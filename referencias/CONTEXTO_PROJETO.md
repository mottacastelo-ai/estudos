# Contexto do Projeto Educacional - Portal Interativo de Aprendizagem

## Visão Geral

Portal web educacional construído como uma aplicação de página única (SPA) destinada ao aprendizado do 5º ano, fundamentado em metodologia de aprendizagem ativa. O projeto combina gamificação, narrativas transmídia e práticas pedagógicas baseadas em pesquisa científica para criar experiências de aprendizagem progressivas.

**Objetivo principal:** Suportar o desenvolvimento acadêmico do filho (5º ano) através de atividades interativas fundamentadas em princípios de aprendizagem ativa.

**Potencial futuro:** Adaptação comercial da plataforma para público mais amplo.

---

## Fundamentação Teórica

O projeto repousa sobre três pilares científicos comprovados:

### 1. **Prática Retrieval (Recuperação de Memória)**
- **Referência:** Roediger & Karpicke (2006) - "The Power of Testing Memory: Basic Research and Implications for Educational Practice"
- **Aplicação:** Cada tema inclui atividades de recuperação progressiva, desde reconhecimento até free recall
- **Racional:** Estudantes que praticam recuperação consolidam conhecimento de forma mais durável do que aqueles que apenas releem conteúdo

### 2. **Teoria Cognitiva da Aprendizagem Multimídia**
- **Referência:** Mayer (2009) - "Multimedia Learning"
- **Aplicação:** Integração de imagens (HQs), texto narrativo e atividades interativas no mesmo ambiente
- **Racional:** Combinação estratégica de modalidades reduz carga cognitiva e melhora retenção

### 3. **Pirâmide de Aprendizagem de Glasser**
- **Aplicação:** Progressão de atividades do simples (leitura/observação passiva via HQ) até complexo (criação/produção)
- **Sequência típica:**
  - 10% - Leitura/Observação passiva (HQ de introdução)
  - 20% - Audição (narrativa integrada)
  - 30% - Observação visual + atividades
  - 50% - Discussão/Interpretação (atividades variadas)
  - 70% - Prática/Aplicação (retrieval practice)
  - 90% - Ensino a outros / Criação (atividades de síntese)

---

## Infraestrutura Técnica

### Hospedagem & Deploy
- **Repositório & Hospedagem:** GitHub (github.com/mottacastelo-ai/estudos)
- **Workflow de Deploy:**
  1. Editar arquivos localmente (`C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos`)
  2. Commit e push via GitHub Desktop (manual)
  3. GitHub publica automaticamente via GitHub Pages
- **URL ao vivo:** Configurada via GitHub Pages

### Estrutura de Arquivos

```
estudos/
├── index.html                        # Aplicação SPA principal
├── README.md                         # Convenções e guia de desenvolvimento
├── referencias/                      # Documentação e referências do projeto
│   ├── CONTEXTO_PROJETO.md
│   ├── temas-existentes.md
│   ├── atividades-por-disciplina.md
│   └── index-template-snippets.md
├── portugues/                        # Disciplina → Tema
│   ├── preposicoes/
│   ├── texto-teatral/
│   ├── tempos-verbais/
│   ├── letra-l/
│   ├── variacao-linguistica/
│   ├── pontuacao/
│   ├── texto-instrucional/
│   └── entonacao/
├── matematica/
│   └── tabuada/
├── ciencias/
│   ├── lixo-que-produzimos/
│   ├── caminho-do-lixo/
│   └── tecnologia-agropecuaria/
├── historia/
│   ├── marcos-memoria/
│   ├── calendarios-povos/
│   ├── diversidade-cultural/
│   └── pais-de-contrastes/
└── [disc-folder]/[slug]/             # Padrão geral: cada tema em sua subpasta
    ├── hq-[slug].png                 # HQ montada (páginas unidas verticalmente)
    ├── hq-[slug]-prompt.md           # Prompt usado para gerar a HQ
    ├── quiz-[slug].html              # Atividade principal
    └── mapa-mental-[slug].html       # Atividade de mapa mental (quando aplicável)
```

**Nota:** imagens canônicas de personagens (`versao canonica *.png`) permanecem na raiz do projeto para que a skill hq-generator as localize via `os.listdir()`.

### Versionamento
- **Ferramenta:** GitHub Desktop
- **Fluxo:** Trabalho local → Commit → Push → Auto-deploy GitHub Pages
- **Nota importante:** Commit e push são passos manuais que levam ~30 segundos; o deploy via GitHub Pages é automático

---

## Organização Pedagógica

### Estrutura por Disciplina

#### **Português (8 temas completados)** — pasta: `portugues/`

1. **Preposições** (`preposicoes/`)
   - Personagem principal: Prepo (robô roxo mascote)
   - Arco: HQ → atividades de reconhecimento → mapeamento visual
   - Foco: Aprendizagem visual e prática de posicionamento

2. **Texto Teatral** (`texto-teatral/`)
   - Novo personagem: Prof. Teatrão (professor dramático com lenço colorido)
   - Arco: HQ teatral → identificação de elementos dramáticos → criação de diálogos
   - Foco: Estrutura narrativa e expressão

3. **Tempos Verbais** (`tempos-verbais/`)
   - Novo personagem: Verbão (letra animada com 3 versões de roupa: passado/presente/futuro)
   - Arco: HQ com viagem temporal → conjugação → produção de narrativas em tempos diferentes
   - Foco: Flexibilidade verbal e consciência temporal

4. **Letra ℓ e U** (`letra-l/`)
   - Novo personagem: Elinho (letra animada estilo cowboy/surfista)
   - Arco: HQ → atividades de discriminação visual → escrita criativa com foco no som
   - Foco: Fonética e discriminação visual-auditiva

5. **Variação Linguística** (`variacao-linguistica/`)
   - Novos personagens: Zé e Das Graças (fantoches)
   - Arco: HQ com diálogos regionais → identificação de variantes → criação de diálogos inclusivos
   - Foco: Conscientização sociolinguística

6. **Pontuação** (`pontuacao/`)
   - Novos personagens: Interrogação (? azul, curioso), Exclamação (! vermelho-laranja, musculoso), Ponto (. cinza, calmo)
   - Arco: HQ com personagens pontuação → interpretação de sentimentos → uso criativo em contextos
   - Foco: Pontuação como instrumento expressivo, não apenas gramatical

7. **Texto Instrucional** (`texto-instrucional/`)
   - Foco: Identificação de estrutura e linguagem de textos instrucionais

8. **Entonação** (`entonacao/`)
   - Foco: Prosódia e leitura expressiva

#### **Matemática (1 tema completado)** — pasta: `matematica/`

1. **Tabuada** (`tabuada/`)
   - Arco: HQ → reconhecimento de padrões → fluência em retrieval → criação de jogos próprios
   - Foco: Automaticidade combinada com compreensão conceitual

#### **Ciências (3 temas completados)** — pasta: `ciencias/`

1. **Lixo que Produzimos** (`lixo-que-produzimos/`)
   - Foco: Tipos de resíduos, consumo consciente e separação de lixo

2. **Caminho do Lixo** (`caminho-do-lixo/`)
   - Foco: Destinação final dos resíduos, reciclagem e impacto ambiental

3. **Tecnologia Agropecuária** (`tecnologia-agropecuaria/`)
   - Foco: Uso de tecnologia na produção agrícola e pecuária brasileira

#### **História (4 temas completados)** — pasta: `historia/`

1. **Marcos da Memória** (`marcos-memoria/`)
   - Foco: Lugares e objetos como registros da memória coletiva e individual

2. **Calendários dos Povos** (`calendarios-povos/`)
   - Foco: Diferentes formas de medir e organizar o tempo em culturas diversas

3. **Diversidade Cultural** (`diversidade-cultural/`)
   - Foco: Pluralidade cultural brasileira e identidade nacional

4. **País de Contrastes** (`pais-de-contrastes/`)
   - Foco: Desigualdades regionais e sociais no Brasil

---

## Padrões de Design

### Continuidade Narrativa
- **Prepo** aparece em múltiplos temas, proporcionando coesão narrativa
- **Bia** (menina 11 anos, cabelos pretos cacheados, uniforme azul) é a protagonista frequente
- Cada novo tema introduz novo personagem, mantendo interesse narrativo
- Todos os personagens dialogam com o aprendiz, criando ilusão de interação social

### Paleta de Cores por Disciplina
Documentada em `README.md`:
- **Português:** Tons quentes (roxo, laranja, vermelho para personagens; variações em atividades)
- **Matemática:** Tons frios (azul, verde para estrutura; acentos amarelos para destaque)
- Consistência visual facilita navegação mental entre temas

### Variação de Tipos de Atividade
**Princípio crítico:** Cada tema usa tipos de atividade diferentes para evitar repetição pedagógica e manter engajamento.

Exemplos de tipos já implementados:
- Reconhecimento múltipla escolha
- Arrastar e soltar (drag-and-drop)
- Mapeamento visual
- Preenchimento de lacunas
- Criação livre de conteúdo
- Ordenação
- Pareamento de conceitos
- Jogo em tempo real

---

## Fluxo de Desenvolvimento para Novos Temas

### 1. Geração de Prompt HQ (Comic Strip)
- Criar arquivo `.md` com descrição detalhada do cenário, personagens, mensagem pedagógica
- Incluir referências de personagens existentes ou novos
- Especificar tom (lúdico, dramático, investigativo, etc.)

### 2. Design de Atividades (Retrieval Practice → Creation)
- Primeiro: atividades de reconhecimento (prática retrieval básica)
- Intermediário: aplicação em contextos variados
- Final: síntese e criação pelo aprendiz

### 3. Implementação Técnica
- Adicionar estrutura HTML no `index.html`
- Integrar com sidebar de navegação
- Aplicar paleta de cores da disciplina
- Garantir responsividade mobile

### 4. Deploy
- Commit + Push via GitHub Desktop
- GitHub Pages publica automaticamente
- Teste em navegador

---

## Convenções de Nomenclatura

Conforme `README.md`:
- **Temas:** kebab-case em IDs HTML, título completo em labels
- **Arquivos:** snake_case para assets (hq_preposicoes.png, atividade_tabuada_01.js)
- **Cores:** Variáveis CSS nomeadas por disciplina (--cor-português-primária, --cor-matemática-secundária)

---

## Workflow Preferido de Entrega

**Formato:** ZIP com arquivos novos/alterados (não projeto completo)

Quando adicionar novo tema:
- Incluir arquivo `.md` com prompt HQ
- Incluir código HTML da seção
- Incluir assets (imagens, SVGs)
- Incluir lógica de atividades (CSS + JavaScript)

---

## Próximas Prioridades

### Curto Prazo
- Novos temas em Português conforme currículo avança (ex.: Adjetivos, Verbos Transitivos/Intransitivos, Concordância)
- Novos temas em Matemática (ex.: Frações, Geometria, Problemas de Múltiplas Etapas)

### Médio Prazo
- Implementação de sistema de progresso (tracking de atividades completadas)
- Feedback adaptativo baseado em performance
- Sistema de recompensas gamificadas (badges, pontos)

### Longo Prazo
- Exploração de comercialização para público mais amplo
- Possível integração com LMS educacionais
- Adaptação para outras séries e disciplinas

---

## Princípios Reitores

1. **Fundamentação científica:** Toda prática pedagógica deve estar ancorada em pesquisa validada
2. **Variedade:** Diferentes tipos de atividade mantêm engajamento e evitam fadiga cognitiva
3. **Progressão clara:** HQ → Retrieval → Aplicação → Criação
4. **Narrativa continua:** Personagens e história facilitam imersão e transfer de aprendizagem
5. **Qualidade sobre quantidade:** Melhor ter 6 temas bem construídos do que 12 superficiais
6. **Iteração:** Feedback do aprendiz informa refinamento contínuo

---

## Contato & Manutenção

- **Responsável:** Léo Motta
- **Repositório:** github.com/mottacastelo-ai/estudos
- **Pasta local:** C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos

---

**Última atualização:** 11 de Maio de 2026 — Reorganização para estrutura por disciplina/tema; adicionadas seções de Ciências e História.
