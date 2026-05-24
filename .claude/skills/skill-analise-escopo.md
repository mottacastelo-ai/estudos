---
name: skill-analise-escopo
description: "Guia procedural para análise de fotos de conteúdo escolar do 5º ano e proposição de estrutura de temas para o portal educacional. Usado pelo agente analisador-pedagogico."
---

# Skill: Análise de Escopo Pedagógico

## Quando usar

Toda vez que o agente `analisador-pedagogico` precisa processar imagens de material didático.

---

## Passo 1 — Leitura exaustiva das imagens

Para cada imagem recebida, extrair:

- **Número de página** — ler o número impresso na página (geralmente no canto superior ou inferior). Registrar a menor e a maior página vista para compor o intervalo (ex.: `"45–52"`).
- **Título do capítulo/seção** exibido na página
- **Todos os termos técnicos em destaque** (negrito, caixas coloridas, legendas, glossário)
- **Exemplos e exercícios visíveis** (anotar o tipo: identificar, classificar, produzir, etc.)
- **Habilidades trabalhadas** (o que o aluno deve ser capaz de fazer com o conteúdo)
- **Volume de conteúdo** (quantas páginas abrange o tema)

> Se nenhuma foto mostrar número de página legível, registrar `paginas_livro: null`.

**Regra absoluta:** nenhum conceito que não esteja visível nas imagens pode ser incluído na proposta.

---

## Passo 2 — Decisão de divisão em temas

| Critério | Mesmo tema | Temas separados |
|---|---|---|
| Foco conceitual | Subtemas subordinados a um conceito central | Subtemas com autonomia conceitual própria |
| Volume | Até ~8 páginas densas | Mais de ~8 páginas ou capítulos distintos |
| Narrativa HQ | Uma HQ cobre o arco completo | Uma HQ por bloco seria necessária |
| Habilidades | Mesmas habilidades ao longo do material | Habilidades distintas por bloco |

**Sinal de alerta obrigatório:** se o material cobrir dois ou mais capítulos com subtemas autônomos → propor divisão e justificar.

---

## Passo 3 — Sugestão de personagem

O personagem deve ser uma **metáfora visual do conceito central** — não um personagem genérico.

| Disciplina | Exemplos de metáforas |
|---|---|
| Matemática | Formas geométricas, números, operadores animados (ex.: Poli = cubo, Verbão = letra) |
| Português | Pontuação, letras, elementos textuais animados |
| Ciências | Organismos, fenômenos naturais, processos animados |
| História | Objetos de época, símbolos históricos, figuras estilizadas |
| Geografia | Relevos, biomas, elementos geográficos animados |

Descrever:
- Forma visual (o que é o personagem?)
- Paleta de cores (usar as CSS vars da disciplina)
- 3 expressões distintas (feliz, explicando, surpreso)
- Elementos visuais que remetem ao conteúdo

---

## Passo 4 — Sugestão de tipos de atividade

### 4.1 Verificar variedade

Listar os tipos já usados na disciplina:
```bash
ls C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos\[disciplina]\*\*.html
```

Identificar os prefixos (`quiz-*`, `mapa-mental-*`, etc.) para evitar repetição.

### 4.2 Matching conteúdo → tipo

| Tipo de conteúdo | Tipo de atividade indicado |
|---|---|
| Definições, conceitos, terminologia | `quiz`, `flashcards` |
| Classificação (colocar em categorias) | `classificador` |
| Sequências, processos, etapas | `ordenacao` |
| Correção de erros/regras | `caca-erro` |
| Reescrita, transformação | `transformador` |
| Completar textos/frases | `complete-lacuna` |
| Produção textual guiada | `criador` |
| Desafio gamificado geral | `missao` |
| Identificação em texto | `detetive-nomes` |
| Relações entre conceitos (obrigatório) | `mapa-mental` |

### 4.3 Regra de variedade

- `mapa-mental` é obrigatório em todo tema
- Nunca repetir o mesmo tipo entre temas da mesma disciplina (exceto mapa-mental)
- Propor 2–3 tipos por tema (qualidade sobre quantidade)

---

## Passo 5 — Formato da proposta para Léo

```
📚 Conteúdo identificado
[Disciplina] — [Capítulo(s)/Unidade(s) identificados]

🗂️ Subtemas mapeados
- [Subtema 1]: [conceitos-chave em bullets]
- [Subtema 2]: [conceitos-chave em bullets]

🎯 Proposta de estrutura

> Opção A — [N] tema(s): [Nome 1] + [Nome 2]
> Justificativa: [por que essa divisão serve melhor pedagogicamente]

> Opção B — Tema único: [Nome]
> Justificativa: [por que agrupar pode funcionar, com ressalvas de cobertura]

⚠️ Alertas de cobertura
[Conceitos ou habilidades que ficariam de fora se o conteúdo fosse comprimido]

✅ Aguardando sua decisão para prosseguir.
```

---

## Boas práticas

- Extrair os termos na forma que aparecem no livro (ex.: "poliedro regular", não "sólido regular")
- Para termos com acento ou grafia específica do livro — copiar exatamente
- Se o livro mostrar uma tabela ou quadro de referência, listar todos os itens como termos técnicos
- Preferir slugs curtos e descritivos: `poliedros-prismas-piramides`, não `solidos-geometricos-3d`
