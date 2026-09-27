---
name: wizard
description: Generiert einen interaktiven Bash-Wizard, der einen Menschen Schritt für Schritt durch eine manuelle Prozedur führt, die nur er selbst ausführen kann. Wird verwendet beim Provisionieren von Infrastruktur, beim Einrichten von Credentials oder CI-Secrets, beim Durchlaufen eines unbekannten Drittanbieter-Dashboards oder bei einer einmaligen Migration oder Umstellung (cutover). Nicht aufrufen für Schritte, die der Agent selbst ausführen kann. „erstell mir einen Wizard für das Setup“, „bau mir ein Skript, das mich durch die Einrichtung führt“, „ich brauch eine geführte Schritt-für-Schritt-Anleitung als Bash-Skript“, „leg mir einen Setup-Wizard für die Credentials an“, „schreib mir ein Skript für die Migration, das mich durchklickt“
---

# Wizard

Ein **Wizard** ist ein Bash-Skript, das einen Menschen Schritt für Schritt durch eine manuelle Prozedur führt, die mühsam von Hand zu erledigen und mühsam jedes Mal neu einer KI zu erklären ist. Es öffnet jede URL, sagt genau, was zu klicken und zu kopieren ist, erfasst die Werte, schreibt sie dorthin, wo sie hingehören (`.env`, GitHub-Secrets), bestätigt bei jeder Stufe und zeigt, wie viele Stufen noch übrig sind. Es kann Drittanbieter-Dienste konfigurieren, eine einmalige Migration durchführen oder das Projekt von einem Zustand in einen anderen überführen.

Die angenehme UX ist bereits durch [template.sh](template.sh) gelöst: Fortschritt Stufe für Stufe, Bestätigungs-Gates, plattformübergreifendes Öffnen von URLs (auch unter WSL), verdeckte Eingabe von Secrets, idempotente `.env`-Upserts, `gh secret`/`gh variable`-Schreibvorgänge und eine abschließende Zusammenfassung. **Deine Aufgabe ist nur, die Prozedur einzugrenzen und ihre Stufen zu verfassen.** Die Bibliothek oberhalb der `STAGES`-Markierung ist in jedem Wizard identisch; diese Konsistenz ist der Sinn der Sache: Bearbeite sie nie von Hand.

Ein Wizard ist standardmäßig vergänglich: gebaut für einen einzigen Durchlauf, gespeichert unter einem Scratch- oder `scripts/`-Pfad, gelöscht, sobald die Aufgabe erledigt ist. Committe ihn nur, wenn der Nutzer einen wiederholbaren Setup-Pfad möchte, der im Repo bleiben soll.

## Prozess

### 1. Die Prozedur eingrenzen

Arbeite jeden manuellen Schritt heraus, den der Mensch ausführen muss, und jeden Wert, der dabei erfasst wird. Lies zuerst das Repo, frag nicht ins Blaue:

- Für ein Setup: `.env`, `.env.example`, `.env.*`, `README`, `docker-compose*`, Framework-Konfiguration und `.github/workflows/*` (jede `secrets.*`/`vars.*`-Referenz ist ein Wert, den der Wizard erzeugen muss).
- Für eine Migration oder Umstellung: den aktuellen Zustand, den Zielzustand und die nicht umkehrbaren Aktionen dazwischen.

Zeig dem Nutzer anschließend die geordnete Liste der Stufen und die Werte, die jede davon erzeugt, und lass sie bestätigen: Er darf ergänzen, streichen oder umsortieren.

**Fertig, wenn:** jede Stufe der Reihe nach benannt ist und du für jeden erfassten Wert weißt, (a) woher der Mensch ihn bekommt, (b) wohin er geschrieben wird (`.env`, ein GitHub-Secret, beides oder nirgendwohin; manche Stufen sind reine Aktionen), und (c) ob er geheim ist (verdeckte Eingabe) oder öffentlich.

### 2. Den Weg jeder Stufe abbilden

Schreib für jede Stufe den genauen Pfad, dem ein Mensch folgt: welche URL zu öffnen ist, was dort zu tun ist, wo ein Wert angezeigt wird, welche Variable er befüllt: z. B. "Dashboard → Developers → API keys → Reveal test key → copy". Wo du die aktuelle UI oder den genauen Befehl nicht wirklich kennst, sag das und frag den Nutzer oder sieh in der Dokumentation nach: Erfinde nie Schritte, die es vielleicht nicht gibt.

**Fertig, wenn:** jede Stufe zu konkreten Anweisungen führt, denen ein Fremder folgen könnte.

### 3. Den Wizard verfassen

Kopiere `template.sh` an den Zielpfad. Ersetze die Beispielstufe durch einen `stage`-Aufruf pro Schritt, in Abhängigkeitsreihenfolge. Nutze die Bibliotheks-Helper: `stage`, `say`/`step`, `open_url`, `ask`/`ask_secret`, `write_env`, `set_secret`/`set_var`, `pause`/`confirm`. Setze `TOTAL_STAGES` auf die Anzahl der Stufen, die du geschrieben hast.

Halte den Standard, den das Template setzt: Öffne die URL, bevor du nach ihrem Wert fragst, nutze `ask_secret` für alles Geheime, schreibe mit `write_env` jeden persistierten Wert, setze mit `set_secret` nur die Werte, die CI tatsächlich braucht, und bestätige mit `confirm` vor jeder nicht umkehrbaren Aktion. Jede `stage` leert den Bildschirm, sodass nur der aktuelle Schritt sichtbar ist: Halte eine Stufe auf eine fokussierte Aufgabe beschränkt, damit dem Menschen nichts Benötigtes wegscrollt. Fass die Bibliothek oberhalb der Markierung nicht an.

### 4. Prüfen und übergeben

- `bash -n <script>`; führe `shellcheck` aus, falls verfügbar.
- `chmod +x <script>`.
- Führe es nicht selbst end-to-end aus: Es öffnet Browser und blockiert auf menschliche Eingabe. Verfolge es stattdessen statisch: Jeder Wert aus Schritt 1 wird erfasst und landet dort, wo Schritt 1 es festgelegt hat, und jeder `set_secret`-Name entspricht exakt einer `secrets.*`-Referenz in CI.
- Sag dem Nutzer, wie er es ausführt. Falls es ein wiederholbarer Setup-Pfad ist, committe ihn und verlinke ihn aus der README, damit die nächste Person das Skript ausführt, statt eine KI zu fragen.
