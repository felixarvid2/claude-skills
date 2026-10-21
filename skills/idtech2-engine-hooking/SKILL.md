---
name: idtech2-engine-hooking
description: Reverse engineer and hook Quake 2-engine (id Tech 2) game DLLs (ref_gl.dll, gamex86.dll, the exe) with the Ghidra (pyghidra) MCP to read engine state from a wrapper or mod - finding functions by byte signature, struct offsets, render flags, globals. Use when a renderer wrapper or mod needs data the game doesn't export (light at a point, entity list, model light), or when the Ghidra MCP misbehaves.
---

# Hooking a Quake 2-engine game

Learned on Anachronox (heavily modified Quake 2). Offsets are examples; re-derive them for each game build.

## Ghidra MCP

- Binaries are named with a hash suffix (e.g. `/ref_gl.dll-06f8cd`); list them with `list_project_binaries`.
- `CONNECTION_CLOSED` / project lock errors: an orphaned pyghidra process holds the project lock. Find it with
  `pgrep -fa pyghidra`, kill only that PID, then have the user reconnect with `/mcp`.
- Start from strings: `search_strings` for console variable/command names or error texts, then `list_xrefs` to
  the function, then `decompile_function`. Quake 2 source names match closely (R_RenderView, R_LightPoint,
  R_DrawEntitiesOnList), so compare with the GPL Quake 2 source to name things.

## Finding functions in a running game

- Don't hard-code addresses; scan the loaded module for a byte signature taken from the disassembly
  (function prologue + a distinctive instruction), then verify a second pattern at a fixed offset. Example
  (R_LightPoint): `55 8B EC 83 EC 34 A1`, and at +11 `83 B8 AC 01 00 00 00 75`.
- Read globals out of the instruction bytes instead of guessing addresses, e.g. the dlight count from
  `3B 0D <addr> 0F 8D` (cmp ecx,[addr]; jge), a colour pointer from `D9 41 30 D9 1D <addr>` (fstp [addr]).
- Hook by wrapping: call the original, then read state (e.g. after R_RenderView the refdef/entity list is
  complete). Log "found / not found" for every signature once, so a different game build fails loudly.
- When calling engine helpers for your own purposes, neutralise side inputs (e.g. set num_dlights to 0 around
  an R_LightPoint call so dynamic lights don't leak into a static measurement), and remember clamps
  (R_LightPoint clamps to 0.15..1 in this engine).

## Structs and flags

- Get struct sizes from loop strides in the decompiler (entity_t was 0x1b0 bytes; origin at +0x64,
  renderfx +0x174, model +0x184; model type at model+0x104).
- Model types and flag bits are game-specific. Anachronox added a type (6 = MDA, characters and props) and
  its own renderfx bits. The flag names appear as strings in gamex86.dll in bit order (`RF_...` table), which
  gives the bit for each name (0x800 RF_DIRLIGHT = gets the model light, i.e. characters; 0x2000 RF_NODRAW).
- Verify a filter in the running game by logging what passes it, before building on it (a wrong model-type
  filter silently matched nothing).

## Before building a feature on engine data

- Check the engine actually produces it: in Anachronox `CL_NewDlight` is dead code and `cl_testlights` a stub;
  dynamic lights come only from entity light fields and effect flags. A test light injected from outside
  (file polled by the wrapper) proves the draw path when the game produces none.
