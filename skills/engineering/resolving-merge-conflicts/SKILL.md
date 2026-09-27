---
name: resolving-merge-conflicts
description: Löst einen laufenden git-Merge- oder Rebase-Konflikt auf. Verwenden, wenn ein bestehender git merge/rebase conflict aufgelöst werden muss, etwa bei „löse den Merge-Konflikt“, „hilf mir beim Rebase-Konflikt“, „der Merge hängt fest, löse die Konflikte auf“, „behebe die Konflikte im aktuellen Rebase“.
---

1. **Sieh dir den aktuellen Stand** des Merges/Rebases an. Prüfe die Git-Historie und die betroffenen Dateien.

2. **Finde die Primärquellen** für jeden Konflikt. Verstehe genau, warum jede Änderung vorgenommen wurde und was die ursprüngliche Absicht war. Lies die Commit-Messages, prüfe die PRs, prüfe die ursprünglichen Issues/Tickets.

3. **Löse jeden Hunk auf.** Erhalte nach Möglichkeit beide Absichten. Wo das nicht geht, wähle die Variante, die dem erklärten Ziel des Merges entspricht, und vermerke den Trade-off. Erfinde **kein** neues Verhalten. Löse immer auf; verwende niemals `--abort`.

4. Ermittle die **automatisierten Checks** des Projekts und führe sie aus, typischerweise Typecheck, dann Tests, dann Format. Behebe alles, was der Merge kaputt gemacht hat.

5. **Schließe den Merge/Rebase ab.** Stage alles und committe. Bei einem Rebase führe den Rebase-Prozess fort, bis alle Commits rebased sind.
