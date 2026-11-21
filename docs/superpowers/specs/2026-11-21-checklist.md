# Build checklist: Human Writing Rules product

Design: `2026-11-21-writing-skill-product-design.md`.

## Product (repo)

- [x] 1. Remove LICENSE and CC0 wording
- [x] 2. Rewrite `writing-rules.md` in a neutral voice: adjustable defaults, locked honesty rules, header rule by reader, people rules, voice matching, screenshot test
- [x] 3. Checker: engagement bait, performance tags, throat-clearing openers, anecdote attributions, absolute-claim review
- [x] 4. Catalog rows for the new tells
- [x] 5. Skill source `skill/`: SKILL.md (layers, first run, feedback loop, niches, promote, core-only, no-file fallback), defaults sheet, references
- [x] 6. Claude plugin packaging (verify manifest format first)
- [x] 7. `build.py`: skill folder, zip, plugin, always-on block; `--install` writes between markers and copies the skill
- [x] 8. README and install/README
- [x] 9. Verify: build --check, checker on examples, skill loads in Claude Code

## David's machine

- [x] 10. Backup folder with manifest and restore script
- [x] 11. Inventory for David's sign-off (STOP until approved)
- [x] 12. David's personal layer from his CLAUDE.md section and writing memories
- [x] 13. Niches by pointer: PowerPlatCopilot, linkedin-elicitation, davidsoden.com, analyst house style
- [x] 14. Replace CLAUDE.md Writing Style section with the marked block
- [x] 15. Fix the two public-link mentions
- [x] 16. Delete superseded copies (after 10 and 11)
- [x] 17. Smoke test on real tasks

## Outward (ask first)

- [ ] 18. Commit, make repo private, push
