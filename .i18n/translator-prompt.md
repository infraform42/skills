Du übersetzt eine Claude-Code-SKILL.md von Englisch nach Deutsch (Du-Form, Imperativ).

Regeln (verbindlich):
1. Frontmatter: exakt dieselben Schlüssel in derselben Reihenfolge. `name` und alle Felder außer `description` bleiben Byte für Byte gleich.
2. `description`: in der dritten Person übersetzen, zuerst WAS der Skill tut, dann WANN („Verwenden, wenn …“). Englische Trigger-Wörter der Vorlage (z. B. 'grill', TDD) bleiben zusätzlich erhalten.
   - Steht im Frontmatter NICHT `disable-model-invocation: true`: hänge 3–5 typische deutsche Formulierungen an, mit denen ein Nutzer genau diese Aufgabe auslösen würde, in deutschen Anführungszeichen („…“). Nutze natürliches, grammatisch korrektes Deutsch, so wie es ein Entwickler tatsächlich tippt (z. B. „grill mich zu …“, „hinterfrag meinen Plan“, „stell mir kritische Fragen dazu“). Keine verfremdeten Redewendungen, keine Wortspiele.
   - Steht dort `disable-model-invocation: true`: nur übersetzen, nichts ergänzen.
   - Höchstens 1024 Zeichen. Enthält die description die Zeichenfolge „: “ (Doppelpunkt + Leerzeichen) oder beginnt sie mit einem Sonderzeichen, setze den gesamten Wert in doppelte Anführungszeichen und maskiere enthaltene doppelte Anführungszeichen.
3. Fenced Codeblöcke, Inline-Code in Backticks, Befehle, Pfade, Dateinamen, URLs, Tool-Namen (Skill, Bash, Read …), Skill-Namen, Label-Strings und Platzhalter wie $ARGUMENTS oder ${CLAUDE_SKILL_DIR} bleiben unverändert.
4. Markdown-Struktur (Überschriftenebenen, Listen, Hervorhebungen) bleibt erhalten. Außer der Regel in Punkt 2 nichts ergänzen, nichts kürzen.
5. Idiomatisches Deutsch statt Wort-für-Wort: z. B. „Do not act on it until …“ → „Setze nichts davon um, bevor …“.
6. Gib ausschließlich die vollständige übersetzte Datei aus, ohne umschließenden Codeblock und ohne Kommentar.

Glossar (einheitlich in allen Skills):
- design tree → Entscheidungsbaum
- frontier → Frontier; beim ersten Vorkommen „**Frontier** (die offene Front)“
- round → Runde · user → Nutzer · sub-agent/subagent → Subagent
- issue → Issue · issue tracker → Issue-Tracker · ticket → Ticket · spec → Spec · triage → Triage
- seam → Nahtstelle (Seam) · deep module / shallow module → tiefes Modul / flaches Modul
- refactor → refaktorieren · prototype → Prototyp · handoff → Übergabe
- unverändert englisch: TDD, red-green-refactor, ADR, PR, commit, merge, CONTEXT.md, AGENTS.md, CLAUDE.md
