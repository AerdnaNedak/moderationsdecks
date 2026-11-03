# Moderationsdeck

Moderationskarten für Workshops und Vorträge auf dem iPad: Moderationsmodus, Lernmodus, offline nutzbar.

## Was wo liegt

| Ort | Inhalt |
|---|---|
| dieser Ordner (`~/Repositories/Moderationsdecks`) | die App, öffentlich über GitHub Pages |
| `prototyp/` | der erste Prototyp als einzelne HTML-Datei |
| `.claude/skills/moderationskarten/` | der Skill: macht aus Konzepten Workshop-Dateien |
| `tools/pruefen.js` | prüft eine Workshop-Datei: `node tools/pruefen.js <datei.md>` |
| Dropbox: `00 AK Business/03 Eigene Vorträge/Moderationsdeck/workshops/` | **die Workshops**, eine Markdown-Datei pro Workshop, privat |

Die Workshops liegen bewusst nicht hier. Die App liest sie direkt aus der Dropbox und speichert sie auf dem iPad für offline.

## Format einer Workshop-Datei

```
# Titel des Workshops
Untertitel: Anlass, Kunde, Datum
Termin: 9:30–13:00                             (optional, Uhrzeiten für diesen Termin)
Material: allgemeines Material (vor der ersten Karte, eine Zeile pro Eintrag)

## Block 1 · Name des Blocks | 25 min        (Blöcke sind freiwillig)
Ziel: steht klein auf jeder Karte des Blocks

### Kartentitel | 10 min | Ich spreche       (oder: TN aktiv, Pause)
> Satz, den ich wörtlich sage
- Kernpunkt
1. Schritt der Anleitung
Rahmen: Satz an die Gruppe, gehört zur Anleitung
! Achtung Falle: worauf ich achten muss
Notiz: nur für mich
Material: erscheint in der Packliste
```

Pause mit fester Uhrzeit: `### Pause | 15 min | Pause | 10:45`. Mit `Termin:` zeigt die App auf jeder Karte, bis wann sie fertig sein sollte (Plan bleibt fest; Luft und Überzug stehen auf der Workshop-Seite). In der App: „Termin festlegen“.

Ohne Blöcke beginnt jede Karte mit `##` statt `###`.

## Farben

Ich spreche = Lindgrün · TN aktiv = Violett · Achtung Falle = Pink (Farben von work-with-ease.com), Schrift Space Grotesk.
