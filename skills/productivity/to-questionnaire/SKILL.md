---
name: to-questionnaire
description: Verwandelt eine Entscheidung, die der Nutzer nicht vollständig selbst beantworten kann, in einen questionnaire (Fragebogen), den eine andere Person ausfüllt.
disable-model-invocation: true
---

Verwandle etwas, das der Nutzer nicht allein beantworten kann, in einen **Fragebogen**: ein Markdown-Dokument, das er einer Person zum asynchronen Ausfüllen übergibt oder gemeinsam in einem Meeting durchgeht. Die empfangende Person besitzt Wissen, das dem Nutzer fehlt; der Fragebogen zieht dieses Wissen aus ihr heraus.

**Grill den Versand, nicht das Thema.** Befrage den Nutzer nur zum _Versand_, den er immer beantworten kann: an wen er geht und was er zurückbraucht. Die Fragen im Dokument zielen dann auf die **Lücke** zwischen dem, was die empfangende Person weiß, und dem, was der Nutzer braucht.

1. **An wen geht es?** Frage in einem Austausch nach Rolle, Fachwissen und Beziehung der empfangenden Person zum Nutzer. Das legt Ton und nötigen Kontextumfang des Fragebogens fest. Abgeschlossen, wenn klar ist, wer die empfangende Person ist und was sie weiß, was der Nutzer nicht weiß.

2. **Was brauchst du zurück?** Frage in einem Austausch nach den konkreten Entscheidungen oder Fakten, die der Nutzer allein nicht klären kann und von dieser Person braucht. Abgeschlossen, wenn eine konkrete Liste vorliegt, was der Nutzer danach tun oder entscheiden können muss.

3. **Schreibe den Fragebogen.** Entwirf Fragen, die auf die Lücke aus den Schritten 1–2 zielen, gemäß der Dokumentstruktur unten. Schreibe ihn in `to-questionnaire-<slug>.md` im aktuellen Verzeichnis (Slug aus dem Thema) und melde den Pfad. Abgeschlossen, wenn die Datei existiert und jeder in Schritt 2 genannte Punkt durch eine Frage abgedeckt ist.

## Dokumentstruktur

Rahme das Dokument als **Discovery-Fragebogen**: dem Nutzer fehlt Kontext, die empfangende Person besitzt ihn. Ordne die Fragen nach Wichtigkeit absteigend, da async bedeutet, dass eventuell nur ein Durchgang möglich ist, und gruppiere sie unter `##`-Überschriften nach Thema, sobald mehr als eine Handvoll Fragen vorliegt. Verwende die Vorlage unten.

<questionnaire-template>

# <Titel des Fragebogens>

**Zweck:** warum dieser Fragebogen existiert und welche Entscheidung davon abhängt.

**Von:** <der Nutzer>, **An:** <die empfangende Person>, **Wie deine Antworten verwendet werden:** <wo sie einfließen>

## Kontext

Ein Absatz, der eine Person orientiert, die nicht im Kopf des Nutzers steckte. Genug, um gut antworten zu können, keine ganze Seite.

## Wie antworten

Deadline und grober Aufwand. Teilantworten und „Ich weiß es nicht" sind hilfreich: markiere alles Unsichere, statt es auszulassen.

## <Themenüberschrift>

Ein `##`-Abschnitt pro Thema. Darunter die Fragen, wichtigste zuerst. Jede Frage transportiert eine einzige Idee, nie zusammengesetzt, mit einem Antwortfeld direkt darunter, und einer einzeiligen Begründung, _warum das wichtig ist_, nur dort, wo die Frage missverstanden werden könnte oder eine Wegwerfantwort provoziert.

<question-example>
### Welche Last soll das System zum Start bewältigen?

_Warum das wichtig ist: es entscheidet, ob wir jetzt für Lastspitzen vorsorgen oder das aufschieben._

>
</question-example>

## Sonst noch etwas?

Ein abschließender Auffangposten: gibt es etwas, das wir nicht gefragt haben, aber wissen sollten?

</questionnaire-template>
