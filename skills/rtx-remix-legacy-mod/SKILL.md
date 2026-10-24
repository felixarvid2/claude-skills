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
- Deadlock on heavy loads (map loads, many texture uploads): the client waits for room in the data ring
  (stack: `UnlockRect` in the bridge client) while the idle server waits in `waitForCommand`. The chance scales
  with the ring size `clientChannelMemSize` (bytes, default 96 MB): Anachronox servicetunnel stalled 10/10 at
  48 MB, 3-5/10 at 96 MB, 0/10 at 192 MB (`clientChannelMemSize = 201326592`). `clientDataQueueSize` (item
  count) does not size that ring and did not help.
- Other options (defaults): `clientCmdQueueSize` / `clientDataQueueSize` 3000, `serverCmdQueueSize` 10,
  `serverDataQueueSize` 25. Change none of them without repeated runs (10+ loads) against an unchanged
  baseline.
- Intermittent hangs: measure the failure rate of the unchanged baseline first (10 runs). One passing run after
  a change proves nothing. Bisecting data (e.g. a light list) only works when the failure is deterministic;
  knocking out features one at a time can show "no single cause" for a size/timing problem.
- Thread stacks of a hung Proton game: with the game's `WINEPREFIX`, Proton's `files/bin/wineserver` as
  `WINESERVER` and `files/bin/wine`, run `wine winedbg --command "info proc"`, then pipe
  `attach 0x<pid>` / `bt all` / `detach` into `wine winedbg`. NvRemixBridge.exe ships a PDB, so server frames
  get names; map wrapper addresses with `llvm-addr2line -f -e opengl32.dll <ImageBase+offset>`.

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
- Sky opaque grey behind windows/openings while the original shows its skybox: Remix fog remap turned the
  game fog into volumetric fog that fills the view to the sky (only distant emissives show through). Turn
  `rtx.volumetrics.enableFogRemap` off for that map. Knock out mod layers one at a time before theorising.
- Skybox nearly black on sunlit outdoor maps (looks like a night sky) while the ground matches: autoexposure
  adapts to the bright path-traced ground and the skybox keeps a fixed radiance. Raise `rtx.skyBrightness` per
  map (Anachronox: 140), then re-match exposure; measure sky and ground regions separately. A coloured game fog
  remapped to volumetrics can tint the ground once the sky lights it.
- A colour cast over the whole scene that the original lacks (Anachronox: purple under a yellow-white fog) can
  come from the fog remap too; turn it off for that map before touching materials or lights.
- To find dark skies across many maps, shoot views pitched upwards (sky in the top third) and compare top-third
  vs bottom-third EV; a gap of several EV is the skybox, an even offset is plain exposure.
- Characters: old engines light models from the lightmap under them plus a model-light colour; path tracing
  has neither, so characters come out dark. A per-character fill light scaled by the map lights' irradiance
  at the model (not a fixed brightness) survives different exposures; filter to real characters (engine
  render flags), not props, or lamps blow out walls. Outdoor maps need less (sky not counted).
  Tuning per map: the fill is only part of the light on a character (Anachronox: 0.25-0.65 EV per doubling of
  the fill), so scale once, measure the response, then scale again from it. Where the path-traced room light
  alone over-lights the character, no fill value fixes it; record that instead of pushing to 0.
- Props lit by a model-light flag in the original (Anachronox: entity.dat lighting 1 = RF_DIRLIGHT, the same as
  characters) come out nearly black when no fill light reaches them. Check what a flag does in the game code
  before naming it (it is not fullbright). Fix: emission from the prop's own texture (~0.5); world-space-UI
  texture lists make them flat and too bright.
- Local fog volumes (Anachronox func_fog) can render as opaque black boxes under Remix.
- Free-camera views: Quake-style engines draw only what the player's PVS shows, so place test cameras in the
  spawn cluster's PVS. A camera at the spawn sits inside the player model and Remix renders a black frame.

- Untextured additive draws (Quake 2 style beams: `glDisable(GL_TEXTURE_2D)`, blend SRC_ALPHA/ONE, vertex colour)
  render dark under Remix, and no texture-hash setting can reach them. Log untextured perspective draws in the
  wrapper to identify them. Fix: bind a small solid texture of their colour AND add a texcoord set to the vertex
  format; without texcoords Remix still treats the draw as untextured and ignores
  `enableEmissiveBlendEmissiveOverride`. With both, the per-map override makes them glow (Anachronox: func_fog indoors
  at intensity 8; laser beams on a sunlit map needed 150, since outdoor exposure is far lower).
- Textured additive effects (blend SRC_ALPHA/ONE with a texture: energy columns, glows) also come out very faint, but
  they do respond to `rtx.enableEmissiveBlendEmissiveOverride = True` + `rtx.emissiveBlendOverrideEmissiveIntensity`
  (Anachronox bricksd: 2.5 matched the original, 10 blew out white). It changes every additive draw, so set it per
  map. Before un-ignoring a texture from `rtx.ignoreTextures` that such an effect uses, check its other users: it may
  be ignored because it breaks something else (a character's env-map layer turned the model blue-white).
- Quake 2 engines keep `gl_log`: `gl_log 1;wait;wait;gl_log 0` in the console writes every GL call of a few frames
  to `<gamedir>/gl.log`, which shows how an effect is drawn (blend, texture binds, vertex colours).

## Procedural / animated textures

- Textures updated per frame with `glTexSubImage2D` change their Remix hash every frame. Freeze one stable
  frame (fixed size, recreated D3D texture filled with that frame) so a replacement material can bind to it.
- Loose-file texture packs (e.g. a community upscale mod) change the Remix hash of every texture they replace, so
  every hash list and material override keyed by the old hash silently stops matching (skybox list, decals,
  emissive overrides). Map old -> new hash per file, keep the old hashes and add the new ones (identical originals
  can map to several pack files; a new hash can equal an unrelated old one, so in-place replacement is unsafe).
  Check one functional override in-game afterwards (an emissive prop at the same EV as before).
- HD texture packs that upscale palettes can break engine code that requires exact sizes (Anachronox's lava
  palette must be 256 px wide).

## Linux / Proton rules worth keeping

- Never enable `rtx.automation.disableBlockingDialogBoxes` (it accepts the first-use consent dialog).
- Keep NVIDIA crash/usage reporting off if the owner turned it off.
- Run the game in a nested Xwayland session for automation; restore Steam launch options afterwards.
- Do not run the game together with other big GPU jobs on a small GPU.
