#!/usr/bin/env python3
"""
update-docs.py
Regenera referencias/CONTEUDO.md lendo index.html como fonte primária e
valida a existência de cada arquivo no sistema de arquivos.
Também atualiza a tabela de agentes do SQUAD.md.
Executado automaticamente pelo hook Stop do Claude Code.
"""

import os, re
from datetime import date

BASE        = r"C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos"
PERS_DIR    = r"C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\Personagens\5o ano"
CONTEUDO    = os.path.join(BASE, "CONTEUDO.md")
SQUAD       = os.path.join(BASE, "SQUAD.md")
AGENTS_DIR  = os.path.join(BASE, ".claude", "agents")
INDEX_HTML  = os.path.join(BASE, "index.html")

DISC_LABELS = {
    "port": "📝 Português",
    "mat":  "🔢 Matemática",
    "cien": "🔬 Ciências",
    "geo":  "🌍 Geografia",
    "hist": "📜 História",
}
DISC_ORDER = ["port", "mat", "cien", "geo", "hist"]


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def abs_path(rel_slash):
    """Converte caminho relativo (separador /) para absoluto a partir de BASE."""
    return os.path.join(BASE, rel_slash.replace("/", os.sep))

def rel_exists(rel_slash):
    """Verifica se arquivo relativo a BASE existe."""
    return os.path.isfile(abs_path(rel_slash))

def get_personagem(folder_abs, slug):
    """Extrai nome do personagem do hq-[slug]-prompt.md na pasta."""
    prompt = os.path.join(folder_abs, f"hq-{slug}-prompt.md")
    if not os.path.isfile(prompt):
        return None
    try:
        with open(prompt, encoding="utf-8") as f:
            txt = f.read()
        for pattern in [
            r"\*\*Personagem:\*\*\s*(.+)",
            r"###\s+Personagem principal:\s+(.+)",
            r"\*\*Personagem principal:\*\*\s*(.+)",
        ]:
            m = re.search(pattern, txt)
            if m:
                return m.group(1).strip()
    except Exception:
        pass
    return None

def parse_frontmatter(filepath):
    """Lê frontmatter YAML simples de um arquivo .md."""
    try:
        with open(filepath, encoding="utf-8") as f:
            txt = f.read()
        m = re.match(r"^---\n(.+?)\n---", txt, re.DOTALL)
        if not m:
            return {}
        result = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                result[k.strip()] = v.strip().strip('"')
        return result
    except Exception:
        return {}


# ──────────────────────────────────────────────
# Parse index.html — fonte primária
# ──────────────────────────────────────────────

def parse_index():
    """
    Lê index.html e extrai todos os temas publicados.
    Usa id="theme-[disc]-[slug]" para descobrir disciplina e slug.
    Extrai src da hq-img e hrefs dos act-cards.
    Retorna dict: disc → list of theme dicts.
    """
    if not os.path.isfile(INDEX_HTML):
        print("[update-docs] ERRO: index.html não encontrado em", INDEX_HTML)
        return {}

    with open(INDEX_HTML, encoding="utf-8") as f:
        html = f.read()

    # Localizar todas as divs theme-content pela posição no arquivo
    # Suporta tanto class="theme-content" quanto class="theme-content active"
    starts = list(re.finditer(
        r'<div\s+class="theme-content(?:\s+\w+)?"\s+id="theme-([a-z]+)-([a-z0-9-]+)"',
        html
    ))

    if not starts:
        print("[update-docs] AVISO: nenhum theme-content encontrado no index.html")
        return {}

    themes_by_disc = {d: [] for d in DISC_ORDER}

    for i, m in enumerate(starts):
        disc = m.group(1)
        slug = m.group(2)

        # Bloco vai até o início do próximo theme-content (ou fim do arquivo)
        block_start = m.start()
        block_end   = starts[i + 1].start() if i + 1 < len(starts) else len(html)
        block       = html[block_start:block_end]

        if disc not in themes_by_disc:
            # Disc desconhecido — registrar e pular
            print(f"[update-docs] AVISO: disc desconhecido '{disc}' no tema '{slug}'")
            continue

        # ── HQ img ──────────────────────────────────────────────
        # Padrão: <img class="hq-img" src="..." alt="...">
        # ou:     <img class="hq-img" src="..." ...>
        hq_m = re.search(r'<img\b[^>]*\bclass="hq-img"[^>]*\bsrc="([^"]+)"', block)
        if not hq_m:
            # Tenta ordem invertida: src antes de class
            hq_m = re.search(r'<img\b[^>]*\bsrc="([^"]+)"[^>]*\bclass="hq-img"', block)

        hq_src          = hq_m.group(1) if hq_m else None
        hq_folder_abs   = None

        if hq_src:
            hq_filename   = os.path.basename(hq_src)
            hq_folder_abs = os.path.dirname(abs_path(hq_src))
            hq_exists     = rel_exists(hq_src)

            hq_status_str = f"✅ `{hq_filename}`" if hq_exists else f"❌ `{hq_filename}` (ausente)"

            # Páginas individuais pg1–pg4
            pages = [os.path.join(hq_folder_abs, f"hq-{slug}-pg{n}.png") for n in range(1, 5)]
            if all(os.path.isfile(p) for p in pages):
                hq_status_str += " | Páginas: ✅ pg1–pg4"

            # Arquivo de prompt
            if os.path.isfile(os.path.join(hq_folder_abs, f"hq-{slug}-prompt.md")):
                hq_status_str += " | Prompt: ✅"
        else:
            hq_status_str = "❌ sem HQ"

        # ── Atividades (act-card) ────────────────────────────────
        # Padrão: <a class="act-card [disc]" href="..." target="_blank">
        #           ...
        #           <div class="act-title">Título</div>
        # class sempre antes de href neste HTML; usa \s+ para separar atributos
        act_matches = re.findall(
            r'<a\s+class="act-card[^"]*"\s+href="([^"]+)"[^>]*>'
            r'.*?<div\s+class="act-title">([^<]+)</div>',
            block, re.DOTALL
        )
        activities = []
        for href, title in act_matches:
            activities.append({
                "title":    title.strip(),
                "filename": os.path.basename(href),
                "href":     href,
                "exists":   rel_exists(href),
            })

        # ── Personagem ───────────────────────────────────────────
        personagem = get_personagem(hq_folder_abs, slug) if hq_folder_abs else None

        themes_by_disc[disc].append({
            "slug":       slug,
            "hq_status":  hq_status_str,
            "personagem": personagem,
            "activities": activities,
        })

    return themes_by_disc


# ──────────────────────────────────────────────
# Geração de referencias/CONTEUDO.md
# ──────────────────────────────────────────────

def build_conteudo():
    themes_by_disc = parse_index()
    if not themes_by_disc:
        return

    today       = date.today().strftime("%Y-%m-%d")
    total_temas = sum(len(v) for v in themes_by_disc.values())
    total_ativs = sum(len(t["activities"]) for v in themes_by_disc.values() for t in v)

    lines = [
        "# Conteúdo do Portal — Estado Atual",
        f"**Última atualização:** {today}",
        "",
        "---",
        "",
        "## Resumo",
        "",
        "| Disciplina | Temas | Atividades |",
        "|---|---|---|",
    ]
    for disc in DISC_ORDER:
        themes = themes_by_disc.get(disc, [])
        n_t = len(themes)
        n_a = sum(len(t["activities"]) for t in themes)
        lines.append(f"| {DISC_LABELS[disc]} | {n_t} | {n_a} |")
    lines += [
        f"| **Total** | **{total_temas}** | **{total_ativs}** |",
        "",
        "---",
        "",
    ]

    for disc in DISC_ORDER:
        themes = themes_by_disc.get(disc, [])
        label  = DISC_LABELS[disc]
        lines.append(f"## {label}")
        lines.append("")

        if not themes:
            lines.append("_(sem temas cadastrados)_")
            lines.append("")
            lines.append("---")
            lines.append("")
            continue

        for t in themes:
            slug = t["slug"]
            nome = slug.replace("-", " ").title()
            lines.append(f"### {nome}")
            if t["personagem"]:
                lines.append(f"**Personagem:** {t['personagem']}")
            lines.append(f"**HQ:** {t['hq_status']}")
            lines.append("")
            if t["activities"]:
                lines.append("| Atividade | Arquivo |")
                lines.append("|---|---|")
                for act in t["activities"]:
                    icon = "✅" if act["exists"] else "❌"
                    lines.append(f"| {act['title']} | {icon} `{act['filename']}` |")
            lines.append("")
            lines.append("---")
            lines.append("")

    # Personagens
    pers_files = []
    if os.path.isdir(PERS_DIR):
        pers_files = sorted(f for f in os.listdir(PERS_DIR) if f.lower().endswith(".png"))

    lines += [
        "## 🖼️ Personagens criados (Personagens\\5o ano\\)",
        "",
        "| Arquivo |",
        "|---|",
    ]
    for p in pers_files:
        lines.append(f"| `{p}` |")
    if not pers_files:
        lines.append("| _(nenhum ainda)_ |")

    lines += [
        "",
        "---",
        "",
        "## Legenda",
        "",
        "| Símbolo | Significado |",
        "|---|---|",
        "| ✅ | Arquivo presente |",
        "| ❌ | Arquivo ausente |",
        "| ⭐ | Template canônico de referência |",
        "| Páginas: ✅ pg1–pg4 | Páginas individuais da HQ salvas |",
        "| Prompt: ✅ | Arquivo `hq-[slug]-prompt.md` presente |",
    ]

    with open(CONTEUDO, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[update-docs] CONTEUDO.md atualizado — {total_temas} temas, {total_ativs} atividades")


# ──────────────────────────────────────────────
# Atualização da tabela de agentes no SQUAD.md
# ──────────────────────────────────────────────

SKILL_MAP = {
    "analisador-pedagogico": "`skill-analise-escopo`",
    "gerador-hq-prompt":     "`skill-gerar-hq-prompt`",
    "gerador-atividades":    "`skill-gerar-atividades-html`",
    "atualizador-index":     "`skill-atualizar-index`",
    "revisor-qualidade":     "—",
    "gerador-hq-imagens":    "`skill-hq-imagens`",
    "colador-hq":            "—",
    "atualizador-docs":      "—",
}

RESP_MAP = {
    "analisador-pedagogico": "Analisa fotos do livro, extrai conceitos e páginas, propõe estrutura de temas (Fase 0)",
    "gerador-hq-prompt":     "Cria `hq-[slug]-prompt.md` com narrativa de 4 páginas + folha de personagens",
    "gerador-atividades":    "Cria HTMLs das atividades interativas (quiz, mapa mental, etc.)",
    "atualizador-index":     "Adiciona o tema na sidebar, bloco de conteúdo e contador do index.html",
    "revisor-qualidade":     "Audita terminologia, escopo, gamificação e mapa mental — retorna score JSON",
    "gerador-hq-imagens":    "Escreve JSON de pedido em `.claude/pending/`; polling até Codex confirmar em `.claude/done/`",
    "colador-hq":            "Empilha pg1–pg4 verticalmente com Pillow → `hq-[slug].png`",
    "atualizador-docs":      "Regenera referencias/CONTEUDO.md (via index.html) e tabela de agentes do SQUAD.md",
}

def build_agents_table():
    if not os.path.isdir(AGENTS_DIR):
        return None
    rows = []
    for fname in sorted(os.listdir(AGENTS_DIR)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(AGENTS_DIR, fname)
        fm    = parse_frontmatter(fpath)
        name  = fm.get("name", fname.replace(".md", ""))
        model = fm.get("model", "—")

        model_short = (model
            .replace("claude-opus-4-7",   "**Opus 4.7**")
            .replace("claude-sonnet-4-6", "Sonnet 4.6")
            .replace("claude-haiku-4-5",  "Haiku 4.5"))

        resp  = RESP_MAP.get(name, fm.get("description", "—")[:80])
        skill = SKILL_MAP.get(name, "—")
        rows.append(f"| `{name}` | {model_short} | {resp} | {skill} |")

    header = [
        "| Agente | Modelo | Responsabilidade | Usa skill |",
        "|---|---|---|---|",
    ]
    return "\n".join(header + rows)

def update_squad():
    if not os.path.isfile(SQUAD):
        print("[update-docs] SQUAD.md não encontrado — pulando")
        return

    with open(SQUAD, encoding="utf-8") as f:
        content = f.read()

    new_table = build_agents_table()
    if not new_table:
        return

    # Substituir bloco entre "## Agentes" e a próxima seção "##"
    pattern     = r"(## Agentes\n\n)(\|.+?)(\n\n---)"
    replacement = r"\g<1>" + new_table + r"\g<3>"
    new_content, n = re.subn(pattern, replacement, content, flags=re.DOTALL)

    if n == 0:
        print("[update-docs] Padrão da tabela de agentes não encontrado no SQUAD.md")
        return

    # Atualizar data
    today = date.today().strftime("%Y-%m-%d")
    new_content = re.sub(
        r"\*\*Última atualização:\*\*.+",
        f"**Última atualização:** {today}",
        new_content
    )

    with open(SQUAD, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("[update-docs] SQUAD.md atualizado — tabela de agentes regenerada")


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    build_conteudo()
    update_squad()
