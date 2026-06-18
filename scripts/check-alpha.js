const sharp = require('../node_modules/sharp');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const paths = [
  path.join(ROOT, '..', 'Personagens', '5o ano', 'Prepo.png'),
  path.join(ROOT, '_landing', 'prepo-hd.png'),
  path.join(ROOT, '_landing', 'prepo-stage.png')
];
(async () => {
  for (const p of paths) {
    try {
      const m = await sharp(p).metadata();
      console.log(path.basename(p), '→ channels=' + m.channels, 'hasAlpha=' + m.hasAlpha);
    } catch(e) { console.log(path.basename(p), '→ ERRO:', e.message.slice(0,60)); }
  }
})();
