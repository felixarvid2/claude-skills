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
| [playwright-webgl-testing](skills/playwright-webgl-testing/SKILL.md) | any WebGL browser game in a headless container | SwiftShader setup, driving the game, catching one-frame glitches, regression tests, README screenshots |
| [krabba-passet-release](skills/krabba-passet-release/SKILL.md) | [Krabba-passet](https://github.com/felixarvid2/Krabba-passet) | version bump checklist, test suite, republishing the artifact, releases with a zip |

The two `anox-*` skills use tools in the anoxrtx repo (`tools/rigsession.sh`, `anoxcheck.py`, `ab_ev.py`);
their source of truth is that repo's `.claude/skills/`. The general skills come from one project (Anachronox):
treat the examples as a checklist to re-check, not as facts for every game.

`krabba-passet-release` is specific to the game's source in [felixarvid2/test](https://github.com/felixarvid2/test)
(`natverksspel/`); its source of truth, like the two general three.js/Playwright skills, is that repo's
`.claude/skills/`. The general skills come from one project: re-check versions and paths before relying on them.
