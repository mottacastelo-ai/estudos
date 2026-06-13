// Simula aparência dos ícones em iOS e Android
// Gera também icons/apple-touch-icon.png (180×180, sem alpha — iOS não usa transparência)

const path  = require('path');
const sharp = require(path.join(__dirname, '../node_modules/sharp'));

const ROOT = path.join(__dirname, '..');
const OUT  = path.join(ROOT, 'icons');

// ── Máscara rounded-rect ─────────────────────────────
// iOS: corner radius ≈ 22.5% do size (squircle suave)
// Android: corner radius ≈ 12% do size (squircle menos arredondado)
function roundedMaskSvg(size, radiusPct) {
  const r = Math.round(size * radiusPct);
  return Buffer.from(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}">
      <rect width="${size}" height="${size}" rx="${r}" ry="${r}" fill="white"/>
    </svg>`
  );
}

// ── Aplica máscara + wallpaper e retorna buffer ───────
async function simulateIcon(iconPath, size, radiusPct, wallpaperColor) {
  const mask = await sharp(roundedMaskSvg(size, radiusPct)).png().toBuffer();

  // Ícone recortado com a máscara
  const masked = await sharp(iconPath)
    .resize(size, size)
    .composite([{ input: mask, blend: 'dest-in' }])
    .png()
    .toBuffer();

  // Wallpaper: gradiente simulando tela do celular
  const wallpaper = await sharp({
    create: { width: size, height: size, channels: 3, background: wallpaperColor }
  }).jpeg().toBuffer();

  return sharp(wallpaper)
    .composite([{ input: masked, blend: 'over' }])
    .png()
    .toBuffer();
}

// ── Card de simulação side-by-side ───────────────────
async function buildSimulation() {
  const iconSize = 180;
  const padding  = 32;
  const labelH   = 36;
  const cardW    = (iconSize + padding * 2) * 2 + padding;
  const cardH    = padding + iconSize + labelH + padding;
  const BG       = { r: 18, g: 18, b: 24, alpha: 1 };

  // iOS: corner radius 22.5%, wallpaper azul típico
  const iosIcon = await simulateIcon(
    path.join(OUT, 'icon-512.png'), iconSize, 0.225,
    { r: 40, g: 60, b: 120 }
  );

  // Android: usa maskable, corner radius 12% (squircle padrão)
  const androidIcon = await simulateIcon(
    path.join(OUT, 'icon-maskable-512.png'), iconSize, 0.22,
    { r: 30, g: 30, b: 40 }
  );

  // Labels como SVG
  const labelSvg = (text, w) => Buffer.from(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${labelH}">
      <text x="${w/2}" y="24" font-family="sans-serif" font-size="14"
        font-weight="600" fill="rgba(255,255,255,0.6)" text-anchor="middle">${text}</text>
    </svg>`
  );

  const iosLabel     = await sharp(labelSvg('iOS', iconSize + padding * 2)).png().toBuffer();
  const androidLabel = await sharp(labelSvg('Android', iconSize + padding * 2)).png().toBuffer();

  await sharp({ create: { width: cardW, height: cardH, channels: 4, background: BG } })
    .composite([
      // iOS
      { input: iosIcon,     top: padding,           left: padding },
      { input: iosLabel,    top: padding + iconSize, left: 0 },
      // Android
      { input: androidIcon, top: padding,            left: padding * 2 + iconSize + padding },
      { input: androidLabel,top: padding + iconSize, left: padding + iconSize + padding },
    ])
    .png()
    .toFile(path.join(ROOT, 'scripts', 'icon-simulation.png'));

  console.log('✓ scripts/icon-simulation.png');
}

// ── apple-touch-icon 180×180 (sem alpha, iOS preenche transparência com preto) ──
async function buildAppleTouchIcon() {
  await sharp(path.join(OUT, 'icon-512.png'))
    .resize(180, 180)
    .flatten({ background: { r: 13, g: 13, b: 13 } })  // alpha → #0D0D0D
    .png()
    .toFile(path.join(OUT, 'apple-touch-icon.png'));

  console.log('✓ icons/apple-touch-icon.png (180×180)');
}

(async () => {
  await buildAppleTouchIcon();
  await buildSimulation();
})();
