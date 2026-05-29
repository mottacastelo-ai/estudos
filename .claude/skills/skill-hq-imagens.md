---
name: skill-hq-imagens
description: "Documenta o contrato de geração de HQ via Codex Desktop para o portal educacional 5º Ano. O Codex monitora .claude/pending/, gera as imagens e move o JSON para .claude/done/ ou .claude/error/."
---

# Skill: Geração de Imagens HQ via Codex — Portal 5º Ano

## Quando usar

Quando o `gerador-hq-imagens` precisa produzir as imagens de uma HQ (pg1–pg4 + folha de personagens). Todo o processamento é delegado ao Codex Desktop via contrato de arquivo — sem ChromeMCP, sem intervenção manual de Léo.

---

## Arquitetura do contrato

```
estudos/
└── .claude/
    ├── pending/   ← gerador-hq-imagens escreve o pedido aqui
    ├── done/      ← Codex move o JSON aqui após sucesso
    └── error/     ← Codex move o JSON aqui com error_message após falha
```

A automação **"Gerar HQs pendentes"** do Codex Desktop (status PAUSED, intervalo 2 min) monitora `.claude/pending/` e processa cada JSON encontrado.

---

## Estrutura do JSON de pedido

Arquivo: `.claude/pending/hq-[slug].json`

```json
{
  "slug": "string — identificador do tema (ex: poliedros-prismas-piramides)",
  "disciplina": "string — nome da pasta da disciplina (ex: matematica)",
  "prompt_path": "string — caminho RELATIVO à raiz do projeto para o hq-[slug]-prompt.md",
  "canonicas_path": "C:\\Users\\wizar\\OneDrive\\Documentos\\Projeto Estudos\\Personagens\\5o ano\\",
  "output_dir": "string — caminho RELATIVO à raiz do projeto para a pasta do tema",
  "expected_outputs": [
    "hq-[slug]-pg1.png",
    "hq-[slug]-pg2.png",
    "hq-[slug]-pg3.png",
    "hq-[slug]-pg4.png"
  ]
}
```

### Exemplo preenchido

```json
{
  "slug": "poliedros-prismas-piramides",
  "disciplina": "matematica",
  "prompt_path": "matematica/poliedros-prismas-piramides/hq-poliedros-prismas-piramides-prompt.md",
  "canonicas_path": "C:\\Users\\wizar\\OneDrive\\Documentos\\Projeto Estudos\\Personagens\\5o ano\\",
  "output_dir": "matematica/poliedros-prismas-piramides",
  "expected_outputs": [
    "hq-poliedros-prismas-piramides-pg1.png",
    "hq-poliedros-prismas-piramides-pg2.png",
    "hq-poliedros-prismas-piramides-pg3.png",
    "hq-poliedros-prismas-piramides-pg4.png"
  ]
}
```

---

## Destinos de arquivo

| Arquivo | Destino absoluto |
|---|---|
| Folha de personagens (`chars`) | `C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\Personagens\5o ano\[NomePersonagem].png` |
| pg1–pg4 | `C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos\[output_dir]\hq-[slug]-pg1..4.png` |

> O nome do personagem é extraído pelo Codex da seção `### Personagem principal: [NOME]` do `prompt_path`. O `chars` **não entra** em `expected_outputs` — o Codex o salva automaticamente em `canonicas_path`.

---

## Responsabilidades do Codex (não do agente)

1. Ler o `prompt_path` e extrair prompts por seção (`## FOLHA DE PERSONAGENS`, `## PÁGINA 1`–`## PÁGINA 4`)
2. Carregar as canônicas de `canonicas_path` antes de cada geração
3. **Validar dimensão 1024×1536px** antes de salvar — rejeitar qualquer imagem com dimensão diferente (ex.: `864×1821` é thumbnail de comparação do GPT, não a imagem final)
4. Salvar chars em `canonicas_path\[NomePersonagem].png`
5. Salvar pg1–pg4 em `output_dir\hq-[slug]-pg{n}.png`
6. Mover o JSON para `.claude/done/hq-[slug].json` em caso de sucesso
7. Mover o JSON para `.claude/error/hq-[slug].json` com campo `error_message` em caso de falha

---

## Comportamento de polling do `gerador-hq-imagens`

| Parâmetro | Valor |
|---|---|
| Intervalo entre verificações | 30 segundos |
| Timeout total | 30 minutos (60 ciclos) |
| Sinal de sucesso | Arquivo em `.claude/done/hq-[slug].json` |
| Sinal de falha | Arquivo em `.claude/error/hq-[slug].json` |

Após timeout sem resposta: reportar ao orquestrador com instrução para Léo verificar se a automação "Gerar HQs pendentes" está ativa no Codex Desktop.

---

## Resposta do Codex em `done/`

O JSON movido para `done/` pode conter campos adicionais de confirmação:

```json
{
  "slug": "poliedros-prismas-piramides",
  "status": "done",
  "outputs_salvos": [
    "matematica/poliedros-prismas-piramides/hq-poliedros-prismas-piramides-pg1.png",
    "matematica/poliedros-prismas-piramides/hq-poliedros-prismas-piramides-pg2.png",
    "matematica/poliedros-prismas-piramides/hq-poliedros-prismas-piramides-pg3.png",
    "matematica/poliedros-prismas-piramides/hq-poliedros-prismas-piramides-pg4.png"
  ]
}
```

## Resposta do Codex em `error/`

```json
{
  "slug": "poliedros-prismas-piramides",
  "status": "error",
  "error_message": "Descrição do problema"
}
```

---

## Regras invioláveis

1. **Dimensão 1024×1536 é obrigatória** — validada pelo Codex; o agente confirma existência dos arquivos após `done/` mas não revalida dimensão.
2. **Canônicas não precisam ser reenviadas** — ficam permanentemente em `Personagens\5o ano\`. Léo não tem ação nessa etapa.
3. **`colador-hq` só roda após confirmação em `done/`** — nunca em paralelo ou antes.
4. **Em caso de erro**, o orquestrador reporta a Léo com o `error_message` completo e aguarda instrução antes de retentar.
5. **Caminhos em `prompt_path` e `output_dir` são sempre relativos à raiz do projeto** (`estudos/`) — o Codex resolve para absoluto internamente.
