# -*- coding: utf-8 -*-
"""
Единая тема оформления СПО учета личного состава.
Светлая и тёмная («чёрная») темы: аккуратные карточки, мягкие тени,
продуманная типографика, единая палитра.
"""

# ---------------------------------------------------------------------------
# Палитры (светлая и тёмная)
# ---------------------------------------------------------------------------
LIGHT = dict(
    ACCENT='#155e9c',        # основной акцент (глубокий синий)
    ACCENT_DARK='#0f4a7d',   # наведение / активные элементы
    ACCENT_LIGHT='#e3eefb',  # подсветка выбранных элементов
    SUCCESS='#2e7d32',
    DANGER='#c62828',
    BG='#eef2f7',            # фон окна
    SURFACE='#ffffff',       # фон карточек/полей
    BORDER='#d5dde8',        # нейтральные рамки
    TEXT='#1f2a37',          # основной текст
    MUTED='#5b6b7f',         # второстепенный текст
    HOVER_BG='#e8f0fa',      # hover вкладок
    ROW_HOVER='#eef4fb',     # hover строк списка
    ALT_ROW='#f6f9fc',       # чередование строк таблиц
    GRID='#e6ecf3',          # линии сетки таблиц
    DISABLED_BG='#f1f4f8',
    DISABLED_TEXT='#9aa7b6',
    BTN_TOP='#2a7abf',
    BTN_TOP_HOVER='#2f8ad6',
    BTN_BOTTOM_HOVER='#1a6cab',
    DANGER_TOP='#d94343',
    DANGER_HOVER='#b02020',
    TOOL_TOP='#ffffff',
    TOOL_BOTTOM='#f2f6fb',
    PRESSED='#cfe1f5',
    HEAD_TOP='#f4f8fc',
    HEAD_BOTTOM='#e9eff6',
    HANDLE='#c3cedb',
    GROOVE='#dbe4ee',
    TAB_BG='#dfe7f1',           # неактивные вкладки (светлая)
    PANE_BG='#ffffff',          # подложка области вкладок (светлая)
)

DARK = dict(
    ACCENT='#4da3ff',        # яркий синий на тёмном фоне
    ACCENT_DARK='#2f7fd1',
    ACCENT_LIGHT='#16324f',  # подсветка выбранных элементов (тёмно-синяя)
    SUCCESS='#66bb6a',
    DANGER='#ef5350',
    BG='#0d0f12',            # почти чёрный фон окна
    SURFACE='#171a1f',       # фон карточек/полей
    BORDER='#2b313a',        # нейтральные рамки
    TEXT='#e8edf3',          # основной текст
    MUTED='#9aa8ba',         # второстепенный текст
    HOVER_BG='#1f2630',
    ROW_HOVER='#1c232c',
    ALT_ROW='#1b1f25',
    GRID='#262c34',
    DISABLED_BG='#20242b',
    DISABLED_TEXT='#5c6672',
    BTN_TOP='#2b6ea6',
    BTN_TOP_HOVER='#3580bd',
    BTN_BOTTOM_HOVER='#1f5a8c',
    DANGER_TOP='#d34545',
    DANGER_HOVER='#a92e2e',
    TOOL_TOP='#14171b',
    TOOL_BOTTOM='#101317',
    PRESSED='#22364d',
    HEAD_TOP='#1b2027',
    HEAD_BOTTOM='#171b21',
    HANDLE='#3a434f',
    GROOVE='#2a303a',
    TAB_BG='#12151a',           # неактивные вкладки (тёмная)
    PANE_BG='#12151a',          # подложка области вкладок — тёмная, не режет глаза
)
DARK['ACCENT_LIGHT'] = '#16324f'   # подсветка выбранных элементов (тёмно-синяя)
# значения по умолчанию для палитр, если ключ не задан
for _pal in (LIGHT, DARK):
    _pal.setdefault('TAB_BG', _pal.get('BG'))
    _pal.setdefault('PANE_BG', _pal.get('SURFACE'))

# Активная палитра (по умолчанию — светлая); переключается set_dark_mode()
P = dict(LIGHT)

# Совместимость со старым кодом, использующим style.ACCENT / style.MUTED и т.п.
def _sync_globals():
    g = globals()
    g['ACCENT'] = P['ACCENT']
    g['ACCENT_DARK'] = P['ACCENT_DARK']
    g['ACCENT_LIGHT'] = P['ACCENT_LIGHT']
    # остальные цвета палитры — автоматически, чтобы style.BG / style.SURFACE и т.д.
    # всегда соответствовали активной теме
    for k, v in P.items():
        if k not in g or g[k] != v:
            g[k] = v
    g['SUCCESS'] = P['SUCCESS']
    g['DANGER'] = P['DANGER']
    g['BG'] = P['BG']
    g['SURFACE'] = P['SURFACE']
    g['BORDER'] = P['BORDER']
    g['TEXT'] = P['TEXT']
    g['MUTED'] = P['MUTED']

_sync_globals()


def set_dark_mode(enabled):
    """Переключает активную палитру (True — чёрная тема)."""
    P.clear()
    P.update(DARK if enabled else LIGHT)
    _sync_globals()


def is_dark():
    return P is not None and P.get('BG') == DARK['BG']


def build_qss(p=None):
    p = p or P
    A = p['ACCENT']; AD = p['ACCENT_DARK']; AL = p['ACCENT_LIGHT']
    SU = p['SUCCESS']; DA = p['DANGER']; BGG = p['BG']; SF = p['SURFACE']
    BD = p['BORDER']; TX = p['TEXT']; MU = p['MUTED']
    return f'''
/* ================================ БАЗА ================================= */
* {{
    font-family: "Segoe UI", "Noto Sans", "Liberation Sans", Arial, sans-serif;
    font-size: 13pt;
    color: {TX};
}}

QMainWindow, QDialog, QWidget#CentralHost {{
    background: {BGG};
}}

QToolTip {{
    background: {TX};
    color: {BGG};
    border: none;
    padding: 6px 10px;
    border-radius: 6px;
}}

/* ============================== ТУЛБАР ================================= */
QToolBar {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {p['TOOL_TOP']}, stop:1 {p['TOOL_BOTTOM']});
    border: none;
    border-bottom: 1px solid {BD};
    padding: 8px 12px;
    spacing: 6px;
}}

/* правая часть тулбара — прижимает кнопку темы к краю окна */
QToolButton#spacer_btn {{
    background: transparent;
    border: none;
}}

QToolButton#theme_btn {{
    background: transparent;
    border: 1px solid {BD};
    border-radius: 8px;
    padding: 4px 10px;
    color: {TX};
    font-size: 12pt;
}}

QToolButton#theme_btn:hover {{
    background: {p['HOVER_BG']};
    border-color: {A};
    color: {A};
}}

QToolBar::separator {{
    background: {BD};
    width: 1px;
    margin: 6px 10px;
}}

QToolButton {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 8px 14px;
    color: {TX};
    font-size: 12pt;
}}

QToolButton:hover {{
    background: {AL};
    border: 1px solid {AD};
}}

QToolButton:pressed {{
    background: {p['PRESSED']};
}}

/* =============================== ВКЛАДКИ =============================== */
QTabWidget::pane {{
    background: {p['PANE_BG']};
    border: 1px solid {BD};
    border-radius: 12px;
    top: -1px;
}}

/* содержимое вкладки (карточки сотрудников и т.п.) — всегда в цвете темы */
QTabWidget > QWidget, QStackedWidget, QScrollArea {{
    background: {p['PANE_BG']};
}}

QScrollArea > QWidget > QWidget {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {p['PANE_BG']}, stop:1 {BGG});
}}

QTabBar::tab {{
    background: {p['TAB_BG']};
    color: {MU};
    padding: 11px 26px;
    margin-right: 4px;
    border: 1px solid {BD};
    border-bottom: none;
    border-top-left-radius: 9px;
    border-top-right-radius: 9px;
    font-size: 13pt;
}}

QTabBar::tab:hover {{
    color: {A};
    background: {p['HOVER_BG']};
}}

QTabBar::tab:selected {{
    background: {SF};
    color: {A};
    font-weight: 600;
    border: 1px solid {BD};
    border-bottom: 2px solid {A};
}}

/* =========================== ГРУППЫ-КАРТОЧКИ =========================== */
QGroupBox#GBox {{
    background: {SF};
    border: 1px solid {BD};
    border-radius: 12px;
    margin-top: 28px;
    margin-left: 4px;
    margin-right: 4px;
    padding: 16px 14px 14px 14px;
    font-size: 13pt;
}}

QGroupBox#GBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    top: 4px;
    color: {A};
    font-size: 14.5pt;
    font-weight: 700;
    background: transparent;
    padding: 0px 4px;
}}

QGroupBox {{
    background: {SF};
    border: 1px solid {BD};
    border-radius: 12px;
    margin-top: 24px;
    padding: 14px 12px 12px 12px;
    font-size: 13pt;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    top: 2px;
    color: {A};
    font-weight: 700;
    padding: 0px 4px;
}}

/* ============================ ФОРМЫ (QFormLayout) ====================== */
QLabel {{
    background: transparent;
}}

QLabel#Name {{
    font-size: 19pt;
    font-weight: 700;
    color: {TX};
}}

QFormLabel, QFormLayout label {{
    color: {MU};
}}

/* ============================ ПОЛЯ ВВОДА =============================== */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox,
QDateEdit, QComboBox {{
    background: {SF};
    border: 1px solid {BD};
    border-radius: 8px;
    padding: 8px 12px;
    selection-background-color: {A};
    selection-color: #ffffff;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus,
QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus, QComboBox:focus {{
    border: 2px solid {A};
    padding: 7px 11px;
}}

QLineEdit:disabled, QComboBox:disabled {{
    background: {p['DISABLED_BG']};
    color: {p['DISABLED_TEXT']};
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border: none;
}}

QComboBox QAbstractItemView {{
    background: {SF};
    border: 1px solid {BD};
    border-radius: 8px;
    selection-background-color: {AL};
    selection-color: {A};
    outline: none;
    padding: 4px;
}}

/* ============================== КНОПКИ ================================= */
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {p['BTN_TOP']}, stop:1 {A});
    color: #ffffff;
    border: none;
    border-radius: 9px;
    padding: 10px 22px;
    font-size: 13pt;
    font-weight: 600;
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {p['BTN_TOP_HOVER']}, stop:1 {p['BTN_BOTTOM_HOVER']});
}}

QPushButton:pressed {{
    background: {AD};
}}

QPushButton:disabled {{
    background: {p['DISABLED_BG']};
    color: {p['DISABLED_TEXT']};
}}

QPushButton#DangerBtn {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {p['DANGER_TOP']}, stop:1 {DA});
}}

QPushButton#DangerBtn:hover {{
    background: {p['DANGER_HOVER']};
}}

QPushButton#GhostBtn {{
    background: {SF};
    color: {A};
    border: 1px solid {BD};
    font-weight: 600;
}}

QPushButton#GhostBtn:hover {{
    background: {AL};
    border: 1px solid {A};
}}

/* ============================ СПИСОК ЛЮДЕЙ ============================= */
QListWidget {{
    background: {SF};
    border: 1px solid {BD};
    border-radius: 12px;
    padding: 6px;
    outline: none;
}}

QListWidget::item {{
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 2px;
    color: {TX};
    font-size: 13.5pt;
}}

QListWidget::item:hover {{
    background: {p['ROW_HOVER']};
}}

QListWidget::item:selected {{
    background: {AL};
    color: {AD};
    font-weight: 600;
    border-left: 3px solid {A};
}}

/* ============================== ТАБЛИЦЫ ================================ */
QTableWidget, QTableView {{
    background: {SF};
    alternate-background-color: {p['ALT_ROW']};
    border: 1px solid {BD};
    border-radius: 12px;
    gridline-color: {p['GRID']};
    selection-background-color: {AL};
    selection-color: {AD};
    outline: none;
}}

QTableWidget::item, QTableView::item {{
    padding: 9px 10px;
    border: none;
    font-size: 12.5pt;
}}

QHeaderView::section {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {p['HEAD_TOP']}, stop:1 {p['HEAD_BOTTOM']});
    color: {MU};
    font-weight: 700;
    font-size: 12pt;
    padding: 10px 8px;
    border: none;
    border-right: 1px solid {BD};
    border-bottom: 2px solid {BD};
}}

QTableCornerButton::section {{
    background: {p['HEAD_BOTTOM']};
    border: none;
}}

/* ========================= ЧЕКБОКСЫ / РАДИО ============================ */
QCheckBox, QRadioButton {{
    spacing: 8px;
    background: transparent;
    font-size: 13pt;
}}

QCheckBox::indicator, QRadioButton::indicator {{
    width: 20px;
    height: 20px;
}}

QCheckBox::indicator:unchecked {{
    border: 2px solid {BD};
    border-radius: 5px;
    background: {SF};
}}

QCheckBox::indicator:checked {{
    border: 2px solid {A};
    border-radius: 5px;
    background: {A};
    image: url(data/check.svg);
}}

QRadioButton::indicator:unchecked {{
    border: 2px solid {BD};
    border-radius: 10px;
    background: {SF};
}}

QRadioButton::indicator:checked {{
    border: 2px solid {A};
    border-radius: 10px;
    background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
                fp:0.45, fx:0.5, fy:0.5,
                stop:0 {A}, stop:0.5 {A}, stop:0.51 {SF});
}}

/* =============================== СЛАЙДЕР =============================== */
QSlider {{
    /* вертикальные отступы = половине высоты ручки, чтобы ручка целиком
       влезала в виджет (иначе её «съедают» соседние подписи) */
    padding: 8px 0px;
}}

QSlider::groove:horizontal {{
    height: 6px;
    background: {p['GROOVE']};
    border-radius: 3px;
}}

QSlider::sub-page:horizontal {{
    background: {A};
    border-radius: 3px;
}}

QSlider::add-page:horizontal {{
    background: {p['GROOVE']};
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: {SF};
    border: 2px solid {A};
    width: 16px;
    height: 16px;
    margin: -7px 0;
    border-radius: 9px;
}}

QSlider::handle:horizontal:hover {{
    background: {AL};
}}

/* ============================== СКРОЛЛБАРЫ ============================= */
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background: {p['HANDLE']};
    min-height: 30px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical:hover {{
    background: {A};
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 2px;
}}

QScrollBar::handle:horizontal {{
    background: {p['HANDLE']};
    min-width: 30px;
    border-radius: 5px;
}}

QScrollBar::add-line, QScrollBar::sub-line {{
    height: 0; width: 0;
}}

QScrollBar::add-page, QScrollBar::sub-page {{
    background: transparent;
}}

/* ======================= СТАТУС-БАР / МЕНЮ / СТИТУС ==================== */
QStatusBar {{
    background: {SF};
    border-top: 1px solid {BD};
    color: {MU};
    font-size: 12pt;
}}

QMenuBar {{
    background: {SF};
    border-bottom: 1px solid {BD};
}}

QMenu {{
    background: {SF};
    border: 1px solid {BD};
    border-radius: 10px;
    padding: 6px;
}}

QMenu::item {{
    padding: 7px 26px 7px 16px;
    border-radius: 7px;
}}

QMenu::item:selected {{
    background: {AL};
    color: {AD};
}}

QMessageBox {{
    background: {SF};
}}

/* =============================== SPLITTER ============================== */
QSplitter::handle {{
    background: transparent;
}}

QSplitter::handle:horizontal {{
    width: 6px;
}}
'''


def apply_theme(app):
    """Применяет активную тему к приложению: шрифт по умолчанию + QSS."""
    from PyQt5 import QtGui

    font = QtGui.QFont('Segoe UI', 13)
    app.setFont(font)
    app.setStyleSheet(build_qss())
    app.setStyle('Fusion')
