#!/usr/bin/env python3
"""
Regenerate everything derived from the two source files.

Sources of truth:
  writing-rules.md        the prompt
  reference/ai-tells.csv  the catalog

Generated:
  install/writing-rules.txt   plain text for paste boxes
  install/CLAUDE.md           Claude Code
  install/AGENTS.md           Codex and anything else reading AGENTS.md
  install/GEMINI.md           Gemini CLI
  install/writing-rules.mdc   Cursor, copy to .cursor/rules/
  install/Modelfile           Ollama
  reference/ai-tells.xlsx     same rows as the CSV

Usage:
  python tools/build.py            rewrite the generated files
  python tools/build.py --check    exit 1 if any generated file is out of date
"""
import csv, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SEP = "\n---\n"

AGENT_HEADER = """# Writing style

Scope: these rules cover prose that a person reads, including documentation,
README text, commit messages, pull request and issue descriptions, code
comments, and replies in this session. They do not apply to code itself,
command syntax, or strings that have to match something exactly.

"""

MDC_FRONTMATTER = """---
description: Write prose like a skilled human rather than an AI assistant. Apply to documentation, README text, comments, commit messages, and any prose the user will read. Does not apply to code.
globs:
alwaysApply: false
---

"""

MODELFILE_HEADER = """# Ollama writing model.
# Build it with:  ollama create writer -f Modelfile
# Then:           ollama run writer
# Change the FROM line to whichever local model you prefer.

FROM llama3.1

PARAMETER temperature 0.8

SYSTEM \"\"\"
"""


def read_rules():
    path = os.path.join(ROOT, "writing-rules.md")
    text = io.open(path, encoding="utf-8").read()
    if SEP not in text:
        sys.exit("writing-rules.md is missing the '---' separator line")
    return text.split(SEP, 1)[1].strip() + "\n"


def build_xlsx(rows, header):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment
    wb = Workbook()
    ws = wb.active
    ws.title = "AI telltale signs"
    ws.append(header)
    for r in rows:
        ws.append(r)
    for c in ws[1]:
        c.font = Font(bold=True)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for col, width in zip("ABCD", (16, 52, 62, 58)):
        ws.column_dimensions[col].width = width
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=True)
    return wb


def main():
    check = "--check" in sys.argv
    rules = read_rules()

    targets = {
        "install/writing-rules.txt": rules,
        "install/CLAUDE.md": AGENT_HEADER + rules,
        "install/AGENTS.md": AGENT_HEADER + rules,
        "install/GEMINI.md": AGENT_HEADER + rules,
        "install/writing-rules.mdc": MDC_FRONTMATTER + rules,
        "install/Modelfile": MODELFILE_HEADER + rules + '"""\n',
    }

    stale = []
    for rel, content in sorted(targets.items()):
        path = os.path.join(ROOT, rel)
        current = io.open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if current == content:
            print("  ok       %s" % rel)
            continue
        stale.append(rel)
        if check:
            print("  STALE    %s" % rel)
        else:
            io.open(path, "w", encoding="utf-8", newline="\n").write(content)
            print("  written  %s" % rel)

    csv_path = os.path.join(ROOT, "reference", "ai-tells.csv")
    xlsx_path = os.path.join(ROOT, "reference", "ai-tells.xlsx")
    rows = list(csv.reader(io.open(csv_path, encoding="utf-8-sig", newline="")))
    header, body = rows[0], [r for r in rows[1:] if any(c.strip() for c in r)]
    bad = [i for i, r in enumerate(body, 2) if len(r) != len(header)]
    if bad:
        sys.exit("ai-tells.csv rows have the wrong column count: %s" % bad[:10])

    if check:
        try:
            from openpyxl import load_workbook
            ws = load_workbook(xlsx_path).active
            xrows = [[("" if c.value is None else str(c.value)) for c in row]
                     for row in ws.iter_rows(min_row=2)]
            if xrows != body:
                stale.append("reference/ai-tells.xlsx")
                print("  STALE    reference/ai-tells.xlsx")
            else:
                print("  ok       reference/ai-tells.xlsx")
        except Exception as e:
            stale.append("reference/ai-tells.xlsx")
            print("  STALE    reference/ai-tells.xlsx (%s)" % e)
    else:
        build_xlsx(body, header).save(xlsx_path)
        print("  written  reference/ai-tells.xlsx (%d rows)" % len(body))

    if check and stale:
        print("\n%d file(s) out of date. Run: python tools/build.py" % len(stale))
        return 1
    print("\n%d catalog rows, %d generated files." % (len(body), len(targets) + 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
