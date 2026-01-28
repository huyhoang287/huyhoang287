# CLAUDE.MD - Developer Guide for AI Assistants

This document provides essential context about the **HRSG Weld Management System** for AI assistants working on this codebase.

---

## Project Overview

**HRSG Weld Management System** is a desktop application for managing welding operations in Heat Recovery Steam Generator (HRSG) projects. It tracks welds, welders, materials, NDT inspections, and WPS documentation.

### Key Facts
- **Language**: Python 3.8+
- **GUI Framework**: PyQt6 (Fusion Style)
- **Database**: SQLite (file-based, auto-created)
- **Architecture**: Model-View pattern with DAO (Data Access Object) layer
- **Translations**: Multi-language support (English & Vietnamese)
- **Target Users**: Welding engineers, QA/QC inspectors, project managers

---

## Technology Stack

### Core Dependencies
```
PyQt6==6.8.0           # Modern desktop UI framework
openpyxl==3.1.5        # Excel import/export
Pillow==11.1.0         # Image handling
passlib==1.7.4         # Password hashing
```

### Database
- **SQLite** - No server setup required
- Locations: `database/hrsg_welds.db` (primary data), `hrsg_weld.db` (legacy/alternate)
- Auto-initialized on first run with sample data
- Main tables:
  - `tblWelders` - Welder information and certifications
  - `tblWPS` - Welding Procedure Specifications
  - `tblDrawingUnits` - Drawings and serial numbers
  - `tblWelds` - Weld joints and status
  - `tblNDTRequests` - NDT inspection records
  - `tblNDTMethods` - Configurable NDT types (RT, UT, PT, MT, etc.)
  - `tblMaterialLog` - Material tracking
  - `tblUsers` - User accounts with roles (Admin, Editor, Viewer)

---

## Project Structure

```
hrsg_weld_management/
├── run_app.py                    # Application entry point
├── START_APP.bat                 # Windows launcher
├── requirements.txt              # Python dependencies
├── database/
│   └── hrsg_welds.db            # SQLite database
├── docs/                         # Documentation
│   ├── BUG_FIXES.md             # History of fixes
│   ├── UI_UX_GUIDE.md           # Design principles
│   └── EXCEL_BEHAVIOR.md         # Table interaction guides
├── logs/                         # Application logs
└── src/
    ├── database/
    │   ├── connection.py        # DBConnection singleton & Schema init
    │   └── models.py            # Data Access Objects (DAO)
    ├── ui/
    │   ├── main_window_qt.py    # Main application window
    │   ├── login_dialog.py      # Secure authentication
    │   ├── advanced_dashboard.py # Main Dashboard with KPIs
    │   ├── weld_view.py         # Weld management (Excel-like)
    │   ├── welder_view.py       # Welder management
    │   ├── ndt_request_view.py  # NDT management
    │   ├── repair_view.py       # Dedicated repair tracking
    │   ├── report_view.py       # Report generation interface
    │   ├── wps_view.py          # WPS library
    │   ├── drawing_view.py      # Drawings & Units
    │   ├── material_log_view.py # Material tracking
    │   ├── components/
    │   │   ├── minimalist_nav.py # Top navigation bar
    │   │   ├── header.py        # Page headers
    │   │   ├── stat_card.py     # KPI cards
    │   │   └── skeleton.py      # Loading animations
    │   ├── ui_helpers.py        # Shared UI utilities
    │   └── virtual_table_model.py # Performance for large lists
    └── utils/
        ├── modern_theme.py      # Global styling (Slate/Blue theme)
        ├── language_manager.py  # I18n support (tr() function)
        ├── report_generator.py  # Excel report engine
        ├── export.py            # Data export utilities
        ├── session.py           # User session state
        ├── config.py            # App settings
        └── logger.py            # Logging setup
```

---

## Architecture & Patterns

### 1. Database Layer (`src/database/`)
- **DAO Pattern**: Every table has a corresponding DAO class (e.g., `WeldDAO`).
- **Standardized CRUD**: All DAOs implement `get_all`, `get_by_id`, `create`, `update`, `delete`.
- **Search & Filters**: DAOs handle complex filtering logic to keep UI code clean.

### 2. UI Layer (`src/ui/`)
- **Stacked Widgets**: Navigation swaps views within a `QStackedWidget`.
- **Excel-like Tables**: Uses `EditableTableWidgetItem` for inline editing and keyboard navigation (Tab/Enter).
- **Optimistic Updates**: UI updates immediately while background workers handle DB persistence.
- **Font Standards**:
  - Tab Titles: 16px Bold (#1E293B)
  - Stats/KPIs: 22px Bold (#0F172A)
  - General: 9pt Segoe UI

### 3. Internationalization
- All UI strings must use `tr("key.path")` from `src.utils.language_manager`.
- Translation files are stored in `src/resources/i18n/` (json format).

---

## Key Features

### 1. Advanced Reporting
- Generates professional Excel reports using templates.
- Supports Welder Performance, NDT Summaries, and Project Progress.
- Implementation: `src/utils/report_generator.py`.

### 2. Repair Workflow
- Dedicated tracking for failed welds.
- Links original welds to repair requests and re-inspections.
- View: `src/ui/repair_view.py`.

### 3. Batch Editing
- Allows updating multiple records simultaneously.
- Refined UI with 3-column layout for better organization.
- Includes smart field restrictions (e.g., Cannot batch edit unique IDs).

### 4. Smart Deletion
- **Safe Delete Pattern**: Checks for dependencies before deleting (e.g., cannot delete a Welder if they have assigned welds).
- Provides clear feedback on why a deletion was blocked.

---

## Development Guidelines

### DO:
- ✅ **Use `tr()` for all text**: Ensure multi-language support is maintained.
- ✅ **DAO for DB**: Never write `cursor.execute()` inside a UI file.
- ✅ **Background Workers**: Use `QThread` for heavy operations (Loading data, Exporting).
- ✅ **Input Validation**: Check data type and range before Calling DAO update.
- ✅ **Filter Preservation**: Maintain user's search/filter state after editing records.
- ✅ **Modern Theme**: Use `ModernTheme` constants for colors and styling.

### DON'T:
- ❌ **Hardcode Paths**: Use `os.path` and relative structure.
- ❌ **Block UI**: Avoid `time.sleep()` or long loops on the main thread.
- ❌ **Raw DB Access**: Avoid direct sqlite3 calls in views.
- ❌ **Inconsistent Modals**: Use `ui_helpers.py` for standard dialogs.

---

## Common Tasks

### Adding a New Navigation Item
1. Define the module name in `main_window_qt.py`.
2. Add the item to `MinimalistTopNav.nav_items`.
3. Update `_load_module()` in `main_window_qt.py` to lazy-load the view.
4. Add a keyboard shortcut in `_setup_keyboard_shortcuts()`.

### Updating Translations
1. Locate the key in `src/utils/language_manager.py` (if hardcoded) or dedicated JSON files.
2. Add/Update both English and Vietnamese values.
3. Use placeholders like `{count}` for dynamic values.

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Alt+1` | Dashboard |
| `Alt+2` | Welds |
| `Alt+3` | NDT |
| `Alt+4` | WPS Library |
| `Alt+5` | Welders |
| `Alt+6` | Drawings |
| `Alt+7` | Material Log |
| `Alt+8` | Consumables |
| `Alt+9` | User Management / Settings |
| `Alt+0` | Reports |
| `Ctrl+F` | Focus Search |
| `Ctrl+N` | New Entry (where available) |
| `Del`    | Delete Selected |

---

## Debugging

- **Logs**: Check `logs/app.log` or console output for traceback.
- **Database**: Use DB Browser for SQLite on `database/hrsg_welds.db`.
- **Session**: `src/utils/session.py` contains the current user role and username.

---

**Version**: 2.1
**Last Updated**: 2026-01-28
**Python**: 3.8+
**Framework**: PyQt6

---

## Quick Reference for AI Assistants

When working on this codebase:

1. **Always read existing code first** before proposing changes
2. **Use DAO classes** for all database operations
3. **Follow existing UI patterns** in components/
4. **Use background workers** for slow operations
5. **Test with sample data** before proposing changes
6. **Check docs/** for implementation details
7. **Maintain consistency** with existing code style
8. **Validate user input** before database operations
9. **Handle errors gracefully** with user feedback
10. **Keep it simple** - don't over-engineer solutions
