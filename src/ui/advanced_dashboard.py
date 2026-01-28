"""
Advanced Dashboard
Main dashboard with KPIs and statistics
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QGridLayout, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import logging

from src.database.models import WeldDAO, WelderDAO, NDTRequestDAO
from src.utils.modern_theme import ModernTheme
from src.utils.language_manager import tr

logger = logging.getLogger(__name__)


class StatCard(QFrame):
    """Statistics card widget"""

    def __init__(self, title, value, icon="📊", color="#3B82F6"):
        super().__init__()
        self._setup_ui(title, value, icon, color)

    def _setup_ui(self, title, value, icon, color):
        """Setup the UI"""
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
                padding: 20px;
            }}
            QFrame:hover {{
                border: 2px solid {color};
            }}
        """)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Icon and title row
        header_layout = QHBoxLayout()

        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 32px; color: {color};")
        header_layout.addWidget(icon_label)

        header_layout.addStretch()

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #64748B; font-size: 12px;")
        header_layout.addWidget(title_label)

        layout.addLayout(header_layout)

        # Value
        value_label = QLabel(str(value))
        value_font = QFont()
        value_font.setPointSize(28)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)

        layout.addStretch()


class AdvancedDashboard(QWidget):
    """Advanced dashboard with statistics and recent activity"""

    def __init__(self):
        super().__init__()
        self.weld_dao = WeldDAO()
        self.welder_dao = WelderDAO()
        self.ndt_dao = NDTRequestDAO()

        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Header
        header_label = QLabel(tr('nav.dashboard'))
        header_font = QFont()
        header_font.setPointSize(20)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)

        # Statistics cards grid
        stats_grid = QGridLayout()
        stats_grid.setSpacing(20)

        self.total_welds_card = StatCard(tr('dashboard.total_welds'), "0", "🔧", "#3B82F6")
        self.pending_card = StatCard(tr('dashboard.pending'), "0", "⏳", "#F59E0B")
        self.rejection_card = StatCard(tr('dashboard.rejection_rate'), "0%", "📉", "#EF4444")
        self.welders_card = StatCard(tr('dashboard.active_welders'), "0", "👷", "#10B981")

        stats_grid.addWidget(self.total_welds_card, 0, 0)
        stats_grid.addWidget(self.pending_card, 0, 1)
        stats_grid.addWidget(self.rejection_card, 0, 2)
        stats_grid.addWidget(self.welders_card, 0, 3)

        layout.addLayout(stats_grid)

        # Recent activity section
        recent_label = QLabel("Recent Welds")
        recent_font = QFont()
        recent_font.setPointSize(14)
        recent_font.setBold(True)
        recent_label.setFont(recent_font)
        layout.addWidget(recent_label)

        # Recent welds table
        self.recent_table = QTableWidget()
        self.recent_table.setColumnCount(6)
        self.recent_table.setHorizontalHeaderLabels([
            "Weld Number", "Welder", "WPS", "Date", "Status", "Visual"
        ])
        self.recent_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.recent_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.recent_table.setAlternatingRowColors(True)
        self.recent_table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.recent_table)

    def _load_data(self):
        """Load dashboard data"""
        try:
            # Get statistics
            stats = self.weld_dao.get_statistics()

            # Update stat cards
            self.total_welds_card.findChild(QLabel, "").setText(str(stats['total_welds']))
            self.pending_card.findChild(QLabel, "").setText(str(stats['pending_welds']))
            self.rejection_card.findChild(QLabel, "").setText(f"{stats['rejection_rate']}%")

            # Get active welders count
            active_welders = len(self.welder_dao.get_active_welders())
            self.welders_card.findChild(QLabel, "").setText(str(active_welders))

            # Load recent welds
            self._load_recent_welds()

            logger.info("Dashboard data loaded successfully")

        except Exception as e:
            logger.error(f"Error loading dashboard data: {e}")

    def _load_recent_welds(self):
        """Load recent welds into table"""
        try:
            welds = self.weld_dao.get_all()

            # Sort by date (most recent first) and take top 10
            welds = sorted(welds, key=lambda x: x['WeldDate'] or '', reverse=True)[:10]

            self.recent_table.setRowCount(len(welds))

            for row, weld in enumerate(welds):
                self.recent_table.setItem(row, 0, QTableWidgetItem(weld['WeldNumber']))
                self.recent_table.setItem(row, 1, QTableWidgetItem(weld['WelderName'] or 'N/A'))
                self.recent_table.setItem(row, 2, QTableWidgetItem(weld['WPSNumber'] or 'N/A'))
                self.recent_table.setItem(row, 3, QTableWidgetItem(weld['WeldDate'] or 'N/A'))

                # Status with color
                status_item = QTableWidgetItem(weld['Status'])
                status_color = self._get_status_color(weld['Status'])
                from PyQt6.QtGui import QColor
                status_item.setBackground(QColor(status_color))
                self.recent_table.setItem(row, 4, status_item)

                self.recent_table.setItem(row, 5, QTableWidgetItem(weld['VisualInspection'] or 'N/A'))

            # Resize columns to content
            self.recent_table.resizeColumnsToContents()

        except Exception as e:
            logger.error(f"Error loading recent welds: {e}")

    def _get_status_color(self, status):
        """Get color for status"""
        colors = {
            'Pending': '#FEF3C7',
            'Accepted': '#D1FAE5',
            'Rejected': '#FEE2E2',
            'Repair': '#FFE4E6'
        }
        return colors.get(status, '#FFFFFF')

    def refresh(self):
        """Refresh dashboard data"""
        self._load_data()
