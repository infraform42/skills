---
name: ask-matt
description: Fragt, welcher Skill oder Flow zur jeweiligen Situation passt. Ein Router über die Skills in diesem Repository.
disable-model-invocation: true
---

# Ask Matt

Du merkst dir nicht jeden Skill, also frag.

Ein **Flow** ist ein Pfad durch die Skills. Die meisten Pfade verlaufen entlang eines **Hauptflows**, und zwei **Einstiege** münden darauf ein. Alles andere ist eigenständig oder eine Vokabularschicht, die darunter läuft.

## Der Hauptflow: Idee → Ship

Der Weg, den die meiste Arbeit nimmt. Du hast eine Idee und willst sie gebaut haben.

1. **`/grill-with-docs`** schärft die Idee durch ein Interview. Starte hier, wenn du **in einem Arbeitsverzeichnis arbeitest**: Es ist zustandsbehaftet und hält fest, was es lernt, in `CONTEXT.md` und ADRs. (Kein Arbeitsverzeichnis? Nutze stattdessen `/grill-me`, behandelt unter Eigenständig. Beide nutzen dieselbe `/grilling`-Primitive; `grill-with-docs` ist diejenige, die eine Papierspur hinterlässt, was sie zur besseren der beiden macht, sobald ein Repo da ist, in dem sie hinterlassen werden kann.)
2. **Verzweigung: Kannst du jede Frage im Gespräch klären?** Wenn eine Frage eine lauffähige Antwort braucht (Zustand, Fachlogik, eine UI, die du sehen musst), mach einen Abstecher über einen Prototyp, überbrückt durch **`/handoff`** in beide Richtungen (ein Prototyp lebt in seinem eigenen Verzeichnis, genau dafür ist `/handoff` da; siehe Phasengrenzen):
   - **`/handoff`** raus, dann eine frische Session gegen diese Datei öffnen,
   - **`/prototype`**, um die Frage mit Wegwerfcode zu beantworten,
   - **`/handoff`** zurück, was du gelernt hast, und aus dem ursprünglichen Ideen-Thread darauf verweisen.
3. **Verzweigung: Ist das ein Build über mehrere Sessions?**
   - **Ja** → **`/to-spec`** (verwandelt den Thread in eine Spec), dann **`/to-tickets`**, um sie in Tracer-Bullet-Tickets aufzuteilen, von denen jedes seine **blockierenden Kanten** deklariert. Auf einem lokalen Tracker ist das eine Datei pro Ticket unter `.scratch/<feature>/issues/`, von Hand blocker-first abgearbeitet; auf einem echten Tracker werden die Kanten zu nativen blockierenden Links, sodass jedes Ticket, dessen Blocker erledigt sind, gegriffen werden kann: Starte **`/implement`** pro Ticket, wobei du **zwischen jedem den Context mit `/clear` leerst**. Jedes Ticket ist in sich abgeschlossen, sodass der Context des letzten wegwerfbar ist.
   - **Nein** → **`/implement`** direkt hier, im selben Context-Fenster.

   So oder so baut **`/implement`** jedes Issue, indem es intern **`/tdd`** antreibt (eine Red-Green-Slice nach der anderen), und schließt dann ab, indem es **`/code-review`** ausführt, eine zweiachsige Review (Standards + Spec) des Diffs, bevor committet wird. Greif eigenständig zu **`/tdd`**, wenn du einfach ein konkretes Verhalten test-first bauen willst, ohne vollständige Spec, und zu **`/code-review`** eigenständig, wenn du einen Branch oder PR gegen einen Fixpunkt reviewen willst.

### Context-Hygiene

Halte die Schritte 1–3 in **einem ununterbrochenen Context-Fenster** (nicht komprimieren oder leeren, bis `/to-tickets` durch ist), damit Grilling, Spec und Tickets alle auf demselben Denken aufbauen. Jedes `/implement` startet dann frisch, ausgehend vom Ticket.

Die Grenze dafür ist die **[Smart Zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone)**: das Fenster (~150k Tokens bei State-of-the-Art-Modellen), innerhalb dessen das Modell noch scharf denkt. Nähert sich eine Session dieser Grenze, bevor `/to-tickets` erreicht ist, arbeite nicht im degradierten Zustand weiter; komprimiere mit `/compact` an der nächsten Phasengrenze und mach weiter (siehe Phasengrenzen).

## Einstiege

Eine Ausgangssituation, die Arbeit erzeugt und dann in den Hauptflow einmündet.

- **Bugs und Anfragen stapeln sich** → **`/triage`**. Es bewegt Issues durch Triage-Rollen und erzeugt agent-ready Issues, die **`/implement`** später aufgreift.

  Triage ist nur für Issues, **die du nicht selbst erstellt hast**: Bug-Reports, eingehende Feature-Requests, alles, was roh ankommt. Tickets, die `/to-tickets` erzeugt hat, sind bereits agent-ready, also **triagiere sie nicht**.

- **Etwas ist kaputt** → **`/diagnosing-bugs`**. Für die harten Fälle: der Bug, der sich einem ersten Blick widersetzt, der intermittierende Flake, die Regression, die sich zwischen zwei bekannt-guten Zuständen eingeschlichen hat. Es theoretisiert erst, wenn es eine **enge Feedback-Loop** hat (ein Befehl, der bei *diesem* Bug bereits rot wird), und behebt dann mit einem Regressionstest. Sein Post-Mortem übergibt an **`/improve-codebase-architecture`**, wenn der eigentliche Befund ist, dass es keine gute Nahtstelle (Seam) gibt, um den Bug festzunageln.

- **Ein riesiges, nebliges Vorhaben: ein Greenfield-Projekt oder ein gewaltiger Feature-Build, zu groß für eine Session** → **`/wayfinder`**, der kognitiv anspruchsvollste Flow hier. Wenn der Weg von hier zum Ziel noch nicht sichtbar ist, entwirft es eine **gemeinsame Karte** aus **Entscheidungstickets** auf dem Issue-Tracker und löst sie eins nach dem anderen, wobei es **Entscheidungen liefert, keine Deliverables**, bis der Nebel zurückgedrängt ist und der Weg klar ist. Während **`/grill-with-docs`** eine Idee schärft, die du in einer Session im Kopf behalten kannst, ist wayfinder für die Idee, die du nicht behalten kannst, und es ist langsamer und dichter, also hebe es dir genau dafür auf, nie für ein gut umrissenes Feature.

  Wenn sich die Karte lichtet, **übergibt es, es baut nicht**: münde in den Hauptflow bei **`/to-spec`** ein, das die verknüpften Entscheidungen der Karte zu einem baubaren Plan verdichtet, dann `/to-tickets` und `/implement` wie gewohnt. Die Karte direkt in `/implement` zu schleifen überspringt diese Verdichtung und wirft die verknüpften Details weg, also geh nur dann direkt zu `/implement`, wenn sich das Vorhaben als wirklich klein herausgestellt hat.

## Codebase-Gesundheit

Keine Feature-Arbeit, nur Pflege.

- **`/improve-codebase-architecture`** läuft, wann immer du einen Moment übrig hast, um die Codebase gut für den Betrieb durch Agenten zu halten. Es fördert **Vertiefungsmöglichkeiten** zutage; wählst du eine aus, _erzeugt das eine Idee_, die du in den Hauptflow bei `/grill-with-docs` mitnehmen kannst. Es ist die Bestandsaufnahme, die die Kandidaten findet; **`/codebase-design`** (unten) ist die Werkbank, auf der du den gewählten entwirfst.

## Vokabular darunter

Zwei modellgesteuerte Referenzen, die *unterhalb* der anderen Skills laufen, jede die einzige Quelle der Wahrheit für ihr Vokabular. Greif direkt zu ihnen, wenn die **Wörter**, nicht der Prozess, das Problem sind; oder lass die Skills oben sie einziehen.

- **`/domain-modeling`**: schärft die *Domänen*-Sprache des Projekts: einen unscharfen Begriff hinterfragen, ein überladenes Wort auflösen („account“, das drei Jobs macht), eine schwer umkehrbare Entscheidung als ADR festhalten. Es ist die aktive Disziplin, die `/grill-with-docs` antreibt, um `CONTEXT.md` als sauberes Glossar zu halten.
- **`/codebase-design`** ist das Vokabular für tiefe Module (Modul, Interface, Tiefe, Nahtstelle (Seam), Adapter, Leverage, Lokalität) zum Entwerfen der *Form* eines Moduls: viel Verhalten hinter einem kleinen Interface an einer sauberen Nahtstelle. `/tdd` und `/improve-codebase-architecture` sprechen es beide.

## Phasengrenzen

Eine **Phase** ist ein Arbeitsabschnitt innerhalb einer Session: das Grilling, die Implementierung, die QA. An der **Grenze** zwischen zwei davon hast du fünf Optionen, und die Wahl zwischen ihnen ist die unschärfste Entscheidung in dieser ganzen Map:

- **Continue**: bleib, wo du bist. Kostet nichts, verliert nichts.
- **`/clear`**: leert das Fenster, wenn nichts hier für das Nächste relevant ist.
- **`/handoff`** schreibt eine portable Markdown-Datei. Eng gefasst: nur für ein **neues Harness**, ein **neues Verzeichnis**, einen **Kollegen**, oder um eine Nebenaufgabe **mitten in der Phase** abzuzweigen. Was es bringt, ist Portabilität.
- **Subagent**: schick eine eng umrissene Aufgabe in ihr eigenes Fenster und bekomm einen Bericht zurück.
- **`/compact`** komprimiert diesen Context und speist eine frische Session damit. Der **Default**, am unteren Ende des Baums statt der erste Griff.

Lies [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) für den geordneten Baum: die fünf Fragen, die Begründung hinter jeder Verzweigung, und warum die Primärquellen-Kosten dazu führen, dass **Continue** als Erstes ausscheidet. Triff die Entscheidung **an** einer Grenze; mitten in der Phase mach weiter oder teile den Rest in Subagenten auf.

## Eigenständig

Komplett abseits des Hauptflows.

- **`/grill-me`**: dasselbe unerbittliche Interview wie `/grill-with-docs`, aber **zustandslos**: Es speichert nichts lokal und baut kein `CONTEXT.md` auf. Greif dazu, wenn du **nicht in einem Arbeitsverzeichnis arbeitest** (einen Plan schärfen, ein Design, ein Schriftstück, alles ohne Repo darunter). Bist du in einem Arbeitsverzeichnis, nutze stattdessen `/grill-with-docs`: Es führt dasselbe Interview und hinterlässt eine Papierspur, ist also strikt das bessere.
- **`/grilling`** ist die Interview-Primitive selbst: Runden, die Frontier (die offene Front), Fakten sind der Job des Agenten und Entscheidungen sind deine. `/grill-me` und `/grill-with-docs` sind die zwei benannten Einstiege, und `/triage`, `/wayfinder` und `/improve-codebase-architecture` führen sie alle intern aus. Greif direkt zu ihr, nur wenn du das Interview ohne Wrapper drumherum willst.
- **`/resolving-merge-conflicts`** arbeitet einen laufenden Merge- oder Rebase-Konflikt Hunk für Hunk ab, löst nach **Intent** auf, zurückverfolgt zur Primärquelle jeder Seite, statt einzelne Zeilen auszuwählen, und schließt dann die Operation ab. Es führt niemals `--abort` aus. Eigenständig und außerhalb jedes Flows: greif dazu, wenn du bereits mitten im Konflikt steckst.
- **`/prototype`** ist ein kleines Wegwerfprogramm, das eine Designfrage beantwortet: Fühlt sich dieses State-Modell richtig an, oder wie sollte diese UI aussehen. Wegwerf ist eine Einschränkung dafür, wie der Code geschrieben wird, kein Versprechen, ihn zu zerstören: Die Antwort fließt in den echten Code ein, und der Prototyp selbst wird als **Primärquelle** auf einem `prototype/<name>`-Branch außerhalb von main aufbewahrt, worauf vom Implementierungs-Issue aus verwiesen wird. Es ist der Abstecher in Schritt 2 des Hauptflows, aber greif dazu, wann immer eine Designfrage sich auf Papier schwer klären lässt.
- **`/research`**: delegiert die Lesearbeit an einen **Background-Agenten**: Er untersucht eine Frage anhand von **Primärquellen** und hinterlässt dann eine zitierte Markdown-Datei im Repo. Arbeite weiter, während er liest. Die Datei, die er erzeugt, ist etwas, das du *in* den Hauptflow bei `/grill-with-docs` mitnimmst, da Research das Denken füttert, statt es zu ersetzen.
- **`/to-questionnaire`** kommt zum Einsatz, wenn das, was dich blockiert, nicht in deinem Kopf oder der Codebase sitzt, sondern in **dem eines anderen**, und schreibt für diese Person einen Fragebogen zum Ausfüllen. Es ist das Gegenstück zu `/grill-me`: Statt dich zum Thema zu befragen, befragt es dich zum **Versand** (an wen es geht, was du zurückbrauchst) und richtet die Fragen auf die Lücke. Was zurückkommt, ist Material für `/grill-with-docs` oder `/to-spec`.
- **`/wizard`** ist für die Schritte, die nur ein **Mensch** ausführen kann: Infrastruktur bereitstellen, Credentials oder CI-Secrets einrichten, sich durch ein unbekanntes Dashboard eines Drittanbieters klicken, eine einmalige Migration oder ein Cutover durchführen. Es erzeugt ein interaktives Bash-Skript, das jede URL öffnet, jeden Wert erfasst und ihn in `.env` und GitHub-Secrets schreibt, sodass die Prozedur aufhört, etwas zu sein, das du einem Agenten jedes Mal neu erklären musst. Modellgesteuert, sodass der Agent danach greift, sobald er auf eine Wand trifft, die nur du überwinden kannst. Könnte der Agent es einfach selbst tun, sollte er es tun; das hier ist für den Fall, dass ein Mensch wirklich im Loop ist.
- **`/wait-what`** ist die Korrektur für eine Nachricht, die nicht angekommen ist. Nutze es mitten im Gespräch, innerhalb jedes anderen Skills, und der Agent präsentiert das gerade Gesagte erneut, mit dem Context, der dir gefehlt hat, in klarem Deutsch, unter Verwendung des `CONTEXT.md`-Vokabulars. Es wirkt im Nachhinein; `/grill-with-docs` ist die vorbeugende Kur, weil eine früh vereinbarte gemeinsame Sprache genau das ist, was Fachjargon von vornherein verhindert.
- **`/teach`**: ein Konzept über mehrere Sessions hinweg lernen, wobei das aktuelle Verzeichnis als zustandsbehafteter Workspace genutzt wird.
- **`/writing-for-agents`** ist die Referenz zum Schreiben von Dokumenten, die Agenten konsumieren: Skills, AGENTS.md, referenzierte Docs.

## Voraussetzung

**`/setup-matt-pocock-skills`**: vor deinem ersten Engineering-Flow ausführen, um Issue-Tracker, Triage-Labels und Doc-Layout zu konfigurieren, die die anderen Skills voraussetzen. Auch benutzerdefinierte Issue-Tracker funktionieren.
