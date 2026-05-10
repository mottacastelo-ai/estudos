---
name: portal-educacional
description: "Skill para o Portal Educacional do 5º Ano (github.com/mottacastelo-ai/estudos). Acione quando Léo fornecer fotos de conteúdo escolar ou mencionar novo tema, nova disciplina, fotos da escola, atividades para o portal ou atualizar o site. SEMPRE executa Fase 0 de análise de escopo e aguarda aprovação antes de gerar HQs, atividades ou HTML. Modo padrão via Cowork: edita index.html diretamente na pasta local e salva arquivos na raiz do projeto sem subpastas nem ZIPs. Fallback Claude.ai: ZIP com index.html completo já atualizado."
---

# Skill: Portal Educacional — 5º Ano

## Visão geral do processo

Dado um conjunto de fotos de conteúdo escolar, esta skill executa o seguinte pipeline:

```
FOTOS → [FASE 0] Análise de escopo → Proposta estrutural → ⏸ AGUARDAR APROVAÇÃO DE LÉO
         ↓ (após aprovação)
         Separação por tema → Para cada tema:
           1. Prompt HQ (.md)                   ← entregue para uso externo por Léo
           2. Atividades HTML (Quiz + variáveis + Mapa Mental)
           3. Atualização do index.html
           4. Entrega via Cowork
```

> **Nota:** A geração das imagens de HQ (ChatGPT) e a colagem das páginas são etapas externas à skill, executadas por Léo com a skill dedicada de HQ. A skill do portal entrega o prompt `.md` e segue direto para as atividades — o `hq-[slug].png` deve ser copiado manualmente por Léo para a raiz do projeto antes do deploy.

> **Regra absoluta:** Nenhum arquivo é gerado antes da aprovação explícita de Léo na Fase 0.

---

## FASE 0 — Análise de escopo e proposta estrutural ⚠️ OBRIGATÓRIA

**Esta fase ocorre antes de qualquer geração de conteúdo e exige confirmação explícita de Léo.**

### 0.1 Leitura do conteúdo

Examine todas as imagens fornecidas e extraia:
- Disciplina(s) identificada(s)
- Capítulos ou unidades visíveis
- Todos os subtemas e conceitos-chave presentes (listar exaustivamente)
- Habilidades específicas trabalhadas pelo livro (interpretar gráficos, produção escrita, etc.)

### 0.2 Critérios de divisão em temas

Aplique os seguintes critérios para decidir se o conteúdo deve ser dividido em um ou mais temas:

| Critério | Um único tema | Dois ou mais temas |
|---|---|---|
| Foco conceitual | Subtemas se subordinam a um conceito central | Subtemas têm autonomia conceitual própria |
| Volume de conteúdo | Até ~8 páginas do livro com densidade similar | Capítulos distintos ou mais de ~8 páginas densas |
| Coerência narrativa | Uma HQ consegue cobrir o arco com foco | Uma HQ por tema seria necessária para narrativa coesa |
| Habilidades distintas | Mesmas habilidades ao longo do material | Habilidades diferentes por bloco (ex.: gráficos em um, escrita em outro) |

**Sinal de alerta obrigatório:** se o conteúdo cobrir dois ou mais capítulos do livro com subtemas autônomos, a skill deve propor divisão em temas separados e justificar.

### 0.3 Formato da proposta estrutural

Apresente a Léo um relatório no seguinte formato **antes de gerar qualquer arquivo**:

---

**📚 Conteúdo identificado**
[Disciplina] — [Capítulo(s)/Unidade(s)]

**🗂️ Subtemas mapeados**
- [Subtema 1]: [conceitos-chave em bullets]
- [Subtema 2]: [conceitos-chave em bullets]
- ...

**🎯 Proposta de estrutura**

> Opção A — [N] tema(s): [Nome do Tema 1] + [Nome do Tema 2]
> Justificativa: [por que essa divisão serve melhor pedagogicamente]

> Opção B — Tema único: [Nome]
> Justificativa: [por que agrupar pode funcionar, com ressalvas de cobertura]

**⚠️ Alertas de cobertura**
[Listar conceitos ou habilidades que poderiam ficar de fora se o conteúdo for comprimido em menos temas do que o ideal]

**✅ Aguardando sua decisão para prosseguir.**

---

### 0.4 Regra de bloqueio

A skill **não avança para a Fase 1** até receber de Léo:
- Qual opção de estrutura foi aprovada (ou uma estrutura alternativa)
- Confirmação explícita para começar a geração

### 0.5 Regras de fidelidade ao conteúdo ⚠️ INVIOLÁVEIS

Estas duas regras se aplicam a **todas as fases** — HQ, atividades e index.html:

**Regra 1 — Termos técnicos do livro são obrigatórios**
Todo termo técnico presente nas fotos enviadas (ex.: "pretérito perfeito", "fotossíntese", "chorume") **deve aparecer** na HQ e nas atividades, com esse nome exato. Nunca substituir por sinônimos coloquiais como substituto exclusivo (ex.: usar só "passado" no lugar de "pretérito perfeito"). O aluno precisa reconhecer o termo quando encontrá-lo na prova.

> Origem desta regra: em Tempos Verbais o termo "pretérito" presente no livro foi omitido das atividades. O André não o reconheceu na prova.

**Regra 2 — Proibido introduzir termos fora do escopo das fotos**
Nenhum conceito, termo técnico ou conteúdo que **não esteja visível nas fotos enviadas** pode ser introduzido nas atividades ou HQ. Se a foto não mostrar, não existe para esta geração.

> Origem desta regra: em atividade do portal da Lis foram introduzidos termos que ela ainda não havia estudado, gerando esforço de aprendizado desnecessário e fora do momento pedagógico correto.

**Checklist de fidelidade** (executar antes de finalizar cada tema):
- [ ] Todos os termos técnicos das fotos estão presentes na HQ e em pelo menos uma atividade com o nome exato do livro
- [ ] Nenhum conceito foi introduzido sem respaldo nas fotos enviadas
- [ ] Sinônimos coloquiais (se usados para facilitar compreensão) sempre acompanham o termo técnico, nunca os substituem

---

## FASE 1 — Identificação e separação de temas (após aprovação da Fase 0)

### 1.1 Separação por tema

Com base na estrutura aprovada na Fase 0, delimite com precisão quais imagens/páginas pertencem a cada tema. Se um tema foi aprovado com dois capítulos separados, trate-os como projetos independentes e execute as fases seguintes para cada um.

### 1.2 Verificação de conflito com temas existentes

Consulte `references/temas-existentes.md` para verificar se o tema já foi implementado. Se já existir, pergunte antes de sobrescrever.

### 1.3 Mapeamento de disciplina → código

| Disciplina  | Código HTML | Cor primária | Cor clara   | Bg          | Gradiente hero                              |
|-------------|-------------|--------------|-------------|-------------|---------------------------------------------|
| Português   | `port`      | `#7C3AED`    | `#A78BFA`   | `#F3F0FF`   | `135deg, #2D1B69, #7C3AED 60%, #A78BFA`    |
| Matemática  | `mat`       | `#059669`    | `#34D399`   | `#ECFDF5`   | `135deg, #064E3B, #059669 60%, #34D399`    |
| Ciências    | `cien`      | `#0284C7`    | `#38BDF8`   | `#F0F9FF`   | `135deg, #0C4A6E, #0284C7 60%, #38BDF8`   |
| História    | `hist`      | `#B45309`    | `#F59E0B`   | `#FFFBEB`   | `135deg, #78350F, #B45309 60%, #F59E0B`   |
| Geografia   | `geo`       | `#15803D`    | `#4ADE80`   | `#F0FDF4`   | `135deg, #14532D, #15803D 60%, #4ADE80`   |

Para novas disciplinas não listadas, proponha uma paleta ao usuário antes de continuar.

---

## FASE 2 — Criação de personagem narrativo

Cada novo tema deve ter um personagem ou elemento narrativo novo (ou reutilizar existentes quando fizer sentido).

### Personagens já existentes (sempre disponíveis)
- **Prepo** — robô roxo mascote, aparece em múltiplos temas
- **Bia** — menina 11 anos, cabelos pretos cacheados, uniforme azul; protagonista frequente
- **Prof. Teatrão** — professor dramático com lenço colorido
- **Verbão** — letra animada, 3 versões de roupa (passado/presente/futuro)
- **Elinho** — letra ℓ animada, versões cowboy e surfista
- **Zé e Das Graças** — fantoches para variação linguística
- **? (azul/curioso), ! (vermelho-laranja/musculoso), . (cinza/calmo)** — pontuações animadas
- **Toni** — onda sonora animada (entonação)

### Diretrizes para novos personagens
- Deve ser metáfora visual do conteúdo (ex.: para Cadeia Alimentar → uma corrente animada chamada "Cadinho")
- Tom: lúdico, acolhedor, levemente dramático/engraçado
- Cor e estilo devem dialogar com a paleta da disciplina
- Sempre interage com Bia e/ou Prepo na HQ

---

## FASE 3 — Geração do prompt de HQ

O arquivo `.md` gerado deve ser um **documento de produção completo** — deve poder ser colado diretamente no ChatGPT (Images 2.0) sem nenhuma edição adicional. O padrão de qualidade é o arquivo `prompt-hq-entonacao.md`.

**Critérios obrigatórios:**
- Mínimo de 250 linhas
- Prompts em inglês para as ferramentas de geração (as ferramentas respondem melhor em inglês)
- Cada página tem seu próprio bloco de prompt pronto para colar, entre três backticks
- Bloco de estilo visual separado e reutilizável, aplicado em todas as páginas
- Folha de personagens dedicada (usada primeiro como referência visual na sessão do ChatGPT, mas não baixada)
- Instruções de uso no topo (qual ferramenta, qual ordem de geração)
- Dicas práticas no final (o que fazer se o texto dos balões sair errado, como obter consistência visual)
- Falas dos personagens em português dentro dos prompts em inglês, entre aspas

Crie o arquivo `.md` seguindo este template expandido:

```markdown
# PROMPT PARA HISTÓRIA EM QUADRINHOS
## Tema: [Nome do Tema]
## [Disciplina] — 5º ano

---

## INSTRUÇÕES DE USO

Cole o bloco de cada página diretamente no ChatGPT (Images 2.0) ou outra ferramenta de geração.
Gere uma página por vez, na ordem definida abaixo.

---

## ESTILO VISUAL (aplique em todas as páginas)

\`\`\`
[Bloco em inglês com: estilo geral, paleta de cores, traço, público-alvo,
elementos visuais temáticos da disciplina/tema, bordas dos painéis, estética dos balões]
\`\`\`

---

## PERSONAGENS FIXOS

| Personagem | Descrição visual |
|---|---|
| **Prepo** | [descrição visual consistente] |
| **Bia** | [descrição consistente] |
| [outros personagens recorrentes que aparecem no tema] | [descrição] |

---

## ROTEIRO — 4 PÁGINAS

---

### PÁGINA 1 — "[Título da página]"
**Objetivo pedagógico:** [o que o aluno deve aprender nesta página]

**PROMPT:**
\`\`\`
[Prompt completo em inglês, pronto para colar na ferramenta.
Descreve cada painel com: cenário, personagens, expressões, falas em português entre aspas,
elementos visuais temáticos, ondas/setas/ícones de apoio pedagógico]
\`\`\`

---

### PÁGINA 2 — "[Título]"
**Objetivo pedagógico:** [...]

**PROMPT:**
\`\`\`
[Prompt completo em inglês]
\`\`\`

---

### PÁGINA 3 — "[Título]"
**Objetivo pedagógico:** [...]

**PROMPT:**
\`\`\`
[Prompt completo em inglês]
\`\`\`

---

### PÁGINA 4 — "[Título]"
**Objetivo pedagógico:** [...]

**PROMPT:**
\`\`\`
[Prompt completo em inglês — último painel termina com personagem convidando o leitor a praticar no portal]
\`\`\`

---

## FOLHA DE PERSONAGENS (gere primeiro)

\`\`\`
[Prompt em inglês para folha de referência visual de todos os personagens.
Para personagens novos: mostrar pelo menos 3 variações emocionais lado a lado.
Fundo branco, nome abaixo de cada personagem, mesmo estilo das outras páginas.]
\`\`\`

---

## DICAS PARA MELHORES RESULTADOS

- [Dica específica sobre o personagem novo ou elemento visual central do tema]
- Se o texto dos balões sair em inglês, corrija no Canva
- [Qualquer outra dica relevante para este tema específico]

---

## ORDEM DE GERAÇÃO

1. Folha de personagens
2. Página 1 — [título]
3. Página 2 — [título]
4. Página 3 — [título]
5. Página 4 — [título]

---

*Conteúdo baseado em: [livro didático, páginas referenciadas]*
*Tema: [descrição resumida do conteúdo pedagógico]*
```

---

## FASE 4 — Design das atividades

> ⚠️ **Lembrete das Regras 0.5 antes de escrever qualquer questão ou enunciado:**
> - Use os termos técnicos exatos do livro (ex.: "pretérito perfeito", não apenas "passado")
> - Não introduza conceitos que não estejam nas fotos enviadas
> - Sinônimos coloquiais podem aparecer entre parênteses, mas nunca sozinhos

### 4.1 Atividades obrigatórias (todo tema, toda disciplina)

#### A) Quiz Interativo
- **Arquivo:** `quiz-[slug].html`
- **Estrutura:** 10 questões de múltipla escolha com 4 alternativas
- **Feedback:** imediato por questão + placar final com mensagem motivacional
- **Nível Glasser:** 📖 Retrieval practice
- **Card no index:**
```html
<a class="act-card [disc]" href="quiz-[slug].html" target="_blank">
  <div class="act-icon">❓</div>
  <div class="act-title">Quiz Interativo</div>
  <div class="act-desc">[10 questões sobre os conceitos principais do tema]</div>
  <div class="act-tags"><span class="tag tag-[tag-disc]">Digital</span><span class="tag tag-a">Ativo</span></div>
  <div class="level lv4">📖 Retrieval practice</div>
</a>
```

#### B) Mapa Mental
- **Arquivo:** `mapa-mental-[slug].html`
- **Estrutura:** Nós arrastáveis com conexões, gabarito ao final
- **Conteúdo:** 6-10 nós representando os conceitos-chave do tema
- **Nível Glasser:** 🏆 Ensinar (90%)
- **Sempre é a última atividade listada no act-grid**
- **Card no index:**
```html
<a class="act-card [disc]" href="mapa-mental-[slug].html" target="_blank">
  <div class="act-icon">🗺️</div>
  <div class="act-title">Mapa Mental</div>
  <div class="act-desc">Arraste os balões e conecte com setas para montar o mapa do tema. Compare com o gabarito ao final.</div>
  <div class="act-tags"><span class="tag tag-[tag-disc]">Digital</span><span class="tag tag-a">Síntese</span></div>
  <div class="level lv3">🏆 Ensinar (90%)</div>
</a>
```

### 4.2 Atividades variáveis

Consulte `references/atividades-por-disciplina.md` para sugestões por disciplina. Selecione **2-3 atividades** respeitando:
1. Nenhuma deve repetir o tipo de interação de outro tema da mesma disciplina
2. Deve cobrir pelo menos um nível intermediário (70% ou 80% da pirâmide)
3. Deve haver pelo menos uma atividade de criação/produção (90%)

A escolha deve ser **justificada** com base no conteúdo específico do tema.

### 4.3 Níveis e classes CSS

| Nível Glasser | Label               | Classe CSS |
|---------------|---------------------|------------|
| 50-60%        | 💬 Discutir (70%)   | `lv1`      |
| 70-80%        | ⚡ Praticar (80%)   | `lv2`      |
| 90%           | 🏆 Ensinar (90%)    | `lv3`      |
| Retrieval     | 📖 Retrieval practice | `lv4`    |

---

## FASE 5 — Geração de HTML das atividades

Cada arquivo HTML de atividade deve:

1. **Ser autocontido** — CSS e JS inline, sem dependências externas além de Google Fonts
2. **Usar as fontes do projeto:** `Baloo 2` + `Space Mono`
3. **Aplicar a paleta da disciplina** conforme tabela da Fase 1
4. **Ter feedback imediato** para cada interação
5. **Ter botão "Voltar ao Portal"** que fecha a aba (`window.close()`) ou vai para `index.html`
6. **Ser responsivo** (funcionar em mobile)
7. **Ter cabeçalho** com nome do tema e personagem em destaque

### Template base de atividade HTML

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Nome da Atividade] — [Tema]</title>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700;800;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root {
  --primary: [cor primária da disciplina];
  --light: [cor clara da disciplina];
  --bg: [bg da disciplina];
}
/* ... estilos da atividade ... */
</style>
</head>
<body>
<!-- Cabeçalho com personagem + título -->
<!-- Corpo da atividade -->
<!-- Rodapé com botão Voltar ao Portal -->
<script>
// Lógica da atividade
</script>
</body>
</html>
```

---

## FASE 6 — Atualização do index.html via Cowork

**Modo de operação padrão: Cowork acessa e edita o arquivo diretamente na pasta local.**

O `index.html` vive em:
```
C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos\index.html
```

O Cowork deve ler o arquivo, aplicar todas as modificações programaticamente e salvar — sem gerar arquivo de instrução separado, sem etapa manual de substituição.

### 6.1 Sequência de edições no index.html

Para cada novo tema, o Cowork executa as seguintes edições em ordem:

**Se nova disciplina:**

1. **Variáveis CSS** — inserir dentro do bloco `:root`:
```css
--[disc]-color: [cor primária];
--[disc]-light: [cor clara];
--[disc]-bg: [bg];
```

2. **Classes CSS da disciplina** — inserir após as classes `.act-card.mat:hover`:
```css
.act-card.[disc]:hover { box-shadow: 0 6px 24px rgba([rgb],.15); transform: translateY(-3px); border-color: var(--[disc]-light); }
.act-card.[disc] { border-top: 4px solid var(--[disc]-color); }
.act-card.[disc]::after { color: var(--[disc]-color); }
.disc-hero.[disc] { background: linear-gradient([gradiente da disciplina]); }
.disc-home-card.[disc]:hover { border-color: var(--[disc]-light); box-shadow: 0 8px 28px rgba([rgb],.15); }
.theme-tab-btn.[disc]-tab:hover { border-color: var(--[disc]-color); color: var(--[disc]-color); }
.theme-tab-btn.[disc]-tab.active { background: var(--[disc]-bg); border-color: var(--[disc]-color); color: var(--[disc]-color); }
.tag-[disc] { background: [bg claro]; color: [cor primária]; }
```

3. **Sidebar** — substituir o botão `soon` da disciplina pelo botão ativo com sub-menu:
```html
<button class="disc-nav-btn" id="nav-[disc]" onclick="showDisc('[disc]')">
  <span class="d-icon">[emoji]</span>
  <span class="d-name">[Nome]</span>
  <span class="d-count">[N temas]</span>
</button>
<div class="theme-sub" id="sub-[disc]">
  <button class="theme-link" onclick="showTheme('[disc]','[slug]')">[emoji] [Nome do Tema]</button>
</div>
```

4. **Card na home** — substituir o `div.disc-home-card.soon` da disciplina pelo card ativo:
```html
<button class="disc-home-card [disc]" onclick="showDisc('[disc]')">
  <div class="dhc-icon">[emoji]</div>
  <div class="dhc-name">[Nome]</div>
  <div class="dhc-desc">[descrição]</div>
  <div class="dhc-chips">
    <span class="chip" style="background:[bg];color:[cor]">[N] temas</span>
    <span class="chip" style="background:#ECFDF5;color:#065F46">[N] atividades</span>
  </div>
</button>
```

5. **Contadores da home** — atualizar os três `hstat` com os totais corretos.

6. **JavaScript `firstTheme`** — adicionar a disciplina no objeto:
```js
var firstTheme = { port: 'preposicoes', mat: 'tabuada', ..., [disc]: '[primeiro-slug]' }[disc];
```

7. **Screen da disciplina** — inserir antes de `</main>`:
```html
<div class="screen" id="screen-[disc]">
  <div class="disc-hero [disc]">...</div>
  <div class="disc-body">
    <div class="theme-tabs">...</div>
    <!-- theme-contents de cada tema -->
  </div>
</div>
```

**Se disciplina já existe (apenas novo tema):**

1. Adicionar `<button class="theme-link">` dentro do `div#sub-[disc]` na sidebar
2. Adicionar `<button class="theme-tab-btn [disc]-tab">` dentro do `.theme-tabs` da disciplina
3. Inserir novo `<div class="theme-content" id="theme-[disc]-[slug]">` dentro do `screen-[disc]`
4. Atualizar contador `d-count` da disciplina na sidebar
5. Atualizar chips e contadores da home

### 6.2 Estrutura do theme-content

```html
<div class="theme-content" id="theme-[disc]-[slug]">
  <div class="hq-card">
    <img class="hq-img" src="hq-[slug].png" alt="HQ [Nome do Tema]">
    <div class="hq-caption"><span>📖</span><span>[Título HQ] — 4 páginas · Personagens: [lista] · Tema: [tema]</span></div>
  </div>
  <hr class="sdiv">
  <div class="act-grid">
    <!-- act-cards -->
  </div>
  <hr class="sdiv">
  <div class="sched-title">📅 Sugestão de uso semanal</div>
  <div class="sched">
    <!-- sched-rows -->
  </div>
</div>
```

> **Atenção:** a extensão padrão do arquivo HQ é `.png`. Usar `.jpg` apenas se Léo fornecer a imagem nesse formato.

---

## FASE 7 — Entrega via Cowork

**Modo de operação padrão: tudo é escrito diretamente na pasta local do projeto.**

### 7.1 O que o Cowork escreve na pasta local

```
C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos\
├── index.html                         ← editado diretamente (Fase 6)
├── hq-[slug]-prompt.md                ← criado (Fase 3)
├── quiz-[slug].html                   ← criado (Fase 5)
├── mapa-mental-[slug].html            ← criado (Fase 5)
├── [atividade-variavel-1]-[slug].html ← criado (Fase 5)
└── [atividade-variavel-2]-[slug].html ← criado (Fase 5)
```

> **Nota:** o arquivo `hq-[slug].png` **não é gerado por esta skill** — Léo o gera externamente (skill de HQ) e o copia manualmente para a raiz do projeto antes do deploy.

### 7.2 Checklist antes de concluir

- [ ] `index.html` salvo com todas as alterações da Fase 6
- [ ] Todos os arquivos HTML das atividades na raiz da pasta
- [ ] Todos os `href` dos `act-card` no index batem com os nomes dos arquivos criados
- [ ] O `id` do `theme-content` bate com o `onclick` do tab e do sidebar
- [ ] Contadores da home atualizados
- [ ] `firstTheme` atualizado no JavaScript (se nova disciplina)
- [ ] Nenhum arquivo criado em subpasta
- [ ] `src` da `hq-img` no index usa extensão `.png` (ou `.jpg` se aplicável)
- [ ] Léo foi informado de que precisa copiar manualmente o `hq-[slug].png` para a pasta antes do deploy

### 7.3 Mensagem de conclusão

Ao finalizar, informar Léo:
1. Quais temas foram gerados e em qual disciplina
2. Quais atividades variáveis foram escolhidas e **por que** (justificativa pedagógica)
3. O personagem novo criado (se houver) com breve descrição
4. Se algum conceito da Fase 0 ficou sem cobertura nas atividades geradas
5. Lembrete para gerar as imagens de HQ com a skill dedicada e copiar o `hq-[slug].png` para a raiz do projeto
6. Próximo passo: commit + push no GitHub Desktop → GitHub Pages publica automaticamente

### 7.4 Fallback — quando executado fora do Cowork

Se a skill for executada no Claude.ai (sem acesso ao sistema de arquivos local), entregar um **único ZIP** contendo:
- Todos os arquivos HTML das atividades
- O `hq-[slug]-prompt.md`
- O `index.html` **completo e já atualizado** — nunca um arquivo de instruções separado

O `index.html` completo exige que Léo forneça o arquivo atual no início da conversa. Se não for fornecido, solicitar antes de prosseguir para a Fase 5.

---

## Referências

- `references/temas-existentes.md` — lista de todos os temas já implementados
- `references/atividades-por-disciplina.md` — catálogo de tipos de atividade por disciplina com critérios de escolha
- `references/index-template-snippets.md` — snippets HTML prontos para copiar ao atualizar o index
