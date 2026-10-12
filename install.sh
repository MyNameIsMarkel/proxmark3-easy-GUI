#!/usr/bin/env bash
#
# Instalador de Proxmark3 Easy GUI.
# - Comprueba dependencias (python3 + PyQt5).
# - Crea el acceso directo en el menú de aplicaciones y en el Escritorio.
# - Registra el icono.
#
# No requiere conexión a Internet salvo que falte PyQt5 y elijas instalarlo.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ICON_SRC="$DIR/pm3gui/resources/icon.png"
RUN="$DIR/run.sh"
APP_ID="proxmark3-easy-gui"

say()  { printf '\033[1;36m[*]\033[0m %s\n' "$*"; }
ok()   { printf '\033[1;32m[+]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[!]\033[0m %s\n' "$*"; }
err()  { printf '\033[1;31m[x]\033[0m %s\n' "$*" >&2; }

# ---------------------------------------------------------------- Python
if ! command -v python3 >/dev/null 2>&1; then
    err "No se encuentra python3. Instálalo con: sudo apt install python3"
    exit 1
fi

check_pyqt() { python3 -c "import PyQt5" >/dev/null 2>&1; }

if ! check_pyqt; then
    warn "No se encontró PyQt5."
    if command -v apt >/dev/null 2>&1; then
        read -r -p "¿Instalar python3-pyqt5 con apt ahora? [S/n] " ans
        ans=${ans:-S}
        if [[ "$ans" =~ ^[SsYy]$ ]]; then
            sudo apt update && sudo apt install -y python3-pyqt5
        fi
    fi
    if ! check_pyqt; then
        warn "Creando entorno virtual local con PyQt5 (pip)…"
        python3 -m venv "$DIR/.venv"
        "$DIR/.venv/bin/pip" install --upgrade pip >/dev/null
        "$DIR/.venv/bin/pip" install PyQt5
        ok "Entorno virtual listo en $DIR/.venv"
    fi
fi
check_pyqt || "$DIR/.venv/bin/python" -c "import PyQt5" >/dev/null 2>&1 \
    || { err "PyQt5 sigue sin estar disponible."; exit 1; }
ok "Dependencias correctas."

# ----------------------------------------------------- Comprobar pm3
if ! command -v pm3 >/dev/null 2>&1 && ! command -v proxmark3 >/dev/null 2>&1; then
    warn "No se encontró el cliente 'pm3' en el PATH."
    warn "La GUI se instalará igualmente, pero necesitarás el cliente Proxmark3"
    warn "(en Kali: sudo apt install proxmark3) para que funcione."
fi

# ----------------------------------------------------- Permisos de ejecución
chmod +x "$RUN"

# ----------------------------------------------------- Icono en el tema
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
mkdir -p "$ICON_DIR"
cp -f "$ICON_SRC" "$ICON_DIR/$APP_ID.png"
gtk-update-icon-cache -q "$HOME/.local/share/icons/hicolor" 2>/dev/null || true

# ----------------------------------------------------- Generar .desktop
build_desktop() {
    sed -e "s|__EXEC__|$RUN|g" -e "s|__ICON__|$ICON_SRC|g" \
        "$DIR/$APP_ID.desktop.in" > "$1"
    chmod +x "$1"
}

APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPS_DIR"
build_desktop "$APPS_DIR/$APP_ID.desktop"
update-desktop-database -q "$APPS_DIR" 2>/dev/null || true
ok "Entrada de menú instalada."

# ----------------------------------------------------- Acceso directo en el Escritorio
# Carpeta del Escritorio. xdg-user-dir puede devolver una ruta en inglés
# (/root/Desktop) o inexistente aunque la carpeta real sea "Escritorio",
# así que elegimos la PRIMERA carpeta localizada que exista de verdad.
XDG_DESKTOP="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
DESKTOP_DIR=""
for cand in "$HOME/Escritorio" "$XDG_DESKTOP" "$HOME/Desktop"; do
    if [[ -n "$cand" && "$cand" != "$HOME" && -d "$cand" ]]; then
        DESKTOP_DIR="$cand"; break
    fi
done
# Si no existe ninguna, créala (la de xdg si es válida; si no, Escritorio).
if [[ -z "$DESKTOP_DIR" ]]; then
    if [[ -n "$XDG_DESKTOP" && "$XDG_DESKTOP" != "$HOME" ]]; then
        DESKTOP_DIR="$XDG_DESKTOP"
    else
        DESKTOP_DIR="$HOME/Escritorio"
    fi
    mkdir -p "$DESKTOP_DIR"
fi
DESK_FILE="$DESKTOP_DIR/$APP_ID.desktop"
build_desktop "$DESK_FILE"
# Marcar como confiable para que GNOME/otros muestren el icono y no una advertencia.
gio set "$DESK_FILE" metadata::trusted true 2>/dev/null || true
chmod +x "$DESK_FILE"
ok "Acceso directo creado en: $DESK_FILE"

echo
ok "Instalación completada."
echo "   Puedes abrir la app desde el menú de aplicaciones, el icono del Escritorio,"
echo "   o ejecutando:  $RUN"
