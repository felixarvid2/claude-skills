# claude-skills

Claude Code skills from my projects. Copy a folder from `skills/` to `~/.claude/skills/` (all projects) or
`<repo>/.claude/skills/` (one project).

| Skill | For | Use |
| --- | --- | --- |
| [rtx-remix-legacy-mod](skills/rtx-remix-legacy-mod/SKILL.md) | any RTX Remix mod of an old game, esp. Linux/Proton | Remix API lights, bridge stalls vs crashes, matching the original look, animated textures |
| [idtech2-engine-hooking](skills/idtech2-engine-hooking/SKILL.md) | Quake 2-engine games | Ghidra MCP workflow, byte-signature hooks, structs and render flags |
| [anox-ab-measure](skills/anox-ab-measure/SKILL.md) | [anoxrtx](https://github.com/felixarvid2/anoxrtx) | measure Remix vs the original renderer, set exposure bias / character fill light |
| [anox-game-test](skills/anox-game-test/SKILL.md) | [anoxrtx](https://github.com/felixarvid2/anoxrtx) | run the game in the test rig and collect evidence |
| [parallel-subagent-builds](skills/parallel-subagent-builds/SKILL.md) | any large feature in one repo | split work across parallel subagents: shared contracts first, file ownership, waves, checkpoints |
| [claude-artifact-game-publish](skills/claude-artifact-game-publish/SKILL.md) | Vite/Three.js web games | build and publish a game as a claude.ai artifact, CSP pitfalls, updating in place |
| [headless-browser-game-checks](skills/headless-browser-game-checks/SKILL.md) | WebGL browser games | Playwright + software-GL Chromium, mobile emulation, tap/overlap assertions |
| [mobile-portrait-game-ui](skills/mobile-portrait-game-ui/SKILL.md) | browser games on phones | audit and fix portrait UI: thumb zone, 44 px targets, panel stack, Back button, confirm sheets |
| [free-game-asset-pipeline](skills/free-game-asset-pipeline/SKILL.md) | web games | CC0 models, textures, audio (Kenney, Quaternius, Poly Haven, ambientCG), import, paid-generation guardrails |
| [cloud-session-github-ops](skills/cloud-session-github-ops/SKILL.md) | Claude Code cloud sessions | pushes, releases without tag pushes, new repos, splitting repos, secret checks |
| [ashfall-region-pipeline](skills/ashfall-region-pipeline/SKILL.md) | [Ashfall](https://github.com/felixarvid2/Ashfall) | how a region or game phase is planned, built, tested and shipped |

The two `anox-*` skills use tools in the anoxrtx repo (`tools/rigsession.sh`, `anoxcheck.py`, `ab_ev.py`);
their source of truth is that repo's `.claude/skills/`. The general skills come from one project (Anachronox):
treat the examples as a checklist to re-check, not as facts for every game.

The game skills come from [Ashfall](https://github.com/felixarvid2/Ashfall), whose `.claude/skills/` is their source of
truth; `ashfall-region-pipeline` is specific to that repo, the others are general.
