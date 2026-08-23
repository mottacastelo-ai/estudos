---
name: skill-hq-imagens
description: "OBSOLETA (desde 2026-08-22) — documentava o contrato de geração de HQ via Codex Desktop + pasta .claude/pending/. Substituída pela chamada direta ao Codex via MCP, documentada em .claude/agents/gerador-hq-imagens.md."
---

# Skill: Geração de Imagens HQ via Codex — OBSOLETA

> ⚠️ **Este arquivo está obsoleto.** O fluxo que ele documentava (contrato JSON em `.claude/pending/`/`.claude/done/`/`.claude/error/`, monitorado pela automação "Gerar HQs pendentes" no Codex Desktop) **foi removido em 2026-08-22**, após a geração via MCP ser validada de ponta a ponta em produção (5 temas do Capítulo 6 de Português).
>
> A geração de imagens de HQ agora é feita **exclusivamente** chamando o Codex diretamente via MCP (tool `codex`), sem Codex Desktop, sem pasta de controle, sem intervenção manual de Léo. O fluxo completo e atualizado está documentado em `.claude/agents/gerador-hq-imagens.md` — consulte esse arquivo, não este.
>
> Mantido apenas como referência histórica. Não seguir as instruções abaixo.

---

## Ver também

- `.claude/agents/gerador-hq-imagens.md` — fluxo atual (Codex via MCP)
- `ERROS.md` seção ERR-005 — defeitos conhecidos de geração de HQ e regras de prevenção
- `CLAUDE.md` seção "Geração de imagens — Codex via MCP (única via suportada)"
