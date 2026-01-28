"""
UI Helper Functions
Provides reusable UI components and helper functions
"""

from PyQt6.QtWidgets import (
    QMessageBox, QTableWidgetItem, QDialog, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox,
    QDateEdit, QTextEdit, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
import logging

logger = logging.getLogger(__name__)


class EditableTableWidgetItem(QTableWidgetItem):
    """Custom table widget item that supports Excel-like editing"""

    def __init__(self, text=""):
        super().__init__(text)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsEditable)


def show_message(parent, title, message, icon=QMessageBox.Icon.Information):
    """
    Show a message dialog

    Args:
        parent: Parent widget
        title: Dialog title
        message: Message text
        icon: Message icon (Information, Warning, Critical, Question)
    """
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(icon)
    msg_box.exec()


def show_success(parent, message):
    """Show success message"""
    show_message(parent, "Success", message, QMessageBox.Icon.Information)


def show_error(parent, message):
    """Show error message"""
    show_message(parent, "Error", message, QMessageBox.Icon.Critical)


def show_warning(parent, message):
    """Show warning message"""
    show_message(parent, "Warning", message, QMessageBox.Icon.Warning)


def show_confirm(parent, title, message):
    """
    Show confirmation dialog

    Args:
        parent: Parent widget
        title: Dialog title
        message: Confirmation message

    Returns:
        bool: True if user clicked Yes, False otherwise
    """
    reply = QMessageBox.question(
        parent,
        title,
        message,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )
    return reply == QMessageBox.StandardButton.Yes


def set_table_row_color(table, row, color):
    """
    Set background color for an entire table row

    Args:
        table: QTableWidget
        row: Row index
        color: QColor or color string
    """
    if isinstance(color, str):
        color = QColor(color)

    for col in range(table.columnCount()):
        item = table.item(row, col)
        if item:
            item.setBackground(color)


def get_status_color(status):
    """
    Get color for weld status

    Args:
        status: Status string (Pending, Accepted, Rejected, Repair)

    Returns:
        str: Color hex code
    """
    status_colors = {
        'Pending': '#FEF3C7',    # Light yellow
        'Accepted': '#D1FAE5',   # Light green
        'Rejected': '#FEE2E2',   # Light red
        'Repair': '#FFE4E6'      # Light pink
    }
    return status_colors.get(status, '#FFFFFF')


def populate_combo_box(combo_box, items, current_value=None):
    """
    Populate a combo box with items

    Args:
        combo_box: QComboBox to populate
        items: List of items (strings or dicts with 'id' and 'text' keys)
        current_value: Current value to select
    """
    combo_box.clear()

    for item in items:
        if isinstance(item, dict):
            combo_box.addItem(item['text'], item['id'])
        else:
            combo_box.addItem(str(item))

    # Set current value if provided
    if current_value is not None:
        index = combo_box.findText(str(current_value))
        if index >= 0:
            combo_box.setCurrentIndex(index)


def create_date_edit(date_value=None):
    """
    Create a QDateEdit with sensible defaults

    Args:
        date_value: Initial date (QDate, datetime, or string YYYY-MM-DD)

    Returns:
        QDateEdit: Configured date edit widget
    """
    date_edit = QDateEdit()
    date_edit.setCalendarPopup(True)
    date_edit.setDisplayFormat("yyyy-MM-dd")

    if date_value:
        if isinstance(date_value, str):
            date_edit.setDate(QDate.fromString(date_value, "yyyy-MM-dd"))
        else:
            date_edit.setDate(date_value)
    else:
        date_edit.setDate(QDate.currentDate())

    return date_edit


class SimpleFormDialog(QDialog):
    """
    Simple form dialog for data entry

    Usage:
        dialog = SimpleFormDialog(parent, "Add Welder")
        dialog.add_field("Welder Code", QLineEdit())
        dialog.add_field("Full Name", QLineEdit())
        if dialog.exec():
            data = dialog.get_data()
    """

    def __init__(self, parent=None, title="Form"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.fields = {}

        # Buttons
        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

    def add_field(self, label, widget, key=None):
        """
        Add a field to the form

        Args:
            label: Field label
            widget: Input widget (QLineEdit, QComboBox, etc.)
            key: Key for data dictionary (default: label)
        """
        if key is None:
            key = label

        field_layout = QHBoxLayout()
        label_widget = QLabel(label + ":")
        label_widget.setMinimumWidth(120)
        field_layout.addWidget(label_widget)
        field_layout.addWidget(widget)

        self.layout.addLayout(field_layout)
        self.fields[key] = widget

    def finalize(self):
        """Call this after adding all fields"""
        self.layout.addLayout(self.button_layout)

    def get_data(self):
        """
        Get form data as dictionary

        Returns:
            dict: Field values keyed by field names
        """
        data = {}

        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                data[key] = widget.text()
            elif isinstance(widget, QComboBox):
                data[key] = widget.currentText()
                data[key + '_id'] = widget.currentData()
            elif isinstance(widget, QDateEdit):
                data[key] = widget.date().toString("yyyy-MM-dd")
            elif isinstance(widget, QTextEdit):
                data[key] = widget.toPlainText()
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                data[key] = widget.value()

        return data

    def set_data(self, data):
        """
        Set form data from dictionary

        Args:
            data: Dictionary of field values
        """
        for key, value in data.items():
            if key in self.fields:
                widget = self.fields[key]

                if isinstance(widget, QLineEdit):
                    widget.setText(str(value) if value else "")
                elif isinstance(widget, QComboBox):
                    index = widget.findText(str(value))
                    if index >= 0:
                        widget.setCurrentIndex(index)
                elif isinstance(widget, QDateEdit):
                    if isinstance(value, str):
                        widget.setDate(QDate.fromString(value, "yyyy-MM-dd"))
                elif isinstance(widget, QTextEdit):
                    widget.setPlainText(str(value) if value else "")
                elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                    widget.setValue(value)


def validate_required_fields(fields_dict):
    """
    Validate that required fields are filled

    Args:
        fields_dict: Dictionary of {field_name: value}

    Returns:
        tuple: (is_valid, error_message)
    """
    for field_name, value in fields_dict.items():
        if not value or (isinstance(value, str) and not value.strip()):
            return False, f"Field '{field_name}' is required"

    return True, ""


def format_date_for_display(date_str):
    """
    Format date string for display

    Args:
        date_str: Date string in format YYYY-MM-DD

    Returns:
        str: Formatted date string
    """
    if not date_str:
        return ""

    try:
        from datetime import datetime
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d %b %Y")
    except:
        return date_str


def truncate_text(text, max_length=50):
    """
    Truncate text to maximum length

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        str: Truncated text with ellipsis if needed
    """
    if not text:
        return ""

    text = str(text)
    if len(text) <= max_length:
        return text

    return text[:max_length-3] + "..."
