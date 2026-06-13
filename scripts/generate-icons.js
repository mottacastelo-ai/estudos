// Gera icon-192.png, icon-512.png e icon-maskable-512.png
// Base: Personagens/5o ano/Prepo.png (PNG com canal alpha — fundo transparente)
// Layout: fundo preto #0D0D0D | Prepo centralizado | "sabendo." abaixo (Syne 800)

const path  = require('path');
const fs    = require('fs');
const sharp = require(path.join(__dirname, '../node_modules/sharp'));

const ROOT  = path.join(__dirname, '..');
const PREPO = path.join(ROOT, '..', 'Personagens', '5o ano', 'Prepo.png');
const FONT  = path.join(__dirname, 'syne-800.ttf');
const OUT   = path.join(ROOT, 'icons');

const BG    = { r: 13,  g: 13,  b: 13,  alpha: 1 };   // #0D0D0D
const FONT_PATH = FONT.replace(/\\/g, '/');

// ── SVG de texto "sabendo." ───────────────────────────
function textSvg(width, fontSize, y) {
  const kern = -Math.round(fontSize * 0.02);
  return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${Math.round(fontSize * 1.3)}">
  <defs><style>
    @font-face { font-family: Syne; src: url("file:///${FONT_PATH}"); font-weight: 800; }
  </style></defs>
  <text x="${width / 2}" y="${Math.round(fontSize * 1.05)}"
    font-family="Syne, sans-serif" font-weight="800" font-size="${fontSize}"
    text-anchor="middle" letter-spacing="${kern}">
    <tspan fill="#FFFFFF">sabendo</tspan><tspan fill="#00C896">.</tspan>
  </text>
</svg>`);
}

// ── Gera um ícone ─────────────────────────────────────
// prepoFrac  : fração da altura ocupada pelo Prepo
// textFrac   : tamanho da fonte como fração do size
// padFrac    : padding top/lateral como fração do size
async function makeIcon(size, prepoFrac, textFrac, padFrac, outFile) {
  const pad      = Math.round(size * padFrac);
  const prepoSz  = Math.round(size * prepoFrac);
  const fontSize = Math.round(size * textFrac);

  // Prepo: remove área transparente ao redor antes de redimensionar
  const prepoBuf = await sharp(PREPO)
    .trim({ background: { r: 0, g: 0, b: 0, alpha: 0 }, threshold: 10 })
    .resize(prepoSz, prepoSz, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
    .png()
    .toBuffer();

  // Posição central horizontal do Prepo
  const prepoX = Math.round((size - prepoSz) / 2);
  const prepoY = pad;

  // Texto "sabendo."
  const textH   = Math.round(fontSize * 1.3);
  const textBuf = await sharp(textSvg(size, fontSize, 0)).png().toBuffer();
  const textY   = prepoY + prepoSz + Math.round(size * 0.02);

  // Monta o ícone
  await sharp({ create: { width: size, height: size, channels: 4, background: BG } })
    .composite([
      { input: prepoBuf, top: prepoY, left: prepoX },
      { input: textBuf,  top: textY,  left: 0 },
    ])
    .png()
    .toFile(outFile);

  console.log(`✓ ${path.basename(outFile)} (${size}×${size})`);
}

(async () => {
  // icon-192: Prepo 72%, fonte 15%, padding 3%
  await makeIcon(192, 0.72, 0.15, 0.03, path.join(OUT, 'icon-192.png'));

  // icon-512: Prepo 72%, fonte 15%, padding 3%
  await makeIcon(512, 0.72, 0.15, 0.03, path.join(OUT, 'icon-512.png'));

  // maskable-512: padding maior (12%) para safe zone — Prepo 60%
  await makeIcon(512, 0.60, 0.13, 0.12, path.join(OUT, 'icon-maskable-512.png'));

  console.log('Ícones gerados em icons/');
})();
