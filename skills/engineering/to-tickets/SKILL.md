---
name: to-tickets
description: Zerlegt einen Plan, eine Spec oder die aktuelle Konversation in eine Reihe von Tracer-Bullet-Tickets, wobei jedes seine blockierenden Kanten deklariert, und veröffentlicht sie im konfigurierten Tracker (Kanten als Text in je einer Datei pro Ticket lokal, oder native Blocking-Links auf einem echten Tracker).
disable-model-invocation: true
---

# To Tickets

Zerlege einen Plan, eine Spec oder eine Konversation in eine Reihe von **Tickets**: vertikale Tracer-Bullet-Slices, wobei jedes die Tickets deklariert, die es **blockieren**.

Der Issue-Tracker und das Vokabular des Triage-Labels sollten dir bereits bereitgestellt worden sein. Falls nicht, sag dem Nutzer, dass er `/setup-matt-pocock-skills` ausführen soll.

## Ablauf

### 1. Kontext sammeln

Arbeite mit dem, was bereits im Konversationskontext vorhanden ist. Wenn der Nutzer eine Referenz (einen Spec-Pfad, eine Issue-Nummer oder URL) als Argument übergibt, ruf sie ab und lies ihren vollständigen Inhalt sowie die Kommentare.

### 2. Codebase erkunden (optional)

Falls du die Codebase noch nicht erkundet hast, tu dies, um den aktuellen Stand des Codes zu verstehen. Ticket-Titel und -Beschreibungen sollten das Domänen-Glossar-Vokabular des Projekts verwenden und ADRs in dem Bereich respektieren, den du bearbeitest.

Suche nach Gelegenheiten, den Code zu prefaktorieren, um die Implementierung zu erleichtern. „Mach die Änderung leicht, dann mach die leichte Änderung.“

### 3. Vertikale Slices entwerfen

Zerlege die Arbeit in **Tracer-Bullet**-Tickets.

<vertical-slice-rules>

- Jedes Slice schneidet einen schmalen, aber VOLLSTÄNDIGEN Pfad durch jede Schicht (Schema, API, UI, Tests): vertikal, NICHT eine horizontale Scheibe einer einzelnen Schicht
- Ein abgeschlossenes Slice ist für sich allein demonstrierbar oder verifizierbar
- Jedes Slice ist so bemessen, dass es in ein einziges frisches Kontextfenster passt
- Jegliches Prefaktorieren sollte zuerst erledigt werden

</vertical-slice-rules>

Gib jedem Ticket seine **blockierenden Kanten**: die anderen Tickets, die abgeschlossen sein müssen, bevor es beginnen kann. Ein Ticket ohne Blocker kann sofort starten.

**Breite Refactors sind die Ausnahme von der vertikalen Slice-Bildung.** Ein **breiter Refactor** ist eine mechanische Änderung (eine Spalte umbenennen, ein gemeinsam genutztes Symbol umtypisieren), deren **Blast Radius** über die gesamte Codebase streut, sodass eine einzelne Bearbeitung Tausende von Aufrufstellen auf einmal bricht und kein vertikales Slice grün landen kann. Zwing das nicht in einen Tracer-Bullet; sequenziere es stattdessen als **Expand–Contract**. Zuerst Expand: füge die neue Form neben der alten hinzu, sodass nichts bricht. Dann migriere die Aufrufstellen in Batches, deren Größe sich nach dem Blast Radius richtet (pro Package, pro Verzeichnis), jeder Batch ein eigenes Ticket, blockiert vom Expand, wobei CI von Batch zu Batch grün bleibt, weil die alte Form weiterhin existiert. Schließlich Contract: lösche die alte Form, sobald kein Aufrufer mehr übrig ist, in einem Ticket, das von jedem Migrate-Batch blockiert wird. Wenn selbst die Batches nicht allein grün bleiben können, behalte die Sequenz bei, aber lass sie sich einen Integrationsbranch teilen, der alle ein abschließendes Integrate-and-Verify-Ticket blockiert; grün wird nur dort versprochen.

### 4. Den Nutzer befragen

Präsentiere die vorgeschlagene Aufteilung als nummerierte Liste. Zeige für jedes Ticket:

- **Titel**: kurzer beschreibender Name
- **Blockiert durch**: welche anderen Tickets (falls vorhanden) zuerst abgeschlossen sein müssen
- **Was es liefert**: das Ende-zu-Ende-Verhalten, das dieses Ticket funktionsfähig macht

Frag den Nutzer:

- Stimmt die Granularität? (zu grob / zu fein)
- Sind die blockierenden Kanten korrekt: hängt jedes Ticket nur von Tickets ab, die es tatsächlich gaten?
- Sollten Tickets zusammengeführt oder weiter aufgeteilt werden?

Iteriere, bis der Nutzer die Aufteilung freigibt.

### 5. Die Tickets im konfigurierten Tracker veröffentlichen

Veröffentliche die freigegebenen Tickets. **Wie** hängt davon ab, welchen Tracker `/setup-matt-pocock-skills` konfiguriert hat; die Tickets sind in beiden Fällen dieselben, nur die Form der blockierenden Kanten unterscheidet sich:

- **Lokale Dateien** → schreibe eine Datei pro Ticket unter `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, nummeriert ab `01` in Abhängigkeitsreihenfolge (Blocker zuerst). Das „Blockiert durch“ jeder Datei listet die Nummern/Titel auf, von denen sie abhängt. Verwende die untenstehende Vorlage pro Ticket-Datei: ein Ticket pro Datei, niemals eine einzige kombinierte Datei.
- **Ein echter Issue-Tracker (GitHub, Linear, …)** → veröffentliche ein Issue pro Ticket in Abhängigkeitsreihenfolge (Blocker zuerst), sodass die blockierenden Kanten jedes Tickets auf echte Identifikatoren verweisen können. Nutze die native Blocking-/Sub-Issue-Beziehung der Plattform, sofern vorhanden; andernfalls setze das „Blockiert durch“ jedes Tickets auf die blockierenden Issues. Wende das Triage-Label `ready-for-agent` an, sofern nicht anders angewiesen; die Tickets sind konstruktionsbedingt für Agenten greifbar.

Arbeite an der **Frontier** (die offene Front): jedes Ticket, dessen Blocker alle erledigt sind. Bei einer rein linearen Kette bedeutet das von oben nach unten.

Schließe oder verändere KEIN übergeordnetes Issue.

<local-ticket-template>

# <NN>: <Ticket-Titel>

**Was zu bauen ist:** das Ende-zu-Ende-Verhalten, das dieses Ticket funktionsfähig macht, aus Sicht des Nutzers, keine schichtweise Implementierungsliste.

**Blockiert durch:** die Nummern/Titel der Tickets, die dieses gaten, oder „Keine (kann sofort starten)“.

**Status:** ready-for-agent

- [ ] Abnahmekriterium 1
- [ ] Abnahmekriterium 2

</local-ticket-template>

<issue-template>

## Parent

Eine Referenz auf das übergeordnete Issue im Tracker (falls die Quelle ein bestehendes Issue war, andernfalls diesen Abschnitt weglassen).

## Was zu bauen ist

Das Ende-zu-Ende-Verhalten, das dieses Ticket funktionsfähig macht, aus Sicht des Nutzers, nicht schichtweise Implementierung.

## Abnahmekriterien

- [ ] Kriterium 1
- [ ] Kriterium 2

## Blockiert durch

- Eine Referenz auf jedes blockierende Ticket, oder „Keine (kann sofort starten)“.

</issue-template>

In beiden Formen vermeide konkrete Dateipfade oder Code-Snippets: sie veralten schnell. Ausnahme: Wenn ein Prototyp ein Snippet erzeugt hat, das eine Entscheidung präziser kodiert, als Prosa es könnte (Zustandsautomat, Reducer, Schema, Type-Shape), binde es inline ein und vermerke kurz, dass es von einem Prototyp stammt. Kürze auf die entscheidungsreichen Teile, nicht auf eine funktionierende Demo, nur die wichtigen Punkte.
