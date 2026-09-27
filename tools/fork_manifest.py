#!/usr/bin/env python3
"""Setzt die Fork-Namen in plugin.json und marketplace.json. Nach jedem Upstream-Merge ausführen."""
import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / ".claude-plugin"
PLUGIN = "mattpocock-skills-de"
REPO = "https://github.com/infraform42/skills"
DESC = "Matt Pococks Agent-Skills auf Deutsch (Fork von mattpocock/skills)."


def rw(name, fn):
    p = DIR / name
    data = json.loads(p.read_text())
    fn(data)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def plugin(m):
    m.update(name=PLUGIN, description=DESC, repository=REPO, homepage=REPO)
    m.pop("version", None)


def market(m):
    m["name"] = "infraform42"
    m["owner"] = {"name": "infraform42"}
    m["description"] = DESC
    for e in m.get("plugins", []):
        if e.get("name", "").startswith("mattpocock-skills"):
            e.update(name=PLUGIN, description=DESC)
            e.pop("version", None)


rw("plugin.json", plugin)
rw("marketplace.json", market)
