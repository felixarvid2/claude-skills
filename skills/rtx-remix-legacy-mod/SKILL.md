---
name: rtx-remix-legacy-mod
description: Lessons for building NVIDIA RTX Remix mods of old OpenGL/D3D8/D3D9 games, especially on Linux with Proton/Wine (wrapper DLLs like QindieGL, the Remix bridge, Remix API lights, matching the original look). Use when working on any Remix mod or wrapper, when Remix shows black frames/freezes/missing lights, or when calibrating Remix brightness against the original game.
---

# RTX Remix mods of legacy games

Learned on Anachronox (Quake 2 engine, OpenGL -> QindieGL -> D3D9 -> Remix under Proton). Check each claim
against the current project; versions differ (stock Remix vs Remix Plus).

## Remix API lights (wrapper side)

- Lights are immutable: to change brightness/position, `DestroyLight` and `CreateLight` again.
- Use a **fresh hash for every creation** (a serial counter in the hash), never reuse one per slot. Remix Plus
  defers destruction, so a recreated light with the old hash aliases the pending removal and is not drawn.
  Symptom: per-frame lights (dlights, fill lights) never appear although `CreateLight` returns success.
- Per-frame lights also need `DrawLightInstance` each frame. Release handles on device loss / map change.
- Log creation stats (attempted / success / zero handle / first error) once per map; it makes silent failures
  visible.
- API lights need `exposeRemixApi = True` in `.trex/bridge.conf`.

## Bridge (32-bit game -> 64-bit Remix) diagnostics

- Logs: `rtx-remix/logs/bridge32.log` (client), `bridge64.log` (server), `remix-dxvk.log`. Copy them per run;
  the next launch overwrites them.
- Crash: "The RTX Remix Runtime has encountered an unexpected issue". Stall (not a crash): `Data Queue
  overwrite condition triggered` / "Waiting on server" with no "resolved" afterwards, and often
  `Message channel ... handshake timeout. Retrying...` in the Remix log. The frame freezes or stays black and
  the Remix welcome overlay is missing.
- Games that recreate their window/device during startup can stall when they also load a big level at the
  same moment (e.g. a `+map` launch argument). Loading the same level from the menu works: test the path a
  player takes before calling it a game bug.
- Queue options in `bridge.conf` (defaults): `clientChannelMemSize` 96MB, `clientCmdQueueSize` /
  `clientDataQueueSize` 3000, `serverCmdQueueSize` 10, `serverDataQueueSize` 25. Raising the client queue did
  not fix a stall; do not ship a queue change without repeated runs showing it matters.
- Intermittent hangs: measure the failure rate of the unchanged baseline first. One passing run after a
  change proves nothing. Bisecting data (e.g. a light list) only works when the failure is deterministic.

## Matching the original look

- A/B baseline: move Remix' `d3d9.dll` aside and the wrapper renders through Wine's D3D9 with the game's own
  lighting. Back up first, restore after; script it so failures restore too.
- Correct for things the baseline skips: if the game uses hardware gamma (e.g. `gl_gamma 1.4`) the wrapper
  path doesn't apply it, so correct the original shots `v^(1/gamma)` before comparing.
- Compare mean linear luminance (sRGB -> linear, Rec.709 weights) as EV = log2(original / Remix). Crop
  overlays (Remix welcome banner). Shoot twice and reject views that changed between shots.
- `rtx.tonemap.exposureBias` per map; autoexposure absorbs part of every change, so do a second pass.
- Look at every compare image. EV also moves for non-exposure reasons: missing fog, a different sky
  (night vs day), views outside the map, cutscenes, black loading frames. Record those separately.
- Characters: old engines light models from the lightmap under them plus a model-light colour; path tracing
  has neither, so characters come out dark. A per-character fill light scaled by the map lights' irradiance
  at the model (not a fixed brightness) survives different exposures; filter to real characters (engine
  render flags), not props, or lamps blow out walls. Outdoor maps need less (sky not counted).

## Procedural / animated textures

- Textures updated per frame with `glTexSubImage2D` change their Remix hash every frame. Freeze one stable
  frame (fixed size, recreated D3D texture filled with that frame) so a replacement material can bind to it.
- HD texture packs that upscale palettes can break engine code that requires exact sizes (Anachronox's lava
  palette must be 256 px wide).

## Linux / Proton rules worth keeping

- Never enable `rtx.automation.disableBlockingDialogBoxes` (it accepts the first-use consent dialog).
- Keep NVIDIA crash/usage reporting off if the owner turned it off.
- Run the game in a nested Xwayland session for automation; restore Steam launch options afterwards.
- Do not run the game together with other big GPU jobs on a small GPU.
