"""Hoja de estilo (QSS) para un aspecto oscuro y limpio."""

# Paleta
BG = "#0f1419"          # fondo general
PANEL = "#171d26"       # paneles
PANEL_2 = "#1e2631"     # elementos elevados
BORDER = "#2b3443"
TEXT = "#e6edf3"
MUTED = "#8b98a9"
ACCENT = "#16c79a"      # verde-teal (motivo RFID)
ACCENT_DK = "#0fa07c"
CONSOLE_BG = "#0a0e13"
CONSOLE_TEXT = "#c8f7e4"
OK = "#16c79a"
BAD = "#ef5350"
WARN = "#f5a623"

STYLESHEET = f"""
* {{
    font-family: "Inter", "Segoe UI", "Cantarell", sans-serif;
    font-size: 13px;
    color: {TEXT};
}}
QMainWindow, QWidget#central {{
    background: {BG};
}}

/* Cabecera */
QFrame#header {{
    background: {PANEL};
    border-bottom: 1px solid {BORDER};
}}
QLabel#title {{
    font-size: 17px;
    font-weight: 700;
    color: {TEXT};
}}
QLabel#subtitle {{
    color: {MUTED};
    font-size: 12px;
}}

/* Paneles agrupados */
QGroupBox {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 10px;
    margin-top: 14px;
    padding: 10px 10px 10px 10px;
    font-weight: 600;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 4px;
    color: {ACCENT};
}}

/* Botones de acción */
QPushButton {{
    background: {PANEL_2};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 8px 12px;
    color: {TEXT};
    text-align: left;
}}
QPushButton:hover {{
    border-color: {ACCENT};
    background: #233041;
}}
QPushButton:pressed {{
    background: #2a3a4d;
}}
QPushButton:disabled {{
    color: {MUTED};
    border-color: {BORDER};
    background: {PANEL};
}}

/* Botón primario (Ejecutar) */
QPushButton#primary {{
    background: {ACCENT};
    color: #07130f;
    font-weight: 700;
    border: none;
    text-align: center;
}}
QPushButton#primary:hover {{ background: {ACCENT_DK}; }}
QPushButton#primary:disabled {{ background: #2b4b41; color: #6f8a81; }}

QPushButton#danger {{
    background: transparent;
    border: 1px solid {BAD};
    color: {BAD};
    text-align: center;
}}
QPushButton#danger:hover {{ background: rgba(239,83,80,0.12); }}

/* Consola */
QPlainTextEdit#console {{
    background: {CONSOLE_BG};
    color: {CONSOLE_TEXT};
    border: 1px solid {BORDER};
    border-radius: 10px;
    font-family: "JetBrains Mono", "DejaVu Sans Mono", "Consolas", monospace;
    font-size: 12.5px;
    padding: 10px;
    selection-background-color: {ACCENT_DK};
}}

/* Entradas de texto */
QLineEdit {{
    background: {CONSOLE_BG};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 7px 10px;
    color: {TEXT};
    font-family: "JetBrains Mono", "DejaVu Sans Mono", monospace;
}}
QLineEdit:focus {{ border-color: {ACCENT}; }}

/* Pestañas */
QTabWidget::pane {{
    border: 1px solid {BORDER};
    border-radius: 10px;
    top: -1px;
    background: {PANEL};
}}
QTabBar::tab {{
    background: transparent;
    color: {MUTED};
    padding: 8px 16px;
    border: none;
    font-weight: 600;
}}
QTabBar::tab:selected {{
    color: {ACCENT};
    border-bottom: 2px solid {ACCENT};
}}
QTabBar::tab:hover {{ color: {TEXT}; }}

/* Barra de estado */
QStatusBar {{
    background: {PANEL};
    color: {MUTED};
    border-top: 1px solid {BORDER};
}}
QStatusBar::item {{ border: none; }}

/* Barras de desplazamiento */
QScrollBar:vertical {{
    background: transparent; width: 10px; margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER}; border-radius: 5px; min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{ background: {MUTED}; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}
"""
