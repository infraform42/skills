---
name: handoff
description: Fasst die aktuelle Konversation in einem Übergabedokument zusammen, damit ein anderer Agent die Arbeit fortsetzen kann. Verwenden, wenn eine Session an einen neuen Agenten übergeben werden soll (handoff).
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Schreibe ein Übergabedokument, das die aktuelle Konversation zusammenfasst, damit ein neuer Agent die Arbeit fortsetzen kann. Speichere es im temporären Verzeichnis des Betriebssystems des Nutzers – nicht im aktuellen Workspace.

Nimm einen Abschnitt „suggested skills“ in das Dokument auf, der benennt, für welche Skills der nächste Agent das Skill-Tool aufrufen sollte.

Dupliziere keine Inhalte, die bereits in anderen Artefakten erfasst sind (Specs, Pläne, ADRs, Issues, Commits, Diffs). Verweise stattdessen per Pfad oder URL darauf.

Schwärze alle sensiblen Informationen, etwa API-Keys, Passwörter oder personenbezogene Daten.

Falls der Nutzer Argumente übergeben hat, behandle sie als Beschreibung dessen, worauf sich die nächste Session konzentrieren wird, und richte das Dokument entsprechend darauf aus.
