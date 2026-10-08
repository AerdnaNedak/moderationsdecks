---
name: moderationskarten
description: Macht aus Andreas Workshop- oder Vortragskonzepten (Word, PDF, Notizen, Chat) Moderationskarten für die Moderationsdeck-App und legt sie als Markdown-Datei in ihren Dropbox-Ordner. Auch zum Ändern oder Ergänzen bestehender Workshops. Auslöser zum Beispiel "mach daraus Moderationskarten", "neuer Workshop", "wandle das Konzept um", "Karten für …", "ändere im Workshop …".
---

# Moderationskarten erstellen

Andrea moderiert Workshops mit der Moderationsdeck-App auf dem iPad (https://aerdnanedak.github.io/moderationsdecks/). Jeder Workshop ist eine Markdown-Datei in ihrer Dropbox. Die App liest sie von dort. Du schreibst diese Dateien.

**Zielordner:** `~/Library/CloudStorage/Dropbox/00 AK Business/03 Eigene Vorträge/Moderationsdeck/workshops/`

Sprich mit Andrea Deutsch, per du, ohne Fachjargon.

## Ablauf

1. **Quellen vollständig lesen.** Word: `textutil -convert txt -stdout "<datei>.docx"`. PDF: mit dem pdf-Skill. Gehören Vortrag oder Dramaturgie zum Workshop (z. B. ein Impuls am Anfang), lies sie mit.
2. **Unklares fragen, bevor du schreibst.** Erfinde keine Inhalte, Sätze, Übungen oder Zeiten, die nicht in den Quellen stehen. Erlaubt sind: kürzen auf Kernpunkte, Phasenzeiten schätzen, wenn nur Blockzeiten angegeben sind (die Schätzungen nennst du am Ende).
3. **Datei schreiben** nach dem Format unten. Dateiname: kurz, klein, mit Bindestrichen, ohne Umlaute, z. B. `merck-echt-sein.md`. Eine vorhandene Datei überschreibst du nie ungefragt.
4. **Prüfen:** `node tools/pruefen.js "<pfad zur datei>"` im Projektordner `~/Repositories/Moderationsdecks`. Das Programm nutzt den Leser der App. Behebe Fehler. Hinweise auf volle Karten und abweichende Blocksummen gibst du an Andrea weiter.
5. **Bericht an Andrea:** Anzahl Karten und Gesamtzeit (im Vergleich zur geplanten Zeit), geschätzte Zeiten, Karten, die auf dem iPad scrollen, offene Fragen. Zum Schluss: In der App auf „Aktualisieren“ tippen, dann ist der Workshop da.

**Bestehenden Workshop ändern:** Lies die Datei frisch ein, direkt vor dem Ändern. Andrea bearbeitet sie auch auf dem iPad. Ändere nur, was sie verlangt, und prüfe danach mit `tools/pruefen.js`.

## Format

```
# Titel des Workshops
Untertitel: Kunde · Format · Dauer · Teilnehmende

## Block 1 · Name des Blocks | 25 min
Ziel: Ziel des Blocks (steht klein auf jeder Karte des Blocks)

### Titel der Phase | 10 min | Ich spreche        (oder: TN aktiv, Pause)
> Satz, den Andrea wörtlich sagt
- Kernpunkt
1. Schritt der Anleitung
Rahmen: Satz an die Gruppe, der die Aktivität rahmt
! Falle: worauf Andrea achten muss
Notiz: Regie-Hinweis nur für Andrea
Material: was sie dafür braucht (erscheint in der Packliste)
```

- Hat der Workshop keine Blöcke, beginnt jede Karte mit `##`, und es gibt keine `###`.
- Eine Pause ist ein eigener Block mit einer einzigen Karte: `## Pause | 15 min`, darunter `### Pause | 15 min | Pause`.
- Mehrere `>`-Zeilen sind erlaubt. Bei Einstieg und Schluss eines Redeteils: `> Einstieg: „…“` und `> Schluss: „…“`.
- Schritte und Rahmen erscheinen in der Reihenfolge, in der sie in der Datei stehen.
- `**fett**` wird fett angezeigt, sonst kein Markdown in den Zeilen.

## Andreas Begriffe übersetzen

| In ihrem Konzept | Auf der Karte |
|---|---|
| Block mit Zeit und Fokus | `## Block N · Name \| X min` mit `Ziel:` |
| ZIEL | `Ziel:` beim Block |
| DEINE WORTE | `>` Satz, wörtlich übernommen |
| RAHMEN FÜR DIE GRUPPE | `Rahmen:` auf der TN-aktiv-Karte, zu der er gehört |
| ÜBUNG, Einzelarbeit, Partnerarbeit, Gruppen, Runden, Ritual | eigene Karte, `TN aktiv` |
| Einleitung, Ansage, Übergang, Abschlussworte, Plenum moderieren | eigene Karte, `Ich spreche` |
| Ablaufschritte | `1.` `2.` … |
| FALLE (nur für dich) | `!` auf der Karte, auf der die Falle passiert |
| Regie, Tempo, Pausen aus einer Dramaturgie | `Notiz:` |
| Flipchart-Sätze, Beispielsätze, Schlagworte | `-` Kernpunkte |
| Karten, Flipchart vorbereitet, Timer, Handouts | `Material:` |

## Regeln für gute Karten

- **Eine Karte pro Phase.** Jede Karte ist eindeutig „Ich spreche“, „TN aktiv“ oder „Pause“. Wechselt das innerhalb eines Blocks, wird es eine neue Karte.
- **Die Phasenzeiten ergeben zusammen die Blockzeit.** Wenn nicht, sag es.
- **Wörtliche Sätze bleiben wörtlich.** Erklärender Text wird zu kurzen Kernpunkten, höchstens etwa fünf pro Karte.
- **Vorträge und Impulse:** eine Karte pro Szene oder Abschnitt, mit `> Einstieg:` und `> Schluss:`, drei bis fünf Kernpunkten zum Inhalt und den Hinweisen zu Tempo und Pausen als `Notiz:`.
- **Wiederkehrende Rituale** (z. B. „Boden – Atem – Weite“): Einmal ausführlich als eigene Karte, wenn es eingeführt wird. Danach als Schritt `Vorher: … (30 Sek)` in der Anleitung der folgenden Übung.
- **Eine Karte soll ohne Scrollen auf das iPad passen** (Querformat). Meldet `tools/pruefen.js` „sehr voll“, frag Andrea, ob sie kürzen möchte.
- **Persönliches** aus Vorträgen gehört nur in diese private Datei, nie ins öffentliche Repository.

Ein vollständiges Beispiel ist `merck-echt-sein.md` im Zielordner.
