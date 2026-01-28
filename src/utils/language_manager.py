"""
Language Manager
Provides internationalization (i18n) support for the application
Currently supports English and Vietnamese
"""

import logging

logger = logging.getLogger(__name__)

# Translation dictionaries
TRANSLATIONS = {
    'en': {
        # Common
        'app.title': 'HRSG Weld Management System',
        'common.add': 'Add',
        'common.edit': 'Edit',
        'common.delete': 'Delete',
        'common.save': 'Save',
        'common.cancel': 'Cancel',
        'common.search': 'Search',
        'common.filter': 'Filter',
        'common.export': 'Export',
        'common.import': 'Import',
        'common.refresh': 'Refresh',
        'common.yes': 'Yes',
        'common.no': 'No',
        'common.ok': 'OK',
        'common.close': 'Close',

        # Navigation
        'nav.dashboard': 'Dashboard',
        'nav.welds': 'Welds',
        'nav.welders': 'Welders',
        'nav.wps': 'WPS Library',
        'nav.ndt': 'NDT Requests',
        'nav.drawings': 'Drawings',
        'nav.materials': 'Material Log',
        'nav.repairs': 'Repairs',
        'nav.reports': 'Reports',
        'nav.users': 'User Management',

        # Login
        'login.title': 'Login',
        'login.username': 'Username',
        'login.password': 'Password',
        'login.remember': 'Remember Me',
        'login.button': 'Login',
        'login.error': 'Invalid username or password',

        # Dashboard
        'dashboard.total_welds': 'Total Welds',
        'dashboard.pending': 'Pending Inspections',
        'dashboard.rejection_rate': 'Rejection Rate',
        'dashboard.active_welders': 'Active Welders',

        # Status
        'status.pending': 'Pending',
        'status.accepted': 'Accepted',
        'status.rejected': 'Rejected',
        'status.repair': 'Repair',
        'status.active': 'Active',
        'status.inactive': 'Inactive',

        # Messages
        'msg.delete_confirm': 'Are you sure you want to delete this item?',
        'msg.save_success': 'Saved successfully',
        'msg.save_error': 'Failed to save',
        'msg.delete_success': 'Deleted successfully',
        'msg.delete_error': 'Failed to delete',
    },
    'vi': {
        # Common
        'app.title': 'Hệ Thống Quản Lý Hàn HRSG',
        'common.add': 'Thêm',
        'common.edit': 'Sửa',
        'common.delete': 'Xóa',
        'common.save': 'Lưu',
        'common.cancel': 'Hủy',
        'common.search': 'Tìm kiếm',
        'common.filter': 'Lọc',
        'common.export': 'Xuất',
        'common.import': 'Nhập',
        'common.refresh': 'Làm mới',
        'common.yes': 'Có',
        'common.no': 'Không',
        'common.ok': 'Đồng ý',
        'common.close': 'Đóng',

        # Navigation
        'nav.dashboard': 'Bảng Điều Khiển',
        'nav.welds': 'Mối Hàn',
        'nav.welders': 'Thợ Hàn',
        'nav.wps': 'Thư Viện WPS',
        'nav.ndt': 'Yêu Cầu NDT',
        'nav.drawings': 'Bản Vẽ',
        'nav.materials': 'Nhật Ký Vật Tư',
        'nav.repairs': 'Sửa Chữa',
        'nav.reports': 'Báo Cáo',
        'nav.users': 'Quản Lý Người Dùng',

        # Login
        'login.title': 'Đăng Nhập',
        'login.username': 'Tên đăng nhập',
        'login.password': 'Mật khẩu',
        'login.remember': 'Ghi nhớ đăng nhập',
        'login.button': 'Đăng Nhập',
        'login.error': 'Tên đăng nhập hoặc mật khẩu không đúng',

        # Dashboard
        'dashboard.total_welds': 'Tổng Mối Hàn',
        'dashboard.pending': 'Chờ Kiểm Tra',
        'dashboard.rejection_rate': 'Tỷ Lệ Loại Bỏ',
        'dashboard.active_welders': 'Thợ Hàn Đang Làm',

        # Status
        'status.pending': 'Đang chờ',
        'status.accepted': 'Đã chấp nhận',
        'status.rejected': 'Đã loại bỏ',
        'status.repair': 'Sửa chữa',
        'status.active': 'Hoạt động',
        'status.inactive': 'Không hoạt động',

        # Messages
        'msg.delete_confirm': 'Bạn có chắc chắn muốn xóa mục này không?',
        'msg.save_success': 'Lưu thành công',
        'msg.save_error': 'Lưu thất bại',
        'msg.delete_success': 'Xóa thành công',
        'msg.delete_error': 'Xóa thất bại',
    }
}

# Current language
_current_language = 'en'


def set_language(lang_code):
    """
    Set the current language

    Args:
        lang_code: Language code ('en' or 'vi')
    """
    global _current_language
    if lang_code in TRANSLATIONS:
        _current_language = lang_code
        logger.info(f"Language set to: {lang_code}")
    else:
        logger.warning(f"Unknown language code: {lang_code}. Using English.")
        _current_language = 'en'


def get_current_language():
    """
    Get the current language code

    Returns:
        str: Current language code
    """
    return _current_language


def tr(key, **kwargs):
    """
    Translate a key to the current language

    Args:
        key: Translation key (e.g., 'common.add')
        **kwargs: Optional format arguments

    Returns:
        str: Translated string
    """
    translation = TRANSLATIONS.get(_current_language, {}).get(key, key)

    # Format with any provided arguments
    if kwargs:
        try:
            translation = translation.format(**kwargs)
        except KeyError as e:
            logger.warning(f"Missing format argument for key '{key}': {e}")

    return translation
