---
name: tdd
description: Testgetriebene Entwicklung. Verwenden, wenn der Nutzer Features test-first entwickeln oder Bugs test-first beheben möchte, „red-green-refactor“ erwähnt oder Integrationstests wünscht. „lass uns das test-first entwickeln“, „schreib erst den Test, dann den Code“, „fang mit einem roten Test an“, „TDD für dieses Feature“, „red-green-refactor für den Bugfix“
---

# Testgetriebene Entwicklung

TDD ist die Rot-→-Grün-Schleife. Dieser Skill ist die Referenz, die dafür sorgt, dass diese Schleife Tests hervorbringt, die es wert sind, behalten zu werden: was ein guter Test ist, wo Tests hingehören, die Anti-Pattern und die Regeln der Schleife. Jeder Abschnitt gilt in jedem Zyklus: konsultiere sie vor und während der Schleife, nicht danach.

Lies beim Erkunden der Codebasis `CONTEXT.md` (falls vorhanden), damit Testnamen und Interface-Vokabular zur Domänensprache des Projekts passen, und beachte die ADRs in dem Bereich, den du bearbeitest.

## Was ein guter Test ist

Tests verifizieren Verhalten über öffentliche Schnittstellen, nicht über Implementierungsdetails. Code kann sich komplett ändern; Tests sollten das nicht. Ein guter Test liest sich wie eine Spezifikation: „user can checkout with valid cart“ sagt dir genau, welche Fähigkeit existiert, und er übersteht Refactorings, weil er sich nicht um interne Struktur kümmert.

Siehe [tests.md](tests.md) für Beispiele und [mocking.md](mocking.md) für Richtlinien zum Mocking.

## Nahtstellen (Seams): wo Tests hingehören

Eine **Nahtstelle (Seam)** ist die öffentliche Grenze, an der du testest: die Schnittstelle, an der du Verhalten beobachtest, ohne nach innen zu greifen. Tests befinden sich an Nahtstellen, niemals gegen Interna.

**Teste nur an vorab vereinbarten Nahtstellen.** Bevor du einen Test schreibst, halte die zu testenden Nahtstellen fest und stimme sie mit dem Nutzer ab. Kein Test wird an einer nicht bestätigten Nahtstelle geschrieben. Du kannst nicht alles testen, daher sorgt die vorherige Abstimmung der Nahtstellen dafür, dass der Testaufwand auf die kritischen Pfade und die komplexe Logik fällt, statt auf jeden Randfall.

Frage: „Was ist die öffentliche Schnittstelle, und welche Nahtstellen sollten wir testen?“

Wenn die Form dieser Schnittstelle selbst noch offen ist (wie tief das Modul ist, wohin die Nahtstelle gehört, was die Schnittstelle offenlegen sollte), rufe das Skill-Tool mit "codebase-design" für das Vokabular auf. Es ist die gemeinsame Quelle für die Begriffe Modul, Schnittstelle, Tiefe, Nahtstelle, Adapter, Hebelwirkung und Lokalität, und es ist eine Referenz zum Nachschlagen, keine auszuführende Session.

## Anti-Pattern

- **Implementierungsgekoppelt**: mockt interne Kollaborateure, testet private Methoden oder überprüft über einen Seitenkanal (fragt die Datenbank ab, statt die Schnittstelle zu nutzen). Das Erkennungsmerkmal: Der Test bricht, wenn du refaktorierst, obwohl sich das Verhalten nicht geändert hat.
- **Tautologisch**: Die Assertion berechnet den erwarteten Wert auf dieselbe Weise neu, wie es der Code tut (`expect(add(a, b)).toBe(a + b)`, ein Snapshot, der von Hand auf dieselbe Weise abgeleitet wurde, eine Konstante, die als gleich zu sich selbst behauptet wird), sodass er per Konstruktion besteht und niemals im Widerspruch zum Code stehen kann. Erwartete Werte müssen aus einer unabhängigen Quelle der Wahrheit stammen: einem bekannt guten Literal, einem durchgerechneten Beispiel, der Spec.
- **Horizontales Slicing**: erst alle Tests schreiben, dann die gesamte Implementierung. Tests in Masse verifizieren _eingebildetes_ Verhalten: Du testest die _Form_ der Dinge statt des nutzerseitigen Verhaltens, die Tests werden unempfindlich gegenüber echten Änderungen, und du legst dich auf eine Teststruktur fest, bevor du die Implementierung verstanden hast. Arbeite stattdessen in **vertikalen Slices**: ein Test → eine Implementierung → wiederholen, wobei jeder Test ein **Tracer Bullet** ist, der auf das reagiert, was dich der letzte Zyklus gelehrt hat.

## Regeln der Schleife

- **Rot vor Grün.** Schreibe zuerst den fehlschlagenden Test, dann nur so viel Code, wie nötig ist, um ihn zu bestehen. Antizipiere keine zukünftigen Tests und füge keine spekulativen Features hinzu.
- **Ein Slice nach dem anderen.** Eine Nahtstelle, ein Test, eine minimale Implementierung pro Zyklus.
- **Refactoring ist nicht Teil der Schleife.** Es gehört zur Review-Phase (siehe den `code-review`-Skill), nicht zum Rot-→-Grün-Implementierungszyklus.
