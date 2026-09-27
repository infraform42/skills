---
name: improve-codebase-architecture
description: Scannt eine Codebasis nach Vertiefungsmöglichkeiten, präsentiert sie als visuellen HTML-Report und grillt anschließend die ausgewählte Option durch.
disable-model-invocation: true
---

# Codebasis-Architektur verbessern

Decke architektonische Reibungspunkte auf und schlage **Vertiefungsmöglichkeiten** vor: Refaktorierungen, die flache Module in tiefe Module verwandeln. Das Ziel ist Testbarkeit und KI-Navigierbarkeit.

Dieser Befehl _stützt sich_ auf das Domänenmodell des Projekts und baut auf einem gemeinsamen Design-Vokabular auf:

- Rufe das Skill-Tool mit "codebase-design" auf, um das Architektur-Vokabular zu erhalten (**Modul**, **Schnittstelle**, **Tiefe**, **Nahtstelle (Seam)**, **Adapter**, **Hebelwirkung**, **Lokalität**) sowie dessen Prinzipien (deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Verwende diese Begriffe in jedem Vorschlag exakt so und weiche nicht auf „component", „service", „API" oder „boundary" aus.
- Die Domänensprache in `CONTEXT.md` gibt guten Nahtstellen (Seams) Namen; ADRs in `docs/adr/` halten Entscheidungen fest, die dieser Befehl nicht neu aufrollen sollte.

## Prozess

### 1. Erkunden

**Grenze den Umfang ein, bevor du scannst: YAGNI.** Ein Modul zu vertiefen zahlt sich aus, indem zukünftige Änderungen daran leichter werden – lege daher besonderes Gewicht auf die Teile der Codebasis, die sich kürzlich geändert haben. Entscheide, *wo* du nachsiehst, bevor du nachsiehst:

- Hat der Nutzer eine Richtung vorgegeben (ein Modul, ein Subsystem, einen Schmerzpunkt), nimm diese und überspringe die folgende Ableitung.
- Andernfalls gehe einen guten Abschnitt der Commit-Historie zurück (`git log --oneline`), um die Hot Spots der Codebasis zu finden – die Dateien und Bereiche, die immer wieder auftauchen –, und lass diese Pfade zuerst deine Aufmerksamkeit auf sich ziehen. Sind die Änderungen verstreut ohne klaren Hot Spot, ziehe den Kreis weiter.

Lies zuerst das Domänenglossar des Projekts (`CONTEXT.md`) sowie alle ADRs im Bereich, den du bearbeitest.

Starte anschließend einen Subagenten, der die Codebasis durchgeht. Folge dabei keinen starren Heuristiken; erkunde organisch und notiere, wo du auf Reibung stößt:

- Wo erfordert das Verständnis eines Konzepts, zwischen vielen kleinen Modulen hin- und herzuspringen?
- Wo sind Module **flach**, mit einer Schnittstelle, die fast so komplex ist wie die Implementierung?
- Wo wurden reine Funktionen nur zur Testbarkeit extrahiert, während sich die eigentlichen Bugs darin verstecken, wie sie aufgerufen werden (keine **Lokalität**)?
- Wo lecken eng gekoppelte Module über ihre Nahtstellen (Seams) hinweg?
- Welche Teile der Codebasis sind ungetestet oder schwer über ihre aktuelle Schnittstelle zu testen?

Wende den **deletion test** auf alles an, das du für flach hältst: Würde das Löschen die Komplexität konzentrieren oder sie nur verschieben? Ein „Ja, konzentriert" ist das Signal, das du suchst.

### 2. Kandidaten als HTML-Report präsentieren

Schreibe eine in sich geschlossene HTML-Datei in das temporäre Verzeichnis des Betriebssystems, damit nichts im Repo landet. Ermittle das temporäre Verzeichnis aus `$TMPDIR`, mit `/tmp` als Fallback (bzw. `%TEMP%` unter Windows), und schreibe nach `<tmpdir>/architecture-review-<timestamp>.html`, sodass jeder Durchlauf eine frische Datei erhält. Öffne sie für den Nutzer (`xdg-open <path>` unter Linux, `open <path>` unter macOS, `start <path>` unter Windows) und teile ihm den absoluten Pfad mit.

Der Report nutzt **Tailwind via CDN** für Layout und Styling sowie **Mermaid via CDN** für Diagramme, wo ein Graph/Flow/Sequence-Diagramm die Struktur zuverlässig vermittelt. Mische Mermaid mit handgefertigten CSS/SVG-Visualisierungen: Nutze Mermaid, wenn Beziehungen graphförmig sind (Call-Graphen, Abhängigkeiten, Sequenzen), und selbstgebaute Divs/SVGs, wenn du etwas Redaktionelleres willst (Massendiagramme, Querschnitte, Collapse-Animationen). Jeder Kandidat bekommt eine **Vorher/Nachher-Visualisierung**. Sei visuell.

Rendere für jeden Kandidaten eine Karte mit:

- **Dateien**: welche Dateien/Module betroffen sind
- **Problem**: warum die aktuelle Architektur Reibung verursacht
- **Lösung**: eine leicht verständliche Beschreibung dessen, was sich ändern würde
- **Vorteile**: erklärt anhand von Lokalität und Hebelwirkung sowie danach, wie sich die Tests verbessern würden
- **Vorher-/Nachher-Diagramm**: nebeneinander, selbst gezeichnet, das die Flachheit und die Vertiefung veranschaulicht
- **Empfehlungsstärke**: eine von `Strong`, `Worth exploring`, `Speculative`, dargestellt als Badge

Schließe den Report mit einem Abschnitt **Top recommendation** ab: welchen Kandidaten du zuerst angehen würdest und warum.

**Verwende das CONTEXT.md-Vokabular für die Domäne und das `/codebase-design`-Vokabular für die Architektur.** Wenn `CONTEXT.md` "Order" definiert, sprich von "the Order intake module", nicht von "the FooBarHandler" und nicht von "the Order service."

**ADR-Konflikte**: Widerspricht ein Kandidat einem bestehenden ADR, zeige ihn nur, wenn die Reibung real genug ist, um ein Neuaufrollen des ADR zu rechtfertigen. Markiere das deutlich in der Karte (z. B. als Warnhinweis: _„widerspricht ADR-0007, aber es lohnt sich, das noch einmal zu öffnen, weil …"_). Liste nicht jedes theoretische Refactoring auf, das ein ADR verbietet.

Weitere Details zum vollständigen HTML-Gerüst, den Diagramm-Mustern und den Styling-Hinweisen findest du in [HTML-REPORT.md](HTML-REPORT.md).

Schlage noch KEINE Schnittstellen vor. Frage den Nutzer, nachdem die Datei geschrieben wurde: "Welchen davon möchtest du dir genauer ansehen?"

### 3. Grilling-Runde

Sobald der Nutzer einen Kandidaten ausgewählt hat, rufe das Skill-Tool mit "grilling" auf, um gemeinsam mit ihm den Entscheidungsbaum durchzugehen: Randbedingungen, Abhängigkeiten, die Form des vertieften Moduls, was hinter der Nahtstelle (Seam) liegt, welche Tests überleben.

Seiteneffekte passieren inline, sobald Entscheidungen sich herauskristallisieren; rufe das Skill-Tool mit "domain-modeling" auf, um das Domänenmodell dabei aktuell zu halten:

- **Benennst du ein vertieftes Modul nach einem Konzept, das nicht in `CONTEXT.md` steht?** Füge den Begriff zu `CONTEXT.md` hinzu. Erstelle die Datei bei Bedarf, falls sie noch nicht existiert.
- **Schärfst du während des Gesprächs einen unscharfen Begriff?** Aktualisiere `CONTEXT.md` direkt an Ort und Stelle.
- **Lehnt der Nutzer den Kandidaten aus einem tragfähigen Grund ab?** Biete ein ADR an, formuliert als: _„Soll ich das als ADR festhalten, damit zukünftige Architektur-Reviews das nicht erneut vorschlagen?"_ Biete das nur an, wenn der Grund für einen zukünftigen Erkunder tatsächlich nötig wäre, um denselben Vorschlag nicht zu wiederholen; überspringe flüchtige Gründe („gerade nicht der Mühe wert") und selbstverständliche.
- **Möchtest du alternative Schnittstellen für das vertiefte Modul erkunden?** Rufe das Skill-Tool mit "codebase-design" auf und nutze dessen design-it-twice-Muster mit parallelen Subagenten.
