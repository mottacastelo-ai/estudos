---
name: hq-generator
description: "Gera automaticamente todas as imagens de uma HQ (folha de personagens + 4 páginas) no Codex, solicitando ao usuário o upload manual das imagens canônicas uma única vez antes de iniciar, capturando as imagens via network interception e salvando os arquivos PNG na pasta do projeto. Skill genérica — funciona para qualquer portal (estudos-2ano, estudos, etc.)."
---

# Skill: Gerador de HQ — Codex

## Visão geral

Gera automaticamente todas as imagens de uma HQ (folha de personagens + 4 páginas) no Codex, solicitando ao usuário o upload manual das imagens canônicas de referência uma única vez antes de iniciar, capturando as imagens via network interception, e salvando os arquivos PNG na pasta do projeto.

**Esta skill é genérica — funciona para qualquer projeto** (estudos-2ano, estudos, etc.). A pasta do projeto e o slug do tema são passados por quem a invoca (normalmente a skill do portal correspondente).

---

## Parâmetros de entrada (recebidos de quem invoca)

| Parâmetro | Exemplo | Descrição |
|---|---|---|
| `PASTA_PROJETO` | `C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos` | Raiz do projeto |
| `SLUG` | `marcos-memoria` | Identificador do tema (usado nos nomes dos arquivos) |
| `SUBFOLDER` | `historia/marcos-memoria` | Subpasta relativa dentro de `PASTA_PROJETO` onde as imagens HQ serão salvas. Para estudos-2ano (sem subpastas), passar `""`. |
| `PROMPT_MD` | `C:\...\estudos\historia\marcos-memoria\hq-marcos-memoria-prompt.md` | Arquivo .md com os prompts de cada página |
| `CONVERSA_URL` | `https://chatgpt.com/g/g-69ff2b40169881918c5f75a8d9767f30-gpt-quadrinhos-sabendo/c/...` | URL da conversa ativa no Codex |
| `TAB_ID` | `2093235551` | ID da aba do Chrome com o GPT aberto |

---

## Convenção de nomes dos arquivos de saída

| Imagem | Nome do arquivo |
|---|---|
| Folha de personagens | `hq-[slug]-chars.png` |
| Página 1 | `hq-[slug]-pg1.png` |
| Página 2 | `hq-[slug]-pg2.png` |
| Página 3 | `hq-[slug]-pg3.png` |
| Página 4 | `hq-[slug]-pg4.png` |

Todos os arquivos são salvos na raiz de `PASTA_PROJETO`.

---

## Regras técnicas críticas

1. **Chrome é tier "read" para computer-use** — toda interação com o browser usa Chrome MCP (`mcp__Claude_in_Chrome__*`), nunca computer-use para clicar ou digitar na janela do browser.

2. **Detectar conclusão de geração via network requests** — monitorar `read_network_requests` com `urlPattern: "estuary"` para identificar novos file IDs. **Nunca usar presença/ausência de botões DOM** como sinal de conclusão — é impreciso.

3. **Aguardar durante geração com computer-use wait** — usar `mcp__computer-use__wait` (independente do Chrome) para esperar. `browser_batch` com wait faz timeout porque o Chrome fica ocupado durante a geração.

4. **Estado inconclusivo após espera** — se após a espera nenhum novo file ID aparecer, navegar para a URL da conversa via `navigate` para recarregar. As imagens já geradas são preservadas no servidor e reaparecem nas network requests ao recarregar.

5. **Prefixo único por imagem** — cada download usa um prefixo diferente nos chunks (`CHARS_`, `PG1_`, `PG2_`, `PG3_`, `PG4_`) para evitar colisão nos logs do console.

6. **Upload das canônicas uma única vez, manualmente pelo usuário** — antes de enviar o primeiro prompt (folha de personagens), exibir ao usuário a lista de imagens canônicas encontradas e pedir que as suba no ChatGPT. Aguardar confirmação via `AskUserQuestion` antes de prosseguir. Nos prompts seguintes (pg1–pg4), enviar somente o texto — o contexto da conversa já mantém a referência visual.

7. **Nova conversa por tema** — iniciar sempre uma nova conversa no Codex para cada tema, evitando que o contexto anterior influencie o novo personagem.

8. **Folha de personagens primeiro** — é sempre a primeira geração da conversa, estabelecendo referência visual para as páginas seguintes dentro da mesma sessão do GPT.

9. **Nunca usar `file://` URLs para exibir imagens ao Chrome MCP** — o Chrome extension bloqueia screenshots de páginas `file://` (retorna "Frame showing error page").

10. **`file_upload` do Chrome MCP é bloqueado em chatgpt.com** — a ferramenta `mcp__Claude_in_Chrome__file_upload` retorna "Not allowed" no domínio chatgpt.com por restrição de segurança do Chrome. O único mecanismo funcional para upload de imagens no ChatGPT é o upload manual pelo usuário via interface gráfica.

11. **Sandbox bash não tem acesso à rede Windows** — o ambiente Linux do bash tem apenas loopback (127.0.0.1). Servidores HTTP iniciados no bash não são acessíveis pelo Chrome rodando no Windows. Não tentar `python -m http.server` como solução de upload.

---

## Fase 0 — Preparação

### 0.1 Localizar imagens canônicas

```python
import os

pasta = PASTA_PROJETO  # recebido como parâmetro
canonicas = [f for f in os.listdir(pasta) if 'canonica' in f.lower() and f.lower().endswith('.png')]
canonicas = [os.path.join(pasta, f) for f in canonicas]

if not canonicas:
    raise RuntimeError(f"Nenhuma imagem canônica encontrada em {pasta}")

print(f"Encontradas {len(canonicas)} imagens canônicas:")
for c in canonicas:
    print(f"  {c}")
```

### 0.2 Abrir o Codex no Chrome

Usar `mcp__Claude_in_Chrome__tabs_context_mcp` para obter a lista de abas. Se já houver uma aba com URL contendo `gpt-quadrinhos-sabendo`, usar essa aba como `TAB_ID`. Caso contrário, criar uma nova aba e navegar para a URL base:

```
URL base: https://chatgpt.com/g/g-69ff2b40169881918c5f75a8d9767f30-gpt-quadrinhos-sabendo
```

Aguardar o ChatGPT carregar completamente (verificar via screenshot que o input de texto está visível).

### 0.2b Solicitar upload manual das canônicas ao usuário

Usar `AskUserQuestion` para exibir ao usuário a lista de imagens canônicas encontradas e instruí-lo a fazer o upload manualmente no ChatGPT antes de continuar:

**Pergunta sugerida:**
> "Encontrei [N] imagem(ns) canônica(s) de referência em `[PASTA_PROJETO]`:
> [lista de nomes dos arquivos]
>
> Por favor:
> 1. Clique no botão **+** (anexar) no input do Codex
> 2. Selecione e faça upload de TODAS as imagens listadas acima
> 3. **NÃO envie ainda** — aguarde eu injetar o prompt automaticamente
> 4. Confirme aqui quando as imagens aparecerem no campo de texto"

**Opção:** `["✅ Imagens anexadas, pode continuar"]`

Aguardar a confirmação do usuário antes de prosseguir para a Fase 1.

### 0.3 Extrair prompts do arquivo .md

Ler `PROMPT_MD` e extrair os 5 blocos de prompt delimitados por três backticks (` ``` `), na ordem:
1. Folha de personagens (bloco sob `## FOLHA DE PERSONAGENS`)
2. Página 1 (bloco sob `### PÁGINA 1`)
3. Página 2 (bloco sob `### PÁGINA 2`)
4. Página 3 (bloco sob `### PÁGINA 3`)
5. Página 4 (bloco sob `### PÁGINA 4`)

### 0.4 Iniciar tracking de network requests

Chamar `read_network_requests` com `urlPattern: "estuary"` uma vez para iniciar o tracking. Extrair file IDs já presentes — esses são os `ids_conhecidos` que devem ser ignorados nas próximas verificações.

---

## Fase 1 — Loop de geração

**Ordem e sufixos:** `chars` → `pg1` → `pg2` → `pg3` → `pg4`

Para cada imagem, executar os passos abaixo.

---

### Passo 1: Verificação de canônicas (somente `chars`)

- **Para `chars` (folha de personagens):** as imagens canônicas já estão anexadas no input do ChatGPT (feitas pelo usuário na Fase 0.2b). Prosseguir diretamente para o Passo 2.
- **Para `pg1` a `pg4`:** sem ação neste passo — enviar somente o texto do prompt. O contexto visual da folha de personagens já está na conversa.

---

### Passo 2: Injetar o prompt (duas chamadas separadas)

**Chamada 1 — injeção do texto:**
```javascript
const el = document.querySelector('#prompt-textarea');
el.focus();
document.execCommand('selectAll');
document.execCommand('insertText', false, PROMPT_TEXTO);
'injected';
```

**Chamada 2 — clique no envio:**
```javascript
const btn = document.querySelector('button[data-testid="send-button"]');
if (btn) { btn.click(); 'clicked'; } else { 'not found'; }
```

---

### Passo 3: Aguardar e detectar conclusão

Usar `mcp__computer-use__wait` com 60 segundos por ciclo. Após cada espera, chamar `read_network_requests` com `urlPattern: "estuary"` e verificar se há file IDs novos (não presentes em `ids_conhecidos`).

```
Ciclo máximo: 5 tentativas (5 minutos total)
Se novo file ID encontrado: prosseguir com o download
Se 5 ciclos sem novo file ID: navegar para CONVERSA_URL, aguardar 5s, verificar novamente
```

O file ID mais recente (último na lista) é sempre o da imagem recém-gerada.

---

### Passo 4: Download via base64

Executar via `mcp__Claude_in_Chrome__javascript_tool`:

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
})()
```

Onde:
- `FILE_ID`, `TS`, `SIG` são extraídos da URL interceptada nas network requests
- `PREFIX` é o prefixo da imagem atual (`CHARS`, `PG1`, `PG2`, `PG3`, `PG4`)

> **Nota sobre TS:** o valor `ts` é capturado diretamente da URL interceptada e varia por sessão. Não hardcodar — sempre usar o valor da URL real.

---

### Passo 5: Ler console e reconstruir PNG

```python
# Chamar read_console_messages com:
#   pattern = "PREFIX_"
#   clear = true
#   limit = 500
# Se o resultado exceder o limite de tokens, é salvo em arquivo .txt automaticamente.
# Nesse caso, ler o arquivo .txt:

import json, base64, re, os

with open(CONSOLE_FILE_PATH, 'r') as f:
    data = json.load(f)

full_text = data[0]['text']

chunks = {}
for m in re.finditer(r'PREFIX_CHUNK_(\d+):([\w+/=]+)', full_text):
    chunks[int(m.group(1))] = m.group(2)

b64 = ''.join(chunks[i] for i in sorted(chunks.keys()))
img_bytes = base64.b64decode(b64)

# Validar cabeçalho PNG
assert img_bytes[:4] == b'\x89PNG', "Arquivo corrompido — não é PNG válido"

# Salvar
sufixo = 'chars'  # ou 'pg1', 'pg2', 'pg3', 'pg4' conforme a imagem atual
dest_dir = os.path.join(PASTA_PROJETO, SUBFOLDER) if SUBFOLDER else PASTA_PROJETO
out_path = os.path.join(dest_dir, f'hq-{SLUG}-{sufixo}.png')
with open(out_path, 'wb') as f:
    f.write(img_bytes)

print(f"Salvo: {os.path.basename(out_path)} ({len(img_bytes):,} bytes)")
```

> Se `read_console_messages` retornar o resultado inline (sem criar arquivo), ler diretamente do retorno em vez do arquivo.

---

### Passo 6: Atualizar ids_conhecidos

Adicionar o file ID recém-baixado ao conjunto de `ids_conhecidos` antes de passar para a próxima imagem.

---

## Fase 2 — Verificação final das páginas

```python
sufixos = ['chars', 'pg1', 'pg2', 'pg3', 'pg4']
erros = []

dest_dir = os.path.join(PASTA_PROJETO, SUBFOLDER) if SUBFOLDER else PASTA_PROJETO
for suf in sufixos:
    path = os.path.join(dest_dir, f'hq-{SLUG}-{suf}.png')
    if not os.path.exists(path):
        erros.append(f"FALTANDO: {path}")
        continue
    with open(path, 'rb') as f:
        header = f.read(4)
    if header != b'\x89PNG':
        erros.append(f"PNG INVALIDO: {path}")
        continue
    size = os.path.getsize(path)
    print(f"hq-{SLUG}-{suf}.png — {size:,} bytes")

if erros:
    for e in erros:
        print(f"ERRO: {e}")
else:
    print(f"\nTodas as 5 imagens geradas com sucesso para o tema '{SLUG}'.")
```

---

## Fase 3 — Montagem vertical (somente portal-educacional / André)

**Esta fase só é executada quando `PASTA_PROJETO` aponta para o projeto do André (`estudos`). Para o projeto da Lis (`estudos-2ano`), pular direto para o encerramento.**

Une as 4 páginas verticalmente em um único PNG (`hq-[slug].png`) usando Pillow. Após a montagem bem-sucedida, remove os arquivos de página individuais (`pg1` a `pg4`) e o arquivo de folha de personagens (`chars`), deixando apenas o PNG final na raiz do projeto.

```python
from PIL import Image
import os

dest_dir = os.path.join(PASTA_PROJETO, SUBFOLDER) if SUBFOLDER else PASTA_PROJETO
paginas = [
    os.path.join(dest_dir, f'hq-{SLUG}-pg{n}.png')
    for n in range(1, 5)
]

imgs = [Image.open(p) for p in paginas]
largura_ref = imgs[0].width

imgs_norm = []
for img in imgs:
    if img.width != largura_ref:
        fator = largura_ref / img.width
        nova_altura = int(img.height * fator)
        img = img.resize((largura_ref, nova_altura), Image.LANCZOS)
    imgs_norm.append(img)

altura_total = sum(img.height for img in imgs_norm)
canvas = Image.new('RGB', (largura_ref, altura_total), (255, 255, 255))
y = 0
for img in imgs_norm:
    canvas.paste(img, (0, y))
    y += img.height

out_path = os.path.join(dest_dir, f'hq-{SLUG}.png')
canvas.save(out_path, 'PNG', optimize=True)
print(f"Montagem concluída: hq-{SLUG}.png ({canvas.width}x{canvas.height}px, {os.path.getsize(out_path):,} bytes)")

para_remover = [f'hq-{SLUG}-chars.png'] + [f'hq-{SLUG}-pg{n}.png' for n in range(1, 5)]
for nome in para_remover:
    path = os.path.join(dest_dir, nome)
    if os.path.exists(path):
        os.remove(path)
        print(f"Removido: {nome}")

print(f"\nHQ do tema '{SLUG}' pronta: hq-{SLUG}.png")
```

---

## Tratamento de erros

| Situação | Ação |
|---|---|
| Nenhuma imagem canônica encontrada | Abortar e informar o caminho buscado |
| Usuário não confirma upload das canônicas | Aguardar — não prosseguir sem confirmação |
| Geração não conclui em 5 minutos | Navegar para CONVERSA_URL; aguardar mais 2 ciclos de 60s |
| "Transmissão interrompida" no ChatGPT | Navegar para CONVERSA_URL — imagem já gerada é preservada no servidor |
| File ID não aparece após reload | Verificar se há mensagem de erro no DOM; se sim, reenviar prompt |
| Reconstrução PNG inválida | Repetir Passos 4–5 para o mesmo FILE_ID |
| Arquivo de console não encontrado | Usar resultado inline do read_console_messages |
| Pillow não instalado (Fase 3) | Executar `pip install pillow` e repetir a Fase 3 |
| Larguras das páginas divergem | Redimensionar proporcionalmente conforme código da Fase 3 |

---

## Estrutura de invocação pelas skills do portal

**portal-educacional-2ano** passa:
```
PASTA_PROJETO = C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos-2ano
SLUG          = [slug do tema gerado]
SUBFOLDER     = ""  (salva na raiz — estrutura flat do estudos-2ano)
PROMPT_MD     = [PASTA_PROJETO]\hq-[slug]-prompt.md
MONTAR        = False
```

**portal-educacional (André)** passa:
```
PASTA_PROJETO = C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos
SLUG          = [slug do tema gerado]
SUBFOLDER     = [disc-folder]/[slug]  (ex: historia/marcos-memoria)
PROMPT_MD     = [PASTA_PROJETO]\[disc-folder]\[slug]\hq-[slug]-prompt.md
MONTAR        = True
```

> O parâmetro `MONTAR` controla se a Fase 3 será executada. Quando `True`, as páginas individuais são montadas e removidas ao final.

---

## Codex

URL base: `https://chatgpt.com/g/g-69ff2b40169881918c5f75a8d9767f30-gpt-quadrinhos-sabendo`

Para iniciar nova conversa: navegar para a URL base (sem `/c/...`).
