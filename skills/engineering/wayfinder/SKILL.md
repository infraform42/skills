---
name: wayfinder
description: Plant einen großen Arbeitsblock (mehr als eine Agentensitzung fassen kann) als gemeinsame Karte aus Entscheidungs-Tickets im Issue-Tracker und löst sie eine nach der anderen auf, bis der Weg zum Ziel klar ist.
disable-model-invocation: true
---

Eine lose Idee ist eingetroffen, zu groß für eine Agentensitzung und in Nebel gehüllt: Der Weg von hier zum **Ziel** ist noch nicht sichtbar. Beim Wayfinding geht es darum, diesen Weg zu finden, nicht darum, direkt auf das Ziel loszustürmen. Dieser Skill kartiert den Weg als **gemeinsame Karte** im Issue-Tracker des Repos und arbeitet dann dessen **Entscheidungs-Tickets** ab (Fragen, deren Auflösung eine Entscheidung ist, keine Ausführungsschnitte eines Builds) – eines nach dem anderen, bis die Route klar ist.

Das Ziel variiert je nach Vorhaben, und es zu benennen ist der erste Akt des Kartierens: Es prägt jedes Ticket. Es kann eine Spec sein, die übergeben und iterativ weiterentwickelt wird, eine Entscheidung, die vor Planungsbeginn feststehen muss, oder eine Änderung vor Ort wie eine Datenstruktur-Migration. Die Karte ist domänenunabhängig: Engineering-Arbeit, Kursinhalte, was auch immer passt.

## Planen, nicht ausführen

Wayfinder ist standardmäßig **Planung**: Jedes Ticket löst eine Entscheidung, und die Karte ist fertig, wenn der Weg klar ist – wenn nichts mehr zu entscheiden bleibt, bevor jemand losgeht und die Sache tatsächlich erledigt. Der Drang, einfach loszuarbeiten, ist meist das Signal, dass du den Rand der Karte erreicht hast und es Zeit für eine Übergabe ist. Ein Vorhaben kann dies in seinen **Notizen** außer Kraft setzen und Ausführung in die Karte selbst tragen, aber ohne das gilt: Entscheidungen liefern, keine Deliverables.

## Beim Namen nennen

Jede Karte und jedes Ticket ist ein Issue und hat somit einen **Namen**: seinen Titel. In allem, was der Mensch liest (Erzähltext, die Bisherigen Entscheidungen der Karte), nenne es bei diesem Namen, nie bei einer nackten ID, Nummer oder einem Slug. Eine Wand aus `#42, #43, #44` ist unlesbar; Namen liest man auf einen Blick. Die ID und die URL verschwinden nicht; ein Name umschließt seinen Link, aber sie reisen _innerhalb_ des Namens mit, stehen nie an seiner Stelle.

## Die Karte

Die Karte ist ein einzelnes Issue im Issue-Tracker dieses Repos, mit dem Label `wayfinder:map`, das kanonische Artefakt. Ihre Tickets sind untergeordnete Issues der Karte.

Die Karte ist ein **Index**, kein Speicher. Sie listet die getroffenen Entscheidungen auf und verweist auf die Tickets, die deren Details enthalten; eine Entscheidung existiert an genau einem Ort, ihrem Ticket, sodass die Karte sie nie wiederholt, sondern nur zusammenfasst und verlinkt.

**Wo die Karte, ihre untergeordneten Tickets, Blockierungen und Frontier-Abfragen physisch liegen, ist trackerspezifisch.** Der Issue-Tracker sollte dir bereits vorgegeben worden sein. Falls nicht, weise den Nutzer an, `/setup-matt-pocock-skills` auszuführen. Schau im Abschnitt "Wayfinding operations" der Tracker-Doku nach, wie _dieses_ Repo sie ausdrückt. Wurde kein Tracker angegeben, verwende standardmäßig den local-markdown-Tracker.

### Der Text der Karte

Die gesamte Karte in niedriger Auflösung, einmal pro Sitzung geladen. Offene Tickets werden **nicht** aufgelistet: Sie sind offene untergeordnete Issues, die per Abfrage gefunden werden.

```markdown
## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index: one line per closed ticket, enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Tickets

Jedes Ticket ist ein **untergeordnetes Issue** der Karte; die Issue-ID des Trackers ist seine Identität. Sein Text ist die Frage, dimensioniert auf eine Agentensitzung mit 100K Tokens:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Jedes Ticket trägt ein Label `wayfinder:<type>`, eines von `research`, `prototype`, `grilling`, `task` (siehe [Ticket-Typen](#ticket-types)).

Eine Sitzung **beansprucht** ein Ticket, indem sie es dem Dev zuweist, der die Karte vorantreibt, und zwar **zuerst**, vor jeder Arbeit, sodass parallele Sitzungen es überspringen. Diese Zuweisung _ist_ der Anspruch: Ein offenes, nicht zugewiesenes Ticket ist unbeansprucht.

Blockierung nutzt die **native** Abhängigkeitsbeziehung des Trackers: essenziell, weil sie die Frontier _visuell_ in der eigenen UI des Trackers darstellt, sodass der Mensch sieht, was greifbar ist, ohne die Karte zu öffnen. Nur ein Tracker ohne native Blockierung greift auf eine Text-Konvention zurück. Ein Ticket ist **unblockiert**, wenn jedes Ticket, das es blockiert, geschlossen ist; die **Frontier** (die offene Front) sind die offenen, unblockierten, unbeanspruchten Kind-Tickets, der Rand des Bekannten.

Die Antwort ist nicht Teil des Texts; sie wird bei der Auflösung festgehalten (siehe [Die Karte abarbeiten](#work-through-the-map)). Assets, die bei der Auflösung eines Tickets entstehen, werden vom Issue aus verlinkt, nicht eingefügt.

## Ticket-Typen

Jedes Ticket ist entweder **HITL** (human in the loop, gemeinsam mit einem Menschen bearbeitet, der für sich selbst spricht) oder **AFK**, allein vom Agenten vorangetrieben. Ein HITL-Ticket löst sich nur durch diesen lebendigen Austausch auf; der Agent tritt nie an die Stelle der menschlichen Seite (ein Grilling-Agent, der seine eigenen Fragen beantwortet, hat dies gebrochen).

- **Research** (AFK): Dokumentation lesen, Drittanbieter-APIs oder lokale Ressourcen wie Knowledge Bases, um eine Tatsache zutage zu fördern, auf die eine Entscheidung wartet. Wird durch einen Subagenten aufgelöst, der das Skill-Tool mit "research" aufruft. Verwenden, wenn Wissen außerhalb des aktuellen Arbeitsverzeichnisses benötigt wird.
- **Prototype** (HITL): Die Diskussion auf ein höheres Fidelity-Niveau heben, indem ein günstiges, grobes, konkretes Artefakt zum Reagieren geschaffen wird (ein Outline, ein grober Entwurf, ein Stub oder UI-/Logik-Code), durch Aufruf des Skill-Tools mit "prototype". Verlinkt den Prototyp als Asset. Verwenden, wenn "Wie sollte es aussehen" oder "Wie sollte es sich verhalten" die Schlüsselfrage ist.
- **Grilling** (HITL): Gespräch. Der Standardfall. Rufe immer zweimal das Skill-Tool auf, für "grilling" und "domain-modeling".
- **Task** (HITL oder AFK): Manuelle Arbeit, die geschehen muss, bevor eine _Entscheidung_ getroffen werden kann: nichts zu entscheiden, zu prototypisieren oder zu erforschen, aber die Diskussion ist blockiert, bis sie erledigt ist. Sich bei einem Dienst anmelden, damit dessen API beurteilt werden kann, Zugang bereitstellen, Daten verschieben, damit ihre Form sichtbar wird. Dies ist der einzige Typ, der _tut_ statt zu entscheiden, und er verdient seinen Platz dadurch, dass er eine Entscheidung entblockt, nicht dadurch, dass er das Ziel liefert. Der Agent treibt es allein voran, wo er kann (AFK); andernfalls übergibt er dem Menschen eine präzise Checkliste (HITL). Aufgelöst, wenn die Arbeit erledigt ist; die Antwort hält fest, was getan wurde und welche daraus resultierenden Fakten (Speicherort von Credentials, neue URLs, Zeilenanzahlen) spätere Tickets voraussetzen.

## Nebel des Krieges

Die Karte ist _bewusst_ unvollständig: Kartiere nicht, was du noch nicht sehen kannst. Jenseits der aktiven Tickets liegt der **Nebel des Krieges**: der undeutliche Blick auf Entscheidungen und Untersuchungen, von denen du erkennst, dass sie kommen, die du aber noch nicht festnageln kannst, weil sie von noch offenen Fragen abhängen. Die Auflösung eines Tickets lichtet den Nebel davor und lässt alles, was jetzt spezifizierbar ist, eines nach dem anderen zu frischen Tickets heranreifen, bis der Weg zum Ziel klar ist und keine Tickets mehr übrig sind.

Der Abschnitt **Not yet specified** der Karte ist der Ort, an dem dieser undeutliche Blick festgehalten wird: die vermutete Frage, der später erneut zu betrachtende Bereich. Es ist die unentdeckte Frontier _zum_ Ziel hin: Alles hier ist im Scope, nur noch nicht scharf genug, um daraus ein Ticket zu machen. Schreibe so locker oder so ausführlich, wie es der Blick zulässt; es dient zugleich als Wegweiser für Mitwirkende, die lesen, wohin sich das Vorhaben entwickelt.

**Nebel oder Ticket?** Der Test ist, ob du die Frage jetzt schon präzise formulieren kannst, _nicht_ ob du sie jetzt schon beantworten kannst.

- **Ticket, wenn** die Frage bereits scharf ist, auch wenn sie blockiert ist und du noch nicht handeln kannst.
- **Not yet specified, wenn** du sie noch nicht so scharf formulieren kannst. Zerschneide den Nebel nicht vorab in ticketgroße Stücke: Er ist gröber als ein Ticket, und ein Fleck kann zu mehreren Tickets heranreifen, oder zu keinem, sobald die Frontier ihn erreicht.

**Not yet specified** schließt aus, was bereits entschieden ist (Decisions so far), was bereits ein aktives Ticket ist, und was außerhalb des Scopes liegt (nächster Abschnitt).

## Außerhalb des Scopes

Nebel sammelt sich immer nur _in Richtung_ des Ziels. Das Ziel legt den Scope fest, also ist Arbeit jenseits davon **außerhalb des Scopes**: Sie ist kein Nebel und gehört nicht zu **Not yet specified**. Sie bekommt einen eigenen Abschnitt **Out of scope** auf der Karte: Arbeit, die du bewusst aus _diesem_ Vorhaben ausgeschlossen hast. Scope, nicht Schärfe, bringt sie hierher.

Arbeit außerhalb des Scopes reift nie heran (die Frontier endet am Ziel), sie kehrt also nur zurück, wenn das Ziel neu gezeichnet wird, und dann als frisches Vorhaben, nicht als Fortsetzung.

Etwas als außerhalb des Scopes einzustufen ist ein Akt der Scope-Festlegung, kein Schritt auf der Route. Wenn sich herausstellt, dass ein bereits bestehendes Ticket jenseits des Ziels liegt (beim Kartieren falsch eingeordnet oder durch eine Auflösung aufgedeckt), **schließe es** (ein geschlossenes Ticket liegt eindeutig außerhalb der Frontier) und hinterlasse eine Zeile im Abschnitt **Out of scope**: die Kurzfassung plus den Grund, warum es außerhalb des Scopes liegt, mit Link auf das geschlossene Ticket. Es bleibt außerhalb von **Decisions so far**, das die tatsächlich gegangene Route festhält; eine Scope-Grenze ist kein Schritt darauf.

## Aufruf

Zwei Modi. So oder so: **Löse nie mehr als ein Ticket pro Sitzung**, mit Ausnahme von Research-Tickets.

### Die Karte erstellen

Der Nutzer ruft mit einer losen Idee auf.

1. **Benenne das Ziel.** Rufe das Skill-Tool zweimal auf, für "grilling" und "domain-modeling", um festzunageln, wohin diese Karte den Weg findet: die Spec, die Entscheidung oder die Änderung. Das Ziel legt den Scope fest, wird also zuerst festgelegt.
2. **Kartiere die Frontier.** Grille erneut, diesmal **breadth-first**: fächere über den gesamten Raum auf, statt bei einem einzelnen Strang in die Tiefe zu gehen, und bringe die offenen Entscheidungen sowie die jetzt schon machbaren ersten Schritte zutage. **Ergibt sich dabei kein Nebel** (der Weg zum Ziel ist bereits klar, die gesamte Reise klein genug für eine Sitzung), brauchst du keine Karte. Halte an und frage den Nutzer, wie er weiter vorgehen möchte.
3. **Erstelle die Karte** (Label `wayfinder:map`): Destination und Notes ausgefüllt, Decisions-so-far leer, der Nebel in **Not yet specified** skizziert.
4. **Erstelle die Tickets, die du jetzt schon spezifizieren kannst,** als untergeordnete Issues der Karte, und verdrahte dann die Blockierungs-Kanten in einem **zweiten Durchgang** (Issues brauchen IDs, bevor sie aufeinander verweisen können). Das Verdrahten sortiert sie in die Frontier und die Blockierten ein; alles, was du noch nicht spezifizieren kannst, bleibt im Nebel: dem Abschnitt **Not yet specified**.
5. **Starte die Research-Subagenten.** Für jedes gerade erstellte `research`-Ticket starte einen Subagenten, der das Skill-Tool mit "research" aufruft, um es parallel aufzulösen, wobei die Erkenntnisse auf einem Wegwerf-Branch `research/<name>` festgehalten werden, mit einem Kontextverweis vom Ticket aus.
6. Halte an: Kartieren ist die Arbeit einer Sitzung; es löst nichts von Hand auf.

### Die Karte abarbeiten

Der Nutzer ruft mit einer Karte (URL oder Nummer) auf. Ein Ticket ist **optional**: Ohne eines wählst du die nächste Entscheidung, nicht der Nutzer.

1. Lade die **Karte**: die niedrig aufgelöste Ansicht, nicht jeden Ticket-Text.
2. Wähle das Ticket. Hat der Nutzer eines benannt, verwende dieses. Andernfalls nimm das erste Frontier-Ticket in Reihenfolge. **Beanspruche es**: Weise es dir selbst zu, bevor irgendeine Arbeit beginnt.
3. Löse es auf. **Zoome nach Bedarf**: Lade den vollständigen Text jedes verwandten oder geschlossenen Tickets bei Bedarf nach; rufe das Skill-Tool für die im Block `## Notes` genannten Skills auf. Im Zweifel rufe das Skill-Tool zweimal auf, für "grilling" und "domain-modeling".
4. Halte die Auflösung fest: Poste die Antwort als **Resolution-Kommentar**, **schließe** das Issue und **hänge einen Kontextverweis** an die Decisions-so-far der Karte an.
5. Füge neu aufgetauchte Tickets hinzu (erst erstellen, dann verdrahten); lasse jeden Nebel, den die Antwort spezifizierbar gemacht hat, heranreifen und entferne jeden herangereiften Fleck aus **Not yet specified**, sodass er nur noch als sein neues Ticket existiert. Zeigt die Antwort, dass ein Ticket (dieses oder ein anderes) jenseits des Ziels liegt, **stufe es als außerhalb des Scopes ein**, statt es auf der Route aufzulösen. Macht die Entscheidung andere Teile der Karte ungültig, aktualisiere oder lösche diese Tickets.

Der Nutzer kann unblockierte Tickets parallel bearbeiten, erwarte also, dass andere Sitzungen gleichzeitig am Tracker arbeiten.
