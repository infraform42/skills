---
name: to-spec
description: "Verwandelt die aktuelle Konversation in eine Spec und veröffentlicht sie im Projekt-Issue-Tracker: kein Interview, sondern reine Synthese des bereits Besprochenen. Verwenden, wenn der Nutzer eine bestehende Diskussion in eine formale Spec überführen und ins Ticketsystem übertragen möchte."
disable-model-invocation: true
---

Dieser Skill nimmt den aktuellen Konversationskontext und das Verständnis der Codebase und erstellt daraus eine Spec. Interviewe den Nutzer NICHT; synthetisiere einfach, was du bereits weißt.

Der Issue-Tracker und das Triage-Label-Vokabular sollten dir bereits bereitgestellt worden sein. Falls nicht, weise den Nutzer darauf hin, `/setup-matt-pocock-skills` auszuführen.

## Ablauf

1. Erkunde das Repo, um den aktuellen Stand der Codebase zu verstehen, falls noch nicht geschehen. Verwende durchgängig das Domain-Glossar-Vokabular des Projekts in der Spec und beachte alle ADRs im betroffenen Bereich.

2. Skizziere die Nahtstellen (Seams), an denen du das Feature testen wirst. Bestehende Nahtstellen sind neuen vorzuziehen. Verwende die höchstmögliche Nahtstelle. Falls neue Nahtstellen benötigt werden, schlage sie am höchstmöglichen Punkt vor. Je weniger Nahtstellen über die Codebase verteilt, desto besser – die Idealzahl ist eins.

Kläre mit dem Nutzer, ob diese Nahtstellen seinen Erwartungen entsprechen.

3. Schreibe die Spec anhand der untenstehenden Vorlage und veröffentliche sie im Projekt-Issue-Tracker. Vergib das Triage-Label `ready-for-agent` – eine weitere Triage ist nicht nötig.

<spec-template>

## Problem Statement

Das Problem, mit dem der Nutzer konfrontiert ist, aus Sicht des Nutzers.

## Solution

Die Lösung für das Problem, aus Sicht des Nutzers.

## User Stories

Eine LANGE, durchnummerierte Liste von User Stories. Jede User Story sollte im Format sein:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

Diese Liste von User Stories sollte extrem umfassend sein und alle Aspekte des Features abdecken.

## Implementation Decisions

Eine Liste der getroffenen Implementierungsentscheidungen. Dazu kann gehören:

- Die Module, die gebaut/geändert werden
- Die Interfaces dieser Module, die geändert werden
- Technische Klärungen des Entwicklers
- Architekturentscheidungen
- Schema-Änderungen
- API-Contracts
- Konkrete Interaktionen

Füge KEINE spezifischen Dateipfade oder Codeschnipsel ein. Diese könnten sehr schnell veralten.

Ausnahme: Wenn ein Prototyp einen Schnipsel hervorgebracht hat, der eine Entscheidung präziser kodiert als Prosa es könnte (State Machine, Reducer, Schema, Type Shape), binde ihn innerhalb der entsprechenden Entscheidung ein und vermerke kurz, dass er aus einem Prototyp stammt. Kürze auf die entscheidungsrelevanten Teile – keine funktionierende Demo, nur die wichtigen Punkte.

## Testing Decisions

Eine Liste der getroffenen Testentscheidungen. Enthält:

- Eine Beschreibung dessen, was einen guten Test ausmacht (nur externes Verhalten testen, keine Implementierungsdetails)
- Welche Module getestet werden
- Prior Art für die Tests (d. h. ähnliche Testarten in der Codebase)

## Out of Scope

Eine Beschreibung der Dinge, die für diese Spec nicht im Scope sind.

## Further Notes

Weitere Anmerkungen zum Feature.

</spec-template>
