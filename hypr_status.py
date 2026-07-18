#!/usr/bin/env python3
"""
hypr_status.py — a Waybar-style status generator for Hyprland.

Reads battery, CPU, MEM, clock and prints a JSON line Waybar understands:
  {"text": "CPU 12% | MEM 51% | 🔋 88% | 14:03", "class": "ok"}

If `hyprctl` exists it also appends the active workspace. Without Hyprland it
still works (uses the literal CPU/MEM). Tested headless.

Usage:
  python3 hypr_status.py          # one shot JSON line
  python3 hypr_status.py --loop 2 # update every 2s (for your bar script)

Stdlib only.
"""
import argparse, json, os, subprocess, time

def read_cpu():
    with open("/proc/stat") as f:
        p = f.readline().split()
    idle0 = int(p[4]); tot0 = sum(int(x) for x in p[1:])
    time.sleep(0.3)
    with open("/proc/stat") as f:
        p = f.readline().split()
    idle1 = int(p[4]); tot1 = sum(int(x) for x in p[1:])
    return max(0, min(100, int((1 - (idle1-idle0)/(tot1-tot0))*100)))

def read_mem():
    with open("/proc/meminfo") as f:
        mi = dict(l.split(":",1) for l in f if ":" in l)
    tot = int(mi["MemTotal"].split()[0]); av = int(mi.get("MemAvailable","0").split()[0])
    return int((1-av/tot)*100)

def read_battery():
    base = "/sys/class/power_supply"
    if not os.path.isdir(base):
        return None
    for name in os.listdir(base):
        if name.startswith("BAT"):
            try:
                cap = int(open(f"{base}/{name}/capacity").read().strip())
                return cap
            except Exception:
                return None
    return None

def active_ws():
    hypr = shutil_which("hyprctl")
    if not hypr:
        return None
    try:
        out = subprocess.run([hypr, "activeworkspace", "-j"], capture_output=True, text=True, timeout=3).stdout
        return json.loads(out).get("name")
    except Exception:
        return None

def build():
    cpu = read_cpu(); mem = read_mem(); bat = read_battery(); ws = active_ws()
    parts = [f"CPU {cpu}%", f"MEM {mem}%"]
    if ws is not None:
        parts.append(f"WS {ws}")
    if bat is not None:
        parts.append(f"🔋 {bat}%")
    parts.append(time.strftime("%H:%M"))
    return {"text": " | ".join(parts), "class": "ok"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loop", type=int, default=0)
    args = ap.parse_args()
    if args.loop:
        while True:
            print(json.dumps(build()), flush=True); time.sleep(args.loop)
    else:
        print(json.dumps(build()))

def shutil_which(name):
    for d in os.environ.get("PATH","").split(os.pathsep):
        p = os.path.join(d, name)
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p
    return None

if __name__ == "__main__":
    main()
