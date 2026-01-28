"""
Weld View
Manage weld joints with Excel-like table interface
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QLineEdit, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
import logging

from src.database.models import WeldDAO, WelderDAO, WPSDAO, DrawingUnitDAO
from src.utils.modern_theme import ModernTheme
from src.utils.language_manager import tr
from src.ui.ui_helpers import show_confirm, show_error, show_success, get_status_color

logger = logging.getLogger(__name__)


class WeldView(QWidget):
    """Weld management view"""

    def __init__(self):
        super().__init__()
        self.weld_dao = WeldDAO()
        self.welder_dao = WelderDAO()
        self.wps_dao = WPSDAO()
        self.drawing_dao = DrawingUnitDAO()

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

        title_label = QLabel(tr('nav.welds'))
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(tr('common.search') + " welds...")
        self.search_input.setMaximumWidth(300)
        self.search_input.textChanged.connect(self._filter_welds)
        header_layout.addWidget(self.search_input)

        layout.addLayout(header_layout)

        # Toolbar
        toolbar_layout = QHBoxLayout()

        # Status filter
        status_label = QLabel("Filter by Status:")
        toolbar_layout.addWidget(status_label)

        self.status_filter = QComboBox()
        self.status_filter.addItems(['All', 'Pending', 'Accepted', 'Rejected', 'Repair'])
        self.status_filter.currentTextChanged.connect(self._filter_welds)
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

        # Welds table
        self.welds_table = QTableWidget()
        self.welds_table.setColumnCount(10)
        self.welds_table.setHorizontalHeaderLabels([
            "Weld Number", "Drawing", "WPS", "Welder", "Type",
            "Material", "Thickness", "Date", "Status", "Visual"
        ])
        self.welds_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.welds_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.welds_table.setAlternatingRowColors(True)
        self.welds_table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.welds_table)

        # Status bar
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #64748B; font-size: 11px;")
        layout.addWidget(self.status_label)

    def _load_data(self):
        """Load welds data"""
        try:
            self.all_welds = self.weld_dao.get_all()
            self._display_welds(self.all_welds)
            self.status_label.setText(f"Total welds: {len(self.all_welds)}")
            logger.info(f"Loaded {len(self.all_welds)} welds")

        except Exception as e:
            logger.error(f"Error loading welds: {e}")
            show_error(self, f"Error loading welds: {str(e)}")

    def _display_welds(self, welds):
        """Display welds in table"""
        self.welds_table.setRowCount(len(welds))

        for row, weld in enumerate(welds):
            self.welds_table.setItem(row, 0, QTableWidgetItem(weld['WeldNumber']))
            self.welds_table.setItem(row, 1, QTableWidgetItem(weld['DrawingNumber'] or 'N/A'))
            self.welds_table.setItem(row, 2, QTableWidgetItem(weld['WPSNumber'] or 'N/A'))
            self.welds_table.setItem(row, 3, QTableWidgetItem(weld['WelderName'] or 'N/A'))
            self.welds_table.setItem(row, 4, QTableWidgetItem(weld['WeldType'] or 'N/A'))
            self.welds_table.setItem(row, 5, QTableWidgetItem(weld['MaterialSpec'] or 'N/A'))
            self.welds_table.setItem(row, 6, QTableWidgetItem(str(weld['Thickness']) if weld['Thickness'] else 'N/A'))
            self.welds_table.setItem(row, 7, QTableWidgetItem(weld['WeldDate'] or 'N/A'))

            # Status with color
            status_item = QTableWidgetItem(weld['Status'])
            status_color = get_status_color(weld['Status'])
            status_item.setBackground(QColor(status_color))
            self.welds_table.setItem(row, 8, status_item)

            self.welds_table.setItem(row, 9, QTableWidgetItem(weld['VisualInspection'] or 'N/A'))

        # Resize columns
        self.welds_table.resizeColumnsToContents()

    def _filter_welds(self):
        """Filter welds based on search and status filter"""
        search_text = self.search_input.text().lower()
        status_filter = self.status_filter.currentText()

        filtered_welds = []

        for weld in self.all_welds:
            # Status filter
            if status_filter != 'All' and weld['Status'] != status_filter:
                continue

            # Search filter
            if search_text:
                searchable_text = ' '.join([
                    str(weld.get('WeldNumber', '')),
                    str(weld.get('WelderName', '')),
                    str(weld.get('WPSNumber', '')),
                    str(weld.get('MaterialSpec', '')),
                ]).lower()

                if search_text not in searchable_text:
                    continue

            filtered_welds.append(weld)

        self._display_welds(filtered_welds)
        self.status_label.setText(f"Showing {len(filtered_welds)} of {len(self.all_welds)} welds")

    def _export_data(self):
        """Export welds to Excel"""
        try:
            from src.utils.export import export_to_excel
            from PyQt6.QtWidgets import QFileDialog

            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Export Welds",
                "welds_export.xlsx",
                "Excel Files (*.xlsx)"
            )

            if filename:
                headers = [
                    "WeldNumber", "DrawingNumber", "WPSNumber", "WelderName",
                    "WeldType", "MaterialSpec", "Thickness", "WeldDate",
                    "Status", "VisualInspection"
                ]

                # Get currently displayed welds
                current_text = self.status_label.text()
                if "Showing" in current_text:
                    # Use filtered data
                    self._filter_welds()
                    data = []
                    for row in range(self.welds_table.rowCount()):
                        row_data = []
                        for col in range(10):
                            item = self.welds_table.item(row, col)
                            row_data.append(item.text() if item else '')
                        data.append(row_data)
                else:
                    # Use all data
                    data = [[str(weld.get(h, '')) for h in headers] for weld in self.all_welds]

                if export_to_excel(data, headers, filename, "Welds"):
                    show_success(self, f"Exported {len(data)} welds to {filename}")
                else:
                    show_error(self, "Export failed")

        except Exception as e:
            logger.error(f"Export error: {e}")
            show_error(self, f"Export error: {str(e)}")

    def refresh(self):
        """Refresh the view"""
        self._load_data()
