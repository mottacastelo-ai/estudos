---
name: skill-hq-imagens
description: "Gera automaticamente todas as imagens de uma HQ (folha de personagens + 4 páginas) no GPT Quadrinhos Sabendo para o portal educacional 5º Ano. Adaptação do hq-generator genérico com os parâmetros corretos deste projeto."
---

# Skill: Gerador de Imagens HQ — Portal 5º Ano

## Quando usar

Quando Léo quer gerar as imagens da HQ de um tema a partir do `hq-[slug]-prompt.md`.

---

## Parâmetros para este projeto

| Parâmetro | Valor fixo para este portal |
|---|---|
| `PASTA_PROJETO` | `C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos` |
| `SUBFOLDER` | `[disciplina]/[slug]` (ex.: `historia/marcos-memoria`) |
| `PROMPT_MD` | `[PASTA_PROJETO]\[disciplina]\[slug]\hq-[slug]-prompt.md` |

> Imagens canônicas de referência estão na **raiz do projeto** (arquivos "versao canonica *.png").

---

## Convenção de nomes dos arquivos de saída

| Imagem | Destino | Nome do arquivo |
|---|---|---|
| Folha de personagens | `C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\Personagens\5o ano\` | `[Nome do Personagem].png` |
| Página 1 | `[PASTA_PROJETO]\[disciplina]\[slug]\` | `hq-[slug]-pg1.png` |
| Página 2 | `[PASTA_PROJETO]\[disciplina]\[slug]\` | `hq-[slug]-pg2.png` |
| Página 3 | `[PASTA_PROJETO]\[disciplina]\[slug]\` | `hq-[slug]-pg3.png` |
| Página 4 | `[PASTA_PROJETO]\[disciplina]\[slug]\` | `hq-[slug]-pg4.png` |

> O nome do personagem é extraído do `hq-[slug]-prompt.md` na linha `### Personagem principal: [NOME]`.

---

## Regras técnicas críticas (nunca violar)

1. **Chrome é tier "read" para computer-use** — toda interação com o browser usa Chrome MCP (`mcp__Claude_in_Chrome__*`), nunca computer-use para clicar ou digitar na janela do browser.

2. **Detectar conclusão via network requests** — monitorar `read_network_requests` com `urlPattern: "estuary"` para identificar novos file IDs. **Nunca usar presença/ausência de botões DOM** como sinal de conclusão — é impreciso.

3. **Aguardar com computer-use wait** — usar `mcp__computer-use__wait` (independente do Chrome) para esperar. `browser_batch` com wait faz timeout porque o Chrome fica ocupado durante a geração.

4. **Estado inconclusivo** — se após a espera nenhum novo file ID aparecer, navegar para a URL da conversa via `navigate` para recarregar. As imagens já geradas são preservadas e reaparecem nas network requests ao recarregar.

5. **Prefixo único por imagem** — usar prefixos diferentes nos chunks (`CHARS_`, `PG1_`, `PG2_`, `PG3_`, `PG4_`) para evitar colisão nos logs do console.

6. **Upload das canônicas uma única vez, manualmente pelo usuário** — pedir que o usuário faça upload das imagens canônicas antes do primeiro prompt. Usar `AskUserQuestion`. Não tentar `file_upload` do Chrome MCP em chatgpt.com — é bloqueado por restrição de segurança.

7. **Nova conversa por tema** — iniciar sempre uma nova conversa no GPT Quadrinhos Sabendo para cada tema.

8. **Folha de personagens primeiro** — sempre a primeira geração, estabelecendo referência visual para as páginas seguintes.

9. **Nunca usar `file://` URLs** para exibir imagens ao Chrome MCP — retorna "Frame showing error page".

10. **Sandbox bash sem acesso à rede Windows** — não tentar `python -m http.server` como solução.

---

## Fase 0 — Preparação

### 0.1 Localizar imagens canônicas

```python
import os
pasta = r"C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos"
canonicas = [f for f in os.listdir(pasta) if 'canonica' in f.lower() and f.lower().endswith('.png')]
canonicas = [os.path.join(pasta, f) for f in canonicas]
# Resultado esperado: versao canonica Bia.png, versao canonica Bia com fundo.png, versao canonica prepo.png
```

### 0.2 Abrir o GPT Quadrinhos Sabendo no Chrome

URL base: `https://chatgpt.com/g/g-69ff2b40169881918c5f75a8d9767f30-gpt-quadrinhos-sabendo`

Verificar via `tabs_context_mcp` se já há aba aberta. Se sim, usar o TAB_ID existente.

### 0.3 Solicitar upload manual das canônicas (AskUserQuestion)

Texto da pergunta:
> "Encontrei [N] imagem(ns) canônica(s) de referência:
> [lista dos arquivos]
>
> Por favor:
> 1. Clique no botão **+** (anexar) no input do GPT Quadrinhos Sabendo
> 2. Faça upload de TODAS as imagens listadas acima
> 3. **NÃO envie ainda** — aguarde eu injetar o prompt
> 4. Confirme aqui quando as imagens aparecerem no campo de texto"

Opção: `["✅ Imagens anexadas, pode continuar"]`

### 0.4 Extrair prompts e nome do personagem do .md

Ler o arquivo `hq-[slug]-prompt.md` e extrair:

**Prompts de cada seção:**
- `## FOLHA DE PERSONAGENS` → prompt `chars`
- `## PÁGINA 1` → prompt `pg1`
- `## PÁGINA 2` → prompt `pg2`
- `## PÁGINA 3` → prompt `pg3`
- `## PÁGINA 4` → prompt `pg4`

**Nome do personagem novo** (para nomear o arquivo chars):

```python
import re

with open(PROMPT_MD, encoding='utf-8') as f:
    conteudo = f.read()

# Procurar padrão "### Personagem principal: NOME"
match = re.search(r'###\s+Personagem principal:\s+(.+)', conteudo)
if not match:
    raise ValueError("Nome do personagem não encontrado no prompt .md")

NOME_PERSONAGEM = match.group(1).strip()
# Ex.: "POLI" → salvar como "Poli.png" (title case)
NOME_ARQUIVO_CHARS = NOME_PERSONAGEM.title() + ".png"
```

### 0.5 Iniciar tracking de network requests

Chamar `read_network_requests` com `urlPattern: "estuary"` uma vez. Salvar file IDs já presentes como `ids_conhecidos`.

---

## Fase 1 — Loop de geração

**Ordem:** `chars` → `pg1` → `pg2` → `pg3` → `pg4`

Para cada imagem:

### Passo 1: Injetar prompt (duas chamadas JavaScript separadas)

**Chamada 1 — texto:**
```javascript
const el = document.querySelector('#prompt-textarea');
el.focus();
document.execCommand('selectAll');
document.execCommand('insertText', false, PROMPT_TEXTO);
'injected';
```

**Chamada 2 — envio:**
```javascript
const btn = document.querySelector('button[data-testid="send-button"]');
if (btn) { btn.click(); 'clicked'; } else { 'not found'; }
```

### Passo 2: Aguardar conclusão

- `mcp__computer-use__wait` com 60 segundos
- Após espera: `read_network_requests` com `urlPattern: "estuary"`
- Verificar novos file IDs (não presentes em `ids_conhecidos`)
- Ciclo máximo: 5 tentativas (5 minutos total)
- Se 5 ciclos sem resultado: navegar para URL da conversa, aguardar 5s, verificar novamente

### Passo 3: Download via base64

```javascript
(async () => {
  const url = `https://chatgpt.com/backend-api/estuary/content?id=${FILE_ID}&ts=${TS}&p=fs&cid=1&sig=${SIG}&v=0`;
  const resp = await fetch(url, {credentials: 'include'});
  const buf = await resp.arrayBuffer();
  const u8 = new Uint8Array(buf);
  let binary = '';
  for (let i = 0; i < u8.length; i += 8192) {
    binary += String.fromCharCode(...u8.subarray(i, Math.min(i+8192, u8.length)));
  }
  const b64 = btoa(binary);
  const CHUNK = 100000;
  console.log('PREFIX_START:' + b64.length);
  for (let i = 0; i < b64.length; i += CHUNK) {
    console.log('PREFIX_CHUNK_' + Math.floor(i/CHUNK) + ':' + b64.substring(i, i + CHUNK));
  }
  console.log('PREFIX_END');
  return 'b64_length:' + b64.length;
})();
```

Reconstituir base64 pelos chunks lidos no console e salvar via Python:

```python
import base64, os
b64 = ''.join(chunks)  # concatenar chunks PREFIX_CHUNK_0, PREFIX_CHUNK_1, ...
img_data = base64.b64decode(b64)

pasta_tema = os.path.join(
    r"C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos",
    SUBFOLDER  # ex.: "historia/marcos-memoria"
)

if SUFIXO == "chars":
    # Folha de personagens → pasta de personagens, nomeada pelo personagem
    pasta_destino = r"C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\Personagens\5o ano"
    os.makedirs(pasta_destino, exist_ok=True)
    nome_arquivo = NOME_ARQUIVO_CHARS  # ex.: "Poli.png"
else:
    # Páginas da HQ → pasta do tema
    pasta_destino = pasta_tema
    os.makedirs(pasta_destino, exist_ok=True)
    nome_arquivo = f"hq-{SLUG}-{SUFIXO}.png"  # ex.: hq-poliedros-pg1.png

with open(os.path.join(pasta_destino, nome_arquivo), 'wb') as f:
    f.write(img_data)
print(f"Salvo: {os.path.join(pasta_destino, nome_arquivo)}")
```

---

## Resultado esperado

**Pasta do tema** (`estudos/[disciplina]/[slug]/`):
```
hq-[slug]-pg1.png
hq-[slug]-pg2.png
hq-[slug]-pg3.png
hq-[slug]-pg4.png
```

**Pasta de personagens** (`Personagens/5o ano/`):
```
[Nome do Personagem].png    ← ex.: Poli.png, Verbão.png, Elinho.png
```

Após a skill concluir, o agente `colador-hq` combina pg1–pg4 em `hq-[slug].png` automaticamente.

---

## Referência completa

A skill genérica com todos os detalhes técnicos está em:
`C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos\hq-generator-SKILL-atualizado.md`
