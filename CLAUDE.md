# Moderationsdeck

Web-App (PWA) für Moderationskarten auf dem iPad. Andrea nutzt sie als Web-App vom Home-Bildschirm: Moderationsmodus, Lernmodus, Packliste, offline.

## Zusammenarbeit

- Deutsch, per du, ohne Fachjargon.
- Erst Anforderungen und Optionen besprechen, dann bauen. Bei größeren Änderungen auf ihr ausdrückliches „ja“ oder „los“ warten. Kleine Wünsche („Schrift größer“) direkt umsetzen.
- Workshops erstellen oder ändern: Skill `moderationskarten` (.claude/skills/moderationskarten/SKILL.md).

## Aufbau

- `index.html`: die ganze App (CSS und JS inline). `sw.js`: Offline-Cache. `manifest.webmanifest` und Icons.
- Online über GitHub Pages: https://aerdnanedak.github.io/moderationsdecks/ (Repo `AerdnaNedak/moderationsdecks`, öffentlich). Ein `git push` auf `main` veröffentlicht.
- **Bei jeder App-Änderung** `CACHE` in `sw.js` und `VERSION` in `index.html` hochzählen, sonst bekommt das iPad die neue Fassung nicht sicher.
- Workshops liegen **nicht** im Repo, sondern privat in der Dropbox: `/00 AK Business/03 Eigene Vorträge/Moderationsdeck/workshops/*.md`. Die App liest und schreibt sie über die Dropbox-API (PKCE, App-Schlüssel in `index.html`, Code wird manuell eingefügt).
- `tools/pruefen.js <datei.md>`: prüft eine Workshop-Datei mit dem Leser der App.
- `prototyp/`: der erste Prototyp als einzelne HTML-Datei.

## Design

Farben von work-with-ease.com: Ich spreche = Lindgrün, TN aktiv = Violett, Achtung Falle = gedämpftes Pink, Pause = Grau. Schrift Space Grotesk. Hell und dunkel. Material wird nicht auf den Karten angezeigt, nur in der Packliste.

## Prüfen

Ansichten per Headless-Chrome in iPad-Größe (1180×820) fotografieren. Dazu die Seite lokal mit vorbereitetem `localStorage` öffnen (`md.pref`, `md.auth`, `md.store`) und `fetch` abfangen. Die echte Dropbox-Verbindung kann nur Andrea testen.

## Offen

- Offline bearbeiten (Änderungen merken und später speichern)
- Übungssammlung (zurückgestellt)
