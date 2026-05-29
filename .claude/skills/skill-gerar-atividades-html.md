---
name: skill-gerar-atividades-html
description: "Guia do design system e padrões de código para geração de atividades HTML interativas do portal educacional. Usado pelo agente gerador-atividades."
---

# Skill: Gerador de Atividades HTML

## Quando usar

Quando o agente `gerador-atividades` precisa criar arquivos HTML de atividades interativas.

---

## Design system — Regras invioláveis

### Fontes

```html
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700;800;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
```

- **Baloo 2** — corpo de texto, botões, opções
- **Space Mono** — títulos de seção, headers, contadores

### CSS Variables por disciplina

```css
/* Português */
:root { --port: #7C3AED; --port-light: #A78BFA; --port-bg: #F3F0FF; --port-dark: #4C1D95; --border: #DDD6FE; }

/* Matemática */
:root { --mat: #059669; --mat-light: #34D399; --mat-bg: #ECFDF5; --mat-dark: #064E3B; --border: #D1FAE5; }

/* Ciências */
:root { --cien: #0284C7; --cien-light: #38BDF8; --cien-bg: #F0F9FF; --cien-dark: #075985; --border: #BAE6FD; }

/* História */
:root { --hist: #B45309; --hist-light: #F59E0B; --hist-bg: #FFFBEB; --hist-dark: #78350F; --border: #FDE68A; }

/* Geografia */
:root { --geo: #15803D; --geo-light: #4ADE80; --geo-bg: #F0FDF4; --geo-dark: #14532D; --border: #BBF7D0; }

/* Globais — igual em todas */
:root { --text: #1A1A2E; --muted: #6B7280; --card: #fff; --radius: 18px; }
```

### Estrutura base de todo HTML

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Tipo] — [Nome do Tema]</title>
  <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700;800;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
  <style>/* CSS completo inline */</style>
</head>
<body>
  <!-- Header com back button -->
  <div class="header">
    <a href="../../index.html" class="back-btn">← Voltar</a>
    <h1>[Título da Atividade]</h1>
    <p>[Subtítulo / descrição breve]</p>
  </div>
  <!-- Conteúdo -->
  <script>/* JS completo inline */</script>
</body>
</html>
```

### Header obrigatório

```css
.header {
  background: linear-gradient(135deg, [dark], [primaria] 60%, [clara]);
  color: white; padding: 28px 28px 24px;
}
.back-btn {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12px; font-weight: 800; color: rgba(255,255,255,.7);
  text-decoration: none; margin-bottom: 14px; transition: color .15s;
}
.back-btn:hover { color: white; }
.header h1 { font-family: "Space Mono", monospace; font-size: 22px; margin-bottom: 4px; }
.header p { font-size: 13px; font-weight: 600; opacity: .85; }
```

---

## Gamificação — obrigatória em toda atividade

### Elementos mínimos

1. **Pontuação** — contador visível (ex.: "Acertos: 7/10")
2. **Feedback imediato** — ao responder, mostrar certo/errado com explicação
3. **Barra de progresso** — indicar questão atual / total
4. **Tela de resultado final** — score, mensagem personalizada, opção de refazer

### Feedback imediato — padrão

```css
.feedback { border-radius: 12px; padding: 14px 18px; margin-top: 12px; display: flex; align-items: flex-start; gap: 10px; }
.feedback.correct { background: #D1FAE5; border: 2px solid #34D399; }
.feedback.wrong { background: #FEE2E2; border: 2px solid #FCA5A5; }
.feedback-icon { font-size: 20px; flex-shrink: 0; }
.feedback-text { font-size: 14px; font-weight: 700; color: var(--text); line-height: 1.4; }
```

### Mensagens de resultado por faixa

```javascript
function getMessage(score, total) {
  const pct = score / total;
  if (pct === 1)   return "🏆 Perfeito! Você dominou o tema!";
  if (pct >= 0.8)  return "⭐ Muito bem! Você está ótimo!";
  if (pct >= 0.6)  return "👍 Bom trabalho! Revise o que errou.";
  return "📚 Continue estudando! Tente novamente.";
}
```

---

## Tipos de atividade — padrões de código

### Quiz (quiz-[slug].html)

- 8–12 questões de múltipla escolha
- 4 opções por questão
- Uma questão por tela (não mostrar todas de uma vez)
- Após resposta: bloquear opções + mostrar feedback + botão "Próxima"
- Última tela: resultado com score, percentual e botão "Tentar novamente"

```javascript
// Estrutura de dados
const questions = [
  {
    text: "Qual é a definição de [termo técnico]?",
    options: ["Opção A", "Opção B (correta)", "Opção C", "Opção D"],
    correct: 1, // índice da opção correta
    explanation: "Explicação com o termo técnico exato: [termo]..."
  }
];
```

### Mapa Mental (mapa-mental-[slug].html)

**Template canônico:** `historia/diversidade-cultural/mapa-mental-diversidade-cultural.html`
**OBRIGATÓRIO:** ler esse arquivo antes de escrever qualquer mapa mental. Nunca inventar estrutura diferente.

#### Regras absolutas — NUNCA violar

| ❌ NUNCA fazer | ✅ SEMPRE fazer |
|---|---|
| `connects: ['central']` nos objetos de nó | `{id, label, cls}` apenas — sem propriedade `connects` |
| Função que desenha conexões automaticamente no load | Conexões desenhadas SOMENTE pelo usuário em modo Conectar |
| Gabarito como overlay/modal sobre o stage | Gabarito como painel inline ABAIXO do stage |
| `setMode('connect')` no load | `setMode('move')` no load — Mover ativo por padrão |
| Mais de 10 nós | Máximo 10 nós (exemplos contam para o limite) |
| `btn-connect` com `class="active"` no HTML inicial | `btn-move` com `class="active"` no HTML inicial |

#### Identificação de padrão correto vs. errado

Antes de editar qualquer mapa mental existente, verificar:
- `grep arrowFrom` no arquivo → se encontrar, o padrão connect/delete está implementado ✅
- `grep "load.*setMode\|setMode.*move"` → se encontrar `setMode('move')`, o modo padrão está correto ✅
- Ambos devem estar presentes. Se faltarem, o arquivo precisa de reescrita a partir do canônico.

#### Estrutura de dados obrigatória

```javascript
// 1. Nós — SEM propriedade connects, máximo 10 total
var NODES = [
  {id:'central', label:'🎯 [CONCEITO CENTRAL]', cls:'n-root'},
  {id:'cat1',    label:'[Categoria 1]',          cls:'n-level1'},
  {id:'cat2',    label:'[Categoria 2]',          cls:'n-level1'},
  {id:'cat3',    label:'[Categoria 3]',          cls:'n-level1'},
  {id:'det1',    label:'[Detalhe 1.1]',          cls:'n-level2'},
  {id:'det2',    label:'[Detalhe 2.1]',          cls:'n-level2'},
  // máximo 10 nós — exemplos contam para o limite
];

// 2. Gabarito — array separado, pares [origem, destino]
//    NÃO é desenhado automaticamente; apenas usado para calcular score
var GABARITO = [
  ['central','cat1'], ['central','cat2'], ['central','cat3'],
  ['cat1','det1'], ['cat2','det2'],
];

// 3. Ordem embaralhada para posicionamento inicial no grid
var SHUFFLE = ['det1','cat2','central','cat3','cat1','det2'];
```

#### Toolbar HTML — estrutura exata (5 botões)

```html
<div class="toolbar">
  <button class="tb-btn" id="btn-connect" onclick="setMode('connect')">+ Conectar</button>
  <button class="tb-btn active" id="btn-move" onclick="setMode('move')">✥ Mover</button>
  <button class="tb-btn" id="btn-erase" onclick="setMode('erase')">✕ Apagar seta</button>
  <button class="tb-btn" onclick="resetStage()">↺ Reiniciar</button>
  <button class="tb-btn tb-gabarito" onclick="toggleGabarito()">Ver gabarito</button>
</div>
```

`btn-move` **deve ter** `class="active"` no HTML estático — não apenas setado via JS no load.

#### Modo padrão no load

```javascript
window.addEventListener('load', function() {
  calcPositions();
  setMode('move'); // SEMPRE move, nunca connect
});
```

#### Gabarito — painel inline abaixo do stage

```html
<!-- FORA do stage, logo abaixo dele, oculto por padrão -->
<div id="gabarito-panel" style="display:none;">
  <svg id="gabarito-svg" viewBox="0 0 700 230" style="width:100%;max-width:700px">
    <!-- linhas e nós estáticos desenhados à mão para o tema -->
  </svg>
  <div id="score-bar">0 de N conexões</div>
</div>
```

O `score-bar` mostra conexões corretas ao fechar o gabarito. Nunca usar `position:fixed` ou overlay.

#### CSS — adaptar cores para a disciplina

```css
/* Substituir pelos valores da disciplina conforme tabela de paleta */
.n-root   { background: linear-gradient(135deg,[PRIMARIA],[CLARA]); color:white; border:2px solid [DARK]; }
.n-level1 { background:[BG-MEDIO]; border:2px solid [CLARA]; color:[DARK]; }
.n-level2 { background:white; border:2px solid [BG-MEDIO]; color:#374151; }
```

#### Gabarito SVG — posições de referência

Viewbox `0 0 700 230`. Layout sugerido para 3 categorias L1:
- Raiz: cx≈350, y≈20
- L1 esquerda: cx≈112, L1 centro: cx≈350, L1 direita: cx≈588 — todas y≈96
- L2: distribuídas sob cada L1 em y≈170

### Classificador (classificador-[slug].html)

- 2–4 categorias como destinos (drop zones)
- 8–12 itens para arrastar
- Feedback por item: animação verde/vermelho ao soltar
- Placar final com itens corretos/errados por categoria

### Ordenação (ordenacao-[slug].html)

- Lista de itens embaralhados para colocar em sequência
- Arrastar ou clicar para reposicionar
- "Verificar" mostra a ordem correta destacada

**CSS obrigatório para zonas de destino (drop-zone):**
```css
.drop-zone {
  min-height: 80px;          /* nunca menos — deve acomodar o card arrastado */
  padding: 12px 16px;        /* espaço interno visível mesmo vazio */
  margin-bottom: 8px;
  border-radius: 12px;
  border: 2px dashed var(--border);
  background: #F9FAFB;
  display: flex; align-items: center;
  position: relative;
}
.drag-card {
  min-height: 56px;          /* cards sempre menores que a drop-zone */
  padding: 10px 16px;
}
```
> ⚠️ A `drop-zone` deve ser **sempre maior** que o `drag-card`. Nunca use `min-height` menor que 80px na zona.

### Complete Lacuna (complete-lacuna-[slug].html)

- Frases com `___` para preencher
- Input de texto ou dropdown de opções
- Normalizar comparação (lowercase, trim, remover acentos para matching)

### Detetive de Nomes (detetive-nomes-[slug].html)

- Texto apresentado com elementos para identificar e clicar
- Aluno clica nos elementos corretos (ex.: substantivos, faces de um poliedro)
- Destacar certo (verde) / errado (vermelho) ao clicar

---

## Responsividade — regras para celular

Notebook é o uso principal, mas celular deve ser plenamente navegável. Toda atividade deve funcionar sem perda de funcionalidade em 375px de largura.

### CSS obrigatório

```css
/* Nunca usar largura fixa em px para containers principais */
.main { max-width: 680px; margin: 0 auto; padding: 32px 20px 0; }

/* Cards e botões: full-width em telas pequenas */
@media (max-width: 480px) {
  .main { padding: 20px 14px 0; }
  .header h1 { font-size: 18px; }
  .q-text { font-size: 16px; }
  .opt-btn { font-size: 14px; padding: 12px 14px; }
}
```

### Regras de interação

- **Sem hover exclusivo** — qualquer efeito de hover deve ter equivalente em tap/touch.
- **Tap targets mínimos de 48×48px** — botões, opções, cards de arrastar.
- **Scroll vertical apenas** — nunca scroll horizontal; usar `overflow-x: hidden` no body.
- **Fontes mínimas** — 14px para texto auxiliar, 16px para questões e opções.
- **Drag-and-drop em mobile** — atividades de arrastar devem usar eventos de touch além dos de mouse:
  ```javascript
  // Sempre par: mousedown/touchstart, mousemove/touchmove, mouseup/touchend
  el.addEventListener('mousedown', startDrag);
  el.addEventListener('touchstart', startDrag, { passive: false });
  ```
- **Teclado virtual** — inputs de texto devem ter `font-size: 16px` para evitar zoom automático no iOS.

### O que nunca fazer

- `position: fixed` em elementos grandes (quebra em celular com barra de endereço dinâmica)
- `width: 700px` fixo em qualquer container
- Tabelas sem `overflow-x: auto` no wrapper
- Texto em imagem como único portador de informação (ilegível em tela pequena)

---

## Regras de qualidade

1. **Sem dependências externas** além do Google Fonts — zero `<script src>` externos
2. **Sem `alert()` ou `confirm()`** — toda interação dentro do próprio HTML
3. **Acessibilidade básica** — `aria-label` em botões sem texto descritivo, `alt` em imagens
4. **Evitar `!important`** — estruturar CSS com especificidade adequada
5. **Consistência visual** — espaçamentos múltiplos de 4px, border-radius de 18px para cards
6. **Sem conteúdo inventado** — perguntas e gabaritos derivam exclusivamente dos `conceitos_chave` e `termos_tecnicos` do JSON

---

## Boas práticas

- Abrir o arquivo no browser mentalmente e pensar: "isso funciona num celular de 375px sem scroll horizontal?"
- Botões de opção com altura mínima de 48px (toque fácil em celular)
- Feedback sempre visível sem precisar rolar a tela
- Não usar animações pesadas — transições `0.2s ease` são suficientes
- Textos das questões devem ser claros e diretos; evitar dupla negação
