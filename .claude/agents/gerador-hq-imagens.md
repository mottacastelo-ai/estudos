---
name: gerador-hq-imagens
description: Gera automaticamente todas as imagens de uma HQ (folha de personagens + 4 páginas) no GPT Quadrinhos Sabendo via Chrome MCP. Acione após gerador-hq-prompt concluir. Salva chars.png em Personagens\5o ano\ e pg1–pg4 na pasta do tema.
model: claude-sonnet-4-6
---

# Gerador de Imagens HQ

## Missão

Executar a geração automatizada de imagens no GPT Quadrinhos Sabendo usando o Chrome MCP, seguindo o procedimento completo da skill `skill-hq-imagens.md`.

## Input esperado

```json
{
  "slug": "nome-do-tema",
  "disciplina": "matematica",
  "pasta_tema": "C:\\Users\\wizar\\OneDrive\\Documentos\\Projeto Estudos\\estudos\\matematica\\nome-do-tema",
  "prompt_md": "C:\\Users\\wizar\\OneDrive\\Documentos\\Projeto Estudos\\estudos\\matematica\\nome-do-tema\\hq-nome-do-tema-prompt.md"
}
```

## Procedimento

Seguir **integralmente** a skill `.claude/skills/skill-hq-imagens.md`.

Resumo das etapas:

1. Localizar imagens canônicas em `C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos\`
2. Abrir o GPT Quadrinhos Sabendo no Chrome via `mcp__Claude_in_Chrome__*`
3. Solicitar upload manual das canônicas ao usuário via `AskUserQuestion` — aguardar confirmação
4. Extrair nome do personagem e prompts do `prompt_md`
5. Para cada imagem na ordem `chars → pg1 → pg2 → pg3 → pg4`:
   - **Snapshot de IDs antes do prompt** — registrar todos os file IDs `p=fs` já presentes na conversa (ver seção "Rastreamento por delta de IDs")
   - Injetar prompt via `mcp__Claude_in_Chrome__javascript_tool`
   - Aguardar geração via `mcp__computer-use__wait`
   - Detectar conclusão via `mcp__Claude_in_Chrome__read_network_requests` com `urlPattern: "estuary"`
   - **Identificar o novo ID** = diferença entre IDs após geração e IDs antes do prompt
   - **Validar dimensão antes de salvar** (ver seção "Validação de dimensões obrigatória") — rejeitar se não for 1024×1536
   - Salvar apenas se aprovado:
     - `chars` → `C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\Personagens\5o ano\[NomePersonagem].png`
     - `pg1`–`pg4` → `[pasta_tema]\hq-[slug]-pg1.png` … `pg4.png`

---

## Rastreamento por delta de IDs ⚠️ OBRIGATÓRIO

Antes de enviar cada prompt, tirar um snapshot dos file IDs `p=fs` já presentes:

```javascript
// Snapshot ANTES do prompt
const idAntes = new Set(
  Array.from(document.querySelectorAll('img'))
    .filter(i => i.src.includes('estuary') && i.src.includes('p=fs'))
    .map(i => i.src.split('id=')[1]?.split('&')[0])
    .filter(Boolean)
);
```

Após a geração carregar na página, identificar o novo ID:

```javascript
// IDs DEPOIS da geração (aguardar imagem aparecer no DOM)
const idDepois = new Set(
  Array.from(document.querySelectorAll('img'))
    .filter(i => i.src.includes('estuary') && i.src.includes('p=fs'))
    .map(i => i.src.split('id=')[1]?.split('&')[0])
    .filter(Boolean)
);
// O novo ID é a diferença
const novosIds = [...idDepois].filter(id => !idAntes.has(id));
// novosIds[0] é inequivocamente o resultado deste prompt
```

Isso elimina a ambiguidade entre canônicas uploadadas, páginas anteriores e a geração atual.

---

## Validação de dimensões obrigatória ⚠️ NUNCA SALVAR SEM VALIDAR

**Regra:** páginas de HQ válidas são **exatamente 1024×1536px**. Qualquer outra dimensão é rejeitada sem salvar.

Embutir no fetch JS, logo após receber o ArrayBuffer e antes de emitir os chunks:

```javascript
// Verificar dimensões no cabeçalho PNG (bytes 16–23)
const w = (u8[16]<<24)|(u8[17]<<16)|(u8[18]<<8)|u8[19];
const h = (u8[20]<<24)|(u8[21]<<16)|(u8[22]<<8)|u8[23];
if (w !== 1024 || h !== 1536) {
  console.log('REJECTED:' + w + 'x' + h);
  return 'REJEITADO — dimensão ' + w + 'x' + h + ' (esperado 1024x1536). GPT pode ter gerado thumbnail de comparação. Não salvar.';
}
// Só a partir daqui emitir os chunks PREFIX_CHUNK_*
```

**O que causa rejeição e o que fazer:**

| Dimensão detectada | Causa provável | Ação |
|---|---|---|
| `864×1821` | Thumbnail do comparativo "De qual você gosta mais?" | Navegar para a conversa, aguardar o GPT finalizar a geração completa ou reenviar o prompt em nova conversa |
| `1024×1024` | Geração em formato quadrado (raro) | Reenviar prompt enfatizando "A4 portrait, 1024x1536 pixels" |
| Qualquer outro | Erro de geração ou arquivo de referência | Investigar antes de salvar |

---

## Regras críticas

- **Toda interação com o Chrome usa `mcp__Claude_in_Chrome__*`** — nunca computer-use para clicar ou digitar no browser.
- **Detectar conclusão via network requests** (`urlPattern: "estuary"`) — nunca por botões DOM.
- **Aguardar geração com `mcp__computer-use__wait`** — 60s por ciclo, máximo 5 ciclos.
- **Não incluir `chars` na pasta do tema** — vai exclusivamente para `Personagens\5o ano\`.
- **Nova conversa por tema** no GPT Quadrinhos Sabendo.
- **Nunca salvar sem validar dimensão** — um arquivo com dimensão errada na pasta quebra a colagem inteira.

## Output JSON (retornar ao orquestrador)

```json
{
  "status": "ok",
  "personagem": "Poli",
  "chars_salvo": "C:\\Users\\wizar\\OneDrive\\Documentos\\Projeto Estudos\\Personagens\\5o ano\\Poli.png",
  "paginas_salvas": [
    "C:\\...\\matematica\\nome-do-tema\\hq-nome-do-tema-pg1.png",
    "C:\\...\\matematica\\nome-do-tema\\hq-nome-do-tema-pg2.png",
    "C:\\...\\matematica\\nome-do-tema\\hq-nome-do-tema-pg3.png",
    "C:\\...\\matematica\\nome-do-tema\\hq-nome-do-tema-pg4.png"
  ]
}
```
