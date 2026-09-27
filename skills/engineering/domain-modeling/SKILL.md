---
name: domain-modeling
description: Baut und schärft das Domänenmodell eines Projekts. Verwenden, wenn Codebase-Terminologie diskutiert wird, eine CONTEXT.md geschrieben oder bearbeitet wird, oder ein ADR festgehalten oder bearbeitet wird. „lass uns die Begriffe im Domänenmodell schärfen“, „schreib das in die CONTEXT.md“, „halt das als ADR fest“, „leg die Fachbegriffe für dieses Projekt fest“, „ist unser Glossar noch aktuell“
---

# Domänenmodellierung

Baue und schärfe das Domänenmodell des Projekts aktiv während des Designs. Das ist die *aktive* Disziplin: Begriffe hinterfragen, Edge-Case-Szenarien erfinden und Glossar sowie Entscheidungen genau in dem Moment festhalten, in dem sie sich herauskristallisieren. (Nur *lesend* in `CONTEXT.md` nach Vokabular zu suchen, ist nicht dieser Skill: Das ist eine Ein-Zeilen-Gewohnheit, die jeder Skill mitbringen kann. Dieser Skill ist für den Fall gedacht, dass du das Modell veränderst, nicht nur konsumierst.)

## Dateistruktur

Die meisten Repositories haben einen einzigen Kontext:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

Wenn im Root eine `CONTEXT-MAP.md` existiert, hat das Repo mehrere Kontexte. Die Map zeigt, wo sich jeder davon befindet:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Erstelle Dateien erst bei Bedarf: nur dann, wenn du etwas zu schreiben hast. Existiert noch keine `CONTEXT.md`, erstelle sie, sobald der erste Begriff geklärt ist. Existiert noch kein `docs/adr/`, erstelle es, sobald das erste ADR gebraucht wird.

## Während der Session

### Gegen das Glossar hinterfragen

Wenn der Nutzer einen Begriff verwendet, der der bestehenden Sprache in `CONTEXT.md` widerspricht, sprich das sofort an. „Dein Glossar definiert ‚Stornierung‘ als X, aber du scheinst Y zu meinen. Welches ist es?“

### Unscharfe Sprache schärfen

Wenn der Nutzer vage oder überladene Begriffe verwendet, schlage einen präzisen kanonischen Begriff vor. „Du sagst ‚Account‘: Meinst du den Customer oder den User? Das sind unterschiedliche Dinge.“

### Konkrete Szenarien diskutieren

Wenn Domänenbeziehungen diskutiert werden, teste sie mit konkreten Szenarien auf Herz und Nieren. Erfinde Szenarien, die Edge Cases ausloten und den Nutzer zwingen, die Grenzen zwischen Konzepten präzise zu benennen.

### Mit dem Code abgleichen

Wenn der Nutzer beschreibt, wie etwas funktioniert, prüfe, ob der Code das bestätigt. Findest du einen Widerspruch, sprich ihn an: „Dein Code storniert ganze Orders, aber du hast gerade gesagt, dass eine Teilstornierung möglich ist. Was stimmt?“

### CONTEXT.md direkt aktualisieren

Wenn ein Begriff geklärt ist, aktualisiere `CONTEXT.md` direkt an Ort und Stelle. Sammle das nicht für später: halte es fest, sobald es passiert. Nutze das Format aus [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` sollte vollständig frei von Implementierungsdetails sein. Behandle `CONTEXT.md` nicht als Spec, Notizzettel oder Ablage für Implementierungsentscheidungen. Sie ist ein Glossar und nichts anderes.

### ADRs sparsam anbieten

Biete nur dann an, ein ADR zu erstellen, wenn alle drei Bedingungen zutreffen:

1. **Schwer umkehrbar**: Die Kosten, es sich später anders zu überlegen, sind spürbar
2. **Ohne Kontext überraschend**: Ein künftiger Leser wird sich fragen „Warum haben sie das so gemacht?“
3. **Ergebnis eines echten Trade-offs**: Es gab echte Alternativen, und du hast dich aus konkreten Gründen für eine entschieden

Fehlt eines der drei, verzichte auf das ADR. Nutze das Format aus [ADR-FORMAT.md](./ADR-FORMAT.md).
