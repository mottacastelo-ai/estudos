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
2. **Localizar** o último tema da mesma disciplina — copiar exatamente o padrão HTML dele.
3. **Identificar os 3 pontos de inserção:**
   - Sidebar: botão `<button class="theme-link" onclick="showTheme('[disc]','[último-slug]')">`
   - Tab de navegação da disciplina: botão `<button class="theme-tab-btn [disc]-tab" ...>`
   - Bloco de conteúdo: `<div class="theme-content" id="theme-[disc]-[último-slug]">`
4. **Inserir** o novo tema após o último da mesma disciplina em cada ponto.
5. **Atualizar** o contador de temas da disciplina na seção home (chip `<span class="chip">N temas</span>`).
6. **Não alterar nada** além das seções do novo tema e o contador.

## Padrão do bloco de conteúdo (espelhar do existente)

```html
<div class="theme-content" id="theme-[disc]-[slug]">
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

## Padrão do card de atividade

```html
<a class="act-card [disc]" href="[disciplina]/[slug]/[arquivo].html" target="_blank">
  <div class="act-title">[emoji] [titulo]</div>
  <div class="act-desc">[desc]</div>
</a>
```

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
