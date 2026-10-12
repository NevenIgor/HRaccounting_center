# -*- coding: utf-8 -*-
"""
Единая тема оформления СПО учета личного состава.
Современный «светлый» интерфейс: аккуратные карточки, мягкие тени,
продуманная типографика, единая палитра.
"""

# ---------------------------------------------------------------------------
# Палитра
# ---------------------------------------------------------------------------
ACCENT = '#155e9c'          # основной акцент (глубокий синий)
ACCENT_DARK = '#0f4a7d'     # наведение / активные элементы
ACCENT_LIGHT = '#e3eefb'    # подсветка выбранных элементов
SUCCESS = '#2e7d32'         # позитивные действия
DANGER = '#c62828'          # удаление / опасные действия
BG = '#eef2f7'              # фон окна
SURFACE = '#ffffff'         # фон карточек/полей
BORDER = '#d5dde8'          # нейтральные рамки
TEXT = '#1f2a37'            # основной текст
MUTED = '#5b6b7f'           # второстепенный текст


def build_qss():
    return f'''
/* ================================ БАЗА ================================= */
* {{
    font-family: "Segoe UI", "Noto Sans", "Liberation Sans", Arial, sans-serif;
    font-size: 11pt;
    color: {TEXT};
}}

QMainWindow, QDialog, QWidget#CentralHost {{
    background: {BG};
}}

QToolTip {{
    background: {TEXT};
    color: #ffffff;
    border: none;
    padding: 6px 10px;
    border-radius: 6px;
}}

/* ============================== ТУЛБАР ================================= */
QToolBar {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f2f6fb);
    border: none;
    border-bottom: 1px solid {BORDER};
    padding: 8px 12px;
    spacing: 6px;
}}

QToolBar::separator {{
    background: {BORDER};
    width: 1px;
    margin: 6px 10px;
}}

QToolButton {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 6px 12px;
    color: {TEXT};
    font-size: 10pt;
}}

QToolButton:hover {{
    background: {ACCENT_LIGHT};
    border: 1px solid #c2d9f2;
}}

QToolButton:pressed {{
    background: #cfe1f5;
}}

/* =============================== ВКЛАДКИ =============================== */
QTabWidget::pane {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    top: -1px;
}}

QTabBar::tab {{
    background: transparent;
    color: {MUTED};
    padding: 9px 22px;
    margin-right: 4px;
    border: 1px solid transparent;
    border-bottom: none;
    border-top-left-radius: 9px;
    border-top-right-radius: 9px;
    font-size: 11pt;
}}

QTabBar::tab:hover {{
    color: {ACCENT};
    background: #e8f0fa;
}}

QTabBar::tab:selected {{
    background: {SURFACE};
    color: {ACCENT};
    font-weight: 600;
    border: 1px solid {BORDER};
    border-bottom: 2px solid {ACCENT};
}}

/* =========================== ГРУППЫ-КАРТОЧКИ =========================== */
QGroupBox#GBox {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    margin-top: 26px;
    margin-left: 4px;
    margin-right: 4px;
    padding: 16px 14px 14px 14px;
    font-size: 12pt;
}}

QGroupBox#GBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    top: 4px;
    color: {ACCENT};
    font-size: 12.5pt;
    font-weight: 700;
    background: transparent;
    padding: 0px 4px;
}}

QGroupBox {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    margin-top: 22px;
    padding: 14px 12px 12px 12px;
    font-size: 11pt;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    top: 2px;
    color: {ACCENT};
    font-weight: 700;
    padding: 0px 4px;
}}

/* ============================ ФОРМЫ (QFormLayout) ====================== */
QLabel {{
    background: transparent;
}}

QLabel#Name {{
    font-size: 16pt;
    font-weight: 700;
    color: {TEXT};
}}

QFormLabel, QFormLayout label {{
    color: {MUTED};
}}

/* ============================ ПОЛЯ ВВОДА =============================== */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox,
QDateEdit, QComboBox {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 6px 10px;
    selection-background-color: {ACCENT};
    selection-color: #ffffff;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus,
QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus, QComboBox:focus {{
    border: 2px solid {ACCENT};
    padding: 5px 9px;
}}

QLineEdit:disabled, QComboBox:disabled {{
    background: #f1f4f8;
    color: #9aa7b6;
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border: none;
}}

QComboBox QAbstractItemView {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 8px;
    selection-background-color: {ACCENT_LIGHT};
    selection-color: {ACCENT};
    outline: none;
    padding: 4px;
}}

/* ============================== КНОПКИ ================================= */
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2a7abf, stop:1 {ACCENT});
    color: #ffffff;
    border: none;
    border-radius: 9px;
    padding: 8px 18px;
    font-weight: 600;
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2f8ad6, stop:1 #1a6cab);
}}

QPushButton:pressed {{
    background: {ACCENT_DARK};
}}

QPushButton:disabled {{
    background: #c3ccd8;
    color: #eef1f5;
}}

QPushButton#DangerBtn {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #d94343, stop:1 {DANGER});
}}

QPushButton#DangerBtn:hover {{
    background: #b02020;
}}

QPushButton#GhostBtn {{
    background: {SURFACE};
    color: {ACCENT};
    border: 1px solid {BORDER};
    font-weight: 600;
}}

QPushButton#GhostBtn:hover {{
    background: {ACCENT_LIGHT};
    border: 1px solid {ACCENT};
}}

/* ============================ СПИСОК ЛЮДЕЙ ============================= */
QListWidget {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 6px;
    outline: none;
}}

QListWidget::item {{
    border-radius: 8px;
    padding: 9px 12px;
    margin-bottom: 2px;
    color: {TEXT};
}}

QListWidget::item:hover {{
    background: #eef4fb;
}}

QListWidget::item:selected {{
    background: {ACCENT_LIGHT};
    color: {ACCENT_DARK};
    font-weight: 600;
    border-left: 3px solid {ACCENT};
}}

/* ============================== ТАБЛИЦЫ ================================ */
QTableWidget, QTableView {{
    background: {SURFACE};
    alternate-background-color: #f6f9fc;
    border: 1px solid {BORDER};
    border-radius: 12px;
    gridline-color: #e6ecf3;
    selection-background-color: {ACCENT_LIGHT};
    selection-color: {ACCENT_DARK};
    outline: none;
}}

QTableWidget::item, QTableView::item {{
    padding: 6px 8px;
    border: none;
}}

QHeaderView::section {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f4f8fc, stop:1 #e9eff6);
    color: {MUTED};
    font-weight: 700;
    font-size: 10pt;
    padding: 8px 6px;
    border: none;
    border-right: 1px solid {BORDER};
    border-bottom: 2px solid {BORDER};
}}

QTableCornerButton::section {{
    background: #e9eff6;
    border: none;
}}

/* ========================= ЧЕКБОКСЫ / РАДИО ============================ */
QCheckBox, QRadioButton {{
    spacing: 8px;
    background: transparent;
}}

QCheckBox::indicator, QRadioButton::indicator {{
    width: 18px;
    height: 18px;
}}

QCheckBox::indicator:unchecked {{
    border: 2px solid #b6c2d2;
    border-radius: 5px;
    background: {SURFACE};
}}

QCheckBox::indicator:checked {{
    border: 2px solid {ACCENT};
    border-radius: 5px;
    background: {ACCENT};
    image: url(data/check.svg);
}}

QRadioButton::indicator:unchecked {{
    border: 2px solid #b6c2d2;
    border-radius: 10px;
    background: {SURFACE};
}}

QRadioButton::indicator:checked {{
    border: 2px solid {ACCENT};
    border-radius: 10px;
    background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
                fp:0.45, fx:0.5, fy:0.5,
                stop:0 {ACCENT}, stop:0.5 {ACCENT}, stop:0.51 #ffffff);
}}

/* =============================== СЛАЙДЕР =============================== */
QSlider::groove:horizontal {{
    height: 6px;
    background: #dbe4ee;
    border-radius: 3px;
}}

QSlider::sub-page:horizontal {{
    background: {ACCENT};
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: {SURFACE};
    border: 2px solid {ACCENT};
    width: 16px;
    height: 16px;
    margin: -7px 0;
    border-radius: 9px;
}}

QSlider::handle:horizontal:hover {{
    background: {ACCENT_LIGHT};
}}

/* ============================== СКРОЛЛБАРЫ ============================= */
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background: #c3cedb;
    min-height: 30px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical:hover {{
    background: {ACCENT};
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 2px;
}}

QScrollBar::handle:horizontal {{
    background: #c3cedb;
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
    background: {SURFACE};
    border-top: 1px solid {BORDER};
    color: {MUTED};
    font-size: 10pt;
}}

QMenuBar {{
    background: {SURFACE};
    border-bottom: 1px solid {BORDER};
}}

QMenu {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 6px;
}}

QMenu::item {{
    padding: 7px 26px 7px 16px;
    border-radius: 7px;
}}

QMenu::item:selected {{
    background: {ACCENT_LIGHT};
    color: {ACCENT_DARK};
}}

QMessageBox {{
    background: {SURFACE};
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
    """Применяет тему к приложению: шрифт по умолчанию + QSS."""
    from PyQt5 import QtGui

    font = QtGui.QFont('Segoe UI', 11)
    app.setFont(font)
    app.setStyleSheet(build_qss())
    app.setStyle('Fusion')
