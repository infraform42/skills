---
name: setup-matt-pocock-skills
description: "Konfiguriert dieses Repo für die Engineering-Skills: richtet den Issue-Tracker, das Triage-Label-Vokabular und das Layout der Domain-Docs ein. Einmalig vor der ersten Nutzung der anderen Engineering-Skills ausführen."
disable-model-invocation: true
---

# Richte Matt Pococks Skills ein

Lege die Repo-spezifische Konfiguration an, von der die Engineering-Skills ausgehen:

- **Issue-Tracker**: wo Issues verwaltet werden (standardmäßig GitHub; lokales Markdown wird ebenfalls von Haus aus unterstützt)
- **Triage-Labels**: die Strings für die fünf kanonischen Triage-Rollen
- **Domain-Docs**: wo `CONTEXT.md` und ADRs liegen, sowie die Regeln für Konsumenten, die sie lesen

Dies ist ein prompt-gesteuerter Skill, kein deterministisches Skript. Erkunde, präsentiere, was du gefunden hast, hol dir die Bestätigung des Nutzers und schreibe dann.

## Ablauf

### 1. Erkunden

Sieh dir das aktuelle Repo an, um seinen Ausgangszustand zu verstehen. Lies, was vorhanden ist; nimm nichts an:

- `git remote -v` und `.git/config`: Ist das ein GitHub-Repo? Welches?
- `AGENTS.md` und `CLAUDE.md` im Repo-Root: Existiert eine davon? Gibt es dort bereits einen Abschnitt `## Agent skills`?
- `CONTEXT.md` und `CONTEXT-MAP.md` im Repo-Root
- `docs/adr/` und etwaige `src/*/docs/adr/`-Verzeichnisse
- `docs/agents/`: Existiert die frühere Ausgabe dieses Skills bereits?
- `.scratch/`: ein Hinweis darauf, dass bereits eine lokale-Markdown-Issue-Tracker-Konvention verwendet wird
- Ist der Skill `triage` installiert? (ein `triage`-Skill-Ordner neben diesem, oder `triage` unter deinen verfügbaren Skills.) Das entscheidet, ob Abschnitt B überhaupt läuft.
- Monorepo-Signale: eine `pnpm-workspace.yaml`, ein `workspaces`-Feld in `package.json`, oder ein befülltes `packages/*` mit eigenem `src/`. Diese treten nur bei einem wirklich großen Multi-Package-Repo auf; ihr Fehlen bedeutet Single-Context, was auf fast jedes Repo zutrifft.

### 2. Ergebnisse präsentieren und nachfragen

Fasse zusammen, was vorhanden ist und was fehlt. Gehe die Abschnitte dann der Reihe nach durch. Ein Abschnitt, eine Antwort, dann der nächste.

Leite jeden Abschnitt mit der empfohlenen Antwort ein, damit der Nutzer sie mit einem Wort akzeptieren kann. Gib nur dann eine einzeilige Erklärung, wenn die Wahl tatsächlich verzweigt; überspringe den Abschnitt komplett, wenn die Erkundung das bereits geklärt hat (Abschnitt B, wenn `triage` nicht installiert ist, Abschnitt C, wenn es kein Monorepo gibt).

**Abschnitt A: Issue-Tracker.**

> Erklärung: Der „Issue-Tracker“ ist der Ort, an dem die Issues für dieses Repo geführt werden. Skills wie `to-tickets`, `triage` und `to-spec` lesen daraus und schreiben dorthin. Sie müssen wissen, ob sie `gh issue create` aufrufen, eine Markdown-Datei unter `.scratch/` schreiben oder einem anderen von dir beschriebenen Workflow folgen sollen. Wähle den Ort, an dem du die Arbeit an diesem Repo tatsächlich trackst.

Standardhaltung: Diese Skills wurden für GitHub entworfen. Zeigt ein `git remote` auf GitHub, schlage das vor. Zeigt ein `git remote` auf GitLab (`gitlab.com` oder einen selbst gehosteten Host), schlage GitLab vor. Andernfalls (oder wenn der Nutzer es bevorzugt) biete an:

- **GitHub**: Issues liegen in den GitHub Issues des Repos (nutzt die `gh`-CLI)
- **GitLab**: Issues liegen in den GitLab Issues des Repos (nutzt die [`glab`](https://gitlab.com/gitlab-org/cli)-CLI)
- **Lokales Markdown**: Issues liegen als Dateien unter `.scratch/<feature>/` in diesem Repo (gut für Solo-Projekte oder Repos ohne Remote)
- **Sonstiges** (Jira, Linear usw.): bitte den Nutzer, den Workflow in einem Absatz zu beschreiben; der Skill hält ihn als freien Fließtext fest

Halte die Wahl in `docs/agents/issue-tracker.md` fest. Die GitHub- und GitLab-Vorlagen tragen ein Flag „PRs as a request surface“, standardmäßig **aus**. Lass es aus und sprich es nicht an: Ein Nutzer, der externe PRs in der Triage-Queue haben möchte, kann das Flag später in der Datei umschalten.

**Abschnitt B: Triage-Label-Vokabular.** Überspringe diesen Abschnitt komplett, wenn der Skill `triage` nicht installiert ist (das hat dir die Erkundung schon gesagt), da ein nicht installierter Skill keine Labels braucht.

Ist er installiert, stelle genau eine Frage:

> Möchtest du die Standard-Triage-Labels beibehalten? (empfohlen: **ja**)

Die Standardwerte sind die fünf kanonischen Rollen, jeder Label-String entspricht seinem Namen: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. Bei **ja** schreibe sie unverändert. Nur wenn der Nutzer nein sagt, meist weil sein Tracker bereits andere Namen verwendet (z. B. `bug:triage` für `needs-triage`), sammle die Overrides, damit `triage` bestehende Labels anwendet, statt Duplikate anzulegen.

**Abschnitt C: Domain-Docs.** Standard ist **Single-Context** (eine `CONTEXT.md` + `docs/adr/` im Repo-Root). Das passt auf fast jedes Repo; schreibe es, ohne zu fragen.

Biete **Multi-Context** (eine `CONTEXT-MAP.md` im Root, die auf kontextspezifische `CONTEXT.md`-Dateien verweist) nur an, wenn die Erkundung Monorepo-Signale gefunden hat. Bestätige anschließend, welches Layout gewünscht ist.

### 3. Bestätigen und bearbeiten

Zeig dem Nutzer einen Entwurf von:

- Dem Block `## Agent skills`, der in `CLAUDE.md` bzw. `AGENTS.md` eingefügt wird, je nachdem, welche Datei bearbeitet wird (Auswahlregeln siehe Schritt 4)
- Dem Inhalt von `docs/agents/issue-tracker.md`, `docs/agents/domain.md` und `docs/agents/triage-labels.md` (letztere nur, wenn `triage` installiert ist)

Lass ihn Änderungen vornehmen, bevor du schreibst.

### 4. Schreiben

**Wähle die zu bearbeitende Datei:**

- Existiert `CLAUDE.md`, bearbeite sie.
- Andernfalls, wenn `AGENTS.md` existiert, bearbeite sie.
- Existiert keine von beiden, frage den Nutzer, welche angelegt werden soll; entscheide nicht für ihn.

Lege niemals `AGENTS.md` an, wenn `CLAUDE.md` bereits existiert (und umgekehrt); bearbeite immer die bereits vorhandene Datei.

Existiert in der gewählten Datei bereits ein `## Agent skills`-Block, aktualisiere dessen Inhalt an Ort und Stelle, statt ein Duplikat anzuhängen. Überschreibe keine Nutzeränderungen in den umgebenden Abschnitten.

Der Block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

Nimm den Unterblock `### Triage labels` nur auf und schreibe `docs/agents/triage-labels.md` nur, wenn `triage` installiert ist und Abschnitt B gelaufen ist. Andernfalls entfallen beide.

Schreibe dann die Doku-Dateien und nutze dabei die Seed-Vorlagen in diesem Skill-Ordner als Ausgangspunkt:

- [issue-tracker-github.md](./issue-tracker-github.md): GitHub-Issue-Tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md): GitLab-Issue-Tracker
- [issue-tracker-local.md](./issue-tracker-local.md): lokaler-Markdown-Issue-Tracker
- [triage-labels.md](./triage-labels.md): Label-Mapping (nur, wenn `triage` installiert ist)
- [domain.md](./domain.md): Konsumentenregeln für Domain-Docs + Layout

Schreibe bei „sonstigen“ Issue-Trackern `docs/agents/issue-tracker.md` von Grund auf, basierend auf der Beschreibung des Nutzers.

### 5. Fertig

Teile dem Nutzer mit, dass die Einrichtung abgeschlossen ist und welche Engineering-Skills nun aus diesen Dateien lesen. Erwähne, dass er `docs/agents/*.md` später direkt bearbeiten kann; ein erneutes Ausführen dieses Skills ist nur nötig, wenn er den Issue-Tracker wechseln oder von vorn beginnen möchte.
