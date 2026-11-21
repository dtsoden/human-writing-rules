#!/usr/bin/env python3
"""
Build Human Writing Rules from its sources, and optionally install it.

Sources of truth:
  writing-rules.md          the always-on rules
  storytelling.md           the storytelling course
  skill/SKILL.md            the skill's own instructions
  skill/what-this-changes.md  the buyer-facing summary shown at setup
  reference/ai-tells.csv    the catalog
  tools/style-check.py      the checker

Generated:
  install/writing-rules.txt   plain text for paste boxes
  install/CLAUDE.md           Claude Code
  install/AGENTS.md           Codex and anything else reading AGENTS.md
  install/GEMINI.md           Gemini CLI
  install/writing-rules.mdc   Cursor, copy to .cursor/rules/
  install/Modelfile           Ollama
  skills/human-writing-rules/ the skill, also the Claude plugin's skill
  reference/ai-tells.xlsx     same rows as the CSV
  dist/human-writing-rules.zip  the skill folder zipped, for upload
                              (not checked, not committed)

Usage:
  python tools/build.py                   rewrite the generated files
  python tools/build.py --check           exit 1 if any generated file is out of date
  python tools/build.py --install         install for Claude Code on this computer
  python tools/build.py --install codex   install for Codex as well

--install copies the skill into the tool's skills folder and writes the
always-on rules into the tool's global instructions file between marker
lines. It never changes anything outside those markers, keeps a dated copy
of the instructions file before changing it, and never touches the user's
personal layer (~/.human-writing-rules).
"""
import csv, io, os, shutil, sys, time, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_NAME = "human-writing-rules"
SKILL_DIR = "skills/" + SKILL_NAME

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

MARK_START = "<!-- human-writing-rules:start (managed by the installer, edits inside are replaced) -->"
MARK_END = "<!-- human-writing-rules:end -->"

BLOCK_HEADER = """## Writing style (Human Writing Rules)

Scope: prose a person reads, including replies, documentation, commit
messages, comments and pull request text. Not code, command syntax, or
strings that have to match exactly. For drafted pieces, storytelling, the
writer's personal profile and learning from feedback, use the
`human-writing-rules` skill. The writer's own profile, lessons and niches
win over these defaults wherever they disagree.

"""


def read(rel):
    return io.open(os.path.join(ROOT, rel), encoding="utf-8").read()


def read_part(rel):
    text = read(rel)
    if SEP not in text:
        sys.exit("%s is missing the '---' separator line" % rel)
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


def targets():
    rules = read_part("writing-rules.md")
    skill = {
        SKILL_DIR + "/SKILL.md": read("skill/SKILL.md"),
        SKILL_DIR + "/references/rules.md": "# Human Writing Rules: the always-on rules\n\n" + rules,
        SKILL_DIR + "/references/storytelling.md": "# Storytelling\n\n" + read_part("storytelling.md"),
        SKILL_DIR + "/references/what-this-changes.md": read("skill/what-this-changes.md"),
        SKILL_DIR + "/references/ai-tells.csv": read("reference/ai-tells.csv"),
        SKILL_DIR + "/scripts/style-check.py": read("tools/style-check.py"),
    }
    t = {
        "install/writing-rules.txt": rules,
        "install/CLAUDE.md": AGENT_HEADER + rules,
        "install/AGENTS.md": AGENT_HEADER + rules,
        "install/GEMINI.md": AGENT_HEADER + rules,
        "install/writing-rules.mdc": MDC_FRONTMATTER + rules,
        "install/Modelfile": MODELFILE_HEADER + rules + '"""\n',
    }
    t.update(skill)
    return t, rules


def write_zip():
    src = os.path.join(ROOT, SKILL_DIR)
    out = os.path.join(ROOT, "dist", SKILL_NAME + ".zip")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(src):
            for f in sorted(files):
                full = os.path.join(base, f)
                z.write(full, os.path.join(SKILL_NAME, os.path.relpath(full, src)))
    print("  written  dist/%s.zip" % SKILL_NAME)


def write_block(path, rules):
    """Put the always-on rules between the markers in path, leaving the rest alone."""
    block = MARK_START + "\n" + BLOCK_HEADER + rules + MARK_END
    current = io.open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    if current:
        stamp = time.strftime("%Y%m%d-%H%M%S")
        shutil.copy2(path, path + ".before-hwr-" + stamp)
    if MARK_START in current and MARK_END in current:
        head, rest = current.split(MARK_START, 1)
        tail = rest.split(MARK_END, 1)[1]
        new = head + block + tail
    else:
        new = current.rstrip("\n") + ("\n\n" if current else "") + block + "\n"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, "w", encoding="utf-8", newline="").write(new)
    print("  block    %s" % path)


def install(tools, rules):
    home = os.path.expanduser("~")
    places = {
        "claude": (os.path.join(home, ".claude", "skills"), os.path.join(home, ".claude", "CLAUDE.md")),
        "codex": (os.path.join(home, ".codex", "skills"), os.path.join(home, ".codex", "AGENTS.md")),
    }
    for tool in tools:
        skills_dir, instructions = places[tool]
        dest = os.path.join(skills_dir, SKILL_NAME)
        src = os.path.join(ROOT, SKILL_DIR)
        # Update in place rather than delete the folder: a running tool may
        # hold the folder open, and Windows then refuses to remove it.
        shutil.copytree(src, dest, dirs_exist_ok=True)
        keep = {os.path.relpath(os.path.join(b, f), src)
                for b, _, fs in os.walk(src) for f in fs}
        for b, _, fs in os.walk(dest):
            for f in fs:
                rel = os.path.relpath(os.path.join(b, f), dest)
                if rel not in keep:
                    os.remove(os.path.join(dest, rel))
        print("  skill    %s" % dest)
        write_block(instructions, rules)
    print("\nPersonal layer (never touched): %s" % os.path.join(home, ".human-writing-rules"))


def main():
    args = sys.argv[1:]
    check = "--check" in args
    t, rules = targets()

    stale = []
    for rel, content in sorted(t.items()):
        path = os.path.join(ROOT, rel)
        current = io.open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if current == content:
            print("  ok       %s" % rel)
            continue
        stale.append(rel)
        if check:
            print("  STALE    %s" % rel)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
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
        write_zip()

    if check and stale:
        print("\n%d file(s) out of date. Run: python tools/build.py" % len(stale))
        return 1
    print("\n%d catalog rows, %d generated files." % (len(body), len(t) + 1))

    if "--install" in args:
        tools = [a for a in args if a in ("claude", "codex")] or ["claude"]
        if "claude" not in tools:
            tools.insert(0, "claude")
        install(tools, rules)
    return 0


if __name__ == "__main__":
    sys.exit(main())
