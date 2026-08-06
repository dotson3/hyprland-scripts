# hyprland-scripts

Small, dependency-free helpers for [Hyprland](https://hyprland.org). No pip, no rebuild.

## hypr_status.py

Emits a Waybar-compatible JSON line:
`{"text": "CPU 3% | MEM 54% | 16:24", "class": "ok"}`.
If `hyprctl` exists it appends the active workspace. Without Hyprland it still works.

```bash
python3 hypr_status.py          # one shot
python3 hypr_status.py --loop 2 # for your bar script
```

<!-- Screenshot placeholder: Waybar bar showing the JSON output. -->

## hypr_shot.py

Screenshot wrapper using `grim` + `slurp` (region or full). If they're missing it tells
you and exits cleanly — safe to wire into your config before install.

```bash
python3 hypr_shot.py            # full screen
python3 hypr_shot.py --region   # pick a region
```

## install-minimal.sh

One-shot installer for Arch that sets up a minimal Hyprland
(Hyprland + Waybar + alacritty + fuzzel + audio + notifications).

```bash
sudo ./install-minimal.sh            # install
sudo ./install-minimal.sh --dry-run  # show actions, change nothing
sudo ./install-minimal.sh --force    # overwrite existing ~/.config
```

> Targets a real Arch desktop/laptop, not a headless Pi server.

---

Tip jar (optional, no paywall): https://www.paypal.com/paypalme/ddotson321
