---
name: skill-atualizar-index
description: "Guia dos padrões HTML do index.html para inserção de novos temas no portal educacional. Usado pelo agente atualizador-index."
---

# Skill: Atualizar Index HTML

## Quando usar

Quando o agente `atualizador-index` precisa registrar um novo tema no `index.html`.

---

## Anatomia do index.html

O `index.html` tem 4 regiões que precisam ser atualizadas para cada novo tema:

```
1. SIDEBAR — botão de link para o tema
2. TABS — botão na barra de navegação da disciplina  
3. THEME-CONTENT — bloco completo do tema (HQ + atividades)
4. HOME COUNTER — contador de temas no card da disciplina
```

---

## Região 1 — Sidebar

Localizar o bloco de links da disciplina (ex.: `<!-- MATEMÁTICA -->`).
Inserir após o último `<button class="theme-link"` da disciplina:

```html
<button class="theme-link" onclick="showTheme('[disc]','[slug]')">[emoji] [Nome do Tema] <span style="opacity:.55;font-size:10px;font-weight:700">pp.[paginas_livro]</span></button>
```

Exemplo real (mat, pp. 78–92):
```html
<button class="theme-link" onclick="showTheme('mat','poliedros-prismas-piramides')">🏛️ Poliedros, Prismas e Pirâmides <span style="opacity:.55;font-size:10px;font-weight:700">pp.78–92</span></button>
```

> Se `paginas_livro` for `null`, omitir o `<span>` e usar apenas:
> ```html
> <button class="theme-link" onclick="showTheme('[disc]','[slug]')">[emoji] [Nome do Tema]</button>
> ```

> **Atenção:** os temas existentes no index não têm o `<span>` de páginas — não copiar o botão de um tema existente como modelo para o padrão de sidebar. Usar sempre o padrão acima.

---

## Região 2 — Tabs de navegação da disciplina

Localizar a seção `<div class="theme-tabs [disc]-tabs">`. Inserir após o último botão:

```html
<button class="theme-tab-btn [disc]-tab" onclick="showTheme('[disc]','[slug]')">[emoji] [Nome do Tema]</button>
```

---

## Região 3 — Bloco de conteúdo do tema

Localizar a seção `<div class="themes-container" id="themes-[disc]">`. Inserir após o último `<div class="theme-content"` da disciplina:

```html
<div class="theme-content" id="theme-[disc]-[slug]">
  <div class="hq-section">
    <img class="hq-img"
         src="[disciplina]/[slug]/hq-[slug].png"
         alt="HQ [Nome do Tema] com [Personagem]"
         onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
    <div class="hq-placeholder" style="display:none">
      <span>🎨</span><p>HQ em produção</p>
    </div>
    <div class="hq-caption">
      <span>📖</span>
      <span>[Descrição da HQ — 1 frase com personagens e tema]</span>
    </div>
  </div>

  [CARDS DE ATIVIDADE]

</div>
```

### Cards de atividade — padrão

```html
<a class="act-card [disc]" href="[disciplina]/[slug]/[arquivo].html" target="_blank">
  <div class="act-title">[emoji] [Título da Atividade]</div>
  <div class="act-desc">[Descrição curta — 1 frase]</div>
</a>
```

Exemplos reais de títulos e descrições:

```html
<a class="act-card mat" href="matematica/poliedros-prismas-piramides/quiz-poliedros-prismas-piramides.html" target="_blank">
  <div class="act-title">🧩 Quiz</div>
  <div class="act-desc">10 questões sobre faces, vértices, arestas, poliedros regulares, prismas e pirâmides.</div>
</a>

<a class="act-card mat" href="matematica/poliedros-prismas-piramides/mapa-mental-poliedros-prismas-piramides.html" target="_blank">
  <div class="act-title">🗺️ Mapa Mental</div>
  <div class="act-desc">Arraste os balões e conecte com setas para montar o mapa do tema. Compare com o gabarito ao final.</div>
</a>
```

---

## Região 4 — Contador na home

Localizar o card da disciplina na seção home:
```html
<span class="chip" style="background:#ECFDF5;color:#065F46">4 temas</span>
```

Atualizar o número: `4 temas` → `5 temas`.

Também atualizar o contador global se houver:
```html
<div class="hstat"><span>20</span>temas</div>
```

---

## Mapeamento código da disciplina → classe CSS e pasta

| Disciplina | Código | Classe CSS | Pasta |
|---|---|---|---|
| Português | `port` | `port` | `portugues` |
| Matemática | `mat` | `mat` | `matematica` |
| Ciências | `cien` | `cien` | `ciencias` |
| História | `hist` | `hist` | `historia` |
| Geografia | `geo` | `geo` | `geografia` |

---

## Boas práticas

- Sempre usar a ferramenta `Read` para ler o `index.html` completo antes de editar
- Usar `Grep` com pattern `theme-[disc]-` para localizar o último tema existente da disciplina
- Verificar que o `id` do novo bloco é único: `theme-[disc]-[slug]`
- O `onerror` no `<img>` é obrigatório — a HQ pode não existir ainda quando o index é publicado
- Não quebrar a estrutura de indentação existente — copiar o padrão do último tema da mesma disciplina
- Após editar, verificar que `showTheme('[disc]','[slug]')` nos 3 pontos de inserção usam exatamente o mesmo `[slug]`
