#!/usr/bin/env node
// Prüft eine Workshop-Datei mit genau dem Leser der App (aus index.html) und zeigt die Karten.
// Aufruf: node tools/pruefen.js <workshop.md> [weitere.md ...]
'use strict';
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const js = html.match(/<script>\n([\s\S]*?)<\/script>/g).pop();
const start = js.indexOf('function artOf'), end = js.indexOf('/* ---------- Zustand');
if (start < 0 || end < 0) { console.error('Leser in index.html nicht gefunden.'); process.exit(2); }
const reader = new Function(js.slice(start, end) + '\nreturn { parse: parse };')();

let problems = 0;
for (const file of process.argv.slice(2)) {
  const d = reader.parse(fs.readFileSync(file, 'utf8'));
  const total = d.cards.reduce((a, c) => a + (c.minutes || 0), 0);
  console.log(`\n${path.basename(file)}\n  Titel: ${d.title || '(fehlt)'}\n  Untertitel: ${d.sub || '(keiner)'}\n  ${d.cards.length} Karten · ${total} min · Blöcke: ${d.blocks ? 'ja' : 'nein'}`);
  if (!d.title) { console.log('  ! Kein Titel (Zeile "# Titel")'); problems++; }
  let prev;
  d.cards.forEach((c, i) => {
    if (c.block !== prev) {
      const bm = d.cards.filter(x => x.block === c.block).reduce((a, x) => a + (x.minutes || 0), 0);
      const plan = c.block && c.block.minutes ? ` (geplant ${c.block.minutes})` : '';
      console.log(`  [${c.block ? c.block.title : 'ohne Block'}] ${bm} min${plan}${c.block && c.block.minutes && c.block.minutes !== bm ? '  ! Summe weicht ab' : ''}`);
      prev = c.block;
    }
    const parts = [];
    if (c.say.length) parts.push(`Satz ${c.say.length}`);
    if (c.points.length) parts.push(`Punkte ${c.points.length}`);
    if (c.steps.length) parts.push(`Anleitung ${c.steps.length}`);
    if (c.fallen.length) parts.push(`Falle ${c.fallen.length}`);
    if (c.note.length) parts.push('Notiz');
    if (c.material) parts.push('Material');
    const load = c.say.join(' ').length + c.points.join(' ').length + c.steps.map(s => s.t).join(' ').length + c.fallen.join(' ').length + c.note.join(' ').length;
    const warn = [];
    if (!c.minutes) warn.push('keine Dauer');
    if (!parts.length && c.art !== 'pause') warn.push('leer');
    if (load > 600) warn.push('sehr voll, scrollt auf dem iPad');
    console.log(`    ${String(i + 1).padStart(2)} ${c.art.padEnd(8)} ${String(c.minutes || '-').padStart(3)}  ${c.title}  · ${parts.join(', ')}${warn.length ? '  ! ' + warn.join(', ') : ''}`);
    problems += warn.filter(w => w !== 'sehr voll, scrollt auf dem iPad').length;
  });
}
process.exit(problems ? 1 : 0);
