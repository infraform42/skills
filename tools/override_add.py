#!/usr/bin/env python3
"""Übernimmt die aktuelle deutsche description von Skills in .i18n/overrides.yaml.

Aufruf (Mac, Fork-Repo ~/src/skills-de, venv aktiv):
  python tools/override_add.py skills/engineering/tdd/SKILL.md [weitere Pfade …]

Pro Pfad gespeichert:
  description     – exakt der aktuelle Wert aus der deutschen SKILL.md (Handkorrekturen inklusive)
  source_sha256   – Hash der englischen Quelle auf main zum Zeitpunkt des Overrides;
                    weicht er später ab, meldet i18n.py beim Übersetzen einen HINWEIS.
Vorhandene Einträge anderer Pfade bleiben erhalten.
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OVR = ROOT / ".i18n" / "overrides.yaml"
HEADER = (
    "# Feste deutsche Werte, die nach jeder Übersetzung gesetzt werden (Pfad → Feld → Wert).\n"
    "# source_sha256 = englische Quelle (main) beim Anlegen; weicht sie ab, meldet i18n.py einen HINWEIS.\n"
    "# Pflege: python tools/override_add.py <pfad/SKILL.md> …\n"
)


def description_of(path: str) -> str:
    text = (ROOT / path).read_text()
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise ValueError(f"{path}: kein Frontmatter")
    return (yaml.safe_load(m.group(1)) or {})["description"]


def source_hash(path: str) -> str:
    src = subprocess.run(["git", "show", f"main:{path}"], cwd=ROOT, check=True,
                         capture_output=True, text=True).stdout
    return hashlib.sha256(src.encode()).hexdigest()


def main(paths: list[str]) -> None:
    if not paths:
        sys.exit(__doc__)
    data = (yaml.safe_load(OVR.read_text()) if OVR.exists() else None) or {}
    for p in paths:
        data[p] = {"description": description_of(p), "source_sha256": source_hash(p)}
        print(f"übernommen: {p}")
    OVR.write_text(HEADER + yaml.safe_dump(data, allow_unicode=True, sort_keys=True, width=10**6))
    yaml.safe_load(OVR.read_text())  # Rundlauf-Prüfung
    print(f"geschrieben: {OVR.relative_to(ROOT)} ({len(data)} Einträge)")


if __name__ == "__main__":
    main(sys.argv[1:])
