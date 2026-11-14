![Human Writing Rules](Logo.png)

# Human writing rules

A prompt that stops language models from writing like language models, a catalog of the habits it targets, and a script that checks a finished draft for the ones a machine can catch.

These three pieces work together. Put the prompt in before anything is written, run the checker over the draft afterward, and open the catalog when you disagree with a finding and want the reasoning behind it.

## Quick start

Paste `writing-rules.md` into wherever your tool keeps standing instructions. The `install/` folder has the same text already shaped for specific tools, and `install/README.md` says which file goes where.

Then check what comes back:

```
python tools/style-check.py draft.md
```

Python 3, standard library only, nothing to install.

## What it changes

`examples/before.md` and `examples/after.md` tell the same story about a build pipeline migration. One was written the way models write by default, and the checker finds 32 problems in it: unnamed sources, two negation reframes, a self-answered question, a tailing participle, a Title Case header, a Conclusion section that repeats what came before, and eleven banned words. Its rewrite reports clean and gives an actual failure rate where the original claimed productivity gains with no number behind them.

## What's in here

`writing-rules.md` is the prompt. Roughly 9.5 KB, organized into output separation, punctuation, banned words, banned phrases, sentence patterns, structure, tone, evidence, vocabulary, and formatting. Everything above the `---` line is commentary and everything below it is the prompt itself, which is also how the build script knows where to cut.

`writing-rules-short.md` is a 1,497 character version for boxes that cap out. ChatGPT's custom instructions allow 1,500 characters on free and Go plans and 5,000 on paid plans, so the short version fits everywhere.

`reference/ai-tells.csv` is the catalog: 151 rows across eight categories, with the tell, an example of it, and what a person would write instead. It exists so the rules aren't arbitrary. When the prompt bans a word, this file shows a sentence carrying it and what to write instead. `reference/ai-tells.xlsx` is the same rows with a frozen header and a filter, for people who edit with a spreadsheet open beside the draft.

`tools/style-check.py` reports line numbers for em dashes and other characters you cannot type, the banned word and phrase lists, filler weight, depth adverbs, "is" substitutes, six negation reframe patterns, self-answered questions, three-in-a-row anaphora, rule-of-three rhythm, tailing participles, unnamed sources, stacked one-line paragraphs, the banned opinion label, Title Case headers, and sections named Conclusion. It exits 1 on findings and 0 when clean, so it works as a pre-commit hook or a build step. It reads Markdown and HTML as well as plain text.

What it cannot judge is whether you took a position, whether the enthusiasm matches the subject, or whether an example is real. Those stay yours.

## Editing and rebuilding

Two files are sources of truth: `writing-rules.md` and `reference/ai-tells.csv`. Everything in `install/`, plus the spreadsheet, is generated from them.

```
python tools/build.py           rewrite the generated files
python tools/build.py --check   exit 1 if anything is out of date
```

The check mode runs in CI on every push, so an edit to the prompt that doesn't get rebuilt fails the build instead of drifting out of sync. Building the spreadsheet needs `openpyxl`; nothing else in the repo has dependencies.

## Behavior that looks like a bug

Running the checker on `reference/ai-tells.csv` lights up, because the example column holds specimens of the exact things it looks for. That is the catalog doing its job.

The filler-weight group (crucial, essential, significant, and the rest) fires on legitimate technical writing, where a significant digit really is significant. Treat that group as a prompt to look rather than a failure. The same goes for the context group, which flags words that are only banned as metaphors.

The two rules files light up hardest of all, because a list of banned words is made of banned words. So does this README, which reports four findings: three from the sentence above naming the filler words, and one for "public domain" in the license line. The prose written to be read rather than to be a list, meaning `examples/after.md` and `install/README.md`, reports clean.

Dropping `CLAUDE.md` or `AGENTS.md` into a code project applies these rules to everything the agent does. The generated copies open with a scope note limiting them to prose, and `install/README.md` explains how to add the rules to a file you already have instead of replacing it.

## License

CC0 1.0. Public domain, no attribution required. Take it, change it, ship it inside whatever you want.
