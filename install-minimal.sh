#!/usr/bin/env bash
#
# install-minimal.sh — minimalist Hyprland setup (omarchy spirit, no bloat)
#
# Installs Hyprland + a lean Waybar (clock / wifi / bluetooth) + a fast
# terminal + a launcher. No display manager, no heavy theming.
#
# Target: Arch Linux (and Arch-based). Other distros: not supported here.
#
# Usage:
#   ./install-minimal.sh            # install
#   ./install-minimal.sh --dry-run  # show what it would do, change nothing
#   ./install-minimal.sh --force    # overwrite existing ~/.config files
#
# After install: log in at a TTY and run `Hyprland`.
#
set -euo pipefail

DRY=0; FORCE=0
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    --force)   FORCE=1 ;;
    -h|--help) sed -n '3,18p' "$0"; exit 0 ;;
    *) echo "unknown arg: $a"; exit 1 ;;
  esac
done

run() { if [[ $DRY -eq 1 ]]; then echo "  [dry] $*"; else eval "$@"; fi; }

# ---- requirements ----
if [[ $EUID -ne 0 ]]; then echo "ERROR: run with sudo (needs root for pacman)."; exit 1; fi
if ! command -v pacman >/dev/null 2>&1; then
  echo "ERROR: this installer targets Arch Linux (pacman not found)."
  exit 1
fi

# ---- packages (intentionally small) ----
# hyprland      compositor
# waybar        bar (clock / network / bluetooth)
# alacritty     terminal (light, gpu-accelerated)
# fuzzel        launcher (minimal dmenu-like)
# grim slurp    screenshots
# wl-clipboard  clipboard
# networkmanager + frontends  wifi in the bar
# bluez         bluetooth in the bar
# pipewire wireplumber pavucontrol  audio
# ttf-jetbrains-mono-nerd      icons/glyphs for the bar
# mako          notifications (tiny)
PKGS=(hyprland waybar alacritty fuzzel grim slurp wl-clipboard
      networkmanager bluez bluez-utils pipewire wireplumber pavucontrol
      ttf-jetbrains-mono-nerd mako)

echo "==> Packages to install:"
printf '   %s\n' "${PKGS[@]}"

echo "==> Installing"
run "pacman -Syu --noconfirm"
run "pacman -S --needed --noconfirm ${PKGS[*]}"

echo "==> Enabling services (NetworkManager, Bluetooth)"
run "systemctl enable --now NetworkManager"
run "systemctl enable --now bluetooth"

# ---- config ----
SRC="$(cd "$(dirname "$0")" && pwd)/config"
DEST="$HOME/.config"
if [[ $DRY -eq 1 ]]; then DEST="/tmp/dryrun-config"; fi

for d in hypr waybar fuzzel alacritty; do
  if [[ -d "$DEST/$d" && $FORCE -eq 0 && $DRY -eq 0 ]]; then
    echo "  NOTE: $DEST/$d exists — skipping (use --force to overwrite)"
    continue
  fi
  echo "==> Config: $d"
  run "mkdir -p '$DEST/$d'"
  run "cp -r '$SRC/$d/'* '$DEST/$d/' 2>/dev/null || true"
done

echo
echo "==> Done."
if [[ $DRY -eq 1 ]]; then
  echo "  (dry-run: nothing was installed or written)"
else
  echo "  Log in at a TTY and run:  Hyprland"
  echo "  Keybinds: SUPER+Enter (term)  SUPER+E (launcher)  SUPER+Q (close)  SUPER+M (exit)"
  echo "  Tip: add 'exec Hyprland' to ~/.bash_profile to autostart from TTY."
fi
