#!/usr/bin/env bash
# Desinstala los accesos directos y el icono (no borra el repositorio).
set -euo pipefail
APP_ID="proxmark3-easy-gui"

rm -f "$HOME/.local/share/applications/$APP_ID.desktop"
rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/$APP_ID.png"

DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
for d in "$DESKTOP_DIR" "$HOME/Escritorio" "$HOME/Desktop"; do
    [[ -n "$d" && -f "$d/$APP_ID.desktop" ]] && rm -f "$d/$APP_ID.desktop"
done

update-desktop-database -q "$HOME/.local/share/applications" 2>/dev/null || true
echo "[+] Accesos directos e icono eliminados."
echo "    (El entorno virtual .venv y el código siguen en la carpeta del repo.)"
