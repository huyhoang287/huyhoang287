"""
Welder View
Manage welders and their certifications
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
import logging
from datetime import datetime

from src.database.models import WelderDAO
from src.utils.language_manager import tr
from src.ui.ui_helpers import show_error, show_success

logger = logging.getLogger(__name__)


class WelderView(QWidget):
    """Welder management view"""

    def __init__(self):
        super().__init__()
        self.welder_dao = WelderDAO()

        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel(tr('nav.welders'))
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(tr('common.search') + " welders...")
        self.search_input.setMaximumWidth(300)
        self.search_input.textChanged.connect(self._filter_welders)
        header_layout.addWidget(self.search_input)

        layout.addLayout(header_layout)

        # Toolbar
        toolbar_layout = QHBoxLayout()

        # Status filter
        status_label = QLabel("Filter by Status:")
        toolbar_layout.addWidget(status_label)

        self.status_filter = QComboBox()
        self.status_filter.addItems(['All', 'Active', 'Inactive'])
        self.status_filter.currentTextChanged.connect(self._filter_welders)
        toolbar_layout.addWidget(self.status_filter)

        toolbar_layout.addStretch()

        # Action buttons
        refresh_btn = QPushButton(tr('common.refresh'))
        refresh_btn.clicked.connect(self._load_data)
        toolbar_layout.addWidget(refresh_btn)

        export_btn = QPushButton(tr('common.export'))
        export_btn.clicked.connect(self._export_data)
        toolbar_layout.addWidget(export_btn)

        layout.addLayout(toolbar_layout)

        # Welders table
        self.welders_table = QTableWidget()
        self.welders_table.setColumnCount(7)
        self.welders_table.setHorizontalHeaderLabels([
            "Welder Code", "Full Name", "Cert Number", "Cert Expiry",
            "Processes", "Status", "Notes"
        ])
        self.welders_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.welders_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.welders_table.setAlternatingRowColors(True)
        self.welders_table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.welders_table)

        # Status bar
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #64748B; font-size: 11px;")
        layout.addWidget(self.status_label)

    def _load_data(self):
        """Load welders data"""
        try:
            self.all_welders = self.welder_dao.get_all()
            self._display_welders(self.all_welders)
            self.status_label.setText(f"Total welders: {len(self.all_welders)}")
            logger.info(f"Loaded {len(self.all_welders)} welders")

        except Exception as e:
            logger.error(f"Error loading welders: {e}")
            show_error(self, f"Error loading welders: {str(e)}")

    def _display_welders(self, welders):
        """Display welders in table"""
        self.welders_table.setRowCount(len(welders))

        for row, welder in enumerate(welders):
            self.welders_table.setItem(row, 0, QTableWidgetItem(welder['WelderCode']))
            self.welders_table.setItem(row, 1, QTableWidgetItem(welder['FullName']))
            self.welders_table.setItem(row, 2, QTableWidgetItem(welder['CertNumber'] or 'N/A'))

            # Cert expiry with color coding
            expiry_item = QTableWidgetItem(welder['CertExpiry'] or 'N/A')
            if welder['CertExpiry']:
                expiry_color = self._get_expiry_color(welder['CertExpiry'])
                expiry_item.setBackground(QColor(expiry_color))
            self.welders_table.setItem(row, 3, expiry_item)

            self.welders_table.setItem(row, 4, QTableWidgetItem(welder['Processes'] or 'N/A'))

            # Status with color
            status_item = QTableWidgetItem(welder['Status'])
            if welder['Status'] == 'Active':
                status_item.setBackground(QColor('#D1FAE5'))
            else:
                status_item.setBackground(QColor('#FEE2E2'))
            self.welders_table.setItem(row, 5, status_item)

            self.welders_table.setItem(row, 6, QTableWidgetItem(welder['Notes'] or ''))

        # Resize columns
        self.welders_table.resizeColumnsToContents()

    def _get_expiry_color(self, expiry_date):
        """Get color based on certification expiry date"""
        try:
            expiry = datetime.strptime(expiry_date, "%Y-%m-%d")
            today = datetime.now()
            days_until_expiry = (expiry - today).days

            if days_until_expiry < 0:
                return '#FEE2E2'  # Red - expired
            elif days_until_expiry < 30:
                return '#FEF3C7'  # Yellow - expiring soon
            else:
                return '#D1FAE5'  # Green - valid
        except:
            return '#FFFFFF'

    def _filter_welders(self):
        """Filter welders based on search and status filter"""
        search_text = self.search_input.text().lower()
        status_filter = self.status_filter.currentText()

        filtered_welders = []

        for welder in self.all_welders:
            # Status filter
            if status_filter != 'All' and welder['Status'] != status_filter:
                continue

            # Search filter
            if search_text:
                searchable_text = ' '.join([
                    str(welder.get('WelderCode', '')),
                    str(welder.get('FullName', '')),
                    str(welder.get('CertNumber', '')),
                    str(welder.get('Processes', '')),
                ]).lower()

                if search_text not in searchable_text:
                    continue

            filtered_welders.append(welder)

        self._display_welders(filtered_welders)
        self.status_label.setText(f"Showing {len(filtered_welders)} of {len(self.all_welders)} welders")

    def _export_data(self):
        """Export welders to Excel"""
        try:
            from src.utils.export import export_to_excel
            from PyQt6.QtWidgets import QFileDialog

            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Export Welders",
                "welders_export.xlsx",
                "Excel Files (*.xlsx)"
            )

            if filename:
                headers = [
                    "WelderCode", "FullName", "CertNumber", "CertExpiry",
                    "Processes", "Status", "Notes"
                ]

                data = [[str(welder.get(h, '')) for h in headers] for welder in self.all_welders]

                if export_to_excel(data, headers, filename, "Welders"):
                    show_success(self, f"Exported {len(data)} welders to {filename}")
                else:
                    show_error(self, "Export failed")

        except Exception as e:
            logger.error(f"Export error: {e}")
            show_error(self, f"Export error: {str(e)}")

    def refresh(self):
        """Refresh the view"""
        self._load_data()
