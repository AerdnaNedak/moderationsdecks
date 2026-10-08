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

Ohne Blöcke beginnt jede Karte mit `##` statt `###`.

## Farben

Ich spreche = Lindgrün · TN aktiv = Violett · Achtung Falle = Pink (Farben von work-with-ease.com), Schrift Space Grotesk.
