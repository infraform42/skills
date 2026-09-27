---
name: code-review
description: "Überprüft die Änderungen seit einem festen Referenzpunkt (commit, branch, tag oder merge-base) entlang zweier Achsen: Standards (folgt der Code den in diesem Repo dokumentierten Coding-Standards?) und Spec (entspricht der Code dem, was das ursprüngliche Issue/die Spec verlangt hat?). Führt beide Reviews in parallelen Subagenten aus und stellt die Ergebnisse nebeneinander dar. Verwenden, wenn der Nutzer einen Branch, einen PR oder Work-in-Progress-Änderungen reviewen möchte, oder \"review since X\" verlangt. Typische Formulierungen: „review meine Änderungen seit main“, „check den PR gegen Standards und Spec“, „review diesen Branch seit dem letzten Merge-Base“, „prüf, ob mein Code zum Issue passt“."
---

Zweiachsiges Review des Diffs zwischen `HEAD` und einem vom Nutzer angegebenen Fixpunkt:

- **Standards**: Folgt der Code den in diesem Repo dokumentierten Coding-Standards?
- **Spec**: Setzt der Code das ursprüngliche Issue/die Spec originalgetreu um?

Beide Achsen laufen als **parallele Subagenten**, damit sie sich gegenseitig nicht den Kontext verschmutzen; anschließend aggregiert dieser Skill ihre Ergebnisse.

Der Issue-Tracker sollte dir bereits bereitgestellt worden sein. Fehlt `docs/agents/issue-tracker.md`, weise den Nutzer an, `/setup-matt-pocock-skills` auszuführen.

## Prozess

### 1. Fixpunkt festlegen

Nimm, was auch immer der Nutzer als Fixpunkt genannt hat (ein commit SHA, Branch-Name, Tag, `main`, `HEAD~5` usw.). Hat er keinen angegeben, frag danach.

Halte den Diff-Befehl einmal fest: `git diff <fixed-point>...HEAD` (drei Punkte, damit der Vergleich gegen die merge-base erfolgt). Notiere außerdem die Liste der Commits über `git log <fixed-point>..HEAD --oneline`.

Bevor du weitermachst, bestätige, dass sich der Fixpunkt auflösen lässt (`git rev-parse <fixed-point>`) und der Diff nicht leer ist. Eine ungültige Ref oder ein leerer Diff sollte hier scheitern, nicht erst in zwei parallelen Subagenten.

### 2. Spec-Quelle identifizieren

Suche in dieser Reihenfolge nach der ursprünglichen Spec:

1. Issue-Referenzen in den Commit-Messages (`#123`, `Closes #45`, GitLab `!67` usw.), abgerufen über den Workflow in `docs/agents/issue-tracker.md`.
2. Ein Pfad, den der Nutzer als Argument übergeben hat.
3. Eine Spec-Datei unter `docs/`, `specs/` oder `.scratch/`, die zum Branch-Namen oder Feature passt.
4. Wird nichts gefunden, frag den Nutzer, wo die Spec liegt. Sagt er, es gebe keine, überspringt der **Spec**-Subagent und meldet "no spec available".

### 3. Standards-Quellen identifizieren

Alles im Repo, das dokumentiert, wie Code geschrieben werden soll, etwa `CODING_STANDARDS.md` oder `CONTRIBUTING.md`.

Zusätzlich zu allem, was das Repo dokumentiert, trägt die Standards-Achse immer die folgende **Smell-Baseline**: eine feste Menge von Fowler-Code-Smells (_Refactoring_, Kap. 3), die auch dann gilt, wenn ein Repo nichts dokumentiert. Zwei Regeln binden sie:

- **Das Repo überstimmt.** Ein dokumentierter Repo-Standard gewinnt immer; billigt er etwas, das die Baseline anmerken würde, unterdrücke den Smell.
- **Immer eine Ermessensfrage.** Jeder Smell ist eine benannte Heuristik ("possible Feature Envy"), nie eine harte Verletzung. Wie bei jedem Standard hier: überspringe alles, was Tooling bereits erzwingt.

Jeder Smell liest sich als *was er ist* → *wie man ihn behebt*; gleiche ihn mit dem Diff ab:

- **Mysterious Name**: Eine Funktion, Variable oder ein Typ, deren Name nicht verrät, was sie tut oder enthält. → Benenne um; fällt kein ehrlicher Name ein, ist das Design unklar.
- **Duplicated Code**: Dieselbe Logikstruktur taucht in mehr als einem Hunk oder einer Datei der Änderung auf. → Extrahiere die gemeinsame Struktur, rufe sie von beiden Stellen auf.
- **Feature Envy**: Eine Methode, die stärker auf die Daten eines anderen Objekts zugreift als auf die eigenen. → Verschiebe die Methode zu den Daten, die sie begehrt.
- **Data Clumps**: Dieselben wenigen Felder oder Parameter reisen immer zusammen (ein Typ, der geboren werden will). → Bündle sie in einem Typ und übergib diesen.
- **Primitive Obsession**: Ein Primitive oder String steht für ein Fachkonzept, das einen eigenen Typ verdient. → Gib dem Konzept einen eigenen kleinen Typ.
- **Repeated Switches**: Dieselbe `switch`/`if`-Kaskade über denselben Typ wiederholt sich über die Änderung hinweg. → Ersetze sie durch Polymorphie oder eine Map, die sich beide Stellen teilen.
- **Shotgun Surgery**: Eine logische Änderung erzwingt verstreute Edits über viele Dateien im Diff. → Sammle, was zusammen ändert, in einem Modul.
- **Divergent Change**: Eine Datei oder ein Modul wird aus mehreren unzusammenhängenden Gründen bearbeitet. → Teile so, dass jedes Modul sich nur aus einem Grund ändert.
- **Speculative Generality**: Abstraktion, Parameter oder Hooks für Bedürfnisse hinzugefügt, die die Spec nicht hat. → Lösche sie; inline zurück, bis sich ein echter Bedarf zeigt.
- **Message Chains**: Lange `a.b().c().d()`-Navigation, von der der Aufrufer nicht abhängen sollte. → Verstecke den Durchlauf hinter einer Methode am ersten Objekt.
- **Middle Man**: Eine Klasse oder Funktion, die größtenteils nur weiterdelegiert. → Entferne sie, rufe das eigentliche Ziel direkt auf.
- **Refused Bequest**: Eine Subklasse oder Implementierung, die das meiste ignoriert oder überschreibt, was sie erbt. → Verzichte auf die Vererbung, nutze Komposition.

### 4. Beide Subagenten parallel starten

Der **Standards-Subagent-Prompt** sollte enthalten:

- Den vollständigen Diff-Befehl und die Commit-Liste.
- Die Liste der Standards-Quelldateien, die du in Schritt 3 gefunden hast, **plus die Smell-Baseline aus Schritt 3** vollständig eingefügt (der Subagent hat sonst keinen Zugriff darauf).
- Den Auftrag: "Melde pro Datei/Hunk, wo relevant: (a) jede Stelle, an der der Diff einen dokumentierten Standard verletzt: zitiere den Standard (Datei + Regel); und (b) jeden Baseline-Smell, den du entdeckst: benenne ihn und zitiere den Hunk. Unterscheide harte Verletzungen von Ermessensfragen: Verstöße gegen dokumentierte Standards können hart sein, Baseline-Smells sind aber immer Ermessensfragen, und ein dokumentierter Repo-Standard überstimmt die Baseline. Überspringe alles, was Tooling erzwingt. Unter 400 Wörtern."

Der **Spec-Subagent-Prompt** sollte enthalten:

- Den Diff-Befehl und die Commit-Liste.
- Den Pfad oder den abgerufenen Inhalt der Spec.
- Den Auftrag: "Melde: (a) von der Spec verlangte Anforderungen, die fehlen oder unvollständig sind; (b) Verhalten im Diff, das nicht verlangt wurde (Scope Creep); (c) Anforderungen, die umgesetzt wirken, deren Implementierung aber falsch aussieht. Zitiere für jeden Befund die betreffende Spec-Zeile. Unter 400 Wörtern."

Fehlt die Spec, überspringe den Spec-Subagenten und vermerke dies im Abschlussbericht.

### 5. Aggregieren

Präsentiere die beiden Berichte unter den Überschriften `## Standards` und `## Spec`, wortgetreu oder leicht bereinigt. Führe die Befunde **nicht** zusammen und ordne sie nicht neu, weil die beiden Achsen bewusst getrennt sind (siehe _Warum zwei Achsen_).

Schließe mit einer einzeiligen Zusammenfassung: Gesamtzahl der Befunde pro Achse und das schwerwiegendste Issue _innerhalb jeder Achse_ (falls vorhanden). Wähle keinen einzelnen Gewinner über die Achsen hinweg: genau diese Neuordnung soll die Trennung verhindern.

## Warum zwei Achsen

Eine Änderung kann eine Achse bestehen und an der anderen scheitern:

- Code, der jeden Standard befolgt, aber das Falsche umsetzt → **Standards bestanden, Spec gescheitert.**
- Code, der genau das tut, was das Issue verlangt hat, aber die Konventionen des Projekts bricht → **Spec bestanden, Standards gescheitert.**

Getrennte Berichterstattung verhindert, dass eine Achse die andere verdeckt.
