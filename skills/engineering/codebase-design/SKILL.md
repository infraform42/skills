---
name: codebase-design
description: Stellt ein gemeinsames Vokabular zum Entwerfen tiefer Module bereit. Verwenden, wenn der Nutzer das Interface eines Moduls entwerfen oder verbessern möchte, Vertiefungsmöglichkeiten finden möchte, entscheiden möchte, wo eine Nahtstelle (seam) verläuft, Code testbarer oder KI-navigierbarer machen möchte, oder wenn ein anderer Skill das Vokabular für tiefe Module benötigt. „Wie entwerfe ich das Interface für dieses Modul?“, „hilf mir, dieses Modul zu vertiefen“, „wo sollte die Nahtstelle liegen?“, „mach diesen Code testbarer“, „ist mein Modul zu flach?“
---

# Codebase-Design

Entwerfe **tiefe Module**: viel Verhalten hinter einem kleinen Interface, platziert an einer sauberen Nahtstelle (Seam), testbar durch dieses Interface. Verwende diese Sprache und diese Prinzipien überall dort, wo Code entworfen oder umstrukturiert wird. Das Ziel ist Leverage für Aufrufer, Locality für Maintainer und Testbarkeit für alle.

## Glossar

Verwende diese Begriffe exakt: Ersetze sie nicht durch „Component", „Service", „API" oder „Boundary". Konsistente Sprache ist der ganze Sinn der Sache.

**Modul**: alles mit einem Interface und einer Implementierung. Bewusst skalen-agnostisch: eine Funktion, eine Klasse, ein Package oder ein ebenenübergreifender Ausschnitt. _Vermeide_: Unit, Component, Service.

**Interface**: alles, was ein Aufrufer wissen muss, um das Modul korrekt zu verwenden: die Typsignatur, aber auch Invarianten, Reihenfolgebeschränkungen, Fehlermodi, erforderliche Konfiguration und Performance-Eigenschaften. _Vermeide_: API, Signatur (zu eng gefasst, sie beziehen sich nur auf die Oberfläche auf Typebene).

**Implementierung**: das, was in einem Modul steckt, sein Code-Körper. Zu unterscheiden von **Adapter**: Etwas kann ein kleiner Adapter mit großer Implementierung sein (ein Postgres-Repo) oder ein großer Adapter mit kleiner Implementierung (ein In-Memory-Fake). Greife zu „Adapter", wenn die Nahtstelle (Seam) das Thema ist; sonst zu „Implementierung".

**Tiefe** (Depth): Leverage am Interface. Die Menge an Verhalten, die ein Aufrufer (oder Test) pro Einheit Interface, die er lernen muss, nutzen kann. Ein Modul ist **tief**, wenn hinter einem kleinen Interface eine große Menge Verhalten steckt, **flach**, wenn das Interface nahezu so komplex ist wie die Implementierung.

**Nahtstelle (Seam)** _(Michael Feathers)_: eine Stelle, an der du Verhalten ändern kannst, ohne dort zu editieren; der *Ort*, an dem das Interface eines Moduls lebt. Wo die Nahtstelle (Seam) platziert wird, ist eine eigene Designentscheidung, getrennt davon, was dahinter steckt. _Vermeide_: Boundary (überladen durch DDDs Bounded Context).

**Adapter**: ein konkretes Ding, das ein Interface an einer Nahtstelle (Seam) erfüllt. Beschreibt die *Rolle* (welchen Slot es ausfüllt), nicht die Substanz (was drinsteckt).

**Leverage** (Hebelwirkung): was Aufrufer von Tiefe bekommen. Mehr Fähigkeiten pro Einheit Interface, die sie lernen. Eine Implementierung zahlt sich über N Aufrufstellen und M Tests aus.

**Locality** (Lokalität): was Maintainer von Tiefe bekommen. Änderungen, Bugs, Wissen und Verifikation konzentrieren sich an einer Stelle, statt sich über Aufrufer zu verteilen. Einmal fixen, überall behoben.

## Tief vs. flach

**Tiefes Modul** = kleines Interface + viel Implementierung:

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
└─────────────────────┘
```

**Flaches Modul** = großes Interface + wenig Implementierung (vermeiden):

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

Frage bei der Gestaltung eines Interfaces:

- Kann ich die Anzahl der Methoden reduzieren?
- Kann ich die Parameter vereinfachen?
- Kann ich mehr Komplexität im Inneren verbergen?

## Prinzipien

- **Tiefe ist eine Eigenschaft des Interfaces, nicht der Implementierung.** Ein tiefes Modul kann intern aus kleinen, mockbaren, austauschbaren Teilen zusammengesetzt sein; sie sind nur nicht Teil des Interfaces. Ein Modul kann sowohl **interne Nahtstellen (Seams)** (privat für seine Implementierung, von seinen eigenen Tests genutzt) als auch die **externe Nahtstelle (Seam)** an seinem Interface haben.
- **Der Löschtest.** Stell dir vor, du löschst das Modul. Verschwindet die Komplexität, war es nur ein Durchreicher. Taucht die Komplexität bei N Aufrufern wieder auf, hat es sich gelohnt.
- **Das Interface ist die Testfläche.** Aufrufer und Tests überqueren dieselbe Nahtstelle (Seam). Wenn du *am* Interface vorbei testen willst, hat das Modul wahrscheinlich die falsche Form.
- **Ein Adapter bedeutet eine hypothetische Nahtstelle (Seam). Zwei Adapter bedeuten eine reale.** Führe keine Nahtstelle (Seam) ein, wenn nicht tatsächlich etwas darüber variiert.

## Entwurf für Testbarkeit

Gute Interfaces machen Testen selbstverständlich:

1. **Nimm Abhängigkeiten entgegen, erzeuge sie nicht selbst.**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **Gib Ergebnisse zurück, statt Seiteneffekte zu erzeugen.**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **Kleine Oberfläche.** Weniger Methoden = weniger nötige Tests. Weniger Parameter = einfacheres Test-Setup.

## Beziehungen

- Ein **Modul** hat genau ein **Interface** (die Oberfläche, die es Aufrufern und Tests präsentiert).
- **Tiefe** ist eine Eigenschaft eines **Moduls**, gemessen an seinem **Interface**.
- Eine **Nahtstelle (Seam)** ist der Ort, an dem das **Interface** eines **Moduls** lebt.
- Ein **Adapter** sitzt an einer **Nahtstelle (Seam)** und erfüllt das **Interface**.
- **Tiefe** erzeugt **Leverage** für Aufrufer und **Locality** für Maintainer.

## Verworfene Rahmungen

- **Tiefe als Verhältnis von Implementierungszeilen zu Interfacezeilen** (Ousterhout): belohnt das Aufblähen der Implementierung. Wir verwenden stattdessen Tiefe-als-Leverage.
- **„Interface" als das TypeScript-Schlüsselwort `interface` oder die öffentlichen Methoden einer Klasse**: zu eng gefasst: Interface umfasst hier jede Tatsache, die ein Aufrufer wissen muss.
- **„Boundary"**: überladen durch DDDs Bounded Context. Sag **Nahtstelle (Seam)** oder **Interface**.

## Weiter vertiefen

- **Einen Cluster anhand seiner Abhängigkeiten vertiefen**, siehe [DEEPENING.md](DEEPENING.md): Abhängigkeitskategorien, Disziplin bei der Nahtstelle (Seam) und Replace-don't-layer-Testing.
- **Alternative Interfaces erkunden**, siehe [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md): Starte parallele Subagenten, die das Interface auf mehrere radikal unterschiedliche Arten entwerfen, und vergleiche dann anhand von Tiefe, Lokalität und Platzierung der Nahtstelle (Seam).
