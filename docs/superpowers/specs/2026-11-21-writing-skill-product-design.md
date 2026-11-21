# Writing skill product: design

Date: 2026-11-21. Status: draft for David's approval.

## Intent

David wants to sell this repo's writing rules as a skill people buy for about $10 and install into their own AI tools. A buyer anywhere in the world should get prose that reads like a careful human wrote it, plus storytelling that shows up only when a piece needs it. Each buyer's copy then learns their voice and preferences from how they react to its drafts.

David will run it on his own machine first. That means consolidating the copies of his writing rules spread across this machine into the product without losing any of his personal voice work or his niche work (LinkedIn, Power Platform and Copilot, davidsoden.com).

## Goals

- One installable skill that works the same way in Claude Code, the Claude desktop app (including Cowork), claude.ai, ChatGPT and Codex.
- Three layers: a core everyone shares, a personal layer per writer, and niche layers per channel or subject.
- The skill learns from feedback on real drafts, with the user approving each lesson before it's saved.
- A setup interview that is optional, short, and can be revisited any time.
- Installing or updating the product never deletes or overwrites a user's personal or niche files.
- David's machine ends up with one system, backed up beforehand, with nothing of his lost.

## Non-goals

- Payment, a storefront, licensing keys or a download site. Those come later.
- A hosted service, accounts or any server that stores users' writing.
- Supporting tools that can't load Agent Skills at all, beyond the existing paste-in prompt files in `install/`.

## Anti-goals

The build fails, even if it technically works, if:

- the output ever names a brand or company that came from the product's own examples, or sounds like David
- it turns into a survey: questions after routine replies, or long questionnaires
- an update or install wipes a user's profile, lessons or niches
- the learning file fills with one-off reactions that contradict each other
- anything on David's machine is deleted without a backup and his sign-off on the list

## Constraints

- The skill folder follows the Agent Skills format: a directory with a `SKILL.md` carrying `name` and `description` in its frontmatter, plus optional reference files and scripts. Claude, ChatGPT and Codex all load this format.
- Tools differ in whether a skill can save files between sessions. Claude Code, the Claude desktop app, Codex, Cursor and Gemini CLI can. ChatGPT's chat window most likely can't (unverified, see open items). The design has to work both ways.
- Start-of-session hooks are reported not to fire in Cowork, so nothing may depend on them.
- The repo becomes private and the CC0 license is removed. Copies already taken under CC0 stay CC0. That can't be undone.
- Company names may appear in the product's illustrative examples (for instance the Evidence rule's specimen of stacked company examples). They must never appear in generated output. The core contains no personal voice and no subject-matter knowledge.
- The storytelling material restates ideas from Steve Rawling's Storyteller Tactics in the repo's own words, with no copied text. That has to stay true in anything sold.

## Approaches

1. One portable skill, with the personal and niche layers as plain files beside it. Where the tool can save files, the skill reads and updates them itself. Where it can't, the skill gives the user an updated profile to keep and re-attach, or uses the tool's built-in memory. One product to test and support. Learning is smoothest in tools that can save files.
2. A Claude plugin as the flagship (setup command, start-of-session hooks that load the personal layer) plus a cut-down version for other tools. Nicer in Claude Code, but two products, and the hooks reportedly don't run in Cowork.
3. A separately tuned build per tool from one source. Most polished per tool, but every tool is its own test surface after every change.

Chosen: approach 1, plus a Claude plugin that packages the same skill for Claude owners (Claude Code and the desktop app). David asked for something solid and stable across tools, approved the portable skill, and asked for the plugin as well. The plugin is packaging only and adds no second set of instructions, which keeps approach 2's maintenance cost out. A hosted profile service was dropped for cost and privacy.

## The design

### Layers

| Layer | Holds | Who edits it | Where it lives |
| --- | --- | --- | --- |
| Core | Writing rules, storytelling course, AI-tells catalog, checker script | Nobody by hand. Updates replace it. | The skill folder |
| Personal | Voice samples, interview answers, lessons from feedback, the writer's exceptions | The skill, with the user's approval | A folder outside the skill folder, so updates never touch it |
| Niche | Rules, lessons and pointers for one channel (LinkedIn, Substack, a website) or one subject (Power Platform) | The skill, with approval, or the user | Inside the project the niche belongs to, or in a named niches folder in the personal area when it's global |

Precedence: niche over personal over core, most specific wins. A short list of core rules can't be overridden by any layer: never invent facts, quotes, numbers, anecdotes, people or first-person experiences, and never present something as sourced when it isn't. Style rules can all be overridden, for example a niche allowing Title Case headers or one metaphor carried through a single article.

A niche loads when the user is working in its project, or when the request names it ("a LinkedIn post"). A global niche is labeled as a niche and stays out of unrelated writing. An existing skill can be registered as a niche by pointer. The niche file says "for LinkedIn, also follow this skill," so the original skill stays where it is and keeps working.

### Personal folder contents

Proposed layout (file names are the builder's call):

- `profile.md`: voice notes from samples and interview answers, in plain sentences.
- `samples/`: the writing samples the user supplied, unedited.
- `lessons.md`: one line per approved lesson, each with the date and the scope (personal or a named niche).
- `settings.md`: whether the skill may ask for feedback, and how often.
- `niches/<name>/`: global niches.

Default location for tools that can save files: a folder in the user's home directory that every supported tool can reach, so Claude Code and Codex share one profile. The exact path is the builder's call. It must be documented and must survive reinstalling the skill.

### First run

- When the personal folder doesn't exist, the skill offers a setup that takes about a minute: paste two or three pieces that sound like you, or skip. Skipping is a full answer, and the skill works on the core alone.
- At most three optional questions after the samples, each skippable. The builder drafts them. Example: who you usually write for.
- "Tune my voice", or similar wording, reopens setup any time. So does adding samples later.

### Learning from feedback

- The skill asks only after a substantial piece (a post, article, long email, talk or bio), never after a routine reply.
- It asks one question at most per piece, about one specific choice it made. For example: "I opened on the outage instead of the background. Keep doing that?" It never asks "how was this?"
- It occasionally asks about something that likely went well, because people rarely volunteer praise and silence isn't approval.
- When the user complains or corrects something unprompted, the skill turns that into a one-line lesson, shows it, asks for the scope ("all your writing, or just LinkedIn?"), and saves it once the user agrees.
- If the user pastes back their own edited version of a draft, the skill compares the two and proposes lessons from the differences.
- Questions get rarer as `lessons.md` grows. A setting turns them off completely.
- Before adding a lesson, the skill checks it against existing ones. If the new lesson conflicts with an old one, the skill shows both and asks which wins instead of keeping both.

### Tools that can't save files

The skill keeps the profile and lessons in the conversation. At the end of a session where something changed, it offers the updated profile as a single block for the user to save and attach next time, or saves it to the tool's built-in memory where that exists. Which route each tool gets is settled in testing.

### Packaging

- `tools/build.py` builds the skill folder from the repo sources and produces:
  - a plain folder for Claude Code and Codex
  - a zip for claude.ai and ChatGPT uploads
  - a Claude plugin that wraps the same skill, for people who own Claude, working in both Claude Code and the Claude desktop app. It may add conveniences such as a command to start or reopen setup and a command to show what the skill has learned. Every one of those must also be reachable by asking in plain words, and nothing in the plugin may depend on start-of-session hooks, because those reportedly don't run in Cowork. The plugin and the portable skill share one copy of the instructions, so they can't drift.
  - the existing paste-in files in `install/` for tools without skills
- The current `storytelling` skill folds into this single skill as a reference file. It isn't shipped as a second skill.
- The checker ships inside the skill as a script. Where the tool can't run Python, the skill applies the rules without it.
- Name: the product is Human Writing Rules, and the skill and plugin are named `human-writing-rules`. The website is humanwritingrules.com, chosen for search. nobotspeak.com is an optional second domain that would redirect there. Buying either domain is David's job.

### Repo changes

- Make `dtsoden/human-writing-rules` private, using the `dtsoden` account. Confirm with David immediately before running it.
- Delete `LICENSE` and remove the CC0 license section and wording from `README.md` and from anywhere else it appears.
- Two places point at the public URL: the PowerPlatCopilot memory `dictation-workflow.md`, which tells Claude to link the public repo in replies, and the `linkedin-elicitation` README or skill if it links the repo. Update the wording. Don't delete either.

### Migration on David's machine

1. Backup first. Copy every file the migration will change, move or delete into one dated folder (for example `C:\Users\DavidSoden\writing-backup\2026-11-21\`), keeping the original folder structure. Include:
   - a manifest listing each file's original path and what happened to it
   - a restore script that puts everything back
   
   Nothing else starts until the backup is verified.
2. Inventory. Present a single list of what moves, what stays, and what gets deleted. David signs off before any change. The starting point, from the 2026-11-21 investigation:
   - Moves into David's personal layer: the Writing Style section of `~/.claude/CLAUDE.md`, as his profile and exceptions. CLAUDE.md keeps a short pointer to the skill, and all non-writing sections of CLAUDE.md stay untouched.
   - Becomes niches by pointer, left in place: `PowerPlatCopilot` skills and memories, `linkedin-elicitation`, the davidsoden.com Title Case rule, and the analyst-specific rules in `~/.claude/skills/soden-analyst-report/references/house-style.md`. The generic part of that file is replaced by a pointer to the core.
   - Stays as is: the Resume app's `sanitize.ts` (product code), the deploy and API-MCP skills that only mention em dashes, and the Oz-metaphor memory for the Copilot article.
   - Deleted after backup: `~/GenAIToolKit`, `~/.claude/reference/GenAIToolKit`, `~/.claude/CLAUDE.md.bak` and the standalone `~/.claude/skills/storytelling`, since the new skill replaces it. All are superseded. Row-by-row comparison found nothing in the old catalogs missing from the repo.
   - Needs David's decision: the `C:\REPO\MySkills` copies of `writing-linkedin-content` (older than the PowerPlatCopilot copy) and `linkedin-elicitation` (identical to `C:\REPO\linkedin-elicitation`).
   - Can't be changed from this machine: `job-applications` and `respond-linkedin-post-comments` sync from David's claude.ai account. List the edits for him to make there.
3. Install the skill and point the niches at it. Run it on real tasks (an email, a LinkedIn post through the PowerPlatCopilot skill, a davidsoden.com page) and confirm each picks up the right layers.

### Gaps folded into the core

From the 2026-11-21 investigation, generic enough for every buyer:

- Checker patterns for engagement bait ("thoughts?", "agree?", "comment below", "tag someone", "follow for more"), performance tags ("unpopular opinion", "hot take"), throat-clearing openers ("I wanted to share", "quick story") and anecdote attributions ("a client told me").
- A review flag for absolute claims, plus the screenshot test as a final check: could the writer defend this sentence if someone they respect quoted it back?
- Rules on writing about people: don't build a piece around attacking a named person, and get permission before telling a client's story.
- A rule to match the writer's voice from their samples when a profile exists.

The LinkedIn-specific parts of `linkedin-elicitation` (technique rotation limits, post length, hashtag counts) stay in that niche.

## Rule defaults (decided with David, 2026-11-21)

- Every rule ships on by default, so the product helps most buyers from the first draft. That includes the opinion-label rule, the ban on recap endings and the em dash ban.
- Every style rule can be changed by the user in plain words ("I use em dashes"). The change is saved in their personal layer. Only the honesty rules (never invent facts, quotes, numbers, stories, people or experiences) are locked.
- Setup offers a one-page "what this changes in your writing" sheet, written for a buyer rather than as a rulebook, with the rules people most often adjust marked: em dashes, semicolons, headers, Title Case, opinion labels.
- The core rules are rewritten in a neutral voice, with nothing that sounds like David.
- The headers rule is rewritten around what the reader is doing: headers in documents people scan or return to (guides, reports, specs, READMEs), none in emails, posts, letters or replies, whatever their length. This replaces "no headers under 800 words".
- The copyable-block rule stays as a default for drafts the user will paste elsewhere, and can be switched off.

## Calls made after review

These were settled by Claude after a builder review. David can overturn any of them.

- Always-on rules. A skill loads only when its description matches, so commit messages and one-line replies would stop following the rules if CLAUDE.md shrank to a bare pointer. The product therefore has two parts: a compact always-on rule set (punctuation, banned words and phrases, sentence patterns, evidence, the never-invent rule) that goes into CLAUDE.md, AGENTS.md or the tool's custom instructions, and the skill, which handles drafted pieces, storytelling, the layers and learning. The installer writes the always-on part between clearly marked lines and never touches anything outside them.
- Promoting lessons. David's approved lessons stay personal by default. A "promote to core" step lets him copy a lesson into the repo sources when it would help every buyer, after which it ships in the next build.
- Seeing what buyers see. The skill supports a core-only mode that ignores the personal and niche layers, for testing.
- Order of work. The name is settled (Human Writing Rules), so the product is built and tested first, then David's machine is migrated, with niche pointers and the CLAUDE.md block written once.
- Public links. The two references to the public repo drop the link and keep the rest of the text. They point to humanwritingrules.com once that site is live.
- The uncommitted changes in the repo as of 2026-11-21 (storytelling section and skill, checker patterns, catalog rows) are intended and belong in the core.

## Left to the builder

- File names and formats inside the personal folder, and its exact location per tool.
- Wording of the first-run offer, the three optional questions and the feedback prompts, within the rules above.
- How the skill detects a substantial piece and an edited paste-back.
- Checker regexes for the new patterns, and keeping the example files' clean and not-clean results.
- Tests across Claude Code, the desktop app (with Cowork), claude.ai, ChatGPT and Codex, including whether ChatGPT skills can save files.
