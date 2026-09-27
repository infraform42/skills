---
name: grilling
description: Grillt den Nutzer unnachgiebig zu einem Plan, einer Entscheidung oder einer Idee. Verwenden, wenn der Nutzer sein Denken einem Stresstest unterziehen will, oder bei jeder 'grill'-Auslöserphrase. „grill mich zu meinem Plan“, „stell mir kritische Fragen dazu“, „hinterfrag meine Entscheidung gründlich“, „nimm meine Idee auseinander“, „bohr bei diesem Vorhaben nach“
---

Befrage den Nutzer unnachgiebig, bis ihr ein gemeinsames Verständnis erreicht habt. Bilde dies als **Entscheidungsbaum** ab: Jede Entscheidung verzweigt sich in die Entscheidungen, die von ihr abhängen.

Arbeite den Baum in **Runden** ab. Die **Frontier** (die offene Front) umfasst jede Entscheidung, deren Voraussetzungen bereits geklärt sind: die Fragen, die du _jetzt_ stellen kannst, ohne Antworten zu erraten, die du noch nicht gehört hast. Stelle die gesamte Frontier in einer Runde: nummeriere jede Frage und gib deine empfohlene Antwort an. Warte dann auf die Antworten des Nutzers, bevor die nächste Runde beginnt.

Formatiere eine Runde so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Jede Runde formen die Antworten des Nutzers den Baum neu: geklärte Entscheidungen schieben die Frontier weiter nach außen und geben Fragen frei, die von ihnen abhingen. Berechne die Frontier neu und stelle die nächste Runde. Eine Frage, deren Antwort von einer anderen, in dieser Runde noch offenen Frage abhängt, gehört in eine _spätere_ Runde, nicht in diese.

_Fakten_ zu ermitteln ist deine Aufgabe, niemals die des Nutzers. Wenn eine Frontier-Frage einen Fakt aus der Umgebung benötigt (Dateisystem, Tools usw.), setze einen Subagenten ein, um ihn zu finden; frag den Nutzer nichts, was du selbst nachschlagen könntest. Blockiere dabei nicht: eine laufende Recherche ist eine ungeklärte Voraussetzung, also warten nur die davon abhängigen Fragen auf die Rückmeldung des Subagenten; stelle den Rest der Frontier bereits jetzt. Die _Entscheidungen_ liegen beim Nutzer: lege sie ihm vor und warte.

Die Sitzung ist abgeschlossen, wenn die Frontier leer ist: jeder Zweig des Entscheidungsbaums besucht, nichts stillschweigend angenommen. Setze nichts davon um, bevor der Nutzer bestätigt hat, dass ihr ein gemeinsames Verständnis erreicht habt.
