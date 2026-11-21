![Human Writing Rules](Logo.png)

# Human Writing Rules

Writing rules that stop language models from writing like language models, a skill that applies them in the writer's own voice and learns from their feedback, a catalog of the habits it targets, and a script that checks a finished draft for the ones a machine can catch.

The product lives at humanwritingrules.com. This repo is private and is where it gets built.

## How it fits together

There are three layers, and the most specific one wins.

- Core: the always-on rules (`writing-rules.md`) and the storytelling course (`storytelling.md`). Everyone gets the same core. Updates replace it.
- Personal: one per writer, kept in `~/.human-writing-rules`. It holds the writer's voice samples, a short profile, the lessons the skill has learned from their reactions, and any rules they changed. Updates never touch it.
- Niche: rules for one channel or subject, such as LinkedIn, a newsletter or a website. A niche lives in the project it belongs to (`.human-writing-rules/niche.md`) or in the personal folder's `niches/`, and can point to existing files or skills instead of copying them.

Every style rule is on by default and can be changed by the writer in plain words ("I use em dashes"). The rules on evidence and invented stories can't be changed by any layer. `skill/SKILL.md` describes how the skill loads the layers, runs the optional first-time setup, and asks about one specific choice after a substantial piece so it can learn.

## Install

Claude Code and Codex, on a computer with Python 3:

```
python tools/build.py --install           Claude Code
python tools/build.py --install codex     Claude Code and Codex
```

This copies the skill into the tool's skills folder and writes the always-on rules into its global instructions file between marker lines. Nothing outside the markers changes, a dated copy of the instructions file is kept first, and the personal layer is never touched. Run it again after any rebuild.

Claude plugin: the repo root is a Claude plugin and marketplace (`.claude-plugin/`), with the skill in `skills/human-writing-rules/`.

claude.ai and ChatGPT: upload `dist/human-writing-rules.zip` as a skill. Where a tool can't save files, the skill offers an updated profile at the end of a session for the writer to attach next time.

Everything else: `install/README.md` lists paste-in files for tools without skills.

## What it changes

`examples/before.md` and `examples/after.md` tell the same story about a build pipeline migration. One was written the way models write by default, and the checker finds 33 problems in it, including unnamed sources, two negation reframes, a self-answered question, a Title Case header, and a Conclusion section that repeats what came before. Its rewrite reports clean and gives an actual failure rate where the original claimed productivity gains with no number behind them.

`skill/what-this-changes.md` is the one-page version for buyers, shown during setup.

## What's in here

`writing-rules.md` is the always-on rule set, organized into how the rules adjust, output separation, punctuation, banned words, banned phrases, sentence patterns, structure, storytelling, tone, evidence, people, vocabulary and formatting. Everything above its `---` line is commentary and everything below it is the prompt, which is also how the build script knows where to cut.

`storytelling.md` is the storytelling course written for a model: when a story helps, what it's for, who it's for, where the real material comes from, conflict, characters, a menu of story shapes, telling, and recipes for common jobs. It draws on ideas from Steve Rawling's Storyteller Tactics deck from Pip Decks without reproducing its text.

`skill/` holds the skill's own instructions and the buyer-facing summary. The build combines them with the rules, the course, the catalog and the checker into `skills/human-writing-rules/`.

`writing-rules-short.md` is a 1,497 character version for boxes that cap out, such as the 1,500 character limit on some ChatGPT plans.

`reference/ai-tells.csv` is the catalog: 178 rows across nine categories, with the tell, an example of it, and what a person would write instead. `reference/ai-tells.xlsx` is the same rows as a spreadsheet.

`tools/style-check.py` reports line numbers for characters you cannot type, the banned word and phrase lists, filler weight, depth adverbs, "is" substitutes, negation reframes, self-answered questions, anaphora, rule-of-three rhythm, tailing participles, unnamed sources, stacked one-line paragraphs, the banned opinion label, story cliches, stock persona introductions, engagement bait and performance tags, throat-clearing openers, Title Case headers, and sections named Conclusion. Unnamed anecdotes and claim-shaped absolutes are flagged for review. It exits 1 on findings and 0 when clean.

What it cannot judge is whether you took a position, whether the enthusiasm matches the subject, whether anything in your story changed, or whether an example is real. Those stay yours.

## Editing and rebuilding

The sources are `writing-rules.md`, `storytelling.md`, `skill/`, `reference/ai-tells.csv` and `tools/style-check.py`. Everything in `install/` and `skills/`, plus the spreadsheet and the zip, is generated from them.

```
python tools/build.py           rewrite the generated files
python tools/build.py --check   exit 1 if anything is out of date
```

The check mode runs in CI on every push. Building the spreadsheet needs `openpyxl`, and nothing else has dependencies.

## Behavior that looks like a bug

Running the checker on `reference/ai-tells.csv` or on the rules files lights up, because they hold specimens of the exact things it looks for. The filler-weight group fires on legitimate technical writing, where a significant digit really is significant, so treat it as a prompt to look. The same goes for every finding marked REVIEW.

## Copyright

Copyright 2026 David Soden. All rights reserved.
