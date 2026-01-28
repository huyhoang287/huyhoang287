"""
Modern Theme Module
Provides consistent styling across the application using Slate/Blue theme
"""

class ModernTheme:
    """Modern theme colors and styles"""

    # Color Palette - Slate/Blue Theme
    COLORS = {
        # Primary Colors
        'primary': '#3B82F6',        # Blue
        'primary_hover': '#2563EB',
        'primary_light': '#DBEAFE',

        # Secondary Colors
        'secondary': '#0F172A',      # Dark Slate
        'secondary_hover': '#1E293B',

        # Text Colors
        'text_primary': '#0F172A',   # Dark text
        'text_secondary': '#64748B', # Gray text
        'text_light': '#CBD5E1',     # Light gray
        'text_white': '#FFFFFF',

        # Background Colors
        'bg_primary': '#FFFFFF',     # White
        'bg_secondary': '#F8FAFC',   # Light gray
        'bg_tertiary': '#F1F5F9',    # Lighter gray
        'bg_dark': '#1E293B',        # Dark background

        # Border Colors
        'border': '#E2E8F0',
        'border_dark': '#CBD5E1',

        # Status Colors
        'success': '#10B981',        # Green
        'warning': '#F59E0B',        # Amber
        'error': '#EF4444',          # Red
        'info': '#3B82F6',           # Blue
        'pending': '#F59E0B',        # Amber

        # Table Colors
        'table_header': '#F1F5F9',
        'table_row_even': '#FFFFFF',
        'table_row_odd': '#F8FAFC',
        'table_row_hover': '#EFF6FF',
        'table_row_selected': '#DBEAFE',

        # Weld Status Colors
        'status_pending': '#FEF3C7',     # Light yellow
        'status_accepted': '#D1FAE5',     # Light green
        'status_rejected': '#FEE2E2',     # Light red
        'status_repair': '#FFE4E6',       # Light pink
    }

    # Font Settings
    FONTS = {
        'family': 'Segoe UI, Arial, sans-serif',
        'size_normal': '9pt',
        'size_large': '11pt',
        'size_title': '16px',
        'size_stat': '22px',
    }

    @staticmethod
    def get_stylesheet():
        """
        Get the complete application stylesheet

        Returns:
            str: QSS stylesheet string
        """
        c = ModernTheme.COLORS
        f = ModernTheme.FONTS

        return f"""
        /* Global Styles */
        QWidget {{
            font-family: {f['family']};
            font-size: {f['size_normal']};
            color: {c['text_primary']};
        }}

        QMainWindow {{
            background-color: {c['bg_secondary']};
        }}

        /* Push Buttons */
        QPushButton {{
            background-color: {c['primary']};
            color: {c['text_white']};
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
        }}

        QPushButton:hover {{
            background-color: {c['primary_hover']};
        }}

        QPushButton:pressed {{
            background-color: #1D4ED8;
        }}

        QPushButton:disabled {{
            background-color: {c['border']};
            color: {c['text_light']};
        }}

        QPushButton[secondary="true"] {{
            background-color: {c['bg_tertiary']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
        }}

        QPushButton[secondary="true"]:hover {{
            background-color: {c['border']};
        }}

        QPushButton[danger="true"] {{
            background-color: {c['error']};
        }}

        QPushButton[danger="true"]:hover {{
            background-color: #DC2626;
        }}

        /* Line Edit */
        QLineEdit {{
            background-color: {c['bg_primary']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 8px 12px;
        }}

        QLineEdit:focus {{
            border: 2px solid {c['primary']};
        }}

        QLineEdit:disabled {{
            background-color: {c['bg_tertiary']};
            color: {c['text_secondary']};
        }}

        /* Combo Box */
        QComboBox {{
            background-color: {c['bg_primary']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 8px 12px;
        }}

        QComboBox:hover {{
            border-color: {c['border_dark']};
        }}

        QComboBox:focus {{
            border: 2px solid {c['primary']};
        }}

        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}

        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {c['text_secondary']};
        }}

        QComboBox QAbstractItemView {{
            background-color: {c['bg_primary']};
            border: 1px solid {c['border']};
            selection-background-color: {c['primary_light']};
            selection-color: {c['text_primary']};
        }}

        /* Table Widget */
        QTableWidget {{
            background-color: {c['bg_primary']};
            alternate-background-color: {c['table_row_odd']};
            gridline-color: {c['border']};
            border: 1px solid {c['border']};
            border-radius: 6px;
        }}

        QTableWidget::item {{
            padding: 8px;
        }}

        QTableWidget::item:selected {{
            background-color: {c['table_row_selected']};
            color: {c['text_primary']};
        }}

        QTableWidget::item:hover {{
            background-color: {c['table_row_hover']};
        }}

        QHeaderView::section {{
            background-color: {c['table_header']};
            color: {c['text_primary']};
            font-weight: bold;
            padding: 10px;
            border: none;
            border-bottom: 2px solid {c['border_dark']};
            border-right: 1px solid {c['border']};
        }}

        QHeaderView::section:hover {{
            background-color: {c['bg_tertiary']};
        }}

        /* Scroll Bar */
        QScrollBar:vertical {{
            background-color: {c['bg_tertiary']};
            width: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {c['border_dark']};
            border-radius: 6px;
            min-height: 30px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {c['text_secondary']};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            background-color: {c['bg_tertiary']};
            height: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {c['border_dark']};
            border-radius: 6px;
            min-width: 30px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {c['text_secondary']};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}

        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {c['border']};
            border-radius: 6px;
            background-color: {c['bg_primary']};
        }}

        QTabBar::tab {{
            background-color: {c['bg_tertiary']};
            color: {c['text_secondary']};
            padding: 10px 20px;
            margin-right: 4px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }}

        QTabBar::tab:selected {{
            background-color: {c['primary']};
            color: {c['text_white']};
            font-weight: bold;
        }}

        QTabBar::tab:hover:!selected {{
            background-color: {c['border']};
        }}

        /* Status Bar */
        QStatusBar {{
            background-color: {c['bg_dark']};
            color: {c['text_white']};
            font-size: {f['size_normal']};
        }}

        /* Labels */
        QLabel {{
            color: {c['text_primary']};
        }}

        QLabel[heading="true"] {{
            font-size: {f['size_title']};
            font-weight: bold;
            color: {c['text_primary']};
        }}

        QLabel[stat="true"] {{
            font-size: {f['size_stat']};
            font-weight: bold;
            color: {c['secondary']};
        }}

        /* Group Box */
        QGroupBox {{
            border: 1px solid {c['border']};
            border-radius: 6px;
            margin-top: 10px;
            font-weight: bold;
            background-color: {c['bg_primary']};
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 10px;
            background-color: {c['bg_primary']};
            color: {c['text_primary']};
        }}

        /* Text Edit / Plain Text Edit */
        QTextEdit, QPlainTextEdit {{
            background-color: {c['bg_primary']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 8px;
        }}

        QTextEdit:focus, QPlainTextEdit:focus {{
            border: 2px solid {c['primary']};
        }}

        /* Spin Box / Double Spin Box */
        QSpinBox, QDoubleSpinBox {{
            background-color: {c['bg_primary']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 8px;
        }}

        QSpinBox:focus, QDoubleSpinBox:focus {{
            border: 2px solid {c['primary']};
        }}

        /* Date Edit */
        QDateEdit {{
            background-color: {c['bg_primary']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 8px;
        }}

        QDateEdit:focus {{
            border: 2px solid {c['primary']};
        }}

        QDateEdit::drop-down {{
            border: none;
            width: 30px;
        }}

        /* Progress Bar */
        QProgressBar {{
            border: 1px solid {c['border']};
            border-radius: 6px;
            text-align: center;
            background-color: {c['bg_tertiary']};
        }}

        QProgressBar::chunk {{
            background-color: {c['primary']};
            border-radius: 4px;
        }}

        /* Dialog */
        QDialog {{
            background-color: {c['bg_secondary']};
        }}

        /* Menu Bar */
        QMenuBar {{
            background-color: {c['bg_dark']};
            color: {c['text_white']};
        }}

        QMenuBar::item:selected {{
            background-color: {c['primary']};
        }}

        QMenu {{
            background-color: {c['bg_primary']};
            border: 1px solid {c['border']};
        }}

        QMenu::item:selected {{
            background-color: {c['primary_light']};
        }}

        /* Tooltip */
        QToolTip {{
            background-color: {c['bg_dark']};
            color: {c['text_white']};
            border: 1px solid {c['border_dark']};
            padding: 4px;
        }}
        """

    @staticmethod
    def apply_theme(widget):
        """
        Apply the modern theme to a widget

        Args:
            widget: QWidget to apply theme to
        """
        widget.setStyleSheet(ModernTheme.get_stylesheet())
