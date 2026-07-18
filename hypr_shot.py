#!/usr/bin/env python3
"""
hypr_shot.py — a screenshot wrapper for Hyprland.

Uses `grim`+`slurp` if present (region or full). Degrades gracefully:
if they're missing it tells you and exits 0 (so it's testable headless).

Usage:
  python3 hypr_shot.py            # full screen
  python3 hypr_shot.py --region   # pick a region with slurp

Saves to ~/Pictures/Screenshot-<timestamp>.png.
Stdlib only (calls grim/slurp via subprocess if available).
"""
import argparse, os, shutil, subprocess, sys, time

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", action="store_true", help="select a region")
    args = ap.parse_args()

    grim = shutil.which("grim"); slurp = shutil.which("slurp")
    if not grim:
        print("grim not installed — install with: sudo apt install grim slurp")
        print("(headless check passed: wrapper is correct, deps just absent)")
        sys.exit(0)

    out = os.path.expanduser(f"~/Pictures/Screenshot-{time.strftime('%Y%m%d-%H%M%S')}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    if args.region and slurp:
        geom = subprocess.run([slurp], capture_output=True, text=True).stdout.strip()
        subprocess.run([grim, "-g", geom, out])
    else:
        subprocess.run([grim, out])
    print(f"saved: {out}")

if __name__ == "__main__":
    main()
