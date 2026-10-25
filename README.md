# claude-skills

Claude Code skills from my projects. Copy a folder from `skills/` to `~/.claude/skills/` (all projects) or
`<repo>/.claude/skills/` (one project).

| Skill | For | Use |
| --- | --- | --- |
| [rtx-remix-legacy-mod](skills/rtx-remix-legacy-mod/SKILL.md) | any RTX Remix mod of an old game, esp. Linux/Proton | Remix API lights, bridge stalls vs crashes, matching the original look, animated textures |
| [idtech2-engine-hooking](skills/idtech2-engine-hooking/SKILL.md) | Quake 2-engine games | Ghidra MCP workflow, byte-signature hooks, structs and render flags |
| [anox-ab-measure](skills/anox-ab-measure/SKILL.md) | [anoxrtx](https://github.com/felixarvid2/anoxrtx) | measure Remix vs the original renderer, set exposure bias / character fill light |
| [anox-game-test](skills/anox-game-test/SKILL.md) | [anoxrtx](https://github.com/felixarvid2/anoxrtx) | run the game in the test rig and collect evidence |
| [threejs-web-game-pitfalls](skills/threejs-web-game-pitfalls/SKILL.md) | any three.js/WebGL browser game | black flashes from resizing, sprites clipping into walls, UI left over between view modes, shader patching |
| [playwright-webgl-testing](skills/playwright-webgl-testing/SKILL.md) | any WebGL browser game in a headless container | SwiftShader setup, driving the game, desktop/mobile layout and tap checks, one-frame glitches, regression tests, README screenshots |
| [krabba-passet-release](skills/krabba-passet-release/SKILL.md) | [Krabba-passet](https://github.com/felixarvid2/Krabba-passet) | version bump checklist, test suite, republishing the artifact, releases with a zip |
| [parallel-subagent-builds](skills/parallel-subagent-builds/SKILL.md) | any large feature in one repo | split work across parallel subagents: shared contracts first, file ownership, waves, checkpoints |
| [claude-artifact-game-publish](skills/claude-artifact-game-publish/SKILL.md) | Vite/Three.js web games | build and publish a game as a claude.ai artifact, CSP pitfalls, updating in place |
| [mobile-portrait-game-ui](skills/mobile-portrait-game-ui/SKILL.md) | browser games, esp. on phones | audit and fix portrait UI (thumb zone, 44 px targets, panel stack, Back button, confirm sheets) plus game-UI rules for every viewport: hierarchy, stable layout, event-driven HUD, gamepad focus, accessibility |
| [game-ui-ux](skills/game-ui-ux/SKILL.md) | any game (third-party, Apache-2.0) | engine-neutral HUD/menu layout, scaling, safe areas, focus navigation, screen stack |
| [threejs-game-ui-designer](skills/threejs-game-ui-designer/SKILL.md) | three.js games (third-party, MIT) | HUD/menu workflow, UI states, zones, touch controls, text fit |
| [free-game-asset-pipeline](skills/free-game-asset-pipeline/SKILL.md) | web games | CC0 models, textures, audio (Kenney, Quaternius, Poly Haven, ambientCG), import, paid-generation guardrails |
| [cloud-session-github-ops](skills/cloud-session-github-ops/SKILL.md) | Claude Code cloud sessions | pushes, releases without tag pushes, new repos, splitting repos, secret checks |
| [autonomous-github-release](skills/autonomous-github-release/SKILL.md) | any GitHub repo, incl. Claude Code cloud sessions | cut a release on your own: version, notes since the last release, a notes-file PR that triggers the release workflow (template included), verify the assets |
| [ashfall-region-pipeline](skills/ashfall-region-pipeline/SKILL.md) | [Ashfall](https://github.com/felixarvid2/Ashfall) | how a region or game phase is planned, built, tested and shipped |

The two `anox-*` skills use tools in the anoxrtx repo (`tools/rigsession.sh`, `anoxcheck.py`, `ab_ev.py`);
their source of truth is that repo's `.claude/skills/`. The general skills come from one project (Anachronox):
treat the examples as a checklist to re-check, not as facts for every game.

`krabba-passet-release` is specific to the game's source in [felixarvid2/test](https://github.com/felixarvid2/test)
(`natverksspel/`); its source of truth, like the two general three.js/Playwright skills, is that repo's
`.claude/skills/` (`playwright-webgl-testing` is also kept in Ashfall, merged from both projects). The general skills come from one project: re-check versions and paths before relying on them.

`game-ui-ux` and `threejs-game-ui-designer` are third-party skills, copied with their licences; each folder's
`SOURCE.md` names the upstream repo and commit.

The game skills come from [Ashfall](https://github.com/felixarvid2/Ashfall), whose `.claude/skills/` is their source of
truth; `ashfall-region-pipeline` is specific to that repo, the others are general.
