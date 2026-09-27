---
name: diagnosing-bugs
description: "Diagnose-Loop für schwierige Bugs und Performance-Regressionen. Wird verwendet, wenn der Nutzer „diagnose“ oder „debug this“ sagt oder meldet, dass etwas kaputt ist, einen Fehler wirft, fehlschlägt oder langsam ist. Typische Auslöser: „diagnostizier diesen Bug“, „debugge das für mich“, „warum funktioniert das nicht“, „das ist so langsam, finde raus warum“, „hilf mir den Fehler zu finden“."
---

# Bugs diagnostizieren

Eine Disziplin für schwierige Bugs. Überspringe Phasen nur mit expliziter Begründung.

Lies beim Erkunden der Codebasis `CONTEXT.md` (falls vorhanden), um ein klares mentales Modell der relevanten Module zu bekommen, und prüfe ADRs in dem Bereich, den du bearbeitest.

## Schwärzen

Dieser Skill lässt dich Befehle, Ausgaben und erfasste Artefakte anzeigen. **Schwärze zuerst jedes Secret**: schreibe `<REDACTED>` an dessen Stelle. Baue Loops gegen Umgebungsvariablen, damit das Credential in der Umgebung bleibt statt in dem, was du zeigst. Erfasste Artefakte enthalten Auth-Header: zitiere nur die Zeilen, die das relevante Signal tragen.

Wenn die geschwärzte Ausgabe nicht ausreicht, um den Bug zu diagnostizieren, sag das offen und frage den Nutzer.

## Phase 1: Feedback-Loop aufbauen

**Das ist der eigentliche Skill.** Alles andere ist mechanisch. Wenn du ein **enges** Pass/Fail-Signal für den Bug hast (eines, das bei _diesem_ Bug auf Rot geht), findest du die Ursache; Bisektion, Hypothesentests und Instrumentierung verbrauchen dieses Signal nur. Ohne ein solches Signal hilft dir auch stundenlanges Codelesen nicht.

Investiere hier unverhältnismäßig viel Aufwand. **Sei aggressiv. Sei kreativ. Gib nicht auf.**

### Möglichkeiten, einen Loop zu bauen, ungefähr in dieser Reihenfolge

1. **Fehlschlagender Test** an einer beliebigen Nahtstelle (Seam), die den Bug erreicht: unit, integration, e2e.
2. **Curl-/HTTP-Skript** gegen einen laufenden Dev-Server.
3. **CLI-Aufruf** mit einem Fixture-Input, der `stdout` gegen einen bekannt guten Snapshot diffed.
4. **Headless-Browser-Skript** (Playwright / Puppeteer), das die UI steuert und Assertions auf DOM/Console/Netzwerk macht.
5. **Einen erfassten Trace replayen.** Speichere einen echten Netzwerk-Request / Payload / Event-Log auf der Festplatte; spiele ihn isoliert durch den Code-Pfad ab.
6. **Wegwerf-Harness.** Starte eine minimale Teilmenge des Systems (ein Service, gemockte Abhängigkeiten), die den Bug-Codepfad mit einem einzelnen Funktionsaufruf durchläuft.
7. **Property-/Fuzz-Loop.** Wenn der Bug „manchmal falsche Ausgabe“ ist, führe 1000 zufällige Inputs aus und suche nach dem Fehlermuster.
8. **Bisektions-Harness.** Wenn der Bug zwischen zwei bekannten Zuständen (commit, Datensatz, Version) aufgetreten ist, automatisiere „bei Zustand X starten, prüfen, wiederholen“, sodass du `git bisect run` darauf anwenden kannst.
9. **Differenzieller Loop.** Führe denselben Input durch alte Version vs. neue Version (oder zwei Konfigurationen) und diffe die Ausgaben.
10. **HITL-Bash-Skript.** Letzter Ausweg. Wenn ein Mensch klicken muss, steuere _ihn_ mit `scripts/hitl-loop.template.sh`, damit der Loop trotzdem strukturiert bleibt. Die erfasste Ausgabe fließt zu dir zurück.

Baue den richtigen Feedback-Loop, und der Bug ist zu 90 % behoben.

### Den Loop verengen

Behandle den Loop wie ein Produkt. Sobald du _einen_ Loop hast, **verenge** ihn:

- Kann ich ihn schneller machen? (Setup cachen, unnötige Initialisierung überspringen, den Testumfang verengen.)
- Kann ich das Signal schärfer machen? (Auf das konkrete Symptom prüfen, nicht nur auf „ist nicht abgestürzt“.)
- Kann ich ihn deterministischer machen? (Zeit fixieren, RNG seeden, Dateisystem isolieren, Netzwerk einfrieren.)

Ein 30-Sekunden-Loop, der flakt, ist kaum besser als gar kein Loop; ein deterministischer 2-Sekunden-Loop ist eng und eine echte Superkraft beim Debuggen.

### Nicht-deterministische Bugs

Das Ziel ist nicht eine saubere Reproduktion, sondern eine **höhere Reproduktionsrate**. Lasse den Auslöser 100× durchlaufen, parallelisiere, füge Stress hinzu, verenge Timing-Fenster, injiziere Sleeps. Ein Bug mit 50 % Flake-Rate ist debugbar, einer mit 1 % nicht – also erhöhe die Rate, bis er debugbar ist.

### Wenn du wirklich keinen Loop bauen kannst

Halte an und sag das explizit. Liste auf, was du versucht hast. Bitte den Nutzer um: (a) Zugriff auf die Umgebung, in der der Bug reproduzierbar ist, (b) ein geschwärztes, erfasstes Artefakt (HAR-Datei, Log-Dump, Core-Dump, Bildschirmaufnahme mit Zeitstempeln), oder (c) die Erlaubnis, temporäre Produktions-Instrumentierung hinzuzufügen. Gehe **nicht** ohne Loop zur Hypothesenbildung über.

### Abschlusskriterium: ein enger Loop, der auf Rot geht

Phase 1 ist abgeschlossen, wenn der Loop **eng** und **rot-fähig** ist: Du kannst **einen Befehl** benennen (einen Skriptpfad, einen Testaufruf, ein curl), den du **bereits mindestens einmal ausgeführt** hast (zeige den Aufruf und seine Ausgabe, geschwärzt), und der:

- [ ] **Rot-fähig** ist: er durchläuft den tatsächlichen Bug-Codepfad und prüft **exakt das Symptom des Nutzers**, sodass er bei diesem Bug auf Rot und nach dem Fix auf Grün gehen kann. Nicht „läuft ohne Fehler“; er muss in der Lage sein, _genau diesen Bug zu fangen_.
- [ ] **Deterministisch** ist: gleiches Ergebnis bei jedem Lauf (bei flakigen Bugs: eine fixierte, hohe Reproduktionsrate, siehe oben).
- [ ] **Schnell** ist: Sekunden, nicht Minuten.
- [ ] **Agent-ausführbar** ist: du kannst ihn unbeaufsichtigt laufen lassen; ein Mensch kommt nur über `scripts/hitl-loop.template.sh` in den Loop.

Wenn du dich dabei ertappst, Code zu lesen, um eine Theorie zu bilden, bevor dieser Befehl existiert, **halte an: direkt zur Hypothese zu springen ist genau der Fehler, den dieser Skill verhindern soll.** Kein rot-fähiger Befehl, keine Phase 2.

## Phase 2: Reproduzieren + minimieren

Führe den Loop aus. Beobachte, wie er auf Rot geht, sobald der Bug auftritt.

Bestätige:

- [ ] Der Loop erzeugt den Fehlermodus, den der **Nutzer** beschrieben hat, nicht einen anderen, zufällig ähnlichen Fehler. Falscher Bug = falscher Fix.
- [ ] Der Fehler ist über mehrere Läufe hinweg reproduzierbar (oder bei nicht-deterministischen Bugs mit einer ausreichend hohen Rate reproduzierbar, um daran zu debuggen).
- [ ] Du hast das exakte Symptom erfasst (Fehlermeldung, falsche Ausgabe, langsames Timing), damit spätere Phasen verifizieren können, dass der Fix es tatsächlich behebt.

### Minimieren

Sobald er auf Rot steht, verkleinere die Reproduktion auf das **kleinste Szenario, das noch auf Rot geht**. Entferne Inputs, Aufrufer, Konfiguration, Daten und Schritte **einzeln nacheinander**, führe den Loop nach jedem Schnitt erneut aus und behalte nur das, was für den Fehler tragend ist.

Warum das den Aufwand wert ist: Eine minimale Reproduktion verkleinert den Hypothesenraum in Phase 3 (weniger bewegliche Teile, die verdächtig sein können) und wird in Phase 5 zum sauberen Regressionstest.

Fertig, wenn **jedes verbleibende Element tragend ist**: Entfernst du eines davon, geht der Loop auf Grün.

Mache erst weiter, wenn du reproduziert **und** minimiert hast.

## Phase 3: Hypothesen bilden

Erzeuge **3–5 priorisierte Hypothesen**, bevor du auch nur eine davon testest. Wenn du nur eine Hypothese bildest, verankerst du dich an der ersten plausiblen Idee.

Jede Hypothese muss **falsifizierbar** sein: formuliere die Vorhersage, die sie macht.

> Format: „Wenn <X> die Ursache ist, dann lässt <Änderung von Y> den Bug verschwinden / verschlimmert <Änderung von Z> ihn.“

Wenn du die Vorhersage nicht formulieren kannst, ist die Hypothese nur ein Gefühl: verwirf sie oder schärfe sie.

**Zeige die priorisierte Liste dem Nutzer, bevor du testest.** Er hat oft Fachwissen, das die Reihenfolge sofort ändert (z. B. „wir haben gerade eine Änderung an #3 deployt“), oder kennt Hypothesen, die er bereits ausgeschlossen hat. Ein günstiger Checkpoint mit großer Zeitersparnis. Blockiere aber nicht darauf; mache mit deiner eigenen Priorisierung weiter, wenn der Nutzer nicht erreichbar ist.

## Phase 4: Instrumentieren

Jede Messsonde muss auf eine konkrete Vorhersage aus Phase 3 einzahlen. **Ändere jeweils nur eine Variable.**

Werkzeugpräferenz:

1. **Debugger-/REPL-Inspektion**, wenn die Umgebung das unterstützt. Ein Breakpoint schlägt zehn Logs.
2. **Gezielte Logs** an den Grenzen, die zwischen den Hypothesen unterscheiden.
3. Niemals „alles loggen und greppen“.

**Versieh jedes Debug-Log** mit einem eindeutigen Präfix, z. B. `[DEBUG-a4f2]`. Das Aufräumen am Ende wird dadurch zu einem einzigen `grep`. Nicht getaggte Logs überleben; getaggte Logs sterben.

**Perf-Zweig.** Bei Performance-Regressionen sind Logs meist der falsche Ansatz. Stattdessen: eine Baseline-Messung etablieren (Timing-Harness, `performance.now()`, Profiler, Query-Plan) und dann bisektieren. Erst messen, dann fixen.

## Phase 5: Fix + Regressionstest

Schreibe den Regressionstest **vor dem Fix**, aber nur, wenn es dafür eine **passende Nahtstelle (Seam)** gibt.

Eine passende Nahtstelle ist eine, an der der Test das **reale Bug-Muster** so durchläuft, wie es an der Aufrufstelle auftritt. Wenn die einzige verfügbare Nahtstelle zu flach ist (Test mit einem einzelnen Aufrufer, obwohl der Bug mehrere Aufrufer braucht; Unit-Test, der die Kette, die den Bug ausgelöst hat, nicht nachbilden kann), erzeugt ein Regressionstest dort trügerische Sicherheit.

**Wenn keine passende Nahtstelle existiert, ist das selbst der Befund.** Halte das fest. Die Architektur der Codebasis verhindert, dass der Bug dauerhaft eingefangen werden kann. Markiere das für die nächste Phase.

Wenn eine passende Nahtstelle existiert:

1. Verwandle die minimierte Reproduktion in einen fehlschlagenden Test an dieser Nahtstelle.
2. Beobachte, wie er fehlschlägt.
3. Wende den Fix an.
4. Beobachte, wie er besteht.
5. Führe den Feedback-Loop aus Phase 1 erneut gegen das ursprüngliche (nicht minimierte) Szenario aus.

## Phase 6: Aufräumen

Erforderlich, bevor du den Bug als erledigt erklärst:

- [ ] Die ursprüngliche Reproduktion tritt nicht mehr auf (Phase-1-Loop erneut ausführen)
- [ ] Der Regressionstest besteht (oder das Fehlen einer Nahtstelle ist dokumentiert)
- [ ] Alle `[DEBUG-...]`-Instrumentierung entfernt (Präfix mit `grep` suchen)
- [ ] Wegwerf-Prototypen gelöscht (oder an einen klar markierten Debug-Ort verschoben)
- [ ] Die Hypothese, die sich als richtig erwiesen hat, ist in der commit-/PR-Nachricht festgehalten, damit der nächste Debugger daraus lernt
