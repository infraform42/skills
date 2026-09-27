---
name: prototype
description: "Erstellt einen Wegwerf-Prototyp, um eine Design-Frage zu beantworten. Verwenden, wenn der Nutzer prüfen möchte, ob ein Zustandsmodell oder eine Logik sich richtig anfühlt, oder erkunden möchte, wie eine UI aussehen sollte. „bau mir einen Prototyp dafür“, „lass uns das kurz als Wegwerf-Prototyp durchspielen“, „check mal, ob das State-Modell so passt“, „wie könnte die UI dafür aussehen“"
---

# Prototyp

Ein Prototyp ist **Wegwerfcode, der eine Frage beantwortet**. Die Frage bestimmt die Form.

## Einen Zweig wählen

Ermittle, welche Frage beantwortet wird – anhand des Prompts des Nutzers, des umgebenden Codes, oder indem du nachfragst, falls der Nutzer erreichbar ist:

- **„Fühlt sich diese Logik / dieses Zustandsmodell richtig an?“** → [LOGIC.md](LOGIC.md). Baue eine einzelne, teilbare HTML-Datei (Buttons zum freien Ausprobieren plus tabbed geführte Walkthroughs), die die Zustandsmaschine durch Fälle treibt, die auf dem Papier schwer nachzuvollziehen sind, und die auch jemand ohne Entwicklerhintergrund bedienen kann.
- **„Wie sollte das aussehen?“** → [UI.md](UI.md). Erzeuge mehrere radikal unterschiedliche UI-Varianten auf einer einzigen Route, umschaltbar über einen URL-Suchparameter und eine schwebende Bottom-Bar.

Die beiden Zweige erzeugen sehr unterschiedliche Artefakte – triffst du hier die falsche Wahl, ist der ganze Prototyp hinfällig. Ist die Frage wirklich mehrdeutig und der Nutzer nicht erreichbar, wähle standardmäßig den Zweig, der besser zum umgebenden Code passt (ein Backend-Modul → Logik; eine Seite oder Komponente → UI), und notiere die Annahme oben im Prototyp.

## Regeln, die für beide gelten

1. **Von Anfang an Wegwerfcode – und klar als solcher gekennzeichnet.** Platziere den Prototyp-Code nah an der Stelle, wo er tatsächlich verwendet wird (neben dem Modul oder der Seite, für die er prototypisch entwickelt wird), damit der Kontext offensichtlich ist – benenne ihn aber so, dass ein flüchtiger Leser sofort erkennt: Prototyp, nicht Produktion. Für Wegwerf-UI-Routen halte dich an die Routing-Konvention, die im Projekt bereits existiert; erfinde keine neue Top-Level-Struktur.
2. **Trivial zu starten.** Ein UI-Prototyp startet mit einem einzigen Befehl im Task-Runner des Projekts: `pnpm <name>`, `python <path>`, `bun <path>` usw. Eine Logik-Demo ist eine einzelne HTML-Datei, die der Nutzer per Doppelklick öffnet. So oder so: kein Nachdenken nötig, um sie zu starten.
3. **Standardmäßig keine Persistenz.** Der Zustand lebt im Speicher. Persistenz ist das, was der Prototyp _überprüft_, nicht etwas, wovon er abhängen sollte. Geht es bei der Frage explizit um eine Datenbank, nutze eine Scratch-DB oder eine lokale Datei mit einem eindeutigen Namen wie "PROTOTYPE, wipe me".
4. **Verzichte auf Feinschliff.** Keine Tests, keine Fehlerbehandlung über das hinaus, was den Prototyp _lauffähig_ macht, keine Abstraktionen. Es geht darum, schnell etwas zu lernen.
5. **Mach den Zustand sichtbar.** Gib nach jeder Aktion (Logik) oder bei jedem Varianten-Wechsel (UI) den vollständigen relevanten Zustand aus, damit der Nutzer sieht, was sich geändert hat.
6. **Halte das Ergebnis fest, wenn du fertig bist.** Übertrage jede validierte Entscheidung in den echten Code, und halte den Prototyp selbst als **Primärquelle** fest: committe ihn auf einen Wegwerf-Branch außerhalb von main und hinterlasse im Implementierungs-Issue einen Kontext-Verweis auf diesen Branch. Halte auch die Antwort fest (das Ergebnis und die Frage, die damit geklärt wurde) im Issue oder in einem Commit. Der main-Branch behält nur die validierte Entscheidung.
