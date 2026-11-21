---
name: human-writing-rules
description: Write and edit prose that reads like a careful human wrote it, in the user's own voice, with story used only when a piece needs it. Use for any drafting, rewriting or editing a person will read, such as emails, posts, articles, newsletters, documentation, reports, bios, pitches, talks, slides, case studies and replies. Also use when the user reacts to a draft ("too formal", "I like that", "don't do that"), pastes back their own edit of a draft, says "tune my voice" or "set up my writing profile", asks what the skill has learned, wants to change or drop a writing rule, or names a channel such as LinkedIn, Substack or a blog. Not for code.
user-invocable: true
metadata:
  version: "1.0.0"
---

# Human Writing Rules

Three layers decide how you write. The most specific one wins wherever they disagree.

1. Core: `references/rules.md` (always on) and `references/storytelling.md` (when a piece needs story). These ship with the skill and are replaced on update. Never edit them.
2. Personal: the writer's voice, samples, saved lessons and changed rules. Updates never touch this layer.
3. Niche: rules for one channel or subject, such as LinkedIn, a newsletter, a website or a field of expertise.

Two things no layer can change: the EVIDENCE rules in `references/rules.md`, and the rule against inventing stories, people, quotes, numbers or experiences.

## Where the layers live

If you can read and write files on the user's computer:

- Personal layer: a folder named `.human-writing-rules` in the user's home directory. It holds `profile.md`, a `samples/` folder, `lessons.md`, `settings.md`, and a `niches/` folder with one subfolder per global niche.
- Project niche: `.human-writing-rules/niche.md` in the root of the project being worked in.
- A niche file may point to other files or skills ("For LinkedIn posts, also follow the skill at <path>"). Follow the pointer and leave the target where it is.

If you can't save files, see "When files aren't available" below.

## Every time you write

1. Read `references/rules.md` unless the same rules are already in your instructions.
2. Unless the user asked for core only, load `profile.md`, `lessons.md` and `settings.md` from the personal folder. Then load the niche that matches: the project's `niche.md`, or the global niche for a channel or subject the request names. Never load a niche for unrelated writing.
3. Decide how much story the piece needs: none, a fragment, or a full story, as the STORYTELLING section of the rules explains. For a fragment or a full story, read `references/storytelling.md`.
4. Draft in the writer's voice. With samples, match their sentence length, vocabulary, formality, openings and closings. The rules then only remove what reads as machine-written. Samples teach voice, never subject: don't carry a sample's topics, products, names or numbers into other writing.
   If the piece calls for a story but the user gave only a point, don't pad it. Write the story as a fragment around a bracketed slot (`[the moment you noticed: when, what happened]`), and ask one or two specific questions outside the draft.
5. If you can run Python, run `scripts/style-check.py` on the draft and fix real findings. Findings marked REVIEW need a look, not automatic changes. If a loaded layer allows something the checker flags (Title Case headers, say), pass it with `--ignore "TITLE CASE HEADER"`, or list it in a `checker-ignore:` line in the niche file and pass that. Exit code 1 only means findings were reported.
6. Deliver the draft. Then, if a feedback question is due (see below), ask one.

## First run

If the personal folder doesn't exist and the user asked for writing, do the writing first. After it, offer setup once, in two or three lines:

> I can learn how you write. Paste two or three things you've written that sound like you, or say "skip". You can also say "show me the rules" to see what this changes in your writing.

- With samples: save them unedited in `samples/`, write a short plain-language description of the voice in `profile.md`, and ask at most two optional questions, such as who they usually write for. Every question is skippable.
- On "skip": create the folder with `settings.md` recording that setup was offered and skipped. Don't offer again unless the user asks.
- "Show me the rules" shows `references/what-this-changes.md`.
- "Tune my voice", "set up my writing profile" or new samples reopen setup at any time.

## Learning from feedback

People react honestly to real drafts and rarely volunteer praise, so most learning comes from reactions, and the skill asks about specific choices.

When to ask:
- Only after a substantial piece, such as a post, article, newsletter, long email, talk, bio or pitch. Never after a routine reply, an answer or a short message.
- At most one question per piece. Ask less as `lessons.md` grows. Never ask when `settings.md` says feedback is off.

What to ask:
- About one specific choice you made, so it can be answered in a word: "I opened on the outage instead of the background. Keep doing that?"
- Sometimes about a choice that likely went well, because silence isn't approval.
- Never "how was this?" or "any feedback?"

When the user reacts without being asked ("too formal", "don't use bullets", "I like that opening"):
1. Turn it into one plain-language lesson that would apply next time.
2. Check it against `lessons.md`. If it conflicts with an existing lesson, show both and ask which wins.
3. Ask where it belongs, in one line: "Save that for all your writing, or just for LinkedIn?" Skip this question when only one layer could apply.
4. Save it after they agree, as one line: `- YYYY-MM-DD [scope] lesson`. Scope is `personal` or the niche name.

When the user pastes back their own edited version of your draft, compare the two, propose up to three lessons from what changed, and save the ones they agree to.

When the user changes a rule ("I use em dashes", "Title Case headers are fine", "stop asking me questions"), save it as a lesson or setting straight away, confirm in one line, and follow it from then on.

## Niches

- When the user has asked for the same kind of piece several times (several Substack posts, say), offer once to start a niche for it, so preferences for that channel stay separate.
- A niche holds that channel's or subject's own rules, its lessons, and pointers to related files or skills.
- Knowledge in a niche, such as facts about a product or a field, stays in that niche and never appears in unrelated writing.

## Things the user can say

- "Tune my voice" or "set up my writing profile": reopen setup.
- "What have you learned?": list the lessons, grouped by scope.
- "Forget that" or "forget lesson N": remove it, after confirming.
- "Stop asking for feedback" or "you can ask again": change the setting.
- "Core only": write this piece with the core alone, ignoring the personal and niche layers.
- "Show me the rules": show `references/what-this-changes.md`.
- "Export my profile": give the whole personal layer as one block to keep.
- "Promote that lesson": only when `settings.md` has an `author-repo:` line naming a folder. Append the lesson, with its date, to `promoted-lessons.md` in that folder so the author can fold it into the core. Otherwise say this is for the rules' author and leave the lesson where it is.

## When files aren't available

Some tools can't save files between conversations.

- If the user attaches or pastes a profile block (it starts with `# Human Writing Rules profile`), use it as the personal layer.
- Learn during the conversation as above, keeping lessons in mind instead of in files.
- When something changed, offer at the end, once: "Want an updated profile to keep? Attach it next time and I'll pick up where we left off." Then give the block: profile, lessons and settings, in the same layout as the files.
- If the tool has its own memory feature, offer to save short lessons there instead.
