"""
Database Connection Module
Handles SQLite database connection and schema initialization

This module provides a singleton DBConnection class that manages
the database connection and ensures the schema is initialized properly.
"""

import sqlite3
import os
import logging
from datetime import datetime, timedelta
from passlib.hash import bcrypt

logger = logging.getLogger(__name__)

class DBConnection:
    """Singleton database connection manager"""

    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize database connection and schema"""
        # Get database path
        db_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'database')
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, 'hrsg_welds.db')

        # Check if database exists
        is_new_db = not os.path.exists(db_path)

        # Connect to database
        self._connection = sqlite3.connect(db_path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row  # Access columns by name
        self._connection.execute("PRAGMA foreign_keys = ON")  # Enable foreign keys

        logger.info(f"Database connection established: {db_path}")

        # Initialize schema if new database
        if is_new_db:
            logger.info("New database detected. Initializing schema...")
            self._create_schema()
            self._insert_sample_data()
            logger.info("Database schema initialized with sample data")

    def get_connection(self):
        """Get the database connection"""
        return self._connection

    def _create_schema(self):
        """Create all database tables"""
        cursor = self._connection.cursor()

        # Table 1: Users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tblUsers (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT UNIQUE NOT NULL,
                PasswordHash TEXT NOT NULL,
                FullName TEXT NOT NULL,
                Role TEXT NOT NULL CHECK(Role IN ('Admin', 'Editor', 'Viewer')),
                CreatedDate TEXT NOT NULL,
                LastLogin TEXT
            )
        """)

        # Table 2: Welders
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tblWelders (
                WelderID INTEGER PRIMARY KEY AUTOINCREMENT,
                WelderCode TEXT UNIQUE NOT NULL,
                FullName TEXT NOT NULL,
                CertNumber TEXT,
                CertExpiry TEXT,
                Processes TEXT,
                Status TEXT NOT NULL CHECK(Status IN ('Active', 'Inactive')) DEFAULT 'Active',
                Notes TEXT
            )
        """)

        # Table 3: WPS (Welding Procedure Specifications)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tblWPS (
                WPSID INTEGER PRIMARY KEY AUTOINCREMENT,
                WPSNumber TEXT UNIQUE NOT NULL,
                Revision TEXT,
                BaseMetalType TEXT,
                FillerMetal TEXT,
                WeldingProcess TEXT,
                Position TEXT,
                ApprovedDate TEXT,
                PDFPath TEXT,
                Status TEXT NOT NULL CHECK(Status IN ('Active', 'Obsolete')) DEFAULT 'Active'
            )
        """)

        # Table 4: Drawing Units
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tblDrawingUnits (
                DrawingUnitID INTEGER PRIMARY KEY AUTOINCREMENT,
                DrawingNumber TEXT NOT NULL,
                SerialNumber TEXT,
                UnitDescription TEXT,
                Location TEXT,
                Status TEXT
            )
        """)

        # Table 5: Welds
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tblWelds (
                WeldID INTEGER PRIMARY KEY AUTOINCREMENT,
                WeldNumber TEXT UNIQUE NOT NULL,
                DrawingUnitID INTEGER,
                WPSID INTEGER,
                WelderID INTEGER,
                WeldType TEXT,
                MaterialSpec TEXT,
                Thickness REAL,
                WeldDate TEXT,
                Status TEXT NOT NULL CHECK(Status IN ('Pending', 'Accepted', 'Rejected', 'Repair')) DEFAULT 'Pending',
                VisualInspection TEXT CHECK(VisualInspection IN ('Pass', 'Fail', 'N/A')),
                Notes TEXT,
                FOREIGN KEY (DrawingUnitID) REFERENCES tblDrawingUnits(DrawingUnitID),
                FOREIGN KEY (WPSID) REFERENCES tblWPS(WPSID),
                FOREIGN KEY (WelderID) REFERENCES tblWelders(WelderID)
            )
        """)

        # Table 6: NDT Methods
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tblNDTMethods (
                MethodID INTEGER PRIMARY KEY AUTOINCREMENT,
                MethodCode TEXT UNIQUE NOT NULL,
                MethodName TEXT NOT NULL,
                Description TEXT,
                IsActive INTEGER NOT NULL DEFAULT 1
            )
        """)

        # Table 7: NDT Requests
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tblNDTRequests (
                NDTID INTEGER PRIMARY KEY AUTOINCREMENT,
                WeldID INTEGER NOT NULL,
                NDTMethodID INTEGER NOT NULL,
                RequestDate TEXT NOT NULL,
                InspectionDate TEXT,
                Inspector TEXT,
                Result TEXT CHECK(Result IN ('Accept', 'Reject', 'Pending')) DEFAULT 'Pending',
                DefectDescription TEXT,
                ReportNumber TEXT,
                ReportPath TEXT,
                FOREIGN KEY (WeldID) REFERENCES tblWelds(WeldID),
                FOREIGN KEY (NDTMethodID) REFERENCES tblNDTMethods(MethodID)
            )
        """)

        # Table 8: Material Log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tblMaterialLog (
                MaterialID INTEGER PRIMARY KEY AUTOINCREMENT,
                MaterialType TEXT NOT NULL,
                Specification TEXT,
                HeatNumber TEXT,
                Quantity REAL,
                Unit TEXT,
                Supplier TEXT,
                ReceiveDate TEXT,
                UsedInWeldID INTEGER,
                Status TEXT NOT NULL CHECK(Status IN ('Available', 'Used', 'Returned')) DEFAULT 'Available',
                FOREIGN KEY (UsedInWeldID) REFERENCES tblWelds(WeldID)
            )
        """)

        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_welds_status ON tblWelds(Status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_welds_welder ON tblWelds(WelderID)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_welds_wps ON tblWelds(WPSID)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ndt_weld ON tblNDTRequests(WeldID)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_material_status ON tblMaterialLog(Status)")

        self._connection.commit()
        logger.info("Database schema created successfully")

    def _insert_sample_data(self):
        """Insert sample data for testing"""
        cursor = self._connection.cursor()

        # Insert admin user (password: admin123)
        admin_password_hash = bcrypt.hash("admin123")
        cursor.execute("""
            INSERT INTO tblUsers (Username, PasswordHash, FullName, Role, CreatedDate)
            VALUES (?, ?, ?, ?, ?)
        """, ("admin", admin_password_hash, "System Administrator", "Admin", datetime.now().isoformat()))

        # Insert NDT Methods
        ndt_methods = [
            ("RT", "Radiographic Testing", "X-ray or gamma-ray inspection"),
            ("UT", "Ultrasonic Testing", "High-frequency sound wave inspection"),
            ("PT", "Penetrant Testing", "Liquid penetrant surface inspection"),
            ("MT", "Magnetic Particle Testing", "Magnetic field surface inspection"),
            ("VT", "Visual Testing", "Direct visual inspection")
        ]
        cursor.executemany("""
            INSERT INTO tblNDTMethods (MethodCode, MethodName, Description)
            VALUES (?, ?, ?)
        """, ndt_methods)

        # Insert sample welders
        welders = [
            ("W001", "John Smith", "CERT-2024-001", (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"), "SMAW, GTAW", "Active", "Experienced with stainless steel"),
            ("W002", "Maria Garcia", "CERT-2024-002", (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d"), "GMAW, FCAW", "Active", "Certified for carbon steel"),
            ("W003", "Ahmed Hassan", "CERT-2024-003", (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"), "SMAW, GTAW, GMAW", "Active", "Multi-process certified"),
            ("W004", "Li Wei", "CERT-2023-045", (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"), "GTAW", "Inactive", "Certification expired"),
            ("W005", "Carlos Rodriguez", "CERT-2024-004", (datetime.now() + timedelta(days=270)).strftime("%Y-%m-%d"), "SMAW", "Active", "Pipe welding specialist")
        ]
        cursor.executemany("""
            INSERT INTO tblWelders (WelderCode, FullName, CertNumber, CertExpiry, Processes, Status, Notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, welders)

        # Insert sample WPS
        wps_list = [
            ("WPS-001", "Rev A", "SA-516 Gr 70", "ER70S-6", "GMAW", "1G, 2G", "2024-01-15", None, "Active"),
            ("WPS-002", "Rev B", "SA-213 T11", "ER80S-B2", "GTAW", "5G, 6G", "2024-02-20", None, "Active"),
            ("WPS-003", "Rev A", "SA-106 Gr B", "E7018", "SMAW", "2G, 3G, 4G", "2024-01-10", None, "Active"),
            ("WPS-004", "Rev C", "SA-335 P91", "ER90S-B9", "GTAW", "6G", "2024-03-05", None, "Active"),
            ("WPS-005", "Rev A", "SA-240 304L", "ER308L", "GTAW", "1G, 2G", "2023-12-01", None, "Active"),
            ("WPS-006", "Rev A", "SA-516 Gr 70", "E6010", "SMAW", "3G", "2023-06-15", None, "Obsolete"),
            ("WPS-007", "Rev B", "SA-213 T22", "ER80S-B2L", "GTAW", "5G", "2024-02-28", None, "Active"),
            ("WPS-008", "Rev A", "SA-106 Gr C", "ER70S-3", "GMAW", "1G, 2G", "2024-01-25", None, "Active"),
            ("WPS-009", "Rev A", "SA-240 316L", "ER316L", "GTAW", "6G", "2024-03-10", None, "Active"),
            ("WPS-010", "Rev B", "SA-335 P11", "ER80S-B2", "GTAW", "2G, 5G", "2024-02-15", None, "Active")
        ]
        cursor.executemany("""
            INSERT INTO tblWPS (WPSNumber, Revision, BaseMetalType, FillerMetal, WeldingProcess, Position, ApprovedDate, PDFPath, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, wps_list)

        # Insert sample drawing units
        drawing_units = [
            ("DWG-HRSG-001", "SN-001", "HP Evaporator Module", "Bay 1", "In Progress"),
            ("DWG-HRSG-002", "SN-002", "IP Superheater", "Bay 2", "Completed"),
            ("DWG-HRSG-003", "SN-003", "LP Economizer", "Bay 3", "In Progress")
        ]
        cursor.executemany("""
            INSERT INTO tblDrawingUnits (DrawingNumber, SerialNumber, UnitDescription, Location, Status)
            VALUES (?, ?, ?, ?, ?)
        """, drawing_units)

        # Insert sample welds
        welds = [
            ("WLD-001", 1, 1, 1, "Butt", "SA-516 Gr 70", 12.5, "2024-01-20", "Accepted", "Pass", "Root and fill passes completed"),
            ("WLD-002", 1, 2, 2, "Butt", "SA-213 T11", 8.0, "2024-01-21", "Accepted", "Pass", "All passes inspected"),
            ("WLD-003", 1, 3, 3, "Fillet", "SA-106 Gr B", 6.0, "2024-01-22", "Accepted", "Pass", None),
            ("WLD-004", 2, 4, 1, "Butt", "SA-335 P91", 15.0, "2024-01-23", "Pending", "N/A", "Awaiting NDT"),
            ("WLD-005", 2, 5, 2, "Butt", "SA-240 304L", 10.0, "2024-01-24", "Rejected", "Fail", "Porosity detected"),
            ("WLD-006", 2, 7, 3, "Butt", "SA-213 T22", 9.5, "2024-01-25", "Accepted", "Pass", None),
            ("WLD-007", 3, 8, 5, "Butt", "SA-106 Gr C", 11.0, "2024-01-26", "Accepted", "Pass", "Excellent quality"),
            ("WLD-008", 3, 1, 1, "Fillet", "SA-516 Gr 70", 8.0, "2024-01-27", "Pending", "N/A", "Scheduled for inspection"),
            ("WLD-009", 1, 9, 2, "Butt", "SA-240 316L", 12.0, "2024-01-28", "Accepted", "Pass", None),
            ("WLD-010", 2, 10, 3, "Butt", "SA-335 P11", 14.5, "2024-01-29", "Pending", "N/A", "In progress"),
            ("WLD-011", 3, 3, 5, "Butt", "SA-106 Gr B", 10.0, "2024-01-30", "Accepted", "Pass", "Root gap within spec"),
            ("WLD-012", 1, 2, 1, "Butt", "SA-213 T11", 7.5, "2024-01-31", "Rejected", "Fail", "Incomplete fusion"),
            ("WLD-013", 2, 5, 2, "Fillet", "SA-240 304L", 6.5, "2024-02-01", "Accepted", "Pass", None),
            ("WLD-014", 3, 4, 3, "Butt", "SA-335 P91", 13.0, "2024-02-02", "Accepted", "Pass", "Pre-heat applied correctly"),
            ("WLD-015", 1, 1, 5, "Butt", "SA-516 Gr 70", 11.5, "2024-02-03", "Pending", "N/A", "Final layer in progress"),
            ("WLD-016", 2, 8, 1, "Butt", "SA-106 Gr C", 9.0, "2024-02-04", "Accepted", "Pass", None),
            ("WLD-017", 3, 7, 2, "Butt", "SA-213 T22", 10.5, "2024-02-05", "Accepted", "Pass", "Post-weld heat treatment done"),
            ("WLD-018", 1, 9, 3, "Fillet", "SA-240 316L", 7.0, "2024-02-06", "Pending", "N/A", "Cleaning required"),
            ("WLD-019", 2, 10, 5, "Butt", "SA-335 P11", 12.5, "2024-02-07", "Accepted", "Pass", None),
            ("WLD-020", 3, 3, 1, "Butt", "SA-106 Gr B", 8.5, "2024-02-08", "Rejected", "Fail", "Crack observed")
        ]
        cursor.executemany("""
            INSERT INTO tblWelds (WeldNumber, DrawingUnitID, WPSID, WelderID, WeldType, MaterialSpec, Thickness, WeldDate, Status, VisualInspection, Notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, welds)

        # Insert sample NDT requests
        ndt_requests = [
            (1, 1, "2024-01-21", "2024-01-22", "Inspector A", "Accept", None, "NDT-001", None),
            (2, 2, "2024-01-22", "2024-01-23", "Inspector B", "Accept", None, "NDT-002", None),
            (3, 3, "2024-01-23", "2024-01-24", "Inspector A", "Accept", None, "NDT-003", None),
            (4, 1, "2024-01-24", None, None, "Pending", None, "NDT-004", None),
            (5, 4, "2024-01-25", "2024-01-26", "Inspector C", "Reject", "Porosity found in root pass", "NDT-005", None),
            (6, 2, "2024-01-26", "2024-01-27", "Inspector B", "Accept", None, "NDT-006", None),
            (7, 1, "2024-01-27", "2024-01-28", "Inspector A", "Accept", None, "NDT-007", None),
            (9, 3, "2024-01-29", "2024-01-30", "Inspector C", "Accept", None, "NDT-009", None),
            (11, 3, "2024-01-31", "2024-02-01", "Inspector A", "Accept", None, "NDT-011", None),
            (12, 1, "2024-02-01", "2024-02-02", "Inspector B", "Reject", "Incomplete fusion detected", "NDT-012", None),
            (13, 4, "2024-02-02", "2024-02-03", "Inspector C", "Accept", None, "NDT-013", None),
            (14, 2, "2024-02-03", "2024-02-04", "Inspector A", "Accept", None, "NDT-014", None),
            (16, 1, "2024-02-05", "2024-02-06", "Inspector B", "Accept", None, "NDT-016", None),
            (17, 2, "2024-02-06", "2024-02-07", "Inspector C", "Accept", None, "NDT-017", None),
            (19, 1, "2024-02-08", "2024-02-09", "Inspector A", "Accept", None, "NDT-019", None)
        ]
        cursor.executemany("""
            INSERT INTO tblNDTRequests (WeldID, NDTMethodID, RequestDate, InspectionDate, Inspector, Result, DefectDescription, ReportNumber, ReportPath)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ndt_requests)

        # Insert sample material log
        materials = [
            ("Base Metal", "SA-516 Gr 70", "HEAT-001", 5000.0, "kg", "Steel Supplier Inc", "2024-01-10", None, "Available"),
            ("Filler Metal", "ER70S-6", "LOT-2024-A", 500.0, "kg", "Welding Consumables Co", "2024-01-12", 1, "Used"),
            ("Base Metal", "SA-213 T11", "HEAT-002", 3000.0, "kg", "Alloy Metals Ltd", "2024-01-15", None, "Available"),
            ("Filler Metal", "ER80S-B2", "LOT-2024-B", 300.0, "kg", "Welding Consumables Co", "2024-01-15", 2, "Used"),
            ("Base Metal", "SA-335 P91", "HEAT-003", 2000.0, "kg", "Premium Alloys Inc", "2024-01-18", None, "Available"),
            ("Filler Metal", "ER90S-B9", "LOT-2024-C", 200.0, "kg", "Specialty Welding Supply", "2024-01-20", None, "Available"),
            ("Base Metal", "SA-240 304L", "HEAT-004", 4000.0, "kg", "Stainless Steel Depot", "2024-01-22", None, "Available"),
            ("Filler Metal", "ER308L", "LOT-2024-D", 400.0, "kg", "Welding Consumables Co", "2024-01-25", 5, "Used")
        ]
        cursor.executemany("""
            INSERT INTO tblMaterialLog (MaterialType, Specification, HeatNumber, Quantity, Unit, Supplier, ReceiveDate, UsedInWeldID, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, materials)

        self._connection.commit()
        logger.info("Sample data inserted successfully")

    def close(self):
        """Close the database connection"""
        if self._connection:
            self._connection.close()
            logger.info("Database connection closed")
