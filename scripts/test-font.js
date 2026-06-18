const sharp = require('../node_modules/sharp');
const path = require('path');
const fontPath = path.join(__dirname, 'syne-800.ttf').replace(/\\/g, '/');

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="120">
  <defs><style>
    @font-face { font-family: Syne; src: url("file:///${fontPath}"); font-weight: 800; }
  </style></defs>
  <rect width="400" height="120" fill="#0D0D0D"/>
  <text x="200" y="90" font-family="Syne, sans-serif" font-weight="800"
    font-size="72" text-anchor="middle" fill="white">sabendo<tspan fill="#00C896">.</tspan></text>
</svg>`;

sharp(Buffer.from(svg)).png().toFile(path.join(__dirname, 'test-font-result.png'))
  .then(() => console.log('ok'))
  .catch(e => console.error(e));
