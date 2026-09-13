# PGR Classic Camera

A free and open-source camera-control mod for the **Windows PC / Steam version of Punishing: Gray Raven**.

PGR Classic Camera replaces the normal combat camera feel with a more conventional third-person camera while keeping the game's own battle camera system and cinematic/ultimate camera transitions intact.

> [!WARNING]
> ## Anti-cheat / account risk
>
> This project modifies local Punishing: Gray Raven game asset data. The game uses anti-cheat software, and Kuro Games may consider modified files a violation of its rules or Terms of Service.
>
> **No one can guarantee that this mod is safe from account penalties or bans. Use it entirely at your own risk.**
>
> The author and contributors are not responsible for bans, account loss, lost progress, corrupted files, or any other damage resulting from use of this project.

## Features

- Toggleable **Classic Camera** mode
- True vertical orbit-style camera movement
- Extended vertical pitch range
- Wider manual zoom range
- Independent camera height adjustment
- Camera-local horizontal / shoulder offset
- Keeps your chosen zoom, height, and horizontal offset during combat
- Works across character switches and leaving/re-entering combat
- Ultimate / cinematic camera movements remain functional and return to Classic Camera afterwards
- No DLL injection
- No `GameAssembly.dll` patching
- Does not disable or bypass anti-cheat

### Camera limits

| Setting | Range |
|---|---:|
| Vertical pitch | `-60° .. +80°` |
| Zoom distance | `0.3 .. 6.5` |
| Horizontal offset | `-1.25 .. +1.25` |
| Camera height | manually adjustable |

## Controls

| Input | Action |
|---|---|
| `F6` | Toggle Stock / Classic Camera |
| `F7` | Re-sync pitch/distance/height from the current stock camera and reset horizontal offset |
| Mouse X | Horizontal camera rotation |
| Mouse Y | Vertical orbit / pitch |
| Mouse Wheel | Zoom in / out |
| `Alt + Mouse Wheel` | Raise / lower camera height |
| `Ctrl + Mouse Wheel` | Move camera left / right |

`Ctrl + Mouse Wheel` uses the camera's **local horizontal axis**, so it behaves like a shoulder-camera offset rather than movement along the world's X axis.

## Known limitation: camera collision

Classic Camera currently does **not** reproduce the stock camera's collision/obstruction handling.

The camera can pass through walls, floors, ceilings, or other level geometry. This is currently intentional: a proper collision implementation needs reliable environment-layer filtering to avoid snapping against character colliders, effects, or other non-level objects.

## Requirements

- Windows 10/11
- Punishing: Gray Raven PC / Steam client
- Python **3.13** recommended
- Python packages from `requirements.txt`
- The upstream `apply_pgr_240fps.py` script from [`reiserFSs/pgrfpsunlock`](https://github.com/reiserFSs/pgrfpsunlock)

Install dependencies:

```powershell
py -3.13 -m pip install -r requirements.txt
```

## Installation

### 1. Download this repository

Clone it or download the ZIP.

```powershell
git clone https://github.com/kotaru34/pgr-classic-camera.git
cd pgr-classic-camera
```

### 2. Obtain the upstream patcher

This repository intentionally does **not** redistribute `apply_pgr_240fps.py`.

Download it directly from the original project and place it next to `make_pgr_classic_camera.py`:

```powershell
Invoke-WebRequest `
  https://raw.githubusercontent.com/reiserFSs/pgrfpsunlock/main/apply_pgr_240fps.py `
  -OutFile .\apply_pgr_240fps.py
```

You should now have:

```text
pgr-classic-camera\
├── apply_pgr_240fps.py
├── make_pgr_classic_camera.py
├── requirements.txt
└── ...
```

### 3. Generate the camera patcher

```powershell
py -3.13 .\make_pgr_classic_camera.py
py -3.13 -m py_compile .\pgr_classic_camera.py
```

This creates:

```text
pgr_classic_camera.py
```

### 4. Close Punishing: Gray Raven

Completely exit the game before modifying its files.

### 5. Set your game directory

Example Steam path:

```powershell
$PGR = 'C:\Program Files (x86)\Steam\steamapps\common\Punishing Gray Raven'
```

Change this to your actual installation path.

### 6. Check status

```powershell
py -3.13 .\pgr_classic_camera.py `
    --game-dir "$PGR" `
    --status
```

### 7. Apply the patch

```powershell
py -3.13 .\pgr_classic_camera.py `
    --game-dir "$PGR" `
    --apply `
    --backup-dir ".\backups"
```

The patcher creates a backup before writing.

### 8. Launch the game

Enter combat and press `F6`.

## Restoring clean files

Keep the backup created by the patcher.

If your generated patcher supports `--disable`, you can use:

```powershell
py -3.13 .\pgr_classic_camera.py `
    --game-dir "$PGR" `
    --disable
```

If anything behaves unexpectedly, the safest recovery path is:

1. Close PGR.
2. Restore the original backed-up `.uab` file, **or**
3. Use Steam's **Verify integrity of game files**.

If the game or anti-cheat rejects the modified asset, **restore the original file and stop**. This project does not contain or provide anti-cheat bypasses.

## After a game update

A PGR update may replace or change the target bundle.

Do not blindly copy an old patched `.uab` into a new game version.

After an update:

1. Make sure your game files are clean.
2. Obtain the current upstream `apply_pgr_240fps.py`.
3. Re-run `make_pgr_classic_camera.py`.
4. Run the generated patcher against the updated game.
5. If it reports an unsupported layout, size mismatch, or verification failure, stop and wait for an updated camera patch.

## Free software / scam warning

**PGR Classic Camera is free software. Do not pay anyone for it.**

There are no paid builds, activation keys, premium versions, or official paid mirrors.

If somebody sells this project, charges for an "activation key", or asks for money to unlock the same source code, they are not affiliated with this repository.

## Attribution

The asset-bundle patching approach used by this project is based on:

- **Project:** [`reiserFSs/pgrfpsunlock`](https://github.com/reiserFSs/pgrfpsunlock)
- **Author:** `reiserFSs`
- **Relevant upstream file:** `apply_pgr_240fps.py`

That project provided the original approach for resolving PGR's logical `assets/temp/lua/matrix.ab`, reading/rebuilding the protected UnityFS bundle, patching `XUiMain.lua`, and creating backups.

PGR Classic Camera supplies the camera-specific generator/runtime logic and Windows adaptations around that upstream patcher.

See [`ATTRIBUTION.md`](ATTRIBUTION.md) and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Licensing

The original code in this repository is licensed under the **MIT License**. See [`LICENSE`](LICENSE).

The upstream `reiserFSs/pgrfpsunlock` code is **not included in this repository** and remains subject to its own copyright/licensing status.

As of 2026-09-13, the upstream repository did not publish a `LICENSE` file. For that reason, this project requires users to obtain the upstream patcher directly from its original repository rather than redistributing it here.

The generated `pgr_classic_camera.py` is produced locally by transforming the upstream script and therefore contains/derives from upstream code. Do not redistribute the generated file unless you have the necessary permission from the upstream author.

## Disclaimer

This is an unofficial community modification. It is not affiliated with, endorsed by, sponsored by, or supported by Kuro Games.

Punishing: Gray Raven and related names, assets, and trademarks belong to their respective owners.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. USE IT ENTIRELY AT YOUR OWN RISK. THE AUTHOR AND CONTRIBUTORS SHALL NOT BE LIABLE FOR ACCOUNT PENALTIES, LOSS OF ACCESS, LOSS OF DATA, DAMAGE TO GAME FILES, OR ANY OTHER DIRECT OR INDIRECT DAMAGES ARISING FROM ITS USE.

## Version

Current stable camera behavior: **v0.6.1**

Tested on the Windows Steam PC client. Future game updates may require changes.
