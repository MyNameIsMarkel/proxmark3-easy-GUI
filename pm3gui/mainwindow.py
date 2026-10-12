"""Ventana principal de Proxmark3 Easy GUI."""

from __future__ import annotations

import os
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap, QTextCursor
from PyQt5.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from .runner import Pm3Runner, find_pm3
from .theme import ACCENT, BAD, MUTED, STYLESHEET, WARN

HERE = os.path.dirname(os.path.abspath(__file__))
ICON_PNG = os.path.join(HERE, "resources", "icon.png")

# Catálogo de acciones rápidas: (etiqueta, comando pm3, descripción/tooltip)
HW_ACTIONS = [
    ("Versión", "hw version", "Versión de cliente y firmware"),
    ("Estado", "hw status", "Estado del hardware y configuración"),
    ("Afinar antenas", "hw tune", "Mide los voltajes de las antenas LF y HF"),
]
SEARCH_ACTIONS = [
    ("Buscar LF", "lf search", "Identifica una tarjeta de 125 kHz"),
    ("Buscar HF", "hf search", "Identifica una tarjeta de 13.56 MHz"),
    ("Autodetectar", "auto", "Prueba LF y HF automáticamente"),
]
LF_ACTIONS = [
    ("Leer EM410x", "lf em 410x reader", "Lee un tag EM4100/EM410x"),
    ("Detectar T55xx", "lf t55xx detect", "Detecta una tarjeta regrabable T5577"),
    ("Volcar T55xx", "lf t55xx dump", "Vuelca los bloques de un T5577"),
    ("Buscar LF", "lf search", "Búsqueda genérica LF"),
]
HF_ACTIONS = [
    ("Info 14a", "hf 14a info", "UID, ATQA/SAK y tipo de tarjeta ISO14443-A"),
    ("Info MIFARE", "hf mf info", "Información de una tarjeta MIFARE"),
    ("Lectura rápida MFU", "hf mfu info", "Información de MIFARE Ultralight/NTAG"),
    ("Buscar HF", "hf search", "Búsqueda genérica HF"),
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.runner = Pm3Runner(self)
        self._action_buttons: list[QPushButton] = []
        self._current_buffer = ""

        self.setWindowTitle("Proxmark3 Easy GUI")
        self.setMinimumSize(1040, 660)
        if os.path.exists(ICON_PNG):
            self.setWindowIcon(QIcon(ICON_PNG))
        self.setStyleSheet(STYLESHEET)

        self._build_ui()
        self._wire_runner()
        self._check_binary_on_start()

    # ------------------------------------------------------------------ UI
    def _build_ui(self) -> None:
        central = QWidget(objectName="central")
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_header())

        body = QWidget()
        body_l = QHBoxLayout(body)
        body_l.setContentsMargins(14, 14, 14, 14)
        body_l.setSpacing(14)
        body_l.addWidget(self._build_left_panel(), 0)
        body_l.addWidget(self._build_right_panel(), 1)
        root.addWidget(body, 1)

        self.status = self.statusBar()
        self.status.showMessage("Listo.")

    def _build_header(self) -> QWidget:
        header = QFrame(objectName="header")
        h = QHBoxLayout(header)
        h.setContentsMargins(16, 12, 16, 12)
        h.setSpacing(12)

        logo = QLabel()
        if os.path.exists(ICON_PNG):
            logo.setPixmap(QPixmap(ICON_PNG).scaled(
                40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h.addWidget(logo)

        titles = QVBoxLayout()
        titles.setSpacing(0)
        titles.addWidget(QLabel("Proxmark3 Easy GUI", objectName="title"))
        titles.addWidget(QLabel("Interfaz para el cliente pm3 (firmware Iceman)",
                                objectName="subtitle"))
        h.addLayout(titles)
        h.addStretch(1)

        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet(f"color: {MUTED}; font-size: 16px;")
        self.status_text = QLabel("Sin comprobar")
        self.status_text.setStyleSheet(f"color: {MUTED};")
        h.addWidget(self.status_dot)
        h.addWidget(self.status_text)
        return header

    def _build_left_panel(self) -> QWidget:
        panel = QWidget()
        panel.setFixedWidth(330)
        v = QVBoxLayout(panel)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(12)

        # --- Conexión ---
        conn = QGroupBox("Conexión")
        cl = QGridLayout(conn)
        cl.setSpacing(8)
        cl.addWidget(QLabel("Puerto"), 0, 0)
        self.port_edit = QLineEdit("auto")
        self.port_edit.setToolTip("Déjalo en 'auto' o indica /dev/ttyACM0")
        cl.addWidget(self.port_edit, 0, 1)
        cl.addWidget(QLabel("Binario"), 1, 0)
        self.bin_edit = QLineEdit(find_pm3() or "pm3")
        cl.addWidget(self.bin_edit, 1, 1)
        self.btn_connect = QPushButton("Comprobar conexión")
        self.btn_connect.setObjectName("primary")
        self.btn_connect.clicked.connect(self._on_connect)
        cl.addWidget(self.btn_connect, 2, 0, 1, 2)
        v.addWidget(conn)

        # --- Hardware ---
        v.addWidget(self._action_group("Hardware", HW_ACTIONS))
        # --- Búsqueda ---
        v.addWidget(self._action_group("Búsqueda de tarjetas", SEARCH_ACTIONS))

        # --- Pestañas LF / HF ---
        tabs = QTabWidget()
        tabs.addTab(self._action_tab(LF_ACTIONS), "LF (125 kHz)")
        tabs.addTab(self._action_tab(HF_ACTIONS), "HF (13.56 MHz)")
        v.addWidget(tabs, 1)
        return panel

    def _action_group(self, title: str, actions) -> QGroupBox:
        box = QGroupBox(title)
        g = QVBoxLayout(box)
        g.setSpacing(6)
        for label, cmd, tip in actions:
            g.addWidget(self._make_action_button(label, cmd, tip))
        return box

    def _action_tab(self, actions) -> QWidget:
        w = QWidget()
        g = QVBoxLayout(w)
        g.setSpacing(6)
        g.setContentsMargins(8, 10, 8, 8)
        for label, cmd, tip in actions:
            g.addWidget(self._make_action_button(label, cmd, tip))
        g.addStretch(1)
        return w

    def _make_action_button(self, label: str, cmd: str, tip: str) -> QPushButton:
        btn = QPushButton(label)
        btn.setToolTip(f"{tip}\n\npm3> {cmd}")
        btn.clicked.connect(lambda _=False, c=cmd: self._run(c))
        self._action_buttons.append(btn)
        return btn

    def _build_right_panel(self) -> QWidget:
        panel = QWidget()
        v = QVBoxLayout(panel)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(10)

        self.console = QPlainTextEdit(objectName="console")
        self.console.setReadOnly(True)
        self.console.setFont(QFont("DejaVu Sans Mono", 11))
        self.console.setPlaceholderText(
            "La salida de pm3 aparecerá aquí.\n\n"
            "Pulsa «Comprobar conexión» o escribe un comando abajo."
        )
        v.addWidget(self.console, 1)

        # Fila de comando libre
        row = QHBoxLayout()
        row.setSpacing(8)
        self.cmd_edit = QLineEdit()
        self.cmd_edit.setPlaceholderText("Escribe cualquier comando pm3 (p. ej. hf 14a info) y pulsa Enter")
        self.cmd_edit.returnPressed.connect(self._on_run_typed)
        row.addWidget(self.cmd_edit, 1)

        self.btn_run = QPushButton("Ejecutar")
        self.btn_run.setObjectName("primary")
        self.btn_run.setFixedWidth(100)
        self.btn_run.clicked.connect(self._on_run_typed)
        row.addWidget(self.btn_run)

        self.btn_stop = QPushButton("Detener")
        self.btn_stop.setObjectName("danger")
        self.btn_stop.setFixedWidth(90)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.runner.stop)
        row.addWidget(self.btn_stop)
        v.addLayout(row)

        # Fila inferior de utilidades
        util = QHBoxLayout()
        util.setSpacing(8)
        btn_clear = QPushButton("Limpiar")
        btn_clear.setFixedWidth(90)
        btn_clear.clicked.connect(self.console.clear)
        util.addWidget(btn_clear)
        btn_save = QPushButton("Guardar log")
        btn_save.setFixedWidth(110)
        btn_save.clicked.connect(self._save_log)
        util.addWidget(btn_save)
        util.addStretch(1)
        btn_about = QPushButton("Acerca de")
        btn_about.setFixedWidth(100)
        btn_about.clicked.connect(self._about)
        util.addWidget(btn_about)
        v.addLayout(util)
        return panel

    # -------------------------------------------------------------- runner
    def _wire_runner(self) -> None:
        self.runner.output.connect(self._append)
        self.runner.started.connect(self._on_started)
        self.runner.finished.connect(self._on_finished)
        self.runner.error.connect(self._on_error)

    def _run(self, command: str) -> None:
        self.runner.set_binary(self.bin_edit.text())
        self.runner.set_port(self.port_edit.text())
        self._current_buffer = ""
        self._append(f"\n\033pm3> {command}\n", prompt=True)
        if not self.runner.run(command):
            self._append("[!] Ya hay un comando en ejecución.\n")

    def _on_run_typed(self) -> None:
        cmd = self.cmd_edit.text().strip()
        if cmd:
            self.cmd_edit.clear()
            self._run(cmd)

    def _on_connect(self) -> None:
        self._pending_connect_check = True
        self._run("hw version")

    def _append(self, text: str, prompt: bool = False) -> None:
        self._current_buffer += text
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.End)
        # El marcador \033 se usa para resaltar la línea de prompt del usuario.
        self.console.insertPlainText(text.replace("\033", ""))
        self.console.moveCursor(QTextCursor.End)

    def _on_started(self, command: str) -> None:
        for b in self._action_buttons:
            b.setEnabled(False)
        self.btn_run.setEnabled(False)
        self.btn_connect.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.status.showMessage(f"Ejecutando: {command}…")

    def _on_finished(self, code: int) -> None:
        for b in self._action_buttons:
            b.setEnabled(True)
        self.btn_run.setEnabled(True)
        self.btn_connect.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.status.showMessage(f"Terminado (código {code}).")

        if getattr(self, "_pending_connect_check", False):
            self._pending_connect_check = False
            buf = self._current_buffer
            if "Proxmark3" in buf and "cannot communicate" not in buf and "ERROR" not in buf:
                self._set_status(True, "Conectado")
            elif "cannot communicate" in buf or "not the same" in buf:
                self._set_status(False, "Sin comunicación / versión")
            else:
                self._set_status(None, "Sin dispositivo")

    def _on_error(self, message: str) -> None:
        self._append(f"[!] {message}\n")
        self.status.showMessage(message)
        for b in self._action_buttons:
            b.setEnabled(True)
        self.btn_run.setEnabled(True)
        self.btn_connect.setEnabled(True)
        self.btn_stop.setEnabled(False)

    def _set_status(self, state, label: str) -> None:
        color = {True: ACCENT, False: BAD, None: WARN}.get(state, MUTED)
        self.status_dot.setStyleSheet(f"color: {color}; font-size: 16px;")
        self.status_text.setStyleSheet(f"color: {color};")
        self.status_text.setText(label)

    # --------------------------------------------------------------- utils
    def _check_binary_on_start(self) -> None:
        if find_pm3() is None:
            self._append(
                "[!] No se ha encontrado el cliente 'pm3' en el PATH.\n"
                "    Instálalo (en Kali: sudo apt install proxmark3) o indica la\n"
                "    ruta del binario en el campo «Binario».\n"
            )
            self._set_status(False, "pm3 no encontrado")

    def _save_log(self) -> None:
        default = f"pm3-log-{datetime.now():%Y%m%d-%H%M%S}.txt"
        path, _ = QFileDialog.getSaveFileName(self, "Guardar log", default,
                                              "Texto (*.txt);;Todos (*)")
        if path:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(self.console.toPlainText())
            self.status.showMessage(f"Log guardado en {path}")

    def _about(self) -> None:
        QMessageBox.information(
            self, "Acerca de Proxmark3 Easy GUI",
            "<b>Proxmark3 Easy GUI</b><br>"
            "Interfaz gráfica ligera sobre el cliente <code>pm3</code> de Iceman.<br><br>"
            "No modifica tu instalación: ejecuta los mismos comandos que la consola.<br><br>"
            "Úsalo solo con tarjetas y dispositivos de tu propiedad o con autorización.",
        )
