# Where each file goes

Every file in this folder is generated from `writing-rules.md` in the repo root. Do not edit them by hand. Edit the source and run `python tools/build.py`.

| Tool | File to use | Where it goes |
| --- | --- | --- |
| Claude Code | `CLAUDE.md` | Project root, or `~/.claude/CLAUDE.md` to apply everywhere |
| Human Writing Rules skill | `../skills/human-writing-rules/` | Run `python tools/build.py --install` from the repo root, or upload `../dist/human-writing-rules.zip` in claude.ai or ChatGPT |
| Claude Projects, claude.ai | `writing-rules.txt` | The project instructions box |
| OpenAI Codex | `AGENTS.md` | Repo root, next to `.git` |
| ChatGPT custom instructions | `../writing-rules-short.md` | Settings, Personalization, Custom instructions |
| Cursor | `writing-rules.mdc` | `.cursor/rules/writing-rules.mdc` in the project |
| Gemini CLI | `GEMINI.md` | Project root, or `~/.gemini/GEMINI.md` |
| Ollama | `Modelfile` | `ollama create writer -f Modelfile`, then `ollama run writer` |
| LM Studio | `writing-rules.txt` | System Prompt field in the right sidebar, then save it as a preset |
| Anything else with a system prompt | `writing-rules.txt` | Paste it in |

## Read this before dropping it into a coding project

`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, and Cursor rules apply to everything the agent does, code included. If your project already has one of these files, paste the writing rules into it as a section rather than replacing the file. The generated copies open with a scope note saying the rules cover prose and not code, which keeps an agent from applying "one adjective per noun" to a variable name, but the scope note only helps if you keep it.

The Cursor rule ships with `alwaysApply: false` and a description, so Cursor loads it when the work looks like writing. If you want it on for every request, open the `.mdc` file and set `alwaysApply: true`.

## Notes on specific tools

The files in this folder are the always-on rules on their own. The skill adds storytelling, the writer's personal layer and learning from feedback, so use it wherever the tool supports skills. Without it, the STORYTELLING section of the rules still decides how much story a piece needs.

ChatGPT's custom instructions box caps at 1,500 characters on free and Go plans and 5,000 on paid plans, which is why the short version exists. Everywhere else takes the full text.

LM Studio stores presets as JSON under `~/.lmstudio/config-presets` on macOS and Linux, or `%USERPROFILE%\.lmstudio\config-presets` on Windows. The schema is not documented, so this repo does not ship a preset file. Paste the text into the System Prompt field and save the preset from the app.

The Ollama `Modelfile` uses `llama3.1` as its base. Change the `FROM` line to whatever you have pulled. The rules are long, so give the model enough context length to hold them alongside your actual request.

Cursor's older `.cursorrules` file at the project root still works for autocomplete but is ignored in agent mode, so use the `.mdc` file.
