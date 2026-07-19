# hyprland-scripts

Small, dependency-free helpers for [Hyprland](https://hyprland.org). No pip, no rebuild.

## hypr_status.py
Emits a Waybar-compatible JSON line: `{"text": "CPU 3% | MEM 54% | 16:24", "class": "ok"}`.
If `hyprctl` exists it appends the active workspace. Without Hyprland it still works.
```
python3 hypr_status.py          # one shot
python3 hypr_status.py --loop 2 # for your bar script
```

## hypr_shot.py
Screenshot wrapper using `grim` + `slurp` (region or full). If they're missing it
tells you and exits cleanly — so it's safe to wire into your config before install.
```
python3 hypr_shot.py            # full screen
python3 hypr_shot.py --region   # pick a region
```

## Tested
- `hypr_status.py` → valid JSON headless
- `hypr_shot.py` → graceful no-op when grim absent

## ☕ Support
Free and open. If they helped: https://www.paypal.com/paypalme/ddotson321

## install-minimal.sh — full minimal setup

A one-shot installer for Arch that sets up this exact minimalist Hyprland
(omarchy spirit, no bloat): Hyprland + Waybar (clock/wifi/bluetooth) + alacritty
+ fuzzel + audio + notifications. Verified: `bash -n` clean, waybar config valid JSON.

```
sudo ./install-minimal.sh            # install
sudo ./install-minimal.sh --dry-run  # show actions, change nothing
sudo ./install-minimal.sh --force    # overwrite existing ~/.config
```

Then log in at a TTY and run `Hyprland`. Keybinds: SUPER+Enter (term),
SUPER+E (launcher), SUPER+Q (close), SUPER+M (exit).

> Note: targets a real Arch desktop/laptop, not a headless Pi server.
