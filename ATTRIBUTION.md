# Attribution

PGR Classic Camera uses an external upstream patcher as its base input:

- **Project:** PGR 240 FPS Patch Script / `pgrfpsunlock`
- **Author / GitHub user:** `reiserFSs`
- **Repository:** https://github.com/reiserFSs/pgrfpsunlock
- **Relevant file:** `apply_pgr_240fps.py`

The upstream script implements the protected PGR UnityFS / matrix bundle workflow used to locate and patch:

```text
assets/temp/lua/matrix.ab::XUiMain.lua
```

This repository does **not** include or redistribute the upstream script.

`make_pgr_classic_camera.py` reads a user-supplied copy of the upstream script and generates a local camera patcher by adapting that patching framework and replacing the FPS hook with PGR Classic Camera runtime logic.

## Licensing note

When checked on **2026-09-13**, the root of `reiserFSs/pgrfpsunlock` contained only:

- `README.md`
- `apply_pgr_240fps.py`

and did not publish a `LICENSE` file.

Because a public GitHub repository is not automatically open-source licensed, this project intentionally keeps the upstream code out of this repository.

The MIT license in this repository applies to the original code authored for PGR Classic Camera. It does not grant rights over third-party upstream code.

The generated `pgr_classic_camera.py` contains/derives from the locally supplied upstream patcher. Do not redistribute that generated file unless you have the necessary permission from the upstream author.
