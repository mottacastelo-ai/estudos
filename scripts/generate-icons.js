// Gera icon-192.png, icon-512.png e icon-maskable-512.png
// Base: _landing/prepo-hd.png (Prepo em fundo branco)
// Resultado: ícones com fundo roxo #7C3AED, Prepo centralizado

const path = require('path');
const sharp = require(path.join(__dirname, '../node_modules/sharp'));

const ROOT = path.join(__dirname, '..');
const SRC  = path.join(ROOT, '_landing', 'prepo-hd.png');
const OUT  = path.join(ROOT, 'icons');

// Fundo roxo primário do sabendo.app
const BG = { r: 124, g: 58, b: 237, alpha: 1 };

async function makeIcon(size, prepoScale, outFile) {
  const prepoSize = Math.round(size * prepoScale);

  // Redimensiona o Prepo mantendo aspecto, remove fundo branco via flattenWhite
  const prepo = await sharp(SRC)
    .resize(prepoSize, prepoSize, { fit: 'contain', background: { r: 124, g: 58, b: 237, alpha: 1 } })
    .toBuffer();

  // Cria fundo roxo e compõe o Prepo no centro
  const offset = Math.round((size - prepoSize) / 2);
  await sharp({
    create: { width: size, height: size, channels: 4, background: BG }
  })
    .composite([{ input: prepo, top: offset, left: offset }])
    .png()
    .toFile(outFile);

  console.log(`✓ ${path.basename(outFile)} (${size}×${size}, Prepo ${Math.round(prepoScale*100)}%)`);
}

(async () => {
  // icon-192: Prepo ocupa 82% do ícone
  await makeIcon(192, 0.82, path.join(OUT, 'icon-192.png'));
  // icon-512: Prepo ocupa 82%
  await makeIcon(512, 0.82, path.join(OUT, 'icon-512.png'));
  // maskable-512: Prepo deve caber dentro do safe zone de 80% (raio 40% do centro)
  // → ocupa 70% para garantir espaço nas máscaras circulares
  await makeIcon(512, 0.68, path.join(OUT, 'icon-maskable-512.png'));

  console.log('Ícones gerados em icons/');
})();
