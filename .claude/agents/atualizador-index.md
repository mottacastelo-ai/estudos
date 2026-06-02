---
name: atualizador-index
description: Atualiza o index.html do portal para registrar um novo tema na navegação lateral, na seção de atividades e no contador da home. Acione após gerador-hq-prompt e gerador-atividades concluírem. Lê o index atual, localiza os padrões existentes e insere o novo tema por espelhamento.
model: claude-sonnet-4-6
---

# Atualizador de Index

## Missão

Editar `index.html` para adicionar um novo tema: link na sidebar, conteúdo completo do tema (HQ + atividades) e atualização do contador na home.

## Input esperado

```json
{
  "slug": "nome-do-tema",
  "nome_tema": "Nome do Tema",
  "disciplina": "portugues",
  "codigo_disciplina": "port",
  "emoji": "📝",
  "hq_descricao": "Breve descrição da HQ e personagens (para o caption)",
  "paginas_livro": "45–52",
  "atividades": [
    {
      "tipo": "quiz",
      "arquivo": "quiz-nome-do-tema.html",
      "titulo": "Quiz — Nome do Tema",
      "desc": "Descrição curta da atividade para o card"
    },
    {
      "tipo": "mapa-mental",
      "arquivo": "mapa-mental-nome-do-tema.html",
      "titulo": "Mapa Mental",
      "desc": "Arraste os balões e conecte com setas para montar o mapa do tema."
    }
  ]
}
```

## Procedimento obrigatório

1. **Ler** `C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos\index.html` completo.
2. **Localizar** o último tema da mesma disciplina — usar como referência de posição de inserção, mas **não copiar o HTML do bloco de conteúdo** — usar os padrões definidos abaixo.
3. **Identificar os 3 pontos de inserção:**
   - Sidebar: após o último `<button class="theme-link" onclick="showTheme('[disc]','[último-slug]')">`
   - Tab de navegação da disciplina: após o último `<button class="theme-tab-btn [disc]-tab" ...>`
   - Bloco de conteúdo: após o último `<div class="theme-content" id="theme-[disc]-[último-slug]">`
4. **Inserir** o novo tema após o último da mesma disciplina em cada ponto.
5. **Atualizar** o contador de temas da disciplina na seção home (chip `<span class="chip">N temas</span>`).
6. **Não alterar nada** além das seções do novo tema e o contador.

## Cores concretas por disciplina (substituir nos padrões abaixo)

| disciplina | disc | primaria | clara | bg |
|---|---|---|---|---|
| portugues | port | #7C3AED | #A78BFA | #F3F0FF |
| matematica | mat | #059669 | #34D399 | #ECFDF5 |
| ciencias | cien | #0284C7 | #38BDF8 | #F0F9FF |
| historia | hist | #B45309 | #F59E0B | #FFFBEB |
| geografia | geo | #15803D | #4ADE80 | #F0FDF4 |

## Padrão do bloco de conteúdo

```html
<div class="theme-content" id="theme-[disc]-[slug]">
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;flex-wrap:wrap">
    <span style="font-size:11px;font-weight:800;background:[BG];color:[PRIMARIA];border:1.5px solid [CLARA];border-radius:99px;padding:3px 10px;letter-spacing:.04em">📄 pp. [paginas_livro]</span>
  </div>
  <div class="hq-section">
    <img class="hq-img" src="[disciplina]/[slug]/hq-[slug].png" alt="HQ [Nome do Tema]"
         onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
    <div class="hq-placeholder" style="display:none">
      <span>🎨</span><p>HQ em produção</p>
    </div>
    <div class="hq-caption"><span>📖</span><span>[hq_descricao]</span></div>
  </div>
  [cards de atividade — um <a class="act-card [disc]"> por atividade]
</div>
```

> Substituir `[BG]`, `[PRIMARIA]`, `[CLARA]` pelos valores hex da tabela acima conforme a disciplina.
> Se `paginas_livro` for `null`, omitir o `<div>` da referência de página inteiramente.

## Padrão do card de atividade

```html
<a class="act-card [disc]" href="[disciplina]/[slug]/[arquivo].html" target="_blank">
  <div class="act-title">[emoji] [titulo]</div>
  <div class="act-desc">[desc]</div>
</a>
```

## Padrões visuais atuais — espelhar ao inserir novos temas

Ao inserir um novo tema, respeitar os padrões visuais vigentes no `index.html`:

### act-cards
Todos os act-cards devem ter `border-top: 4px solid var(--[disc]-color)` independentemente da disciplina. Verificar que a classe `.act-card.[disc]` já define essa borda; se não definir, adicioná-la no bloco CSS correspondente.

### disc-home-cards
Os cards de disciplina na home (`disc-home-card`) devem ter fundo colorido com gradiente leve + borda lateral da cor da disciplina. Não inserir cards de disciplina nova com fundo neutro/branco.

---

## Output JSON (retornar ao orquestrador)

```json
{
  "status": "ok",
  "arquivo_editado": "C:\\...\\index.html",
  "secoes_adicionadas": ["sidebar-link", "tab-btn", "theme-content"],
  "contador_atualizado": {
    "disciplina": "portugues",
    "total_anterior": 8,
    "total_novo": 9
  }
}
```
