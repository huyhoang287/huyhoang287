"""
Session Management
Manages user session state throughout the application
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Session:
    """Singleton session manager"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize session variables"""
        self._user_id = None
        self._username = None
        self._full_name = None
        self._role = None
        self._login_time = None
        logger.info("Session initialized")

    def login(self, user_data):
        """
        Log in a user and store session data

        Args:
            user_data: Dictionary or Row object containing user information
        """
        self._user_id = user_data['UserID']
        self._username = user_data['Username']
        self._full_name = user_data['FullName']
        self._role = user_data['Role']
        self._login_time = datetime.now()
        logger.info(f"User logged in: {self._username} ({self._role})")

    def logout(self):
        """Log out the current user and clear session data"""
        logger.info(f"User logged out: {self._username}")
        self._user_id = None
        self._username = None
        self._full_name = None
        self._role = None
        self._login_time = None

    def is_authenticated(self):
        """
        Check if a user is currently logged in

        Returns:
            bool: True if user is logged in, False otherwise
        """
        return self._user_id is not None

    def has_permission(self, required_role):
        """
        Check if current user has required permission level

        Args:
            required_role: Required role ('Admin', 'Editor', or 'Viewer')

        Returns:
            bool: True if user has permission, False otherwise

        Permission hierarchy: Admin > Editor > Viewer
        """
        if not self.is_authenticated():
            return False

        role_hierarchy = {'Admin': 3, 'Editor': 2, 'Viewer': 1}
        user_level = role_hierarchy.get(self._role, 0)
        required_level = role_hierarchy.get(required_role, 0)

        return user_level >= required_level

    def is_admin(self):
        """Check if current user is an admin"""
        return self._role == 'Admin'

    def is_editor(self):
        """Check if current user is an editor or admin"""
        return self._role in ['Admin', 'Editor']

    def is_viewer(self):
        """Check if current user is a viewer (all roles can view)"""
        return self._role in ['Admin', 'Editor', 'Viewer']

    @property
    def user_id(self):
        """Get current user ID"""
        return self._user_id

    @property
    def username(self):
        """Get current username"""
        return self._username

    @property
    def full_name(self):
        """Get current user's full name"""
        return self._full_name

    @property
    def role(self):
        """Get current user's role"""
        return self._role

    @property
    def login_time(self):
        """Get login timestamp"""
        return self._login_time

    def get_session_info(self):
        """
        Get complete session information

        Returns:
            dict: Session information dictionary
        """
        return {
            'user_id': self._user_id,
            'username': self._username,
            'full_name': self._full_name,
            'role': self._role,
            'login_time': self._login_time,
            'is_authenticated': self.is_authenticated()
        }
