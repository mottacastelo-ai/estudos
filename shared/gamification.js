/**
 * SabendoGamification — Fase 2
 * Reveal progressivo do personagem pixelado + reveal cinematográfico da carta.
 *
 * Uso:
 *   await SabendoGamification.run(supa, uid, themeSlug, discipline, config);
 *
 * config: {
 *   characterName,      // ex: 'Prepo'
 *   characterEmoji,     // ex: '🤖'  (fallback se characterImg ausente)
 *   characterImg,       // ex: 'prepo-hd.png'  (relativo a _landing/)
 *   themeLabel,         // ex: 'Preposições · Português'
 *   totalActivities,    // ex: 8
 *   primaryColor, lightColor, bgColor, glowRgb,
 *   assetBase,          // opcional — prefixo de assets (default: '../../')
 *   backUrl             // opcional — redireciona após o reveal da carta
 * }
 */
(function () {
  "use strict";

  /* ------------------------------------------------------------------ */
  /* CSS — modal de reveal do personagem                                   */
  /* ------------------------------------------------------------------ */
  function injectStyles(primaryColor, lightColor, bgColor, glowRgb) {
    if (document.getElementById("sgami-styles")) return;
    var css = [
      "@keyframes sgami-fadein    { from{opacity:0} to{opacity:1} }",
      "@keyframes sgami-slideup   { from{transform:translateY(40px);opacity:0} to{transform:none;opacity:1} }",
      "@keyframes sgami-fillbar   { from{width:0} to{width:var(--sgami-bar-w)} }",
      "@keyframes sgami-chip-in   { from{transform:scale(0) translateY(6px);opacity:0} to{transform:none;opacity:1} }",
      "@keyframes sgami-flash     { 0%{opacity:0} 18%{opacity:1} 100%{opacity:0} }",
      "@keyframes sgami-ring-pulse {",
      "  0%,100% { box-shadow:0 0 0 3px SGAMI_PRIMARY, 0 0 24px rgba(SGAMI_GLOW,.4); }",
      "  50%     { box-shadow:0 0 0 5px SGAMI_LIGHT,   0 0 52px rgba(SGAMI_GLOW,.8); }",
      "}",
      "@keyframes sgami-celebrate { 0%{transform:scale(0)rotate(-20deg);opacity:0} 50%{transform:scale(1.3)rotate(5deg)} 100%{transform:scale(1)rotate(0);opacity:1} }",
      "@keyframes sgami-scan-sweep { 0%{top:-50px;opacity:.9} 100%{top:100%;opacity:0} }",
      "@keyframes sgami-wrap-pop   { 0%{transform:scale(1)} 30%{transform:scale(1.06)} 100%{transform:scale(1)} }",

      "#sgami-overlay {",
      "  position:fixed;inset:0;z-index:99999;",
      "  background:rgba(0,0,0,.65);backdrop-filter:blur(4px);",
      "  display:flex;align-items:center;justify-content:center;",
      "  animation:sgami-fadein .3s ease;",
      "  font-family:'Baloo 2',sans-serif;",
      "}",

      "#sgami-card {",
      "  background:#fff;border-radius:20px;padding:20px 18px 16px;",
      "  max-width:320px;width:90%;text-align:center;",
      "  box-shadow:0 20px 60px rgba(0,0,0,.4);",
      "  animation:sgami-slideup .4s cubic-bezier(.22,1,.36,1);",
      "}",

      "#sgami-title    { font-size:17px;font-weight:800;color:#1e1b4b;margin:0 0 2px; }",
      "#sgami-subtitle { font-size:12px;color:#6b7280;margin:0 0 14px; }",

      /* Canvas */
      ".sgami-canvas-wrap {",
      "  position:relative;width:200px;height:240px;",
      "  margin:0 auto 14px;border-radius:12px;overflow:hidden;",
      "}",
      "#sgami-char-canvas {",
      "  display:block;width:200px;height:240px;border-radius:12px;",
      "  image-rendering:pixelated;image-rendering:crisp-edges;",
      "}",
      ".sgami-canvas-wrap.done #sgami-char-canvas {",
      "  animation:sgami-ring-pulse 1.5s ease infinite;",
      "}",
      ".sgami-unlock-flash {",
      "  position:absolute;inset:0;border-radius:12px;",
      "  background:rgba(SGAMI_GLOW,.48);pointer-events:none;opacity:0;",
      "  animation:sgami-flash .65s ease forwards;",
      "}",
      ".sgami-scan-line {",
      "  position:absolute;left:0;right:0;height:52px;pointer-events:none;z-index:2;",
      "  background:linear-gradient(to bottom,transparent,rgba(SGAMI_GLOW,.55),transparent);",
      "  animation:sgami-scan-sweep linear forwards;",
      "}",
      ".sgami-canvas-wrap.sgami-wrap-pop { animation:sgami-wrap-pop .55s cubic-bezier(.22,1,.36,1) both; }",

      /* Chips */
      ".sgami-chips { display:flex;gap:6px;justify-content:center;flex-wrap:wrap;min-height:28px;margin-bottom:10px; }",
      ".sgami-chip {",
      "  background:SGAMI_BG;border:1.5px solid SGAMI_PRIMARY;",
      "  border-radius:8px;padding:3px 10px;",
      "  font-size:11px;font-weight:800;color:SGAMI_PRIMARY;",
      "  animation:sgami-chip-in .35s cubic-bezier(.22,1,.36,1) both;",
      "}",
      ".sgami-chip-ok  { background:#ECFDF5;border-color:#059669;color:#065F46; }",
      ".sgami-chip-bad { background:#FEF2F2;border-color:#EF4444;color:#991B1B; }",

      /* Barra */
      ".sgami-bar-wrap { background:#e5e7eb;border-radius:99px;height:8px;margin-bottom:4px;overflow:hidden; }",
      ".sgami-bar-fill {",
      "  height:100%;border-radius:99px;",
      "  background:linear-gradient(90deg,SGAMI_PRIMARY,SGAMI_LIGHT);",
      "  width:var(--sgami-bar-w);",
      "  transition:width .6s cubic-bezier(.22,1,.36,1);",
      "}",
      ".sgami-bar-fill.animated { animation:sgami-fillbar .6s .2s cubic-bezier(.22,1,.36,1) both; }",
      ".sgami-bar-label { font-size:11px;color:#9ca3af;margin-bottom:12px; }",

      /* Seção carta (ao completar) */
      ".sgami-carta { display:none;border-radius:14px;padding:10px 14px;margin-bottom:12px;animation:sgami-celebrate .5s cubic-bezier(.22,1,.36,1) both; }",
      ".sgami-carta.show { display:block; }",
      ".sgami-carta.comum    { background:#F9FAFB;border:1.5px solid #D1D5DB; }",
      ".sgami-carta.rara     { background:#EFF6FF;border:1.5px solid #93C5FD; }",
      ".sgami-carta.epica    { background:#EDE9FE;border:1.5px solid #C4B5FD; }",
      ".sgami-carta.lendaria { background:#FFFBEB;border:1.5px solid #FCD34D;box-shadow:0 0 20px rgba(251,191,36,.4); }",
      ".sgami-carta-name  { font-size:13px;font-weight:800;color:#5B21B6;margin-bottom:2px; }",
      ".sgami-carta-score { font-size:11px;color:#6b7280;margin-top:3px; }",
      ".sgami-carta-badge { display:inline-block;color:#fff;padding:2px 12px;border-radius:99px;font-size:11px;font-weight:800;margin-top:6px; }",
      ".sgami-carta.comum    .sgami-carta-badge { background:#6B7280; }",
      ".sgami-carta.rara     .sgami-carta-badge { background:#2563EB; }",
      ".sgami-carta.epica    .sgami-carta-badge { background:#7C3AED; }",
      ".sgami-carta.lendaria .sgami-carta-badge { background:linear-gradient(135deg,#F59E0B,#EF4444);box-shadow:0 2px 8px rgba(245,158,11,.45); }",

      /* Botão */
      "#sgami-continue {",
      "  background:linear-gradient(135deg,SGAMI_PRIMARY,SGAMI_LIGHT);",
      "  color:#fff;border:none;border-radius:50px;",
      "  padding:10px;font-size:13px;font-weight:800;",
      "  cursor:pointer;width:100%;font-family:'Baloo 2',sans-serif;",
      "  transition:opacity .2s;",
      "}",
      "#sgami-continue:hover { opacity:.88; }",
    ]
      .join("\n")
      .replace(/SGAMI_PRIMARY/g, primaryColor)
      .replace(/SGAMI_LIGHT/g, lightColor)
      .replace(/SGAMI_BG/g, bgColor)
      .replace(/SGAMI_GLOW/g, glowRgb);

    var st = document.createElement("style");
    st.id = "sgami-styles";
    st.textContent = css;
    document.head.appendChild(st);
  }

  /* ------------------------------------------------------------------ */
  /* CSS — reveal cinematográfico da carta                                 */
  /* ------------------------------------------------------------------ */
  function injectRevealStyles() {
    if (document.getElementById("sgami-reveal-styles")) return;
    var css = `
      @keyframes sgami-rev-bgfade    { to { opacity:1; } }
      @keyframes sgami-rev-flash-pop { 0%{opacity:0} 15%{opacity:1} 100%{opacity:0} }
      @keyframes sgami-rev-letter-fall { to { opacity:1; transform:translateY(0) rotate(0deg); } }
      @keyframes sgami-rev-card-spring {
        0%   { opacity:0; transform:scale(0.05) rotate(-10deg); }
        55%  { opacity:1; transform:scale(1.1) rotate(1.5deg); }
        75%  { transform:scale(0.96) rotate(-0.5deg); }
        100% { opacity:1; transform:scale(1) rotate(0deg); }
      }
      @keyframes sgami-rev-card-float {
        0%,100% { transform:translateY(0) rotate(0deg); }
        50%     { transform:translateY(-10px) rotate(.4deg); }
      }
      @keyframes sgami-rev-ring-pulse {
        0%   { filter:brightness(1); }
        40%  { filter:brightness(2.5) blur(2px); }
        100% { filter:brightness(1); }
      }
      @keyframes sgami-rev-blink { 0%,100%{opacity:.2} 50%{opacity:.55} }
      @keyframes sgami-rev-rainbow-spin { from{filter:hue-rotate(0deg)} to{filter:hue-rotate(360deg)} }
      @keyframes sgami-rev-name-shine { from{background-position:0% center} to{background-position:200% center} }
      @keyframes sgami-rev-shimmer { 0%{background-position:200% 0} 100%{background-position:-200% 0} }

      #sgami-rev-overlay {
        display:none; position:fixed; inset:0; z-index:999999;
        align-items:center; justify-content:center; flex-direction:column;
        cursor:pointer; overflow:hidden; font-family:"Baloo 2",sans-serif;
      }
      #sgami-rev-overlay.active { display:flex; }
      #sgami-rev-bg {
        position:absolute; inset:0;
        background:radial-gradient(ellipse at center,#120d28 0%,#05040f 70%);
        opacity:0; animation:sgami-rev-bgfade .5s ease forwards;
      }
      #sgami-rev-glow { position:absolute; inset:0; pointer-events:none; opacity:0; transition:opacity .4s; }
      #sgami-rev-canvas { position:absolute; inset:0; pointer-events:none; z-index:2; }
      #sgami-rev-flash { position:absolute; inset:0; pointer-events:none; z-index:3; opacity:0; }
      #sgami-rev-flash.pop { animation:sgami-rev-flash-pop .7s ease-out forwards; }

      #sgami-rev-title {
        position:relative; z-index:5;
        font-family:"Space Mono",monospace;
        font-size:11px; font-weight:700; letter-spacing:.22em; text-transform:uppercase;
        color:rgba(255,255,255,.3); height:24px;
        display:flex; align-items:center; gap:1px; margin-bottom:20px;
      }
      .sgami-rev-letter {
        display:inline-block; opacity:0;
        transform:translateY(-40px) rotate(-8deg);
        animation:sgami-rev-letter-fall .35s cubic-bezier(.22,1,.36,1) forwards;
      }
      .sgami-rev-space { width:8px; }

      #sgami-rev-stage { position:relative; z-index:5; display:flex; align-items:center; justify-content:center; }

      .sgami-rev-card {
        position:relative; width:280px; height:400px;
        border-radius:20px; overflow:visible; margin-top:64px;
      }
      .sgami-rev-frame { position:absolute; inset:0; border-radius:20px; overflow:hidden; }
      .sgami-rev-frame-bg { position:absolute; inset:0; background-size:cover; background-position:center top; }
      .sgami-rev-frame-overlay {
        position:absolute; inset:0;
        background:linear-gradient(to bottom,transparent 0%,transparent 45%,rgba(5,4,15,.7) 65%,rgba(5,4,15,.95) 100%);
      }
      .sgami-rev-char {
        position:absolute; bottom:150px; left:50%; transform:translateX(-50%);
        width:163px; height:163px; z-index:10; pointer-events:none;
        display:flex; align-items:center; justify-content:center;
      }
      .sgami-rev-char img { width:100%; height:100%; object-fit:contain; }
      .sgami-rev-char-emoji { font-size:72px; line-height:1; }
      .sgami-rev-info {
        position:absolute; bottom:0; left:0; right:0; height:148px; z-index:11;
        display:flex; flex-direction:column; align-items:center;
        padding:48px 18px 16px; gap:2px;
      }
      .sgami-rev-name  { font-size:22px; font-weight:900; line-height:1; text-align:center; }
      .sgami-rev-theme { font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:.1em; opacity:.65; text-align:center; }
      .sgami-rev-score { font-family:"Space Mono",monospace; font-size:10px; font-weight:700; margin-top:3px; }
      .sgami-rev-logo  { margin-top:auto; font-family:"Space Mono",monospace; font-size:11px; font-weight:700; }
      .sgami-rev-badge {
        position:absolute; top:256px; left:50%; transform:translateX(-50%);
        white-space:nowrap; font-family:"Space Mono",monospace;
        font-size:10px; font-weight:700; padding:4px 12px; border-radius:99px;
        z-index:12; letter-spacing:.04em;
      }
      .sgami-rev-ring { position:absolute; inset:-2px; border-radius:22px; z-index:-1; }

      .sgami-rev-card.comum .sgami-rev-frame-bg { background-color:#1A1035; }
      .sgami-rev-card.comum .sgami-rev-ring { background:linear-gradient(135deg,#6B7280,#374151,#9CA3AF); }
      .sgami-rev-card.comum .sgami-rev-char img { filter:drop-shadow(0 8px 24px rgba(0,0,0,.7)); }
      .sgami-rev-card.comum .sgami-rev-name  { color:#E5E0FF; }
      .sgami-rev-card.comum .sgami-rev-theme { color:#A78BFA; }
      .sgami-rev-card.comum .sgami-rev-score { color:rgba(255,255,255,.4); }
      .sgami-rev-card.comum .sgami-rev-badge { background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.2); color:#94A3B8; }
      .sgami-rev-card.comum .sgami-rev-logo  { color:rgba(255,255,255,.55); }
      .sgami-rev-card.comum .sgami-rev-logo span { color:#2DD4BF; }

      .sgami-rev-card.rara .sgami-rev-frame-bg { background-color:#0a1628; }
      .sgami-rev-card.rara .sgami-rev-ring { background:linear-gradient(135deg,#60A5FA,#1D4ED8,#93C5FD,#2563EB); box-shadow:0 0 24px rgba(37,99,235,.5); }
      .sgami-rev-card.rara .sgami-rev-char img { filter:drop-shadow(0 0 20px rgba(96,165,250,.5)) drop-shadow(0 8px 24px rgba(0,0,0,.7)); }
      .sgami-rev-card.rara .sgami-rev-name  { color:#fff; text-shadow:0 0 20px rgba(96,165,250,.7); }
      .sgami-rev-card.rara .sgami-rev-theme { color:#60A5FA; }
      .sgami-rev-card.rara .sgami-rev-score { color:rgba(147,197,253,.6); }
      .sgami-rev-card.rara .sgami-rev-badge { background:rgba(37,99,235,.45); border:1px solid #3B82F6; color:#93C5FD; box-shadow:0 0 12px rgba(59,130,246,.5); }
      .sgami-rev-card.rara .sgami-rev-logo  { color:#93C5FD; }
      .sgami-rev-card.rara .sgami-rev-logo span { color:#2DD4BF; }

      .sgami-rev-card.epica .sgami-rev-frame-bg { background-color:#0d0b1a; }
      .sgami-rev-card.epica .sgami-rev-ring { background:linear-gradient(135deg,#A78BFA,#6D28D9,#C4B5FD,#7C3AED); box-shadow:0 0 32px rgba(124,58,237,.65); }
      .sgami-rev-card.epica .sgami-rev-char img { filter:drop-shadow(0 0 28px rgba(167,139,250,.65)) drop-shadow(0 8px 24px rgba(0,0,0,.8)); }
      .sgami-rev-card.epica .sgami-rev-name  { color:#fff; text-shadow:0 0 24px rgba(167,139,250,.9),0 0 48px rgba(124,58,237,.5); }
      .sgami-rev-card.epica .sgami-rev-theme { color:#A78BFA; }
      .sgami-rev-card.epica .sgami-rev-score { color:rgba(196,181,253,.6); }
      .sgami-rev-card.epica .sgami-rev-badge { background:rgba(109,40,217,.5); border:1px solid #7C3AED; color:#C4B5FD; box-shadow:0 0 16px rgba(124,58,237,.65); }
      .sgami-rev-card.epica .sgami-rev-logo  { color:#C4B5FD; }
      .sgami-rev-card.epica .sgami-rev-logo span { color:#2DD4BF; }

      .sgami-rev-card.lendaria .sgami-rev-frame-bg { background-color:#451a03; }
      .sgami-rev-card.lendaria .sgami-rev-ring { background:linear-gradient(135deg,#FCD34D,#B45309,#FDE68A,#92400E,#FCD34D); box-shadow:0 0 40px rgba(245,158,11,.7),0 0 80px rgba(245,158,11,.25); }
      .sgami-rev-card.lendaria .sgami-rev-char img { filter:drop-shadow(0 0 30px rgba(245,158,11,.6)) drop-shadow(0 0 60px rgba(245,158,11,.25)) drop-shadow(0 8px 24px rgba(0,0,0,.9)); }
      .sgami-rev-card.lendaria .sgami-rev-name { background:linear-gradient(135deg,#FDE68A,#F59E0B,#FDE68A); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; filter:drop-shadow(0 0 12px rgba(245,158,11,.8)); }
      .sgami-rev-card.lendaria .sgami-rev-theme { color:#FCD34D; }
      .sgami-rev-card.lendaria .sgami-rev-score { color:rgba(252,211,77,.6); }
      .sgami-rev-card.lendaria .sgami-rev-badge { background:linear-gradient(135deg,rgba(245,158,11,.5),rgba(180,83,9,.5)); border:1px solid #F59E0B; color:#FDE68A; box-shadow:0 0 20px rgba(245,158,11,.7); }
      .sgami-rev-card.lendaria .sgami-rev-logo { background:linear-gradient(90deg,#FDE68A,#F59E0B,#FDE68A); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; filter:drop-shadow(0 0 8px rgba(245,158,11,.9)); }
      .sgami-rev-card.lendaria .sgami-rev-logo span { background:none; -webkit-text-fill-color:#2DD4BF; filter:none; }
      .sgami-rev-card.lendaria .sgami-rev-frame::after {
        content:''; position:absolute; inset:0; border-radius:20px;
        background:linear-gradient(105deg,transparent 25%,rgba(255,220,100,.08) 40%,rgba(255,255,255,.12) 50%,rgba(255,220,100,.08) 60%,transparent 75%);
        background-size:300% 100%; animation:sgami-rev-shimmer 2.5s ease-in-out infinite;
        pointer-events:none; z-index:9;
      }
      .sgami-rev-card.lendepica .sgami-rev-frame-bg { background-color:#0d0b1a; }
      .sgami-rev-card.lendepica .sgami-rev-ring {
        background:conic-gradient(from 0deg,#7C3AED,#3B82F6,#06B6D4,#10B981,#F59E0B,#EF4444,#EC4899,#7C3AED);
        box-shadow:0 0 20px rgba(124,58,237,.5),0 0 40px rgba(245,158,11,.4);
        animation:sgami-rev-rainbow-spin 4s linear infinite;
      }
      .sgami-rev-card.lendepica .sgami-rev-name {
        background:linear-gradient(90deg,#A78BFA,#FCD34D,#F472B6,#A78BFA);
        background-size:200% auto; -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
        animation:sgami-rev-name-shine 3s linear infinite;
      }
      .sgami-rev-card.lendepica .sgami-rev-badge { background:linear-gradient(135deg,rgba(124,58,237,.6),rgba(245,158,11,.5)); border:1px solid rgba(255,255,255,.4); color:#fff; }
      .sgami-rev-card.lendepica .sgami-rev-logo { background:linear-gradient(90deg,#A78BFA,#FCD34D); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
      .sgami-rev-card.lendepica .sgami-rev-logo span { background:none; -webkit-text-fill-color:#2DD4BF; }

      .sgami-rev-card.rev-enter    { animation:sgami-rev-card-spring .85s cubic-bezier(.34,1.56,.64,1) forwards; }
      .sgami-rev-card.rev-floating { animation:sgami-rev-card-float 3.2s ease-in-out infinite; }
      .sgami-rev-card.rev-ring-pulse .sgami-rev-ring { animation:sgami-rev-ring-pulse .5s ease-out !important; }

      #sgami-rev-tier {
        position:relative; z-index:5; font-family:"Space Mono",monospace;
        font-size:18px; font-weight:700; letter-spacing:.12em; text-transform:uppercase;
        margin-top:22px; opacity:0; transform:translateY(16px);
        transition:opacity .5s ease,transform .5s ease;
      }
      #sgami-rev-tier.visible { opacity:1; transform:translateY(0); }
      #sgami-rev-hint {
        position:absolute; bottom:32px; font-family:"Space Mono",monospace;
        font-size:9px; font-weight:700; letter-spacing:.2em; text-transform:uppercase;
        color:rgba(255,255,255,.25); z-index:6;
        opacity:0; transform:translateY(8px); transition:opacity .4s,transform .4s;
        animation:sgami-rev-blink 2s ease-in-out infinite;
      }
      #sgami-rev-hint.visible { opacity:1; transform:translateY(0); }
    `;
    var st = document.createElement("style");
    st.id = "sgami-reveal-styles";
    st.textContent = css;
    document.head.appendChild(st);
  }

  /* ------------------------------------------------------------------ */
  /* Estágios de revelação                                                 */
  /* ------------------------------------------------------------------ */
  var STAGES_8 = [
    { pixelSize: 42, gray: 100, bright: 38 },  // 0 — bloqueado
    { pixelSize: 38, gray: 100, bright: 42 },  // 1
    { pixelSize: 34, gray: 100, bright: 46 },  // 2
    { pixelSize: 30, gray: 95,  bright: 50 },  // 3
    { pixelSize: 26, gray: 88,  bright: 55 },  // 4
    { pixelSize: 20, gray: 78,  bright: 61 },  // 5
    { pixelSize: 13, gray: 55,  bright: 72 },  // 6
    { pixelSize:  4, gray: 15,  bright: 90 },  // 7 — salto dramático
    { pixelSize:  1, gray:  0,  bright: 100 }, // 8 — revelação total
  ];

  function getStages(n) {
    if (n === 8) return STAGES_8;
    var stages = [];
    for (var i = 0; i <= n; i++) {
      var t = i / n;
      var c = Math.pow(t, 3.2);
      stages.push({
        pixelSize: Math.max(1, Math.round(42 - 41 * c)),
        gray:      Math.round(100 * (1 - c)),
        bright:    Math.round(38 + 62 * c)
      });
    }
    return stages;
  }

  var STAGE_LABELS_8 = [
    "", "Quase nada...", "Algo está se formando...", "Uma figura misteriosa!",
    "Tomando forma...", "Quem será?", "Quase lá!", "Só falta um toque...", "Revelado!"
  ];

  function stageLabel(idx, total) {
    if (total === 8 && STAGE_LABELS_8[idx]) return STAGE_LABELS_8[idx];
    var pct = idx / total;
    if (pct <= 0.25) return "Algo está se formando...";
    if (pct <= 0.5)  return "Uma figura misteriosa!";
    if (pct <= 0.75) return "Quem será?";
    return "Quase lá!";
  }

  /* ------------------------------------------------------------------ */
  /* TIER_CONFIG do reveal da carta                                        */
  /* ------------------------------------------------------------------ */
  var REVEAL_TIERS = {
    comum: {
      badge: "⚪ Comum", tierLabel: "⚪ Comum", tierColor: "#9CA3AF",
      glowColor: "rgba(107,114,128,.15)", flash: null,
      rays: false, double: false, shockwave: false,
      particles: { count:28, speed:2.8, gravity:.06, colors:["#9CA3AF","#D1D5DB","#E5E7EB","#F3F4F6"], sizeMin:2, sizeMax:4, type:"circle", decay:.016 }
    },
    rara: {
      badge: "🔵 Rara", tierLabel: "🔵 Rara", tierColor: "#60A5FA",
      glowColor: "rgba(37,99,235,.2)", flash: null,
      rays: false, double: false, shockwave: false,
      particles: { count:45, speed:5, gravity:.06, colors:["#60A5FA","#93C5FD","#3B82F6","#BFDBFE","#ffffff"], sizeMin:2, sizeMax:5, type:"spark", decay:.013 }
    },
    epica: {
      badge: "🟣 Épica", tierLabel: "🟣 Épica", tierColor: "#A78BFA",
      glowColor: "rgba(124,58,237,.25)", flash: null,
      rays: false, double: false, shockwave: true,
      particles: { count:60, speed:6, gravity:.045, colors:["#A78BFA","#7C3AED","#C4B5FD","#DDD6FE","#ffffff"], sizeMin:3, sizeMax:6, type:"circle", decay:.011 }
    },
    lendepica: {
      badge: "✨ Lend-Épica", tierLabel: "✨ Lend-Épica", tierColor: "#FCD34D",
      glowColor: "rgba(124,58,237,.2)", flash: "rgba(180,100,255,0.75)",
      rays: false, double: true, shockwave: false,
      particles: { count:75, speed:7, gravity:.035, colors:["#A78BFA","#FCD34D","#F472B6","#60A5FA","#34D399","#fff"], sizeMin:3, sizeMax:7, type:"mixed", decay:.010 }
    },
    lendaria: {
      badge: "🌟 Lendária", tierLabel: "🌟 Lendária", tierColor: "#F59E0B",
      glowColor: "rgba(245,158,11,.22)", flash: "rgba(255,248,200,0.95)",
      rays: true, rayCount: 14, double: true, shockwave: false,
      particles: { count:95, speed:9, gravity:.025, colors:["#FCD34D","#F59E0B","#FDE68A","#ffffff","#FBBF24","#FEF3C7"], sizeMin:3, sizeMax:8, type:"star", decay:.009 }
    }
  };

  /* ------------------------------------------------------------------ */
  /* Sistema de partículas (reveal da carta)                               */
  /* ------------------------------------------------------------------ */
  var _rp = [], _rr = [], _rs = [], _rid = null, _rc = null, _rx = null;

  function _pNew(x, y, cfg) {
    var angle = Math.random() * Math.PI * 2;
    var spd   = cfg.speed * (.4 + Math.random() * .9);
    var t = cfg.type;
    return {
      x:x, y:y, vx:Math.cos(angle)*spd, vy:Math.sin(angle)*spd - cfg.speed*.3,
      alpha:1, decay:cfg.decay+Math.random()*.008,
      color:cfg.colors[Math.floor(Math.random()*cfg.colors.length)],
      size:cfg.sizeMin+Math.random()*(cfg.sizeMax-cfg.sizeMin),
      gravity:cfg.gravity, rot:Math.random()*Math.PI*2,
      rotSpd:(Math.random()-.5)*.15,
      type:t==="mixed"?(Math.random()>.5?"circle":"spark"):t
    };
  }
  function _pDraw(p, c) {
    if (p.alpha<=0) return;
    c.save(); c.globalAlpha=Math.max(0,p.alpha); c.fillStyle=c.strokeStyle=p.color;
    if (p.type==="circle") { c.beginPath(); c.arc(p.x,p.y,p.size,0,Math.PI*2); c.fill(); }
    else if (p.type==="spark") { c.translate(p.x,p.y); c.rotate(Math.atan2(p.vy,p.vx)); c.beginPath(); c.ellipse(0,0,p.size*3.5,p.size*.7,0,0,Math.PI*2); c.fill(); }
    else if (p.type==="star") {
      c.translate(p.x,p.y); c.rotate(p.rot); c.beginPath();
      for (var i=0;i<4;i++){var a=(i/4)*Math.PI*2,a2=a+Math.PI/4;c.lineTo(Math.cos(a)*p.size*2.2,Math.sin(a)*p.size*2.2);c.lineTo(Math.cos(a2)*p.size*.55,Math.sin(a2)*p.size*.55);}
      c.closePath(); c.fill();
    }
    c.restore();
  }
  function _swNew(x,y,color){return{x:x,y:y,r:10,alpha:.7,color:color};}
  function _swDraw(s,c){if(s.alpha<=0)return;c.save();c.globalAlpha=Math.max(0,s.alpha);c.strokeStyle=s.color;c.lineWidth=3;c.beginPath();c.arc(s.x,s.y,s.r,0,Math.PI*2);c.stroke();c.restore();}
  function _rayNew(cx,cy,angle,color){return{cx:cx,cy:cy,angle:angle,color:color,len:0,maxLen:Math.hypot(window.innerWidth,window.innerHeight)*.55,alpha:0,growing:true};}
  function _rayDraw(r,c){if(r.alpha<=0)return;c.save();c.globalAlpha=Math.max(0,r.alpha);var grd=c.createLinearGradient(r.cx,r.cy,r.cx+Math.cos(r.angle)*r.len,r.cy+Math.sin(r.angle)*r.len);grd.addColorStop(0,r.color);grd.addColorStop(1,"transparent");c.strokeStyle=grd;c.lineWidth=4+Math.random()*2;c.beginPath();c.moveTo(r.cx,r.cy);c.lineTo(r.cx+Math.cos(r.angle)*r.len,r.cy+Math.sin(r.angle)*r.len);c.stroke();c.restore();}

  function _fxLoop() {
    _rx.clearRect(0,0,_rc.width,_rc.height);
    _rr=_rr.filter(function(r){return r.alpha>0;});
    _rs=_rs.filter(function(s){return s.alpha>0;});
    _rp=_rp.filter(function(p){return p.alpha>0;});
    _rr.forEach(function(r){if(r.growing){r.len+=r.maxLen*.045;r.alpha=Math.min(.65,r.alpha+.065);if(r.len>=r.maxLen)r.growing=false;}else{r.alpha-=.028;}_rayDraw(r,_rx);});
    _rs.forEach(function(s){s.r+=14;s.alpha-=.055;_swDraw(s,_rx);});
    _rp.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.vy+=p.gravity;p.vx*=.985;p.rot+=p.rotSpd;p.alpha-=p.decay;_pDraw(p,_rx);});
    if(_rr.length||_rs.length||_rp.length){_rid=requestAnimationFrame(_fxLoop);}else{_rid=null;}
  }
  function _fxStart(){if(_rid)cancelAnimationFrame(_rid);_rid=requestAnimationFrame(_fxLoop);}

  /* ------------------------------------------------------------------ */
  /* Canvas — renderização pixelada                                        */
  /* ------------------------------------------------------------------ */
  function renderPixelated(ctx, img, canvas, pixelSize, grayPct, brightPct) {
    if (!img || !img.complete || !img.naturalWidth) return;
    var W = canvas.width, H = canvas.height;
    if (pixelSize <= 1) {
      ctx.clearRect(0, 0, W, H);
      ctx.filter = "grayscale(" + grayPct + "%) brightness(" + brightPct + "%)";
      ctx.drawImage(img, 0, 0, W, H);
      ctx.filter = "none";
      return;
    }
    var sw = Math.ceil(W / pixelSize), sh = Math.ceil(H / pixelSize);
    var off = document.createElement("canvas");
    off.width = sw; off.height = sh;
    var octx = off.getContext("2d");
    octx.filter = "grayscale(" + grayPct + "%) brightness(" + brightPct + "%)";
    octx.drawImage(img, 0, 0, sw, sh);
    ctx.clearRect(0, 0, W, H);
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(off, 0, 0, W, H);
    ctx.imageSmoothingEnabled = true;
  }

  /* ------------------------------------------------------------------ */
  /* Raridade                                                              */
  /* ------------------------------------------------------------------ */
  async function calcRarity(supa, uid, themeSlug) {
    var res = await supa.from("activity_log").select("score,is_first_attempt,activity_type")
      .eq("user_id", uid).eq("theme_slug", themeSlug).not("score", "is", null);
    var rows = res.data || [];
    if (!rows.length) return { rarity: "comum", avg: 0 };

    // Lendária: TODOS os registros são primeira tentativa com 100%
    var allPerfect = rows.every(function(r) { return r.is_first_attempt === true && r.score === 100; });
    if (allPerfect) return { rarity: "lendaria", avg: 100 };

    // Melhor score por tipo de atividade (cada atividade tem um "slot")
    var best = {};
    rows.forEach(function(r) {
      var key = r.activity_type || "unknown";
      if (best[key] === undefined || r.score > best[key]) best[key] = r.score;
    });
    var keys = Object.keys(best);
    var avg = keys.reduce(function(acc, k) { return acc + best[k]; }, 0) / keys.length;

    return { rarity: avg >= 90 ? "epica" : avg >= 70 ? "rara" : "comum", avg: avg };
  }

  async function saveCard(supa, uid, themeSlug, discipline, rarity) {
    await supa.from("cards").upsert(
      { user_id: uid, theme_slug: themeSlug, discipline: discipline, rarity: rarity },
      { onConflict: "user_id,theme_slug" }
    );
  }

  /* ------------------------------------------------------------------ */
  /* Busca info do progresso                                               */
  /* ------------------------------------------------------------------ */
  async function fetchProgress(supa, uid, themeSlug) {
    var [countRes, lastRes] = await Promise.all([
      supa.from("activity_log").select("id", { count: "exact", head: true })
        .eq("user_id", uid).eq("theme_slug", themeSlug).eq("is_first_attempt", true),
      supa.from("activity_log").select("score,is_first_attempt")
        .eq("user_id", uid).eq("theme_slug", themeSlug)
        .order("created_at", { ascending: false }).limit(1)
    ]);
    return {
      completedCount:  countRes.count  || 0,
      lastScore:       lastRes.data && lastRes.data[0] ? lastRes.data[0].score       : null,
      isFirstAttempt:  lastRes.data && lastRes.data[0] ? lastRes.data[0].is_first_attempt : false
    };
  }

  /* ------------------------------------------------------------------ */
  /* Modal de reveal do personagem                                         */
  /* ------------------------------------------------------------------ */
  function showCharModal(opts) {
    // opts: { stageIndex, prevStageIndex, totalActivities, stages, img,
    //         lastScore, isFirstAttempt, isComplete, rarity, avgPct, config }
    return new Promise(function(resolve) {
      var cfg = opts.config;
      var stage    = opts.stages[opts.stageIndex];
      var prevStage = opts.stages[opts.prevStageIndex];
      var total    = opts.totalActivities;
      var idx      = opts.stageIndex;
      var isComplete = opts.isComplete;
      var barPct   = Math.round((idx / total) * 100) + "%";

      // Título
      var title, subtitle;
      if (isComplete) {
        title    = "🎉 Personagem revelado!";
        subtitle = "Você completou todas as atividades!";
      } else if (!opts.isFirstAttempt) {
        title    = "✅ Atividade concluída";
        subtitle = cfg.characterName + " · " + idx + " de " + total + " atividades";
      } else {
        title    = idx <= 2 ? "✨ Algo está se formando..." : "✨ Ficou mais nítido!";
        subtitle = cfg.characterName + " · " + idx + " de " + total + " atividades";
      }

      // Carta (somente ao completar)
      var rarityLabels = { comum:"Comum ⚪", rara:"Rara 🔵", epica:"Épica 🟣", lendaria:"Lendária 🌟" };
      var cartaHtml = isComplete ? [
        '<div class="sgami-carta ' + opts.rarity + '" id="sgami-carta-el">',
        '  <div class="sgami-carta-name">' + cfg.characterName + ' — ' + (cfg.themeLabel || "") + '</div>',
        '  <div class="sgami-carta-score">Acerto geral: ' + Math.round(opts.avgPct) + '%</div>',
        '  <span class="sgami-carta-badge">' + (rarityLabels[opts.rarity] || opts.rarity) + '</span>',
        '</div>'
      ].join("") : "";

      // Chips
      var chipsHtml = "";
      if (opts.isFirstAttempt && idx > 0 && !isComplete) {
        chipsHtml += '<span class="sgami-chip">' + stageLabel(idx, total) + '</span>';
      }
      if (opts.lastScore !== null) {
        var scoreOk = opts.lastScore >= 70;
        chipsHtml += '<span class="sgami-chip ' + (scoreOk ? "sgami-chip-ok" : "sgami-chip-bad") + '">' +
          opts.lastScore + '%</span>';
      }

      var continueLabel = isComplete ? "Ver minha carta! ✨" : "Continuar →";

      var html = [
        '<div id="sgami-card">',
        '  <div id="sgami-title">' + title + '</div>',
        '  <div id="sgami-subtitle">' + subtitle + '</div>',
        '  <div class="sgami-canvas-wrap" id="sgami-canvas-wrap">',
        '    <canvas id="sgami-char-canvas" width="200" height="240"></canvas>',
        '  </div>',
        '  <div class="sgami-chips">' + chipsHtml + '</div>',
        cartaHtml,
        '  <div class="sgami-bar-wrap"><div class="sgami-bar-fill" id="sgami-bar" style="--sgami-bar-w:' + barPct + '"></div></div>',
        '  <div class="sgami-bar-label">' + idx + ' / ' + total + ' atividades</div>',
        '  <button id="sgami-continue">' + continueLabel + '</button>',
        '</div>'
      ].join("");

      var overlay = document.createElement("div");
      overlay.id = "sgami-overlay";
      overlay.innerHTML = html;
      document.body.appendChild(overlay);

      // Canvas setup
      var canvas = overlay.querySelector("#sgami-char-canvas");
      var ctx    = canvas.getContext("2d");
      var wrap   = overlay.querySelector("#sgami-canvas-wrap");

      // Render inicial (estágio anterior)
      renderPixelated(ctx, opts.img, canvas, prevStage.pixelSize, prevStage.gray, prevStage.bright);

      // Animação para o estágio atual (somente primeira tentativa)
      if (opts.isFirstAttempt && idx > 0) {
        var ANIM_DUR = idx >= total - 1 ? 1500 : 700;
        var animFrom = { pixelSize: prevStage.pixelSize, gray: prevStage.gray, bright: prevStage.bright };
        var animTo   = { pixelSize: stage.pixelSize,     gray: stage.gray,     bright: stage.bright };
        var animStart = performance.now();
        var raf = null;

        function ease(t) { return 1 - Math.pow(1 - t, 3); }
        function lerp(a, b, t) { return a + (b - a) * t; }

        function drawFrame() {
          var raw = Math.min(1, (performance.now() - animStart) / ANIM_DUR);
          var t   = ease(raw);
          renderPixelated(ctx, opts.img, canvas,
            Math.max(1, Math.round(lerp(animFrom.pixelSize, animTo.pixelSize, t))),
            Math.round(lerp(animFrom.gray,  animTo.gray,  t)),
            Math.round(lerp(animFrom.bright, animTo.bright, t))
          );
          if (raw < 1) { raf = requestAnimationFrame(drawFrame); }
          else {
            raf = null;
            if (isComplete) { wrap.classList.add("done"); }
          }
        }

        // Flash + scan-line + wrap-pop + início da animação
        setTimeout(function() {
          // Flash
          var flash = document.createElement("div");
          flash.className = "sgami-unlock-flash";
          wrap.appendChild(flash);
          setTimeout(function() { if (flash.parentNode) flash.remove(); }, 700);

          // Scan-line sweeping top→bottom
          var scan = document.createElement("div");
          scan.className = "sgami-scan-line";
          scan.style.animationDuration = ANIM_DUR + "ms";
          wrap.appendChild(scan);
          setTimeout(function() { if (scan.parentNode) scan.remove(); }, ANIM_DUR + 100);

          // Wrap pop (escala)
          wrap.classList.remove("sgami-wrap-pop");
          void wrap.offsetWidth;
          wrap.classList.add("sgami-wrap-pop");
          setTimeout(function() { wrap.classList.remove("sgami-wrap-pop"); }, 600);

          drawFrame();
        }, 150);

        // Carta aparece após animação (ao completar)
        if (isComplete) {
          setTimeout(function() {
            var el = overlay.querySelector("#sgami-carta-el");
            if (el) el.classList.add("show");
          }, ANIM_DUR + 400);
        }

      } else {
        // Retry: renderiza estágio atual direto, sem animação
        renderPixelated(ctx, opts.img, canvas, stage.pixelSize, stage.gray, stage.bright);
        if (isComplete) { wrap.classList.add("done"); }
      }

      // Botão
      overlay.querySelector("#sgami-continue").addEventListener("click", function() {
        overlay.style.animation = "sgami-fadein .25s ease reverse forwards";
        setTimeout(function() { overlay.remove(); resolve(); }, 250);
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* Reveal cinematográfico da carta                                       */
  /* ------------------------------------------------------------------ */
  function showReveal(rarity, config, avgPct) {
    return new Promise(function(resolve) {
      injectRevealStyles();

      var tierCfg  = REVEAL_TIERS[rarity] || REVEAL_TIERS.comum;
      var base     = config.assetBase || "../../";
      var bgSuffix = rarity === "lendepica" ? "lend-epica" : rarity;
      var cardBgUrl = base + "_landing/cartas/carta-fundo-" + bgSuffix + ".png";
      var scoreText = avgPct != null ? "Acerto: " + Math.round(avgPct) + "%" : "";

      var charInner = config.characterImg
        ? '<img src="' + base + "_landing/" + config.characterImg + '" alt="' + config.characterName + '">'
        : '<span class="sgami-rev-char-emoji">' + (config.characterEmoji || "⭐") + "</span>";

      var old = document.getElementById("sgami-rev-overlay");
      if (old) old.remove();

      var overlay = document.createElement("div");
      overlay.id = "sgami-rev-overlay";
      overlay.innerHTML = [
        '<div id="sgami-rev-bg"></div>',
        '<div id="sgami-rev-glow"></div>',
        '<canvas id="sgami-rev-canvas"></canvas>',
        '<div id="sgami-rev-flash"></div>',
        '<div id="sgami-rev-title"></div>',
        '<div id="sgami-rev-stage">',
        '  <div class="sgami-rev-card ' + rarity + '" id="sgami-rev-card">',
        '    <div class="sgami-rev-ring"></div>',
        '    <div class="sgami-rev-frame">',
        '      <div class="sgami-rev-frame-bg" style="background-image:url(\'' + cardBgUrl + '\')"></div>',
        '      <div class="sgami-rev-frame-overlay"></div>',
        '    </div>',
        '    <div class="sgami-rev-char">' + charInner + '</div>',
        '    <div class="sgami-rev-badge">' + tierCfg.badge + '</div>',
        '    <div class="sgami-rev-info">',
        '      <div class="sgami-rev-name">' + config.characterName + '</div>',
        '      <div class="sgami-rev-theme">' + (config.themeLabel || "") + '</div>',
        '      <div class="sgami-rev-score">' + scoreText + '</div>',
        '      <div class="sgami-rev-logo">sabendo<span>.</span></div>',
        '    </div>',
        '  </div>',
        '</div>',
        '<div id="sgami-rev-tier"></div>',
        '<div id="sgami-rev-hint">toque para continuar</div>',
      ].join("");
      document.body.appendChild(overlay);

      _rc = overlay.querySelector("#sgami-rev-canvas");
      _rx = _rc.getContext("2d");
      _rc.width = window.innerWidth; _rc.height = window.innerHeight;
      _rp = []; _rr = []; _rs = [];
      if (_rid) { cancelAnimationFrame(_rid); _rid = null; }

      var card    = overlay.querySelector("#sgami-rev-card");
      var titleEl = overlay.querySelector("#sgami-rev-title");
      var tierRev = overlay.querySelector("#sgami-rev-tier");
      var cont    = overlay.querySelector("#sgami-rev-hint");
      var glow    = overlay.querySelector("#sgami-rev-glow");
      var flash   = overlay.querySelector("#sgami-rev-flash");

      card.style.cssText = "opacity:0; transform:scale(0.05) rotate(-10deg); animation:none;";

      var TEXT = "NOVA CARTA OBTIDA";
      titleEl.innerHTML = "";
      TEXT.split("").forEach(function(ch, i) {
        if (ch === " ") { var sp=document.createElement("span"); sp.className="sgami-rev-space"; titleEl.appendChild(sp); }
        else { var s=document.createElement("span"); s.className="sgami-rev-letter"; s.textContent=ch; s.style.animationDelay=(i*38)+"ms"; titleEl.appendChild(s); }
      });

      tierRev.textContent = tierCfg.tierLabel;
      tierRev.style.color = tierCfg.tierColor;
      tierRev.style.textShadow = "0 0 24px " + tierCfg.tierColor;
      glow.style.background = "radial-gradient(ellipse at center," + tierCfg.glowColor + " 0%,transparent 65%)";

      overlay.style.display = "flex"; overlay.offsetHeight; overlay.classList.add("active");

      var canClose = false;
      overlay.addEventListener("click", function handler() {
        if (!canClose) return;
        overlay.removeEventListener("click", handler);
        overlay.style.transition = "opacity .35s"; overlay.style.opacity = "0";
        setTimeout(function() { overlay.remove(); _rp=[];_rr=[];_rs=[]; if(_rid){cancelAnimationFrame(_rid);_rid=null;} resolve(); }, 350);
      });

      function at(fn, delay) { setTimeout(fn, delay); }
      at(function(){glow.style.transition="opacity 1s";glow.style.opacity="1";}, 300);
      at(function(){card.style.cssText="";void card.offsetWidth;card.classList.add("rev-enter");}, 820);
      if (tierCfg.flash) {
        at(function(){flash.style.background=tierCfg.flash;flash.className="";flash.offsetHeight;flash.classList.add("pop");}, 900);
      }
      if (tierCfg.shockwave||tierCfg.double) {
        at(function(){var r=card.getBoundingClientRect();_rs.push(_swNew(r.left+r.width/2,r.top+r.height/2,tierCfg.tierColor));_fxStart();}, 1050);
      }
      if (tierCfg.rays) {
        at(function(){var r=card.getBoundingClientRect();var cx=r.left+r.width/2,cy=r.top+r.height/2;for(var i=0;i<tierCfg.rayCount;i++)_rr.push(_rayNew(cx,cy,(i/tierCfg.rayCount)*Math.PI*2,"#FDE68A"));_fxStart();}, 1020);
      }
      at(function(){var r=card.getBoundingClientRect();var cx=r.left+r.width/2,cy=r.top+r.height/3;for(var i=0;i<tierCfg.particles.count;i++)_rp.push(_pNew(cx,cy,tierCfg.particles));_fxStart();}, 1100);
      if (tierCfg.double) {
        at(function(){var r=card.getBoundingClientRect();var cx=r.left+r.width/2,cy=r.top+r.height/2;var n=Math.floor(tierCfg.particles.count*.7);for(var i=0;i<n;i++)_rp.push(_pNew(cx,cy,tierCfg.particles));}, 1400);
      }
      at(function(){card.classList.add("rev-ring-pulse");setTimeout(function(){card.classList.remove("rev-ring-pulse");},600);}, 1350);
      at(function(){card.style.opacity="1";card.style.transform="scale(1) rotate(0deg)";card.classList.remove("rev-enter");void card.offsetWidth;card.style.transform="";card.classList.add("rev-floating");}, 1700);
      at(function(){tierRev.classList.add("visible");}, 1800);
      at(function(){cont.classList.add("visible");canClose=true;}, 2700);
    });
  }

  /* ------------------------------------------------------------------ */
  /* run()                                                                 */
  /* ------------------------------------------------------------------ */
  async function run(supa, uid, themeSlug, discipline, config) {
    var glowRgb = config.glowRgb || "124,58,237";
    injectStyles(config.primaryColor, config.lightColor, config.bgColor, glowRgb);

    var base           = config.assetBase || "../../";
    var totalActivities = config.totalActivities || 8;
    var stages         = getStages(totalActivities);

    // Busca progresso e score da atividade atual
    var progress = await fetchProgress(supa, uid, themeSlug);
    var stageIndex = Math.min(progress.completedCount, totalActivities);
    var prevStageIndex = Math.max(0, progress.isFirstAttempt ? stageIndex - 1 : stageIndex);
    var isComplete = stageIndex >= totalActivities;

    var rarity = null, avgPct = null, prevRarity = null, rarityImproved = false;
    if (isComplete) {
      // Busca raridade atual armazenada (antes de recalcular)
      var cardRes = await supa.from("cards").select("rarity")
        .eq("user_id", uid).eq("theme_slug", themeSlug).single();
      prevRarity = cardRes.data ? cardRes.data.rarity : null;

      var result = await calcRarity(supa, uid, themeSlug);
      rarity = result.rarity; avgPct = result.avg;
      await saveCard(supa, uid, themeSlug, discipline, rarity);

      // Reveal só se: primeira vez OU raridade melhorou
      var RARITY_ORDER = ["comum", "rara", "epica", "lendepica", "lendaria"];
      rarityImproved = RARITY_ORDER.indexOf(rarity) > RARITY_ORDER.indexOf(prevRarity || "");
    }

    // Carrega imagem do personagem
    var img = null;
    if (config.characterImg) {
      img = new Image();
      img.src = base + "_landing/" + config.characterImg;
      await new Promise(function(res) {
        if (img.complete && img.naturalWidth) { res(); return; }
        img.onload = res; img.onerror = res;
      });
    }

    // Modal do personagem pixelado
    await showCharModal({
      stageIndex: stageIndex,
      prevStageIndex: prevStageIndex,
      totalActivities: totalActivities,
      stages: stages,
      img: img,
      lastScore: progress.lastScore,
      isFirstAttempt: progress.isFirstAttempt,
      isComplete: isComplete,
      rarity: rarity,
      prevRarity: prevRarity,
      rarityImproved: rarityImproved,
      avgPct: avgPct,
      config: config
    });

    // Reveal cinematográfico: primeira conclusão OU raridade melhorou
    if (isComplete && (!prevRarity || rarityImproved)) {
      await showReveal(rarity, config, avgPct);
    }

    if (config.backUrl) window.location.href = config.backUrl;
  }

  /* ------------------------------------------------------------------ */
  /* Export                                                                */
  /* ------------------------------------------------------------------ */
  window.SabendoGamification = { run: run };
})();
