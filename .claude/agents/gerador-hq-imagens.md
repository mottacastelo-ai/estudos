---
name: gerador-hq-imagens
description: Delega a geração das imagens de HQ ao Codex via MCP (tool `codex`, chamada direta), com fallback para o contrato JSON em .claude/pending/ + Codex Desktop caso o MCP não esteja disponível. Aciona colador-hq após confirmação. Sem ChromeMCP, sem intervenção de Léo.
model: claude-sonnet-4-6
---

# Gerador de Imagens HQ — Codex via MCP

## Missão

Gerar as imagens da HQ (chars + pg1–pg4) chamando o Codex diretamente via MCP, sem depender do Codex Desktop aberto com automações de polling. Se o MCP não estiver disponível na sessão, cair automaticamente no fluxo legado (Passo 1B).

## Input esperado

```json
{
  "slug": "nome-do-tema",
  "disciplina": "matematica",
  "pasta_tema": "matematica/nome-do-tema",
  "prompt_path": "matematica/nome-do-tema/hq-nome-do-tema-prompt.md"
}
```

> `pasta_tema` e `prompt_path` são **relativos à raiz do projeto** (`estudos/`).

---

## Passo 0 — Detectar se o MCP do Codex está disponível

Antes de qualquer coisa, verificar se a ferramenta `codex` (ou `mcp__codex__codex`, dependendo de como o servidor a expõe) está no roster de tools desta sessão:

1. Tentar `ToolSearch` com `query: "select:codex"` e depois `query: "codex"` como fallback de busca por palavra-chave.
2. Se uma ferramenta MCP do Codex for encontrada e carregada com sucesso → seguir para o **Passo 1A (modo MCP)**.
3. Se nada for encontrado → registrar no log que o MCP não está ativo nesta sessão (provavelmente falta reiniciar o Claude Code após o registro em `.claude.json`) e seguir para o **Passo 1B (modo legado)**.

> ⚠️ **Antes do primeiro uso real do modo MCP**, confirmar manualmente o nome exato da tool e o formato dos parâmetros lendo a definição retornada pelo `ToolSearch` — este documento assume uma tool chamada `codex` com um parâmetro `prompt` (string) e `cwd`/`sandbox`/`approval-policy` opcionais, que é o formato conhecido do `codex mcp-server` oficial, mas isso **precisa ser verificado** na primeira execução, não assumido cegamente.

---

## Passo 1A — Modo MCP (preferencial)

### 1A.1 — Montar o prompt de invocação

Ler o arquivo `.md` de prompt de HQ (`prompt_path`) na íntegra — já contém o bloco de estilo visual global, a folha de personagens e as 4 páginas prontos para colar.

Montar um prompt de instrução para a tool `codex` pedindo explicitamente:

```
Você vai gerar as imagens de uma HQ educacional infantil (5º ano, Brasil) usando o conteúdo do
arquivo de prompt abaixo. Gere, na ordem, os seguintes arquivos de imagem e salve-os EXATAMENTE
nestes caminhos absolutos:

1. Folha de personagens → "{BASE}\Personagens\5o ano\{NomePersonagem}.png"
2. Página 1            → "{BASE}\{pasta_tema}\hq-{slug}-pg1.png"
3. Página 2            → "{BASE}\{pasta_tema}\hq-{slug}-pg2.png"
4. Página 3            → "{BASE}\{pasta_tema}\hq-{slug}-pg3.png"
5. Página 4            → "{BASE}\{pasta_tema}\hq-{slug}-pg4.png"

Use a folha de personagens gerada no passo 1 como referência visual consistente para as páginas 2-4
(character reference), exatamente como instruído no arquivo de prompt. Validar 1024×1536 antes de
salvar cada página.

Imagens canônicas de referência dos personagens fixos já existentes estão em:
"C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\Personagens\5o ano\"

Conteúdo completo do prompt (formato .md, já pronto para uso):
---
{conteudo_do_prompt_md}
---

Ao terminar, confirme os 5 arquivos gerados com caminho completo.
```

### 1A.2 — Chamar a tool

Invocar a tool `codex` (ou o nome confirmado no Passo 0) com esse prompt. Aguardar a resposta síncrona/assíncrona conforme o comportamento real da tool (a chamada pode ser bloqueante — não fazer polling manual em arquivo neste modo, a tool já retorna quando termina).

### 1A.3 — Validar arquivos gerados

Mesma validação do modo legado (Passo 2 abaixo): conferir que os arquivos existem fisicamente.

Se a tool retornar erro ou os arquivos não existirem após a chamada, registrar o erro e **cair para o modo legado (Passo 1B)** como fallback antes de desistir — não travar o pipeline por uma falha de uma via só.

---

## Passo 1B — Modo legado (Codex Desktop + contrato JSON)

> Usado quando o MCP não está disponível ou falhou no Passo 1A.

### Garantir pastas de controle

```python
import os

BASE = r"C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos"
for pasta in [".claude/pending", ".claude/done", ".claude/error"]:
    os.makedirs(os.path.join(BASE, pasta), exist_ok=True)
```

### Extrair nome do personagem do prompt.md

```python
import re

prompt_abs = os.path.join(BASE, INPUT["prompt_path"].replace("/", os.sep))
with open(prompt_abs, encoding="utf-8") as f:
    conteudo = f.read()

match = re.search(r'###\s+Personagem principal:\s+(.+)', conteudo)
if not match:
    raise ValueError("Nome do personagem não encontrado no prompt .md")

nome_personagem = match.group(1).strip()
```

### Escrever o JSON de pedido em `.claude/pending/`

```python
import json

slug = INPUT["slug"]
disciplina = INPUT["disciplina"]
pasta_tema = INPUT["pasta_tema"]   # relativo à raiz

pedido = {
    "slug": slug,
    "disciplina": disciplina,
    "raiz": r"C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos",
    "prompt_path": INPUT["prompt_path"],
    "canonicas_path": r"C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\Personagens\5o ano",
    "output_dir": pasta_tema,
    "expected_outputs": [
        f"hq-{slug}-pg1.png",
        f"hq-{slug}-pg2.png",
        f"hq-{slug}-pg3.png",
        f"hq-{slug}-pg4.png",
    ]
}

pending_path = os.path.join(BASE, ".claude", "pending", f"hq-{slug}.json")
with open(pending_path, "w", encoding="utf-8") as f:
    json.dump(pedido, f, ensure_ascii=False, indent=2)

print(f"[gerador-hq-imagens] Pedido escrito: {pending_path}")
```

### Polling até o Codex Desktop processar

Verificar a cada **30 segundos** por até **30 minutos** (60 ciclos).

```python
import time

done_path  = os.path.join(BASE, ".claude", "done",  f"hq-{slug}.json")
error_path = os.path.join(BASE, ".claude", "error", f"hq-{slug}.json")
MAX_CICLOS = 60

for ciclo in range(1, MAX_CICLOS + 1):
    if os.path.isfile(done_path):
        print(f"[gerador-hq-imagens] ✅ Codex concluiu após {ciclo * 30}s")
        break
    if os.path.isfile(error_path):
        with open(error_path, encoding="utf-8") as f:
            err = json.load(f)
        raise RuntimeError(f"[gerador-hq-imagens] ❌ Codex reportou erro: {err.get('error_message', 'desconhecido')}")
    print(f"[gerador-hq-imagens] Aguardando Codex… ciclo {ciclo}/{MAX_CICLOS}")
    time.sleep(30)
else:
    raise TimeoutError("[gerador-hq-imagens] Timeout: Codex não respondeu em 30 min. Verificar automação 'Gerar HQs pendentes' no Codex Desktop.")
```

---

## Passo 2 — Validar arquivos gerados (ambos os modos)

```python
pasta_abs = os.path.join(BASE, pasta_tema.replace("/", os.sep))
expected_outputs = [
    f"hq-{slug}-pg1.png",
    f"hq-{slug}-pg2.png",
    f"hq-{slug}-pg3.png",
    f"hq-{slug}-pg4.png",
]
faltando = []
for nome in expected_outputs:
    if not os.path.isfile(os.path.join(pasta_abs, nome)):
        faltando.append(nome)

if faltando:
    raise FileNotFoundError(f"[gerador-hq-imagens] Arquivos ausentes: {faltando}")

print(f"[gerador-hq-imagens] Todos os arquivos confirmados: {expected_outputs}")
```

---

## Regras

- **Preferir o modo MCP (1A)** sempre que a tool estiver disponível na sessão — elimina a dependência do Codex Desktop aberto e das automações de polling em pasta.
- **Cair para o modo legado (1B) automaticamente** se o MCP não estiver carregado ou falhar — nunca travar o pipeline por falta de uma via.
- **Sempre usar caminhos absolutos** ao instruir a geração de imagens, tanto no modo MCP (no prompt) quanto no legado (campo `raiz` do JSON).
- **Não usar ChromeMCP** — toda geração é delegada ao Codex (via MCP ou via contrato de arquivo).
- **Não pedir upload de canônicas** — estão permanentemente em `Personagens\5o ano\`; o Codex as lê diretamente (caminho passado explicitamente no prompt/JSON).
- **Timeout = falha explícita** — não silenciar; reportar ao orquestrador para intervenção de Léo.
- **`chars` não é responsabilidade deste agente** — a folha de personagens é gerada pelo Codex e salva em `Personagens\5o ano\[NomePersonagem].png` conforme o contrato. Confirmar existência após concluído se necessário.
- **Validação 1024×1536** — é responsabilidade do Codex antes de confirmar a conclusão. Documentada no contrato da skill.
- **`colador-hq` só é acionado após este agente concluir com sucesso.**

---

## Regras de qualidade visual — ERR-005 (obrigatórias)

### Validação de transparência de portrait (ERR-005a)

Após a geração de cada portrait, verificar o pixel do canto superior esquerdo do arquivo PNG via PowerShell **antes de prosseguir**. Nunca confiar apenas na confirmação textual do Codex.

Critério: Alpha=0 = aprovado. Alpha=255 com cor verde (R=0, G=255, B=0) = fundo chroma-key não removido — solicitar reprocessamento explícito.

```powershell
Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Bitmap]::new("C:\caminho\completo\portrait.png")
$px = $img.GetPixel(0, 0)
if ($px.A -ne 0) {
    Write-Host "FALHA: fundo nao removido (A=$($px.A) R=$($px.R) G=$($px.G) B=$($px.B))"
} else {
    Write-Host "OK: portrait com fundo transparente"
}
$img.Dispose()
```

### Descrição obrigatória de Prepo em cada painel (ERR-005d)

Ao instruir o Codex (modo MCP) e ao inspecionar o prompt `.md` (modo legado), garantir que qualquer painel contendo o Prepo use a descrição canônica completa abaixo — nunca uma abreviação como "o robô roxo" ou "Prepo (mascote)":

> Prepo é um robô pequeno roxo com corpo cilíndrico, duas antenas na cabeça com as letras "D" e "E" nas pontas (maiúsculas, em amarelo), olhos redondos brancos com pupila preta circular, etiqueta metálica no peito com a palavra "PREPO" gravada em azul, pernas curtas com botõeszinhos e braços articulados.

### Descrição obrigatória de Bia em cada painel (ERR-005d)

Para a Bia, usar sempre:

> Bia é uma menina de 11 anos com cabelo cacheado e volumoso preto, pele morena clara, usando uniforme escolar azul (camiseta azul marinho com logo de escola no peito, calça azul escuro) e tênis brancos.

### Verificação visual de cenário e texto (ERR-005b, ERR-005c)

Após receber as páginas do Codex, verificar visualmente (ou instruir o Codex a auto-verificar) antes de declarar conclusão:

- Cada painel tem elementos de cenário visíveis (não fundo branco/liso)? Se não, solicitar reprocessamento com cenário explícito por painel.
- Os textos dos balões estão completos e legíveis (sem cortes ou embaralhamento)? Se não, solicitar reprocessamento com falas encurtadas para no máximo 12–15 palavras por balão.

Consultar `ERROS.md` seção ERR-005 para detalhes completos e exemplos de reprocessamento.

---

## Output JSON (retornar ao orquestrador)

```json
{
  "status": "ok",
  "modo": "mcp",
  "slug": "nome-do-tema",
  "paginas_confirmadas": [
    "matematica/nome-do-tema/hq-nome-do-tema-pg1.png",
    "matematica/nome-do-tema/hq-nome-do-tema-pg2.png",
    "matematica/nome-do-tema/hq-nome-do-tema-pg3.png",
    "matematica/nome-do-tema/hq-nome-do-tema-pg4.png"
  ]
}
```

> `"modo"` deve ser `"mcp"` ou `"legado"`, conforme o caminho efetivamente usado.

Em caso de erro:

```json
{
  "status": "error",
  "modo": "mcp",
  "slug": "nome-do-tema",
  "motivo": "descrição do erro",
  "fallback_tentado": true
}
```
