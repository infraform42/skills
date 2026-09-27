---
name: writing-for-agents
description: Schreibt Dokumente für Agenten. Verwenden, wenn Skills erstellt oder bearbeitet werden oder wenn AGENTS.md oder CLAUDE.md geändert wird. „Hilf mir, einen Skill zu schreiben“, „erstell eine SKILL.md für diesen Workflow“, „überarbeite meine AGENTS.md“, „schreib eine CLAUDE.md für dieses Projekt“, „wie strukturiere ich diesen Skill besser“
---

Referenz zum Schreiben jedes Dokuments, das ein Agent konsumiert: ein Skill, ein `AGENTS.md` / `CLAUDE.md`, ein über einen Pointer erreichtes Dokument. Die Verpackung unterscheidet sich, das Schreiben nicht: Dieselben Hebel machen jedes davon vorhersagbar, da der Agent bei jedem Durchlauf denselben _Prozess_ durchläuft, statt dieselbe Ausgabe zu produzieren.

Wenn das Dokument, das du schreibst, ein Skill ist, lies [`SKILL-MECHANICS.md`](SKILL-MECHANICS.md) zu Frontmatter, Aufrufwahl und Router-Skills.

## Kontext-Pointer

Ein **Kontext-Pointer** ist eine im Kontext des Agenten gehaltene Referenz, die kontextfremdes Material benennt und die Bedingung kodiert, unter der es erreicht wird. Die description eines Skills ist einer davon; eine Zeile in `AGENTS.md`, die ein Dokument benennt, ist dasselbe Objekt. Die _Formulierung_ des Pointers, nicht sein Ziel, entscheidet, wann der Agent das Material erreicht und wie zuverlässig. Ein unverzichtbares Ziel hinter einem schwach formulierten Pointer ist ein Varianz-Bug: Schärfe zuerst die Formulierung, und binde das Material nur dann inline ein, wenn das Schärfen scheitert.

Ein Pointer erfüllt zwei Aufgaben: benennen, was das Material ist, und die **Verzweigungen** auflisten, die das Erreichen auslösen sollen (eine Verzweigung ist ein eigenständiger Fall, den das Dokument behandelt, sodass unterschiedliche Durchläufe unterschiedliche Pfade hindurch nehmen). Jedes Wort eines dauerhaft geladenen Pointers kostet bei jeder Runde, daher verdient es noch härteres Pruning als der Hauptteil:

- **Platziere das Leitwort ganz vorn**: Im Pointer entfaltet es seine auslösende Wirkung.
- **Ein Trigger pro Verzweigung.** Synonyme, die dieselbe Verzweigung nur umbenennen, sind eine Verzweigung, die zweimal geschrieben steht; fasse sie zusammen und behalte nur wirklich unterschiedliche Verzweigungen.
- **Streiche Identität, die der Hauptteil bereits trägt.**

## Die zwei Lasten

Jedes Dokument und jeder Pointer, den du hinzufügst, gibt eines von zwei Budgets aus:

- **Context Load** ist der Preis dauerhaft geladenen Materials im Fenster des Agenten: eine `AGENTS.md`-Zeile, eine Skill-description, alles, was bei jeder Runde im Kontext liegt und Tokens sowie Aufmerksamkeit kostet – ob es nun auslöst oder nicht.
- **Cognitive Load** ist der Preis für den Menschen: welche Dokumente existieren und wann man zu welchem greift. Der Mensch ist der Index. Keine Kosten, die es zu minimieren gilt: Sie sind der Preis menschlicher Handlungsfähigkeit; gib sie aus, wo menschliches Urteilsvermögen zählt, und entferne sie, wo es das nicht tut.

Material, das nur über einen Pointer erreicht wird, entkommt der Context Load um den Preis der eigenen Zeile des Pointers; Material ganz ohne Pointer trägt sich vollständig über die Cognitive Load.

## Informationshierarchie

Ein Dokument besteht aus zwei Inhaltstypen: **Schritte** (die geordneten Aktionen, die der Agent ausführt) und **Referenz** (Definitionen, Regeln, Fakten, die bei Bedarf nachgeschlagen werden). Beide mischen sich frei: nur Schritte (ein Rezept), nur Referenz (die Regeln einer Review, dieser Skill) oder beides. Die zentrale Entscheidung ist, wo jedes Element in der **Informationshierarchie** sitzt, einer Leiter, die danach gestuft ist, wie unmittelbar der Agent das Material braucht:

1. **In-File-Schritt** ist die primäre Stufe: was der Agent tut, der Reihenfolge nach.
2. **In-File-Referenz** wird bei Bedarf nachgeschlagen. Oft eine legitim flache Peer-Menge (jede Regel einer Review auf einer Sprosse), was eine gute Anordnung ist, kein Warnsignal.
3. **Ausgelagerte Referenz** wird in eine separate Datei verschoben, über einen Kontext-Pointer erreicht und nur geladen, wenn der Pointer auslöst. Reicht von einer Nachbardatei im selben Ordner bis zu vollständig externer Referenz, die irgendwo liegen kann und auf die jedes Dokument verweisen darf.

Schiebst du zu wenig nach unten, bläht sich die Spitze auf; schiebst du zu viel, versteckst du Material, das der Agent tatsächlich braucht. Diese Spannung ist die ganze Entscheidung.

**Schrittweise Auslagerung** ist die Bewegung die Leiter hinab (aus der Hauptdatei heraus und hinter einen Pointer), damit die Spitze lesbar bleibt. In erster Linie keine Token-Optimierung: So wird die Hierarchie geschützt. Verzweigen ist der sauberste Test fürs Auslagern: Binde inline ein, was jede Verzweigung braucht, und schiebe hinter einen Pointer, was nur manche Verzweigungen erreichen. Hat ein Dokument Schritte, begräbt In-File-Referenz, die eigentlich ausgelagert werden sollte, diese Schritte und macht das Beachten der Schritte zum Münzwurf: ein Varianz-Hebel, nicht nur ein Lesbarkeits-Hebel.

**Co-Location** ist das Gegenstück innerhalb der Datei: Während die Leiter entscheidet, _wie weit unten_ ein Stück sitzt, entscheidet Co-Location, _was daneben sitzt_, sobald es dort ist. Halte Definition, Regeln und Fallstricke eines Konzepts unter einer Überschrift zusammen statt verstreut, damit das Lesen eines Teils dessen Nachbarn gleich mitbringt. Der Test: Das Dokument sollte sich lesen wie Dokumentation, die für den Agenten geschrieben wurde. Gruppiertes Material liest sich so; verstreutes nicht. (Zu unterscheiden von Duplikation: Die wiederholt eine Bedeutung an zwei Stellen; Streuung zerlegt eine Bedeutung über viele Stellen.)

**Wildwuchs** ist der Fehlermodus hier: ein Dokument schlicht zu lang, selbst wenn jede Zeile lebendig und einzigartig ist. Die Aufmerksamkeit verdünnt sich über den Überschuss, und jede zusätzliche Zeile ist eine mehr, die relevant gehalten werden muss. Die Abhilfe ist die Leiter: Referenz hinter Pointern auslagern und nach Verzweigung oder Sequenz aufteilen, sodass jeder Pfad nur trägt, was er braucht.

## Schritte und Abschlusskriterien

Jeder Schritt endet mit einem **Abschlusskriterium**, der Bedingung, die dem Agenten sagt, dass die Arbeit erledigt ist. Zwei Eigenschaften machen es zu einem Hebel:

- **Klarheit**: Kann der Agent Fertig von Nicht-fertig unterscheiden? Eine vage Grenze („Verständnis erreicht“) lädt zu **vorzeitigem Abschluss** ein: den Schritt zu beenden, bevor er wirklich fertig ist, wobei die Aufmerksamkeit zum _Fertigsein_ abrutscht. Die noch sichtbaren, vorausliegenden Schritte (die **Folgeschritte**) liefern den Zug; die Klarheit des Kriteriums ist der Widerstand dagegen. Verteidige in dieser Reihenfolge: **schärfe zuerst die Grenze** (lokal und billig); nur wenn sie unauflösbar unscharf ist _und_ du das Abrutschen beobachtest, verstecke die späteren Schritte, indem du die Sequenz aufteilst. Verstecken funktioniert nur über eine echte Kontextgrenze hinweg (eine Übergabe oder ein Subagent-Dispatch; ein Inline-Aufruf lässt die späteren Schritte im Kontext und räumt nichts aus).
- **Anspruch**: wie viel er verlangt. „Jedes geänderte Modell erfasst“ erzwingt gründliche Arbeit, wo „erstelle eine Änderungsliste“ das nicht tut. Anspruch treibt **Ermittlungsarbeit** an (das Graben, das der Agent innerhalb der Arbeit betreibt, latent in der Formulierung statt als eigener Schritt ausgeschrieben), und er ist nicht an Schritte gebunden: „jede Regel angewendet“ bindet einen Bestand flacher Referenz genauso, wie „jeder Schritt erledigt“ eine Sequenz bindet – so trägt auch ein reines Referenz-Dokument eine Vollständigkeitsschwelle.

Die stärksten Kriterien sind sowohl überprüfbar als auch erschöpfend.

## Wann aufteilen

Ein Dokument in zwei aufzuteilen kostet eine der beiden Lasten, teile daher nur auf, wenn der Schnitt sich lohnt:

- **Nach Sequenz**: Teile eine Folge von Schritten dort, wo die Folgeschritte den Agenten dazu verleiten, den davorliegenden zu überstürzen. Sie außer Sichtweite zu halten, treibt mehr Ermittlungsarbeit bei der aktuellen Aufgabe an. Achte auf die Umkehrung: Das Zusammenführen von Sequenzen legt die späteren Schritte jedes Schritts gegenüber dem Folgenden offen und lädt zu vorzeitigem Abschluss ein.
- **Nach Aufruf**, skill-spezifisch: siehe [`SKILL-MECHANICS.md`](SKILL-MECHANICS.md).

## Leitwörter

Ein **Leitwort** ist ein kompaktes Konzept, das bereits im Pretraining des Modells lebt und mit dem der Agent denkt, während er das Dokument durchläuft (_lesson_, _fog of war_, _tracer bullets_). Als Token wiederholt, nie als Satz, sammelt es eine verteilte Definition an und verankert einen ganzen Verhaltensbereich mit den wenigsten Tokens, indem es Priors nutzt, die das Modell bereits besitzt. Eigene Wortschöpfungen funktionieren, wenn du sie klar definierst, aber ein erfundenes Wort rekrutiert keine Priors: Du zahlst in Definitions-Tokens, was ein vortrainiertes Wort umsonst liefert; greife zuerst nach einem existierenden Wort.

Es verankert sich zweifach. Im Hauptteil, bei der _Ausführung_: Der Agent greift jedes Mal, wenn das Wort auftaucht, zum selben Verhalten, und innerhalb flacher Referenz lenkt es die Aufmerksamkeit auf eine Klasse von Dingen, nach denen gesucht werden soll. In einem Pointer, beim _Aufruf_: Wenn dasselbe Wort in deinen Prompts, deinen Dokumenten und deiner Codebasis lebt, verknüpft der Agent diese gemeinsame Sprache mit dem Material und erreicht es zuverlässiger.

Jage nach Gelegenheiten, mit Leitwörtern zu refaktorieren. Eine Triade, die an drei Stellen ausformuliert ist, ein Pointer, der einen ganzen Satz aufwendet, um auf eine einzige Idee zu deuten. Jedes davon ist eine Passage, die danach schreit, zu einem einzigen Token zu kollabieren:

- „schnell, deterministisch, mit wenig Overhead“ → _tight_ (eine _tight_ loop).
- „eine Loop, an die du glaubst“ → _red_, das ein unscharfes Gate in einen binär beobachtbaren Zustand verwandelt (die Loop wird beim Bug _red_, oder sie wird es nicht).

Du gewinnst zweifach: weniger Tokens und einen schärferen Haken, an dem der Agent sein Denken aufhängen kann. Geh davon aus, dass jedes Dokument Umformulierungen mit sich trägt, die Leitwörter überflüssig machen. Geh sie suchen.

**Negation** ist der Fehlermodus neben diesem Hebel: Steuern durch Verbote zieht das verbotene Verhalten in den Kontext und macht es _stärker_ verfügbar, nicht weniger. _Denk nicht an einen Elefanten_, und der Elefant ist alles, was da ist; die Negation ist ein schwacher Modifikator, den das stark aktivierte Konzept überrennt, sodass das Verbot halb wie eine Anweisung gelesen wird, die Sache zu tun. Prompte das **Positive**: Formuliere das Zielverhalten („schreib einzeilige Kommentare“), sodass das Verbotene nie ausgesprochen wird. Ein Verbot verdient seinen Platz nur als harte Leitplanke, die du nicht positiv formulieren kannst; selbst dann verbinde es mit dem positiven Ziel, sodass die Aufmerksamkeit dort landet, wo sie hin soll.

## Pruning

- Halte jede Bedeutung in einer **Single Source of Truth**: einem einzigen maßgeblichen Ort, sodass eine Verhaltensänderung eine Bearbeitung an einer Stelle ist. **Duplikation** (dieselbe Bedeutung an mehr als einem Ort) kostet Pflegeaufwand und Tokens und bläht die Sichtbarkeit einer Bedeutung auf der Leiter über ihren tatsächlichen Rang hinaus auf. (Die unabsichtliche Umkehrung eines Leitworts, das absichtlich ein Token wiederholt, niemals die Bedeutung.)
- Die **Umgebung** ist ebenfalls eine Quelle der Wahrheit (`package.json`-Skripte, Konfigurationsdateien, das Verzeichnislayout, `--help`-Ausgaben), und ein Dokument, das sie nur nachformuliert, ist ein **Cache**: eine Kopie eines Nachschlagevorgangs, die ihre Last nur dann verdient, wenn das Nachschlagen teuer ist. Cache das, was der Agent nicht durch Hinsehen findet: die ungeschriebene Konvention, den Grund hinter einer Entscheidung, den Haken, den keine Config gesteht. Überlass die Ein-Datei-, Ein-Befehl-Nachschlagevorgänge der Umgebung, wo sie nicht veralten können.
- Prüfe jede Zeile auf **Relevanz**: Bezieht sie sich noch darauf, was das Dokument tut? Eine Zeile verliert Relevanz, indem sie nie auf die Aufgabe einzahlt (bloße Erläuterung, oder eine Verzweigung, die ausgelagert werden sollte), oder indem sie veraltet, während sich das Verhalten oder die Welt, die sie beschreibt, ändert. Kürzere Dokumente sind leichter relevant zu halten. Ohne Pruning-Disziplin ist das Standardschicksal **Sediment**: veraltete Schichten, die sich ablagern, weil Hinzufügen sich sicher anfühlt und Entfernen riskant, bis du dich durch sie hindurchbohren musst, um zu finden, was noch lebt.
- Jage **No-ops** Satz für Satz: Eine Anweisung, der das Modell ohnehin standardmäßig folgt, kostet Last, um nichts zu sagen. Der Test (ändert es Verhalten gegenüber dem Standard?) ist modellrelativ, nicht leserrelativ: Zwei Personen, die über einen No-op uneins sind, sind über den Standard uneins, und klären das durch Ausführen des Dokuments, nicht durch Debatte. Wenn ein Satz durchfällt, lösche den ganzen Satz, statt nur Wörter daraus zu streichen. Der Test bewertet auch Leitwörter: Ein Wort, das zu schwach ist, um den Standard zu schlagen (_be thorough_, wenn der Agent ohnehin schon einigermaßen gründlich ist), ist ein No-op, und die Lösung ist ein stärkeres Wort (_relentless_), keine andere Technik.
