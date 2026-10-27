// Liest ein PDF genauso aus wie die App (Zeilen nach y-Position, Wortfuge nach Abstand).
// Aufruf: node tests/extract-pdf-text.mjs datei.pdf > datei.txt   (braucht: npm i pdfjs-dist)
import * as lib from 'pdfjs-dist/legacy/build/pdf.mjs';
import fs from 'fs';
const data = new Uint8Array(fs.readFileSync(process.argv[2]));
const doc = await lib.getDocument({ data }).promise;
let out = '';
for (let p = 1; p <= doc.numPages; p++) {
  const tc = await (await doc.getPage(p)).getTextContent(), rows = [];
  for (const it of tc.items) {
    if (!it.str || !it.str.trim()) continue;
    const y = it.transform[5], x = it.transform[4];
    let row = rows.find(r => Math.abs(r.y - y) < 3); if (!row) { row = { y, parts:[] }; rows.push(row); }
    row.parts.push({ x, s:it.str, w:it.width || 0, fs:Math.abs(it.transform[0]) || 10 });
  }
  rows.sort((a, b) => b.y - a.y);
  out += rows.map(r => { let t = '', end = null;
    for (const q of r.parts.sort((a, b) => a.x - b.x)) { if (end != null && q.x - end > q.fs * .18) t += ' '; t += q.s; end = q.x + q.w; }
    return t; }).join('\n') + '\n';
}
process.stdout.write(out);
