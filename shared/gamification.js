/**
 * SabendoGamification — Fase 2
 * Gacha drop modal exibido após concluir uma atividade.
 *
 * Uso:
 *   await SabendoGamification.run(supa, uid, themeSlug, discipline, config);
 *
 * config: {
 *   characterName, characterEmoji,
 *   primaryColor, lightColor, bgColor, glowRgb,
 *   pieces: [{ id, name, emoji }]   // sempre 4 peças
 * }
 */
(function () {
  "use strict";

  /* ------------------------------------------------------------------ */
  /* CSS                                                                  */
  /* ------------------------------------------------------------------ */
  function injectStyles(primaryColor, lightColor, bgColor) {
    if (document.getElementById("sgami-styles")) return;
    var css = [
      "@keyframes sgami-fadein   { from{opacity:0} to{opacity:1} }",
      "@keyframes sgami-slideup  { from{transform:translateY(40px);opacity:0} to{transform:none;opacity:1} }",
      "@keyframes sgami-bounce   { 0%{transform:scale(0)rotate(-10deg);opacity:0} 60%{transform:scale(1.2)rotate(5deg)} 100%{transform:scale(1)rotate(0);opacity:1} }",
      "@keyframes sgami-celebrate{ 0%{transform:scale(0)rotate(-20deg);opacity:0} 50%{transform:scale(1.3)rotate(5deg)} 100%{transform:scale(1)rotate(0);opacity:1} }",
      "@keyframes sgami-glow     { 0%,100%{box-shadow:0 0 8px 2px rgba(SGAMI_GLOW,.4)} 50%{box-shadow:0 0 18px 6px rgba(SGAMI_GLOW,.8)} }",
      "@keyframes sgami-fillbar  { from{width:0} to{width:var(--sgami-bar-w)} }",

      "#sgami-overlay {",
      "  position:fixed;inset:0;z-index:99999;",
      "  background:rgba(0,0,0,.65);backdrop-filter:blur(4px);",
      "  display:flex;align-items:center;justify-content:center;",
      "  animation:sgami-fadein .3s ease;",
      "  font-family:'Baloo 2',sans-serif;",
      "}",

      "#sgami-card {",
      "  background:#fff;border-radius:20px;padding:28px 24px 22px;",
      "  max-width:340px;width:90%;text-align:center;",
      "  box-shadow:0 16px 48px rgba(0,0,0,.2);",
      "  animation:sgami-slideup .4s cubic-bezier(.22,1,.36,1);",
      "}",

      "#sgami-title { font-size:20px;font-weight:800;margin:0 0 4px; color:#1e1b4b; }",
      "#sgami-subtitle { font-size:13px;color:#6b7280;margin:0 0 20px; }",

      ".sgami-slots { display:flex;gap:10px;justify-content:center;margin-bottom:18px; }",
      ".sgami-slot {",
      "  width:64px;height:64px;border-radius:14px;",
      "  display:flex;align-items:center;justify-content:center;",
      "  font-size:26px;transition:transform .2s;",
      "}",
      ".sgami-slot-empty { background:#f3f4f6; }",
      ".sgami-slot-empty-inner { font-size:24px;opacity:.3; }",
      ".sgami-slot-collected { background:SGAMI_BG; }",
      ".sgami-slot-new {",
      "  background:SGAMI_BG;",
      "  border:3px solid SGAMI_PRIMARY;",
      "  animation:sgami-bounce .55s cubic-bezier(.22,1,.36,1) both, sgami-glow 1.8s ease-in-out infinite;",
      "}",

      ".sgami-bar-wrap { background:#e5e7eb;border-radius:99px;height:10px;margin-bottom:18px;overflow:hidden; }",
      ".sgami-bar-fill {",
      "  height:100%;border-radius:99px;",
      "  background:linear-gradient(90deg,SGAMI_PRIMARY,SGAMI_LIGHT);",
      "  width:var(--sgami-bar-w);",
      "  animation:sgami-fillbar .6s .2s cubic-bezier(.22,1,.36,1) both;",
      "}",
      ".sgami-bar-label { font-size:12px;color:#9ca3af;margin-top:4px;margin-bottom:16px; }",

      /* duplicate warning */
      ".sgami-dup-warn {",
      "  background:#fffbeb;border:1.5px solid #fbbf24;border-radius:12px;",
      "  padding:10px 14px;font-size:13px;color:#92400e;margin-bottom:16px;",
      "}",

      /* complete section */
      "#sgami-char { font-size:64px;animation:sgami-celebrate .6s cubic-bezier(.22,1,.36,1) both;margin:4px 0 12px; }",
      ".sgami-carta {",
      "  border-radius:14px;padding:14px;margin-bottom:16px;",
      "  background:SGAMI_BG;",
      "}",
      ".sgami-carta-emoji { font-size:36px;margin-bottom:6px; }",
      ".sgami-carta-name { font-size:15px;font-weight:700;color:#1e1b4b;margin-bottom:8px; }",
      ".sgami-badge { display:inline-block;padding:3px 12px;border-radius:99px;font-size:12px;font-weight:700; }",
      ".sgami-badge-comum  { background:#e5e7eb;color:#4b5563; }",
      ".sgami-badge-rara   { background:#dbeafe;color:#1d4ed8; }",
      ".sgami-badge-epica  { background:#ede9fe;color:#6d28d9; }",
      ".sgami-badge-lendaria { background:linear-gradient(90deg,#f59e0b,#fbbf24);color:#78350f; }",

      /* button */
      "#sgami-continue {",
      "  background:linear-gradient(135deg,SGAMI_PRIMARY,SGAMI_LIGHT);",
      "  color:#fff;border:none;border-radius:50px;",
      "  padding:12px 28px;font-size:15px;font-weight:800;",
      "  cursor:pointer;width:100%;",
      "  box-shadow:0 6px 18px rgba(SGAMI_GLOW,.35);",
      "  font-family:'Baloo 2',sans-serif;",
      "  transition:transform .15s,box-shadow .15s;",
      "}",
      "#sgami-continue:hover { transform:translateY(-1px);box-shadow:0 8px 22px rgba(SGAMI_GLOW,.45); }",
    ]
      .join("\n")
      .replace(/SGAMI_PRIMARY/g, primaryColor)
      .replace(/SGAMI_LIGHT/g, lightColor)
      .replace(/SGAMI_BG/g, bgColor);

    var st = document.createElement("style");
    st.id = "sgami-styles";
    st.textContent = css;
    document.head.appendChild(st);
  }

  /* ------------------------------------------------------------------ */
  /* Raridade                                                             */
  /* ------------------------------------------------------------------ */
  async function calcRarity(supa, uid, themeSlug) {
    var res = await supa
      .from("activity_log")
      .select("score,is_first_attempt")
      .eq("user_id", uid)
      .eq("theme_slug", themeSlug)
      .not("score", "is", null);

    var rows = (res.data || []);
    if (!rows.length) return "comum";

    var allPerfect = rows.every(function (r) {
      return r.is_first_attempt === true && r.score === 100;
    });
    if (allPerfect) return "lendaria";

    var avg = rows.reduce(function (acc, r) { return acc + r.score; }, 0) / rows.length;
    if (avg >= 90) return "epica";
    if (avg >= 70) return "rara";
    return "comum";
  }

  /* ------------------------------------------------------------------ */
  /* Peças já coletadas                                                   */
  /* ------------------------------------------------------------------ */
  async function fetchCollected(supa, uid, themeSlug) {
    var res = await supa
      .from("pieces")
      .select("piece_number")
      .eq("user_id", uid)
      .eq("theme_slug", themeSlug);
    return (res.data || []).map(function (r) { return r.piece_number; });
  }

  /* ------------------------------------------------------------------ */
  /* Salvar peça                                                           */
  /* ------------------------------------------------------------------ */
  async function savePiece(supa, uid, themeSlug, pieceId) {
    await supa.from("pieces").insert({
      user_id: uid,
      theme_slug: themeSlug,
      piece_number: pieceId,
    });
  }

  /* ------------------------------------------------------------------ */
  /* Salvar carta                                                          */
  /* ------------------------------------------------------------------ */
  async function saveCard(supa, uid, themeSlug, discipline, rarity) {
    await supa.from("cards").upsert(
      {
        user_id: uid,
        theme_slug: themeSlug,
        discipline: discipline,
        rarity: rarity,
      },
      { onConflict: "user_id,theme_slug" }
    );
  }

  /* ------------------------------------------------------------------ */
  /* Modal                                                                */
  /* ------------------------------------------------------------------ */
  function buildModal(opts) {
    // opts: { pieces, collectedBefore, newPieceId, isComplete, isDuplicate,
    //         rarity, config }
    var cfg = opts.config;
    var totalPieces = cfg.pieces.length; // 4

    var newCount = opts.isDuplicate
      ? opts.collectedBefore.length
      : opts.collectedBefore.length + 1;

    /* slots HTML */
    var slotsHtml = cfg.pieces
      .map(function (p) {
        var isNew = !opts.isDuplicate && p.id === opts.newPieceId;
        var wasCollected = opts.collectedBefore.indexOf(p.id) !== -1;
        var cls = isNew
          ? "sgami-slot sgami-slot-new"
          : wasCollected
          ? "sgami-slot sgami-slot-collected"
          : "sgami-slot sgami-slot-empty";
        var inner = isNew || wasCollected
          ? p.emoji
          : '<span class="sgami-slot-empty-inner">❓</span>';
        return '<div class="' + cls + '">' + inner + "</div>";
      })
      .join("");

    /* progress bar */
    var barPct = Math.round((newCount / totalPieces) * 100) + "%";

    /* duplicate warning */
    var dupHtml = opts.isDuplicate
      ? '<div class="sgami-dup-warn">🔮 Fragmento! +1 salvo para evoluir sua carta</div>'
      : "";

    /* complete section */
    var completeHtml = "";
    if (opts.isComplete) {
      var badgeClass = "sgami-badge sgami-badge-" + opts.rarity;
      var rarityLabel = {
        comum: "Comum",
        rara: "Rara",
        epica: "Épica",
        lendaria: "Lendária ✨",
      }[opts.rarity] || opts.rarity;

      completeHtml = [
        '<div id="sgami-char">' + cfg.characterEmoji + "</div>",
        '<div class="sgami-carta">',
        '  <div class="sgami-carta-emoji">' + cfg.characterEmoji + "</div>",
        '  <div class="sgami-carta-name">Carta: ' + cfg.characterName + "</div>",
        '  <span class="' + badgeClass + '">' + rarityLabel + "</span>",
        "</div>",
      ].join("\n");
    }

    /* title / subtitle */
    var title, subtitle;
    if (opts.isDuplicate) {
      title = "Peça repetida!";
      subtitle = "Você já completou o set de " + cfg.characterName + ".";
    } else if (opts.isComplete) {
      title = "Set completo! 🎉";
      subtitle = "Você montou o personagem " + cfg.characterName + "!";
    } else {
      var newPiece = cfg.pieces.find(function (p) { return p.id === opts.newPieceId; });
      title = (newPiece ? newPiece.emoji + " " + newPiece.name : "Nova peça") + " desbloqueada!";
      subtitle = newCount + " de " + totalPieces + " peças coletadas.";
    }

    var html = [
      '<div id="sgami-card">',
      '  <div id="sgami-title">' + title + "</div>",
      '  <div id="sgami-subtitle">' + subtitle + "</div>",
      dupHtml,
      completeHtml,
      '  <div class="sgami-slots">' + slotsHtml + "</div>",
      '  <div class="sgami-bar-wrap">',
      '    <div class="sgami-bar-fill" style="--sgami-bar-w:' + barPct + '"></div>',
      "  </div>",
      '  <div class="sgami-bar-label">' + newCount + " / " + totalPieces + " peças</div>",
      '  <button id="sgami-continue">Continuar →</button>',
      "</div>",
    ].join("\n");

    return html;
  }

  function showOverlay(html, backUrl) {
    return new Promise(function (resolve) {
      var overlay = document.createElement("div");
      overlay.id = "sgami-overlay";
      overlay.innerHTML = html;
      document.body.appendChild(overlay);

      overlay.querySelector("#sgami-continue").addEventListener("click", function () {
        overlay.style.animation = "sgami-fadein .25s ease reverse forwards";
        setTimeout(function () {
          overlay.remove();
          resolve();
          if (backUrl) {
            window.location.href = backUrl;
          }
        }, 250);
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* run()                                                                */
  /* ------------------------------------------------------------------ */
  async function run(supa, uid, themeSlug, discipline, config) {
    // Inject styles with theme colors
    var glowRgb = config.glowRgb || "124,58,237";
    injectStyles(config.primaryColor, config.lightColor, config.bgColor);

    // Also patch glow color into already-injected style (replace placeholder)
    var styleEl = document.getElementById("sgami-styles");
    if (styleEl) {
      styleEl.textContent = styleEl.textContent.replace(/SGAMI_GLOW/g, glowRgb);
    }

    // 1. Fetch already-collected pieces
    var collectedBefore = await fetchCollected(supa, uid, themeSlug);
    var allPieceIds = config.pieces.map(function (p) { return p.id; });
    var available = allPieceIds.filter(function (id) {
      return collectedBefore.indexOf(id) === -1;
    });

    var isDuplicate = available.length === 0;
    var isComplete = false;
    var newPieceId = null;
    var rarity = null;

    if (isDuplicate) {
      // All pieces already collected — nothing to save, just show duplicate modal
    } else {
      // Pick random piece from available (gacha with pity: all remaining equally likely)
      newPieceId = available[Math.floor(Math.random() * available.length)];

      // Save piece
      await savePiece(supa, uid, themeSlug, newPieceId);

      // Check if set is now complete
      isComplete = available.length === 1; // was the last one

      if (isComplete) {
        rarity = await calcRarity(supa, uid, themeSlug);
        await saveCard(supa, uid, themeSlug, discipline, rarity);
      }
    }

    // 2. Build and show modal
    var html = buildModal({
      collectedBefore: collectedBefore,
      newPieceId: newPieceId,
      isComplete: isComplete,
      isDuplicate: isDuplicate,
      rarity: rarity,
      config: config,
    });

    await showOverlay(html, config.backUrl);
  }

  /* ------------------------------------------------------------------ */
  /* Export                                                               */
  /* ------------------------------------------------------------------ */
  window.SabendoGamification = { run: run };
})();
