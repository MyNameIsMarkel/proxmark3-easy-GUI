"""Hoja de estilo (QSS) para un aspecto oscuro y limpio."""

# Paleta (azul como color principal; el resto armoniza con él)
BG = "#000000"          # fondo general (azul muy oscuro)
PANEL = "#0c0c0c"       # paneles
PANEL_2 = "#161616"     # elementos elevados
BORDER = "#2b2b2b"
TEXT = "#f4f4f4"
MUTED = "#8c8c8c"
ACCENT = "#ffffff"      # azul principal
ACCENT_DK = "#cccccc"
CONSOLE_BG = "#000000"
CONSOLE_TEXT = "#e8e8e8"  # azul claro para la consola
OK = "#ffffff"          # "conectado" en el azul principal
BAD = "#d7d7d7"         # error (rojo cálido que combina con el azul)
WARN = "#a8a8a8"        # aviso (ámbar)

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
    background: #2e2e2e;
}}
QPushButton:pressed {{
    background: #373737;
}}
QPushButton:disabled {{
    color: {MUTED};
    border-color: {BORDER};
    background: {PANEL};
}}

/* Botón primario (Ejecutar) */
QPushButton#primary {{
    background: {ACCENT};
    color: #0f0f0f;
    font-weight: 700;
    border: none;
    text-align: center;
}}
QPushButton#primary:hover {{ background: {ACCENT_DK}; }}
QPushButton#primary:disabled {{ background: #353535; color: #818181; }}

QPushButton#danger {{
    background: transparent;
    border: 1px solid {BAD};
    color: {BAD};
    text-align: center;
}}
QPushButton#danger:hover {{ background: rgba(129, 129, 129,0.12); }}

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
