// Gera icon-192.png, icon-512.png e icon-maskable-512.png
// Layout: fundo preto #0D0D0D | Prepo + "sabendo." centralizados verticalmente
// O conteúdo total é calculado para caber dentro do padding em todos os lados.

const path  = require('path');
const fs    = require('fs');
const sharp = require(path.join(__dirname, '../node_modules/sharp'));

const ROOT  = path.join(__dirname, '..');
const PREPO = path.join(ROOT, '..', 'Personagens', '5o ano', 'Prepo.png');
const FONT  = path.join(__dirname, 'syne-800.ttf');
const OUT   = path.join(ROOT, 'icons');

const BG        = { r: 13, g: 13, b: 13, alpha: 1 };  // #0D0D0D
const FONT_PATH = FONT.replace(/\\/g, '/');

// ── SVG de texto "sabendo." ───────────────────────────
function textSvg(width, fontSize) {
  const kern = -Math.round(fontSize * 0.02);
  const h    = Math.round(fontSize * 1.25);
  return Buffer.from(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${h}">
  <defs><style>
    @font-face { font-family: Syne; src: url("file:///${FONT_PATH}"); font-weight: 800; }
  </style></defs>
  <text x="${width / 2}" y="${Math.round(fontSize * 1.0)}"
    font-family="Syne, sans-serif" font-weight="800" font-size="${fontSize}"
    text-anchor="middle" letter-spacing="${kern}">
    <tspan fill="#FFFFFF">sabendo</tspan><tspan fill="#00C896">.</tspan>
  </text>
</svg>`
  );
}

// ── Gera um ícone com conteúdo centralizado ───────────
// pad        : pixels de padding em todos os lados (zona segura)
// prepoRatio : tamanho do Prepo como fração da área útil
// fontRatio  : tamanho da fonte como fração do size total
async function makeIcon(size, pad, prepoRatio, fontRatio, outFile) {
  const usable   = size - 2 * pad;           // área útil quadrada
  const prepoSz  = Math.round(usable * prepoRatio);
  const fontSize = Math.round(size * fontRatio);
  const gap      = Math.round(size * 0.02);
  const textH    = Math.round(fontSize * 1.25);

  // Altura total do conteúdo (Prepo + gap + texto)
  const contentH = prepoSz + gap + textH;
  // Offset vertical para centralizar o bloco dentro da área útil
  const vOffset  = Math.round((usable - contentH) / 2);

  const prepoY = pad + vOffset;
  const prepoX = Math.round((size - prepoSz) / 2);
  const textY  = prepoY + prepoSz + gap;

  // Prepo sem fundo, trimado
  const prepoBuf = await sharp(PREPO)
    .trim({ background: { r: 0, g: 0, b: 0, alpha: 0 }, threshold: 10 })
    .resize(prepoSz, prepoSz, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
    .png()
    .toBuffer();

  // Texto
  const textBuf = await sharp(textSvg(size, fontSize)).png().toBuffer();

  await sharp({ create: { width: size, height: size, channels: 4, background: BG } })
    .composite([
      { input: prepoBuf, top: prepoY, left: prepoX },
      { input: textBuf,  top: textY,  left: 0 },
    ])
    .png()
    .toFile(outFile);

  const bottom = textY + textH;
  console.log(`✓ ${path.basename(outFile)} (${size}×${size}) | prepoY=${prepoY} textY=${textY} bottom=${bottom} pad=${pad}`);
}

(async () => {
  // icon-192: pad=16px, Prepo 68% da área útil, fonte 14% do size
  await makeIcon(192, 16, 0.68, 0.14, path.join(OUT, 'icon-192.png'));

  // icon-512: pad=40px, Prepo 68% da área útil, fonte 14% do size
  await makeIcon(512, 40, 0.68, 0.14, path.join(OUT, 'icon-512.png'));

  // maskable-512: pad=72px (14% do size = safe zone circular), Prepo 65%
  await makeIcon(512, 72, 0.65, 0.12, path.join(OUT, 'icon-maskable-512.png'));

  console.log('Ícones gerados em icons/');
})();
