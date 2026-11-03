#!/usr/bin/env python3
"""Macht aus einer Workshop-Datei (.md) ein Word-Dokument im Stil von „Workshop 3.docx“.

Aufruf:  python3 tools/word.py <workshop.md> [ziel.docx]
Ohne Ziel landet die Word-Datei neben der .md-Datei.

Gelesen wird mit dem Leser der App (aus index.html, über node), damit Word und App
immer dasselbe zeigen.
"""
import json
import os
import re
import subprocess
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, '..', 'index.html')

DARK, TEXT, MUTED, BLUE, GREEN, RED = '111111', '444444', '777777', '1F4E79', '1F7A3C', 'B00020'
ART = {'sprechen': 'Ich spreche', 'aktiv': 'TN aktiv', 'pause': 'Pause'}

READ_JS = r"""
const fs = require('fs');
const js = fs.readFileSync(process.argv[1], 'utf8').match(/<script>\n([\s\S]*?)<\/script>/g).pop();
const R = new Function(js.slice(js.indexOf('function artOf'), js.indexOf('/* ---------- Zustand')) +
  '\nreturn { parse: parse, schedule: typeof schedule === "function" ? schedule : null };')();
const d = R.parse(fs.readFileSync(process.argv[2], 'utf8'));
const blocks = [];
d.cards.forEach(c => { if (c.block && blocks.indexOf(c.block) < 0) blocks.push(c.block); });
const out = {
  title: d.title, sub: d.sub, material: d.material || [], termin: d.termin || null, leit: d.leit || null,
  blocks: blocks.map(b => ({ title: b.title, minutes: b.minutes, goal: b.goal })),
  cards: d.cards.map(c => Object.assign({}, c, { block: c.block ? blocks.indexOf(c.block) : -1 })),
  sched: R.schedule ? R.schedule(d) : null,
};
process.stdout.write(JSON.stringify(out));
"""


def read(md):
    res = subprocess.run(['node', '-e', READ_JS, INDEX, md], capture_output=True, text=True)
    if res.returncode:
        sys.exit('Konnte die Workshop-Datei nicht lesen:\n' + res.stderr)
    return json.loads(res.stdout)


def hm(x):
    x = int(x + 0.5)  # wie in der App: halbe Minuten aufrunden
    return '%d:%02d' % ((x // 60) % 24, x % 60)


def mn(x):
    x = round(x * 10) / 10
    return str(int(x)) if x == int(x) else str(x).replace('.', ',')


def quoted(t):
    t = t.strip()
    return t if t[:1] in '„"“»' else '„' + t + '“'


class Doc:
    def __init__(self):
        self.d = Document()
        s = self.d.sections[0]
        s.page_width, s.page_height = Mm(210), Mm(297)
        s.left_margin = s.right_margin = Mm(22)
        s.top_margin = s.bottom_margin = Mm(20)
        st = self.d.styles['Normal']
        st.font.name = 'Calibri'
        st.font.size = Pt(11)
        st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')

    def p(self, before=0, after=4, indent=None, style=None):
        par = self.d.add_paragraph(style=style)
        f = par.paragraph_format
        f.space_before, f.space_after = Pt(before), Pt(after)
        if indent:
            f.left_indent = Pt(indent)
        return par

    @staticmethod
    def run(par, text, size=11, color=TEXT, bold=False, italic=False):
        # **fett** aus der Workshop-Datei als fett übernehmen
        for i, part in enumerate(re.split(r'\*\*([^*]+)\*\*', text)):
            if not part:
                continue
            r = par.add_run(part)
            r.font.size, r.font.bold, r.font.italic = Pt(size), bold or (i % 2 == 1), italic
            r.font.color.rgb = RGBColor.from_string(color)
        return par

    def h1(self, t):
        self.run(self.p(0, 2), t, 26, DARK, True)

    def h2(self, t):
        self.run(self.p(24, 6), t, 18, BLUE, True)

    def h3(self, t):
        self.run(self.p(12, 4), t, 13, TEXT, True)

    def label(self, lab, text, lcol=MUTED, tcol=TEXT, lsize=10, tsize=11, indent=17):
        par = self.p(5, 5, indent)
        self.run(par, lab + '  ', lsize, lcol, True)
        self.run(par, text, tsize, tcol)

    def text(self, t, color=TEXT, size=11, italic=False):
        self.run(self.p(2, 4), t, size, color, italic=italic)

    def bullet(self, t, color=DARK):
        self.run(self.p(0, 2, style='List Bullet'), t, 11, color)

    def table(self, head, rows):
        t = self.d.add_table(rows=1, cols=len(head))
        try:
            t.style = 'Light Grid Accent 1'
        except Exception:
            t.style = 'Table Grid'
        t.alignment = WD_TABLE_ALIGNMENT.LEFT
        for i, h in enumerate(head):
            c = t.rows[0].cells[i]
            c.text = ''
            self.run(c.paragraphs[0], h, 10, DARK, True)
        for r in rows:
            cells = t.add_row().cells
            for i, v in enumerate(r):
                cells[i].text = ''
                self.run(cells[i].paragraphs[0], v, 10, DARK)
        return t


def card(doc, c, sched_row):
    head = c['title'] + '  ·  ' + (mn(c['minutes']) + ' Min' if c['minutes'] else '–')
    if sched_row:
        head += '  ·  bis ' + hm(sched_row['to'])
    head += '  ·  ' + ART[c['art']]
    doc.h3(head)
    ends = []
    for s in c['say']:
        m = re.match(r'^(einstieg|schluss|frage)\s*:\s*(.*)$', s, re.I)
        if m and m.group(1).lower() == 'schluss':
            ends.append(m.group(2))
        elif m:
            doc.label('DEINE WORTE · ' + m.group(1).upper(), quoted(m.group(2)))
        else:
            doc.label('DEINE WORTE', quoted(s))
    for t in c['points']:
        doc.bullet(t)
    steps = [s for s in c['steps'] if not s['r']]
    if steps:
        par = doc.p(6, 2, 0)
        doc.run(par, 'ÜBUNG' if c['art'] == 'aktiv' else 'ABLAUF', 10, GREEN if c['art'] == 'aktiv' else MUTED, True)
    for s in c['steps']:
        if s['r']:
            doc.label('RAHMEN FÜR DIE GRUPPE', quoted(s['t']), BLUE)
        else:
            doc.bullet(s['t'])
    for t in ends:
        doc.label('DEINE WORTE · SCHLUSS', quoted(t))
    for n in c['note']:
        doc.text(n)
    if c.get('material'):
        doc.label('MATERIAL', c['material'], indent=0)
    for f in c['fallen']:
        doc.label('FALLE (nur für dich)', f, RED, RED, 9, 10, 17)


def build(md, out):
    w = read(md)
    cards, blocks, sc = w['cards'], w['blocks'], w['sched']
    doc = Doc()
    doc.h1(w['title'] or 'Workshop')
    if w['sub']:
        doc.run(doc.p(0, 6), w['sub'], 13, TEXT)

    # Übersicht
    doc.h2('Übersicht')
    if blocks:
        groups = [(b, [i for i, c in enumerate(cards) if c['block'] == k]) for k, b in enumerate(blocks)]
    else:
        groups = [({'title': c['title'], 'goal': c.get('goal', '')}, [i]) for i, c in enumerate(cards)]
    head = ['Block', 'Zeit'] + (['Uhrzeit'] if sc else []) + ['Ziel']
    rows = []
    for b, idx in groups:
        if not idx:
            continue
        m = sum(cards[i]['minutes'] or 0 for i in idx)
        row = [b['title'], mn(m) + ' Min']
        if sc:
            row.append(hm(sc['list'][idx[0]]['from']) + '–' + hm(sc['list'][idx[-1]]['to']))
        row.append(b.get('goal') or '')
        rows.append(row)
    doc.table(head, rows)
    total = sum(c['minutes'] or 0 for c in cards)
    info = 'Gesamtzeit ' + mn(total) + ' Min'
    if sc:
        info += ' · Termin ' + hm(sc['start']) + ('–' + hm(sc['end']) if sc['end'] is not None else '') + ' · Plan endet ' + hm(sc['planEnd'])
        if sc['diff'] is not None:
            info += (' · ' + mn(sc['diff'] + sc['gaps']) + ' Min Luft') if sc['diff'] >= 0 else (' · Plan ist ' + mn(-sc['diff']) + ' Min zu lang')
    doc.text(info + '.', MUTED)

    # Leitprinzip (nur im Word, nicht auf den Karten)
    if w.get('leit'):
        L = w['leit']
        doc.h2('Leitprinzip' + (': ' + L['title'] if L['title'] else ''))
        for t in L['text'][:1]:
            doc.text(t, DARK)
        for t in L['points']:
            doc.bullet(t)
        for t in L['text'][1:]:
            doc.text(t)

    # Blöcke und Karten
    cur = None
    for i, c in enumerate(cards):
        if blocks and c['block'] != cur:
            cur = c['block']
            b = blocks[cur]
            idx = [k for k, x in enumerate(cards) if x['block'] == cur]
            m = sum(cards[k]['minutes'] or 0 for k in idx)
            t = b['title'] + ' (' + mn(m) + ' Min)'
            if sc:
                t += '  ·  ' + hm(sc['list'][idx[0]]['from']) + '–' + hm(sc['list'][idx[-1]]['to'])
            doc.h2(t)
            if b.get('goal'):
                doc.label('ZIEL', b['goal'], indent=0)
            if len(idx) == 1 and cards[idx[0]]['title'] == b['title']:
                for n in c['note']:
                    doc.text(n)
                continue
        elif not blocks and i == 0:
            doc.h2('Ablauf')
        card(doc, c, sc['list'][i] if sc else None)

    # Packliste
    mats = list(w['material']) + [c['material'] + '  (' + c['title'] + ')' for c in cards if c.get('material')]
    if mats:
        doc.h2('Material')
        for t in mats:
            doc.bullet(t)

    # Legende
    doc.h2('Legende')
    doc.label('ÜBUNG', 'Was im Raum konkret getan wird.', GREEN, TEXT, indent=0)
    doc.label('DEINE WORTE', 'Satz, den du so (oder nah daran) wörtlich sagst.', indent=0)
    doc.label('RAHMEN FÜR DIE GRUPPE', 'Du nennst eine typische Falle liebevoll beim Namen – damit die Teilnehmerinnen den eigenen Reflex spüren können.', BLUE, indent=0)
    doc.label('FALLE (nur für dich)', 'Regie-Hinweis. Nicht an die Gruppe weitergeben.', RED, RED, 9, 10, 0)

    doc.d.save(out)
    return len(cards)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Aufruf: python3 tools/word.py <workshop.md> [ziel.docx]')
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + '.docx'
    n = build(src, dst)
    print('Word erstellt: %s (%d Karten)' % (dst, n))
