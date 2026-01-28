"""
Login Dialog
Provides secure user authentication
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import logging

from src.database.models import UserDAO
from src.utils.session import Session
from src.utils.modern_theme import ModernTheme
from src.utils.language_manager import tr

logger = logging.getLogger(__name__)


class LoginDialog(QDialog):
    """Login dialog for user authentication"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_dao = UserDAO()
        self.session = Session()
        self._setup_ui()
        ModernTheme.apply_theme(self)

    def _setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle(tr('login.title'))
        self.setFixedSize(400, 300)
        self.setModal(True)

        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title_label = QLabel(tr('app.title'))
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel(tr('login.title'))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #64748B;")
        layout.addWidget(subtitle_label)

        layout.addSpacing(20)

        # Username field
        username_layout = QVBoxLayout()
        username_label = QLabel(tr('login.username'))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(tr('login.username'))
        self.username_input.setText("admin")  # Default for testing
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        # Password field
        password_layout = QVBoxLayout()
        password_label = QLabel(tr('login.password'))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText(tr('login.password'))
        self.password_input.setText("admin123")  # Default for testing
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # Remember me checkbox
        self.remember_checkbox = QCheckBox(tr('login.remember'))
        layout.addWidget(self.remember_checkbox)

        layout.addSpacing(10)

        # Login button
        self.login_button = QPushButton(tr('login.button'))
        self.login_button.setMinimumHeight(40)
        self.login_button.clicked.connect(self._handle_login)
        layout.addWidget(self.login_button)

        # Error label
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: #EF4444;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide()
        layout.addWidget(self.error_label)

        layout.addStretch()

        self.setLayout(layout)

        # Connect Enter key to login
        self.username_input.returnPressed.connect(self._handle_login)
        self.password_input.returnPressed.connect(self._handle_login)

    def _handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()

        # Validate inputs
        if not username:
            self._show_error("Please enter username")
            self.username_input.setFocus()
            return

        if not password:
            self._show_error("Please enter password")
            self.password_input.setFocus()
            return

        # Authenticate user
        try:
            user = self.user_dao.authenticate(username, password)

            if user:
                # Login successful
                self.session.login(user)
                logger.info(f"Login successful: {username}")
                self.accept()
            else:
                # Login failed
                self._show_error(tr('login.error'))
                self.password_input.clear()
                self.password_input.setFocus()
                logger.warning(f"Login failed for user: {username}")

        except Exception as e:
            logger.error(f"Login error: {e}")
            self._show_error(f"Login error: {str(e)}")

    def _show_error(self, message):
        """Show error message"""
        self.error_label.setText(message)
        self.error_label.show()

    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)
