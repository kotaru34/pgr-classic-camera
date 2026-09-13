# Changelog

## v0.6.1 — 2026-09-13

First public release.

### Camera

- Classic third-person camera toggle on `F6`
- Vertical orbit camera on Mouse Y
- Native horizontal yaw on Mouse X
- Zoom range `0.3 .. 6.5`
- Vertical pitch range `-60° .. +80°`
- Manual camera height via `Alt + Mouse Wheel`
- Camera-local horizontal / shoulder offset via `Ctrl + Mouse Wheel`
- Horizontal offset range increased to `-1.25 .. +1.25`
- `F7` re-syncs stock pitch/distance/height and resets horizontal offset
- Camera state remains stable through character switching and leaving/re-entering combat
- PGR ultimate/cinematic camera transitions continue to function and return to Classic Camera

### Packaging

- Publishes only the camera-specific generator
- Requires users to obtain `apply_pgr_240fps.py` directly from `reiserFSs/pgrfpsunlock`
- Does not redistribute PGR game assets or patched `.uab` files
- No anti-cheat bypass, DLL injection, or `GameAssembly.dll` patching

### Known limitation

- No collision/obstruction handling for walls, floors, ceilings, or other level geometry
