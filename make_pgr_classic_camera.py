#!/usr/bin/env python3
"""Generate PGR Classic Camera v0.6.1 from reiserFSs/pgrfpsunlock.

This repository does not redistribute the upstream patcher. Place
apply_pgr_240fps.py from https://github.com/reiserFSs/pgrfpsunlock beside
this script before running it.

PGR Classic Camera original code: MIT licensed.
Upstream code remains subject to the upstream author's terms.
"""

from pathlib import Path
import re

SRC = Path("apply_pgr_240fps.py")
DST = Path("pgr_classic_camera.py")

if not SRC.exists():
    raise SystemExit("apply_pgr_240fps.py not found in current directory")

s = SRC.read_text(encoding="utf-8")

if "from Crypto.Cipher import AES" not in s:
    s = s.replace(
        "import subprocess\n",
        "import subprocess\nfrom Crypto.Cipher import AES\nimport lz4.block\n",
        1,
    )

lz4_func = """def lz4_hc_compress(data: bytes, level: int = 12) -> bytes:
    return lz4.block.compress(
        data,
        mode="high_compression",
        compression=level,
        store_size=False,
    )


"""
s, n = re.subn(
    r"def lz4_hc_compress\(.*?\n(?=def decompress_unityfs_directory)",
    lz4_func,
    s,
    count=1,
    flags=re.S,
)
if n != 1:
    raise SystemExit("could not replace lz4_hc_compress()")

aes_func = """def decrypt_protected_blob(blob: bytes, key: bytes = NATIVE_ASSET_BUNDLE_DECRYPT_KEY) -> bytes | None:
    if len(blob) != 32 or len(key) != 16:
        return None
    iv = blob[16:]
    cipher = AES.new(
        key,
        AES.MODE_CTR,
        nonce=b"",
        initial_value=int.from_bytes(iv, "big"),
    )
    return cipher.decrypt(blob[:16])


"""
s, n = re.subn(
    r"def decrypt_protected_blob\(.*?\n(?=def protected_seed_from_metadata)",
    aes_func,
    s,
    count=1,
    flags=re.S,
)
if n != 1:
    raise SystemExit("could not replace decrypt_protected_blob()")

# PGR Classic Camera v0.6.1 compact build.
#
# Changes from v0.5.1:
# - remove AUTOHEIGHT completely
# - remove PageUp/PageDown height controls
# - min zoom = 0.3
# - Alt + wheel = pivot height
# - Ctrl + wheel = horizontal/shoulder offset
#
# Controls:
#   F6             Stock <-> Classic
#   F7             re-sync pitch/distance/height from current stock camera
#   Mouse X        native PGR yaw
#   Mouse Y        orbit pitch
#   Wheel          zoom
#   Alt + Wheel    camera pivot height
#   Ctrl + Wheel   horizontal camera offset
#
# Collision with level geometry is intentionally NOT implemented in this build.
lua_line = (
    "    if not XUiMain.PgrClassicCameraManager then "
    "local V=CS.UnityEngine.Vector3;local I=CS.UnityEngine.Input;local K=CS.UnityEngine.KeyCode;"
    "local D=function(x) CS.UnityEngine.Debug.Log('[PGR-CC6] '..x) end;"
    "local C=function(x,a,b) if x<a then return a elseif x>b then return b else return x end end;"
    "local S={on=false,i=false,r=nil,b=nil,g=nil,p=8,d=3.7,h=1.5,x=0,old=nil,e=false};XUiMain.PgrClassicCamera=S;"
    "local function Q(r,p)local e=r.eulerAngles.x;if e>180 then e=e-360 end;local q=math.rad(e);"
    "local x=r.position;local a=x.x-p.x;local z=x.z-p.z;local c=math.abs(math.cos(q));if c<.2 then c=.2 end;"
    "local d=math.sqrt(a*a+z*z)/c;return e,d,x.y-math.sin(q)*d-p.y end;"
    "local function Y(r,p)local a,b,c=Q(r,p);S.p=C(a,-60,80);S.d=C(b,.3,6.5);S.h=C(c,0,3.5);S.i=true end;"
    "local function L()"
    "if not CS.XFight.IsRunning or not CS.XRLManager or not CS.XRLManager.Camera then return end;"
    "local c=CS.XRLManager.Camera;local r=c.VCameraRootTransform;local m=c.Camera;if not r or not m or m.gameObject~=S.g then return end;"
    "local f=CS.XFight.Instance;local o,n,l,u;pcall(function()o=f:GetClientRole()end);"
    "if o then pcall(function()n=o.Npc end)end;if n then pcall(function()l=n.RLNpc end)end;if l then pcall(function()u=l.Transform end)end;if not u then return end;"
    "if S.r~=l then S.r=l end;local p=u.position;"
    "if I.GetKeyDown(K.F6)then S.on=not S.on;if S.on then Y(r,p);pcall(function()S.old=c.InputScaleEnable;c.InputScaleEnable=false end);D('ENABLED')"
    "else S.i=false;pcall(function()if S.old~=nil then c.InputScaleEnable=S.old end end);S.old=nil;D('DISABLED')end end;"
    "if not S.on then return end;if not S.i then Y(r,p)elseif I.GetKeyDown(K.F7)then S.x=0;Y(r,p);D('RESET')end;"
    "local y=I.GetAxisRaw('Mouse Y');local w=I.GetAxisRaw('Mouse ScrollWheel');"
    "if y~=0 then S.p=C(S.p-y,-60,80)end;"
    "if w~=0 then "
    "if I.GetKey(K.LeftControl)or I.GetKey(K.RightControl)then S.x=C(S.x+w*.75,-1.25,1.25)"
    "elseif I.GetKey(K.LeftAlt)or I.GetKey(K.RightAlt)then S.h=C(S.h+w*.75,0,3.5)"
    "else S.d=C(S.d-w*3,.3,6.5)end end;"
    "local a=math.rad(S.p);local b=math.rad(r.eulerAngles.y);local q=math.cos(a);"
    "local fx=math.sin(b)*q;local fy=-math.sin(a);local fz=math.cos(b)*q;"
    "local rx=math.cos(b);local rz=-math.sin(b);"
    "local P=V(p.x-fx*S.d+rx*S.x,p.y+S.h-fy*S.d,p.z-fz*S.d+rz*S.x);"
    "local R=V(S.p,r.eulerAngles.y,0);r.position=P;r.eulerAngles=R;m.transform.position=P;m.transform.eulerAngles=R end;"
    "local function A()if not CS.XFight.IsRunning or not CS.XRLManager or not CS.XRLManager.Camera then return end;"
    "local m=CS.XRLManager.Camera.Camera;if not m then return end;local g=m.gameObject;if S.g==g and S.b then return end;"
    "if S.b then pcall(function()CS.UnityEngine.GameObject.Destroy(S.b)end)end;local o,b=pcall(function()return g:AddComponent(typeof(CS.XLuaBehaviour))end);"
    "if not o or not b then return end;S.b=b;S.g=g;S.i=false;S.r=nil;S.e=false;"
    "b.LuaLateUpdate=function()local o,e=pcall(L);if not o and not S.e then S.e=true;D('ERR '..tostring(e))end end end;"
    "XUiMain.PgrClassicCameraManager=XScheduleManager.ScheduleForever(A,250);D('READY') end"
)

const_re = re.compile(
    r'PATCH_MARKER = "PgrNativeFpsTimer"\n'
    r'PATCH_LINE_TEMPLATE = \(\n.*?\n\)\n',
    re.S,
)
replacement = 'PATCH_MARKER = "PgrClassicCameraManager"\nPATCH_LINE = ' + repr(lua_line) + '\n'
s, n = const_re.subn(lambda _m: replacement, s, count=1)
if n != 1:
    raise SystemExit("could not replace patch constants")

patch_func = """def fps_lua_patch_text(text: str, fps: int) -> tuple[str, bool]:
    if PATCH_MARKER in text:
        return text, False
    newline = "\\r\\n" if "\\r\\n" in text else "\\n"
    anchor = "    CS.XInputManager.SetCurInputMap(CS.XInputMapId.System)"
    if anchor not in text:
        raise ValueError("XUiMain:OnStart input-map anchor not found")
    return text.replace(anchor, anchor + newline + PATCH_LINE, 1), True


"""
s, n = re.subn(
    r"def fps_lua_patch_text\(.*?\n(?=def fps_lua_disable_text)",
    lambda _m: patch_func,
    s,
    count=1,
    flags=re.S,
)
if n != 1:
    raise SystemExit("could not replace fps_lua_patch_text()")

s = s.replace("Standalone PGR 240 FPS Lua hook patcher.", "PGR Classic Camera v0.6.1 compact patcher.")
s = s.replace("PgrNativeFpsTimer Application.targetFrameRate hook", "PgrClassicCameraManager LateUpdate hook")
s = s.replace("pgr_240fps_backups", "pgr_classic_camera_backups")
s = s.replace('print(f"fps-state\\t', 'print(f"camera-state\\t')

DST.write_text(s, encoding="utf-8")
print(f"created: {DST.resolve()}")
print("PGR Classic Camera v0.6.1 generator did not touch the game.")
