"""
Main Window
Main application window with navigation and view management
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QPushButton, QLabel, QStatusBar, QMenuBar, QMenu
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QKeySequence
import logging
from datetime import datetime

from src.utils.session import Session
from src.utils.modern_theme import ModernTheme
from src.utils.language_manager import tr
from src.ui.ui_helpers import show_confirm

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.session = Session()
        self.current_view = None

        self._setup_ui()
        self._setup_menu_bar()
        self._setup_status_bar()
        self._setup_keyboard_shortcuts()

        ModernTheme.apply_theme(self)

        # Show dashboard by default
        self._load_view('dashboard')

    def _setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle(tr('app.title'))
        self.setMinimumSize(1200, 800)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        # Top navigation bar
        nav_bar = self._create_navigation_bar()
        main_layout.addWidget(nav_bar)

        # Content area with stacked widget
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)

    def _create_navigation_bar(self):
        """Create the top navigation bar"""
        nav_widget = QWidget()
        nav_widget.setStyleSheet("""
            QWidget {
                background-color: #1E293B;
                padding: 10px;
            }
            QPushButton {
                background-color: transparent;
                color: #CBD5E1;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #334155;
                color: #FFFFFF;
            }
            QPushButton:checked {
                background-color: #3B82F6;
                color: #FFFFFF;
            }
        """)

        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(5)
        nav_widget.setLayout(nav_layout)

        # App title
        title_label = QLabel(tr('app.title'))
        title_label.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: bold; padding: 0 20px;")
        nav_layout.addWidget(title_label)

        nav_layout.addStretch()

        # Navigation buttons
        self.nav_buttons = {}

        nav_items = [
            ('dashboard', tr('nav.dashboard'), 'Alt+1'),
            ('welds', tr('nav.welds'), 'Alt+2'),
            ('welders', tr('nav.welders'), 'Alt+3'),
            ('wps', tr('nav.wps'), 'Alt+4'),
        ]

        for view_id, label, shortcut in nav_items:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, v=view_id: self._load_view(v))
            btn.setToolTip(f"{label} ({shortcut})")
            nav_layout.addWidget(btn)
            self.nav_buttons[view_id] = btn

        nav_layout.addStretch()

        # User info
        user_label = QLabel(f"{self.session.full_name} ({self.session.role})")
        user_label.setStyleSheet("color: #CBD5E1; padding: 0 20px;")
        nav_layout.addWidget(user_label)

        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self._handle_logout)
        nav_layout.addWidget(logout_btn)

        return nav_widget

    def _setup_menu_bar(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #0F172A;
                color: #FFFFFF;
                padding: 5px;
            }
            QMenuBar::item:selected {
                background-color: #3B82F6;
            }
            QMenu {
                background-color: #1E293B;
                color: #FFFFFF;
            }
            QMenu::item:selected {
                background-color: #3B82F6;
            }
        """)

        # File menu
        file_menu = menubar.addMenu("&File")

        export_action = QAction("&Export Data", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        refresh_action = QAction("&Refresh", self)
        refresh_action.setShortcut(QKeySequence("F5"))
        refresh_action.triggered.connect(self._refresh_current_view)
        view_menu.addAction(refresh_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Status message
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)

        self.status_bar.addPermanentWidget(QLabel("  |  "))

        # Clock
        self.clock_label = QLabel()
        self.status_bar.addPermanentWidget(self.clock_label)
        self._update_clock()

        # Update clock every second
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self._update_clock)
        self.clock_timer.start(1000)

    def _update_clock(self):
        """Update the clock in status bar"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.setText(current_time)

    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Navigation shortcuts handled by tooltips and button shortcuts
        pass

    def _load_view(self, view_id):
        """
        Load a view into the content area

        Args:
            view_id: View identifier
        """
        logger.info(f"Loading view: {view_id}")

        # Update navigation buttons
        for btn_id, btn in self.nav_buttons.items():
            btn.setChecked(btn_id == view_id)

        # Lazy load views
        try:
            if view_id == 'dashboard':
                from src.ui.advanced_dashboard import AdvancedDashboard
                view = AdvancedDashboard()
            elif view_id == 'welds':
                from src.ui.weld_view import WeldView
                view = WeldView()
            elif view_id == 'welders':
                from src.ui.welder_view import WelderView
                view = WelderView()
            elif view_id == 'wps':
                # Placeholder for WPS view
                view = self._create_placeholder_view("WPS Library View")
            else:
                view = self._create_placeholder_view(f"View: {view_id}")

            # Clear existing views and add new one
            while self.content_stack.count() > 0:
                widget = self.content_stack.widget(0)
                self.content_stack.removeWidget(widget)
                widget.deleteLater()

            self.content_stack.addWidget(view)
            self.content_stack.setCurrentWidget(view)
            self.current_view = view

            self.status_label.setText(f"Loaded: {view_id}")

        except Exception as e:
            logger.error(f"Error loading view {view_id}: {e}")
            self.status_label.setText(f"Error loading view: {str(e)}")

    def _create_placeholder_view(self, title):
        """Create a placeholder view"""
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel(f"🚧 {title}\n\nComing Soon!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: #64748B;")
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    def _refresh_current_view(self):
        """Refresh the current view"""
        if self.current_view and hasattr(self.current_view, 'refresh'):
            self.current_view.refresh()
            self.status_label.setText("View refreshed")
        else:
            logger.info("Current view does not support refresh")

    def _handle_logout(self):
        """Handle logout button click"""
        if show_confirm(self, "Logout", "Are you sure you want to logout?"):
            logger.info("User logged out")
            self.session.logout()
            self.close()

    def _show_about(self):
        """Show about dialog"""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "About HRSG Weld Management System",
            f"""
            <h2>HRSG Weld Management System</h2>
            <p><b>Version:</b> 2.1</p>
            <p><b>Framework:</b> PyQt6</p>
            <p><b>Python:</b> 3.8+</p>
            <br>
            <p>Desktop application for managing welding operations in Heat Recovery Steam Generator (HRSG) projects.</p>
            <br>
            <p><b>Current User:</b> {self.session.full_name}</p>
            <p><b>Role:</b> {self.session.role}</p>
            """
        )

    def closeEvent(self, event):
        """Handle window close event"""
        if show_confirm(self, "Exit", "Are you sure you want to exit?"):
            logger.info("Application closing")
            event.accept()
        else:
            event.ignore()
