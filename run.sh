#!/usr/bin/env bash
# Lanzador de Proxmark3 Easy GUI.
# Arranca la aplicación usando el Python del sistema (o el venv si existe).
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Si hay un entorno virtual creado por install.sh, úsalo.
if [[ -x "$DIR/.venv/bin/python" ]]; then
    PY="$DIR/.venv/bin/python"
else
    PY="$(command -v python3 || true)"
fi

if [[ -z "${PY:-}" ]]; then
    echo "No se encuentra python3. Instálalo: sudo apt install python3" >&2
    exit 1
fi

cd "$DIR"
exec "$PY" -m pm3gui "$@"
