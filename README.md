# 📚 Estudos – 5º Ano

Portal de atividades educacionais lúdicas para fixação de conteúdo escolar.
Baseado no método ativo de aprendizagem (Roediger & Karpicke, 2006).

---

## 🌐 Site

Hospedado no Netlify. Para atualizar: faça commit e push — o Netlify publica automaticamente.

---

## 📁 Estrutura de arquivos

### Portal
| Arquivo | Descrição |
|---|---|
| `index.html` | Página principal com menu lateral e todas as disciplinas |

### 📝 Português — Preposições
| Arquivo | Descrição |
|---|---|
| `hq-preposicoes.png` | História em quadrinhos — As Aventuras do Prepo |
| `quiz-preposicoes.html` | Quiz interativo — 10 questões |
| `complete-lacuna-preposicoes.html` | Complete a lacuna com banco de palavras |
| `caca-ao-erro-preposicoes.html` | Caça ao erro |
| `frases-malucas-preposicoes.html` | Frases malucas com cronômetro |
| `missao-relampago-preposicoes.html` | Missão relâmpago — locuções adjetivas |
| `criador-de-quiz-preposicoes.html` | Criador de quiz para aplicar na família |
| `domino-preposicoes.html` | Dominó para imprimir — 16 peças |

### 📝 Português — Texto Teatral
| Arquivo | Descrição |
|---|---|
| `hq-texto-teatral.png` | História em quadrinhos — O Vento e o Sol |
| `quiz-texto-teatral.html` | Quiz interativo — 10 questões |
| `complete-lacuna-texto-teatral.html` | Complete a lacuna |
| `caca-erro-texto-teatral.html` | Caça ao erro |
| `ordenacao-cenas-texto-teatral.html` | Ordenação de cenas |
| `criador-dialogo-texto-teatral.html` | Criador de diálogo teatral |

### 📝 Português — Tempos Verbais
| Arquivo | Descrição |
|---|---|
| `hq-tempos-verbais.png` | História em quadrinhos — Passado, Presente e Futuro |
| `quiz-tempos-verbais.html` | Quiz interativo — 10 questões |
| `complete-lacuna-tempos-verbais.html` | Complete a lacuna |
| `caca-erro-tempos-verbais.html` | Caça ao erro |
| `classificador-tempos-verbais.html` | Linha do tempo — classificar verbos |
| `transformador-tempos-verbais.html` | Transformador de verbos entre tempos |

### 🔢 Matemática — Tabuada
| Arquivo | Descrição |
|---|---|
| `flashcards-tabuada.html` | Flashcards com sistema Leitner (repetição espaçada) |
| `treino-tabuada.html` | Treino cronometrado |
| `batalha-tabuada.html` | Batalha da tabuada — 4 modos de jogo |
| `caca-erro-tabuada.html` | Caça ao erro na tabuada |

---

## ➕ Como adicionar um novo tema

1. Gere as atividades (arquivos `.html`) e a HQ (arquivo `.png`)
2. Nomeie os arquivos seguindo o padrão: `tipo-tema-disciplina.html`
   - Exemplo: `quiz-substantivos-portugues.html`
3. Coloque os arquivos na raiz desta pasta
4. Abra o `index.html` e adicione:
   - O link do novo tema no **menu lateral** (`sidebar`)
   - O **tab** na tela da disciplina
   - O **bloco de conteúdo** (`theme-content`) com os cards das atividades
5. Atualize os **contadores** no hero da home (disciplinas, temas, atividades)
6. Faça commit e push — o Netlify publica automaticamente

---

## ➕ Como adicionar uma nova disciplina

1. Crie os arquivos das atividades
2. No `index.html`:
   - Adicione o botão no **menu lateral**
   - Crie a **tela da disciplina** (`screen-NOMEDISCIPLINA`)
   - Adicione o **card** na home
   - Registre a disciplina na função `showDisc()` com seu primeiro tema
3. Escolha uma cor principal para a disciplina e adicione nas variáveis CSS
4. Faça commit e push

---

## 🎨 Padrão de cores por disciplina

| Disciplina | Cor principal | Variável CSS |
|---|---|---|
| Português | Roxo `#7C3AED` | `--port-color` |
| Matemática | Verde `#059669` | `--mat-color` |
| Geografia | *(a definir)* | — |
| História | *(a definir)* | — |
| Ciências | *(a definir)* | — |

---

## 📐 Convenção de nomes de arquivo

```
[tipo]-[tema]-[disciplina].html

Tipos: quiz / complete-lacuna / caca-erro / ordenacao / criador / classificador / transformador / flashcards / treino / batalha / domino / missao / frases

Exemplos:
quiz-substantivos-portugues.html
flashcards-frações-matematica.html
hq-substantivos.png
```

---

## 🧠 Fundamentação pedagógica

As atividades seguem os princípios de:
- **Retrieval practice** — recuperação ativa supera releitura passiva
- **Spaced repetition** — revisão espaçada (Sistema Leitner nos flashcards)
- **Elaborative interrogation** — perguntar "por quê?" em vez de apresentar
- **Gamificação** — pontuação, medalhas e feedback imediato

Referências: Roediger & Karpicke (2006), Mayer (2009), Plass, Homer & Kinzer (2015)

---

## 👤 Projeto

Desenvolvido para apoiar os estudos do 5º ano.
Conteúdo baseado no livro *Aprender Juntos — Língua Portuguesa*.
