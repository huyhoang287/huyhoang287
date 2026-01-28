# HRSG Weld Management System

> **Desktop application for managing welding operations in Heat Recovery Steam Generator (HRSG) projects**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.8.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production-success.svg)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Development](#-development)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The **HRSG Weld Management System** is a comprehensive desktop application designed to streamline and manage welding operations in Heat Recovery Steam Generator (HRSG) manufacturing projects. It provides a centralized platform for tracking welds, welders, welding procedure specifications (WPS), non-destructive testing (NDT) requests, materials, and generating professional reports.

### Target Users

- **Welding Engineers** - Plan and oversee welding operations
- **QA/QC Inspectors** - Track inspections and quality metrics
- **Project Managers** - Monitor project progress and generate reports
- **Welding Supervisors** - Manage welder certifications and assignments

---

## ✨ Features

### Core Functionality

- **Dashboard with KPIs** - Real-time statistics and metrics
- **Weld Management** - Track all weld joints with Excel-like interface
- **Welder Management** - Manage welder certifications and assignments
- **WPS Library** - Digital repository for Welding Procedure Specifications
- **NDT Request Tracking** - Manage non-destructive testing inspections
- **Material Log** - Track material inventory and usage
- **Drawing Management** - Link welds to engineering drawings
- **User Management** - Role-based access control (Admin/Editor/Viewer)

### Advanced Features

- **Multi-language Support** - English and Vietnamese
- **Professional Reports** - Generate Excel reports with formatting
- **Data Export** - Export to Excel/CSV formats
- **Search & Filter** - Advanced filtering across all views
- **Secure Authentication** - Password hashing with bcrypt
- **Audit Trail** - Track user activities and changes

### Technical Highlights

- **Modern UI** - Slate/Blue theme with PyQt6
- **SQLite Database** - No server setup required
- **DAO Pattern** - Clean separation of concerns
- **Responsive Design** - Optimized for 1200x800+ displays
- **Excel-like Editing** - Familiar table interface with Tab/Enter navigation
- **Background Workers** - Non-blocking UI for heavy operations

---

## 🛠 Technology Stack

### Core Technologies

- **Python** 3.8+ - Programming language
- **PyQt6** 6.8.0 - Desktop GUI framework
- **SQLite** - Embedded database
- **openpyxl** 3.1.5 - Excel file generation
- **Pillow** 11.1.0 - Image handling
- **passlib** 1.7.4 - Password security

### Architecture

- **Pattern**: Model-View with DAO (Data Access Object)
- **Database**: 8 tables with foreign key constraints
- **UI**: Stacked widget navigation with lazy loading
- **Security**: Bcrypt password hashing, RBAC

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Windows 10+ / macOS 10.14+ / Linux

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/hrsg-weld-management.git
cd hrsg-weld-management
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python run_app.py
```

### Windows Quick Start

Double-click `START_APP.bat` to automatically:
- Create virtual environment (if not exists)
- Install/update dependencies
- Launch the application

---

## 🚀 Usage

### First Time Login

**Default Credentials:**
- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Security Note**: Change the default password immediately after first login.

### Navigation

Use keyboard shortcuts for quick navigation:

| Shortcut | Action |
|----------|--------|
| `Alt+1` | Dashboard |
| `Alt+2` | Welds |
| `Alt+3` | Welders |
| `Alt+4` | WPS Library |
| `Ctrl+F` | Focus Search |
| `Ctrl+E` | Export Data |
| `F5` | Refresh View |
| `Ctrl+Q` | Exit Application |

### Main Workflows

#### 1. Adding a New Weld

1. Navigate to **Welds** (Alt+2)
2. Click **Add** button
3. Fill in weld details (Number, Drawing, WPS, Welder, etc.)
4. Save

#### 2. Managing Welders

1. Navigate to **Welders** (Alt+3)
2. View welder list with certification status
3. Color-coded expiry dates:
   - 🟢 Green: Valid (>30 days)
   - 🟡 Yellow: Expiring soon (<30 days)
   - 🔴 Red: Expired

#### 3. Generating Reports

1. Navigate to **Reports**
2. Select report type:
   - Welder Performance
   - NDT Summary
   - Project Progress
   - Material Usage
3. Choose date range and parameters
4. Click **Generate** to create Excel report

---

## 📁 Project Structure

```
hrsg_weld_management/
├── run_app.py                    # Application entry point
├── START_APP.bat                 # Windows launcher
├── requirements.txt              # Python dependencies
├── CLAUDE.MD                     # Developer guide (for AI assistants)
├── README.md                     # This file
├── database/
│   └── hrsg_welds.db            # SQLite database (auto-created)
├── logs/                         # Application logs
│   └── app_YYYYMMDD.log
└── src/
    ├── database/
    │   ├── connection.py        # Database connection & schema
    │   └── models.py            # DAO classes (8 DAOs)
    ├── ui/
    │   ├── login_dialog.py      # Authentication dialog
    │   ├── main_window_qt.py    # Main application window
    │   ├── advanced_dashboard.py # Dashboard with KPIs
    │   ├── weld_view.py         # Weld management
    │   ├── welder_view.py       # Welder management
    │   └── ui_helpers.py        # Shared UI utilities
    └── utils/
        ├── modern_theme.py      # UI styling
        ├── language_manager.py  # Internationalization
        ├── session.py           # User session management
        ├── logger.py            # Logging configuration
        ├── config.py            # App settings
        ├── export.py            # Data export utilities
        └── report_generator.py  # Excel report generation
```

---

## 📸 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)
*Real-time KPIs and recent activity*

### Weld Management
![Weld View](docs/screenshots/weld_view.png)
*Excel-like table with color-coded status*

### Welder Management
![Welder View](docs/screenshots/welder_view.png)
*Certification tracking with expiry warnings*

---

## 🔧 Development

### For Developers

See [CLAUDE.MD](CLAUDE.MD) for comprehensive developer guide.

### Database Schema

8 main tables:
- `tblUsers` - User accounts
- `tblWelders` - Welder information
- `tblWPS` - Welding Procedure Specifications
- `tblDrawingUnits` - Engineering drawings
- `tblWelds` - Weld joints
- `tblNDTMethods` - NDT inspection methods
- `tblNDTRequests` - NDT inspection records
- `tblMaterialLog` - Material tracking

### Adding a New View

1. Create view file in `src/ui/`
2. Import in `main_window_qt.py`
3. Add navigation button
4. Update keyboard shortcuts

### Running Tests

```bash
# Run with sample data
python run_app.py

# Check logs
tail -f logs/app_YYYYMMDD.log
```

---

## 📚 Documentation

- **[CLAUDE.MD](CLAUDE.MD)** - Developer guide for AI assistants
- **[API Documentation](docs/api/)** - DAO method reference
- **[User Guide](docs/user-guide.md)** - Detailed user manual
- **[Changelog](CHANGELOG.md)** - Version history

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guide
- Use type hints where applicable
- Add docstrings to all functions/classes
- Write meaningful commit messages
- Test thoroughly before submitting PR

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Development Team** - Initial work and ongoing maintenance

---

## 🙏 Acknowledgments

- PyQt6 team for the excellent GUI framework
- SQLite for the reliable embedded database
- openpyxl developers for Excel file handling
- All contributors and testers

---

## 📞 Support

For questions, issues, or feature requests:

- **Email**: support@example.com
- **Issue Tracker**: [GitHub Issues](https://github.com/yourusername/hrsg-weld-management/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/hrsg-weld-management/wiki)

---

## 🔄 Version History

- **v2.1** (2026-01-28) - Initial Python/PyQt6 release
  - Complete rewrite from Android to Desktop
  - 8 DAO classes with full CRUD
  - Modern Slate/Blue theme
  - Bilingual support (EN/VI)
  - Professional Excel reports

---

**Made with ❤️ for HRSG welding professionals**
