---
name: skill-gerar-hq-prompt
description: "Guia procedural para criar o arquivo hq-[slug]-prompt.md com os prompts de cada página da HQ para o Codex. Usado pelo agente gerador-hq-prompt."
---

# Skill: Gerador de Prompt HQ

## Quando usar

Quando o agente `gerador-hq-prompt` precisa criar o arquivo `.md` com os prompts de geração de imagens.

---

## Estrutura narrativa obrigatória das 4 páginas

Cada HQ tem um arco pedagógico que evolui em 4 atos:

| Página | Função | Conteúdo |
|---|---|---|
| Pg. 1 | Apresentação do problema | Introduzir o conflito ou curiosidade. O personagem aparece. Apresentar o 1º conceito-chave. |
| Pg. 2 | Desenvolvimento | Aprofundar o tema. Apresentar distinções, exemplos, regras. |
| Pg. 3 | Aplicação prática | Mostrar como usar o conceito. Exemplos concretos do cotidiano ou da escola. |
| Pg. 4 | Síntese + encerramento | Revisão dos termos técnicos. Bia ou personagem recapitula. Frase de encerramento. |

---

## Estrutura da Folha de Personagens

A folha de personagens é a **primeira geração** e estabelece a referência visual para todas as páginas.

Deve conter:
1. **Personagem principal** — 3 emoções distintas (feliz/animado, explicando, surpreso)
2. **Bia** — 1 pose de apoio (cabelo cacheado preto, uniforme escolar azul)
3. **Paleta de cores detalhada** — hex de cada elemento visual
4. **Elementos visuais que remetem ao conteúdo** do tema

---

## Regra absoluta — Sem reticências, sem subentendidos

**O Codex renderiza apenas o que está escrito. Ele não infere, não completa sequências, não interpreta reticências.**

❌ **Errado:**
> "The numbers 4, 6, 8, 10... have a red X drawn through them"
> "multiples of 3 (9, 15, 21...) get red X marks"
> "os planetas do sistema solar (...) aparecem ao fundo"

✅ **Certo:**
> "The numbers 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50 each have a red X drawn through them"
> "The multiples of 3 visible on the board — 9, 15, 21, 27, 33, 39, 45 — each have a red X"

**Regra prática:** antes de salvar o arquivo, revisar todos os painéis e substituir qualquer `...` por enumeração completa. Se uma sequência for longa, listar todos os itens. Se um conjunto visual for complexo, descrever cada elemento individualmente.

Isso vale para:
- Sequências numéricas (`4, 6, 8...` → listar todos)
- Listas de objetos (`livros, canetas...` → nomear cada um)
- Padrões visuais (`os demais estão riscados...` → quais exatamente?)
- Posições e disposições (`etc`, `entre outros`, `e assim por diante` → proibidos)

---

## Regras para os prompts de cada painel

### Regra 1 — Termos técnicos nas falas
Todos os termos técnicos do livro devem aparecer **em destaque visual** nas falas dos personagens:
```
Poli: *"Todo sólido com faces planas é um POLIEDRO!"*
```
Usar caixa alta ou itálico para destacar termos-chave dentro das falas.

### Regra 2 — 4–6 painéis por página
Cada página deve ter entre 4 e 6 painéis. Descrever:
- O que cada personagem faz/fala
- A composição visual da cena (ângulo, fundo, elementos)
- Diagramas ou elementos gráficos que devem aparecer (fórmulas, tabelas, mapas)

### Regra 3 — Progressão coerente
As falas devem ser didáticas mas naturais — diálogo, não palestra. Intercalar:
- Pergunta de Bia → resposta do personagem
- Exemplo prático → aplicação
- Humor visual → aprendizado

### Regra 4 — Diagrama ou elemento visual em cada página
Pelo menos 1 painel por página deve incluir um elemento visual explícito:
- Caixa com fórmula/regra
- Diagrama com setas e rótulos
- Comparação lado a lado
- Tabela simples

---

## Estilo visual do Codex

- Traços expressivos, cores vibrantes, quadrinhos ocidentais
- Personagens com expressões exageradas (emoções claras)
- Fundo detalhado mas não poluído
- Balões de fala bem legíveis
- Paleta alinhada à disciplina (usar as cores do CSS vars)

---

## Boas práticas

- Descrever a cena de abertura de cada página para dar contexto visual
- Especificar ângulos importantes: "close no rosto de Poli surpreso", "plano geral do museu"
- Para personagens novos: mencionar a paleta toda vez nas instruções de produção (o GPT não tem memória entre sessões)
- Verificar se todos os `conceitos_chave` do JSON do analisador estão cobertos nas 4 páginas antes de finalizar
- A última fala da Pg. 4 deve recapitular os termos técnicos de forma resumida

---

## Exemplo de painel bem descrito

```
**Painel 3:**
Close em Poli apontando para si mesmo com expressão de professor:
*"Todo poliedro tem três elementos: FACES 🔲 (os lados planos), 
ARESTAS ➖ (onde duas faces se encontram) e VÉRTICES 📍 (onde 
três ou mais arestas se juntam)!"*

Diagrama ao lado mostrando um cubo com setas coloridas 
indicando face (azul), aresta (verde) e vértice (laranja).
```

---

## Nomes dos arquivos de saída (para a seção INSTRUÇÕES DE PRODUÇÃO)

```
hq-[slug]-chars.png   ← folha de personagens
hq-[slug]-pg1.png
hq-[slug]-pg2.png
hq-[slug]-pg3.png
hq-[slug]-pg4.png
```

Obs.: a skill `skill-hq-imagens.md` usa esses nomes para capturar e salvar as imagens automaticamente.
