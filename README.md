# claude-skills

Claude Code skills from my projects. Copy a folder from `skills/` to `~/.claude/skills/` (all projects) or
`<repo>/.claude/skills/` (one project).

| Skill | For | Use |
| --- | --- | --- |
| [rtx-remix-legacy-mod](skills/rtx-remix-legacy-mod/SKILL.md) | any RTX Remix mod of an old game, esp. Linux/Proton | Remix API lights, bridge stalls vs crashes, matching the original look, animated textures |
| [idtech2-engine-hooking](skills/idtech2-engine-hooking/SKILL.md) | Quake 2-engine games | Ghidra MCP workflow, byte-signature hooks, structs and render flags |
| [anox-ab-measure](skills/anox-ab-measure/SKILL.md) | [anoxrtx](https://github.com/felixarvid2/anoxrtx) | measure Remix vs the original renderer, set exposure bias / character fill light |
| [anox-game-test](skills/anox-game-test/SKILL.md) | [anoxrtx](https://github.com/felixarvid2/anoxrtx) | run the game in the test rig and collect evidence |

The two `anox-*` skills use tools in the anoxrtx repo (`tools/rigsession.sh`, `anoxcheck.py`, `ab_ev.py`);
their source of truth is that repo's `.claude/skills/`. The general skills come from one project (Anachronox):
treat the examples as a checklist to re-check, not as facts for every game.
