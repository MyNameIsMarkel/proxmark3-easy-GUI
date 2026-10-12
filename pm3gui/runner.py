"""
runner.py — Puente entre la GUI y el cliente `pm3` de Iceman.

La aplicación NO reimplementa nada del Proxmark: simplemente invoca el cliente
oficial ya instalado en el sistema (`pm3 -c "<comando>"`) usando QProcess, de
forma que la salida se transmite en tiempo real a la interfaz sin bloquearla.

Esto mantiene total compatibilidad con la instalación existente: cualquier
comando que funcione en la consola `pm3` funciona aquí igual.
"""

from __future__ import annotations

import re
import shutil

from PyQt5.QtCore import QObject, QProcess, pyqtSignal

# Secuencias de escape ANSI (colores/estilos) que emite el cliente pm3.
_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")


def strip_ansi(text: str) -> str:
    """Elimina códigos de color ANSI para mostrar texto limpio en el log."""
    return _ANSI_RE.sub("", text)


def find_pm3() -> str | None:
    """Localiza el ejecutable `pm3` en el PATH. Devuelve la ruta o None."""
    return shutil.which("pm3") or shutil.which("proxmark3")


class Pm3Runner(QObject):
    """
    Ejecuta comandos del Proxmark3 de uno en uno mediante QProcess.

    Señales:
        output(str)        -> fragmento de texto (ya sin ANSI) listo para mostrar
        started(str)       -> se ha lanzado un comando (se pasa el comando)
        finished(int)      -> el comando terminó (código de salida)
        error(str)         -> no se pudo lanzar el proceso (motivo)
    """

    output = pyqtSignal(str)
    started = pyqtSignal(str)
    finished = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._proc: QProcess | None = None
        self._binary: str = find_pm3() or "pm3"
        self._port: str = "auto"  # "auto" = dejar que el wrapper pm3 detecte el puerto

    # ---- configuración ---------------------------------------------------
    def set_binary(self, path: str) -> None:
        if path.strip():
            self._binary = path.strip()

    def set_port(self, port: str) -> None:
        self._port = (port or "auto").strip() or "auto"

    @property
    def binary(self) -> str:
        return self._binary

    @property
    def port(self) -> str:
        return self._port

    def is_running(self) -> bool:
        return self._proc is not None and self._proc.state() != QProcess.NotRunning

    # ---- ejecución -------------------------------------------------------
    def run(self, command: str) -> bool:
        """Lanza `pm3 [puerto] -c "<command>"`. Devuelve False si ya hay uno en curso."""
        if self.is_running():
            return False

        command = command.strip()
        if not command:
            return False

        if not (shutil.which(self._binary) or self._binary.startswith("/")):
            self.error.emit(
                f"No se encuentra el ejecutable '{self._binary}'. "
                "¿Está instalado el cliente pm3 y en el PATH?"
            )
            return False

        args: list[str] = []
        if self._port and self._port != "auto":
            args.append(self._port)
        args += ["-c", command]

        self._proc = QProcess(self)
        self._proc.setProcessChannelMode(QProcess.MergedChannels)
        self._proc.readyReadStandardOutput.connect(self._on_ready_read)
        self._proc.finished.connect(self._on_finished)
        self._proc.errorOccurred.connect(self._on_error)

        self.started.emit(command)
        self._proc.start(self._binary, args)
        return True

    def stop(self) -> None:
        """Interrumpe el comando en curso, si lo hay."""
        if self.is_running() and self._proc is not None:
            self._proc.terminate()
            if not self._proc.waitForFinished(1500):
                self._proc.kill()

    # ---- manejadores internos -------------------------------------------
    def _on_ready_read(self) -> None:
        if self._proc is None:
            return
        data = bytes(self._proc.readAllStandardOutput()).decode("utf-8", "replace")
        self.output.emit(strip_ansi(data))

    def _on_finished(self, code: int, _status) -> None:
        self.finished.emit(int(code))
        self._proc = None

    def _on_error(self, err) -> None:
        mapping = {
            QProcess.FailedToStart: "El proceso no pudo arrancar (ruta o permisos).",
            QProcess.Crashed: "El proceso terminó de forma inesperada.",
            QProcess.Timedout: "Tiempo de espera agotado.",
        }
        self.error.emit(mapping.get(err, "Error desconocido al ejecutar pm3."))
