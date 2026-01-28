"""
Data Access Object (DAO) Layer
Provides CRUD operations for all database tables

Each DAO class handles database operations for a specific table,
keeping business logic separate from UI code.
"""

import logging
from datetime import datetime
from passlib.hash import bcrypt
from src.database.connection import DBConnection

logger = logging.getLogger(__name__)


class UserDAO:
    """Data Access Object for tblUsers"""

    def __init__(self):
        self.db = DBConnection().get_connection()

    def get_all(self):
        """Get all users"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tblUsers ORDER BY Username")
        return cursor.fetchall()

    def get_by_id(self, user_id):
        """Get user by ID"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tblUsers WHERE UserID = ?", (user_id,))
        return cursor.fetchone()

    def get_by_username(self, username):
        """Get user by username"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tblUsers WHERE Username = ?", (username,))
        return cursor.fetchone()

    def authenticate(self, username, password):
        """Authenticate user with username and password"""
        user = self.get_by_username(username)
        if user and bcrypt.verify(password, user['PasswordHash']):
            # Update last login
            self.update_last_login(user['UserID'])
            return user
        return None

    def create(self, data):
        """Create new user"""
        cursor = self.db.cursor()
        # Hash password
        password_hash = bcrypt.hash(data['password'])
        cursor.execute("""
            INSERT INTO tblUsers (Username, PasswordHash, FullName, Role, CreatedDate)
            VALUES (?, ?, ?, ?, ?)
        """, (data['username'], password_hash, data['full_name'], data['role'], datetime.now().isoformat()))
        self.db.commit()
        return cursor.lastrowid

    def update(self, user_id, data):
        """Update user"""
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE tblUsers
            SET FullName = ?, Role = ?
            WHERE UserID = ?
        """, (data['full_name'], data['role'], user_id))
        self.db.commit()
        return cursor.rowcount

    def update_password(self, user_id, new_password):
        """Update user password"""
        cursor = self.db.cursor()
        password_hash = bcrypt.hash(new_password)
        cursor.execute("UPDATE tblUsers SET PasswordHash = ? WHERE UserID = ?", (password_hash, user_id))
        self.db.commit()
        return cursor.rowcount

    def update_last_login(self, user_id):
        """Update last login timestamp"""
        cursor = self.db.cursor()
        cursor.execute("UPDATE tblUsers SET LastLogin = ? WHERE UserID = ?", (datetime.now().isoformat(), user_id))
        self.db.commit()

    def delete(self, user_id):
        """Delete user"""
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM tblUsers WHERE UserID = ?", (user_id,))
        self.db.commit()
        return cursor.rowcount

    def search(self, query):
        """Search users by username or full name"""
        cursor = self.db.cursor()
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT * FROM tblUsers
            WHERE Username LIKE ? OR FullName LIKE ?
            ORDER BY Username
        """, (search_pattern, search_pattern))
        return cursor.fetchall()


class WelderDAO:
    """Data Access Object for tblWelders"""

    def __init__(self):
        self.db = DBConnection().get_connection()

    def get_all(self):
        """Get all welders"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tblWelders ORDER BY WelderCode")
        return cursor.fetchall()

    def get_by_id(self, welder_id):
        """Get welder by ID"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tblWelders WHERE WelderID = ?", (welder_id,))
        return cursor.fetchone()

    def create(self, data):
        """Create new welder"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO tblWelders (WelderCode, FullName, CertNumber, CertExpiry, Processes, Status, Notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data['welder_code'], data['full_name'], data.get('cert_number'), data.get('cert_expiry'),
              data.get('processes'), data.get('status', 'Active'), data.get('notes')))
        self.db.commit()
        return cursor.lastrowid

    def update(self, welder_id, data):
        """Update welder"""
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE tblWelders
            SET WelderCode = ?, FullName = ?, CertNumber = ?, CertExpiry = ?,
                Processes = ?, Status = ?, Notes = ?
            WHERE WelderID = ?
        """, (data['welder_code'], data['full_name'], data.get('cert_number'), data.get('cert_expiry'),
              data.get('processes'), data.get('status', 'Active'), data.get('notes'), welder_id))
        self.db.commit()
        return cursor.rowcount

    def delete(self, welder_id):
        """Delete welder (with dependency check)"""
        cursor = self.db.cursor()
        # Check if welder has assigned welds
        cursor.execute("SELECT COUNT(*) as count FROM tblWelds WHERE WelderID = ?", (welder_id,))
        count = cursor.fetchone()['count']
        if count > 0:
            raise ValueError(f"Cannot delete welder. {count} welds are assigned to this welder.")

        cursor.execute("DELETE FROM tblWelders WHERE WelderID = ?", (welder_id,))
        self.db.commit()
        return cursor.rowcount

    def search(self, query):
        """Search welders by code or name"""
        cursor = self.db.cursor()
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT * FROM tblWelders
            WHERE WelderCode LIKE ? OR FullName LIKE ? OR CertNumber LIKE ?
            ORDER BY WelderCode
        """, (search_pattern, search_pattern, search_pattern))
        return cursor.fetchall()

    def get_by_status(self, status):
        """Get welders by status"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tblWelders WHERE Status = ? ORDER BY WelderCode", (status,))
        return cursor.fetchall()

    def get_active_welders(self):
        """Get all active welders"""
        return self.get_by_status('Active')


class WPSDAO:
    """Data Access Object for tblWPS"""

    def __init__(self):
        self.db = DBConnection().get_connection()

    def get_all(self):
        """Get all WPS"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tblWPS ORDER BY WPSNumber")
        return cursor.fetchall()

    def get_by_id(self, wps_id):
        """Get WPS by ID"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tblWPS WHERE WPSID = ?", (wps_id,))
        return cursor.fetchone()

    def create(self, data):
        """Create new WPS"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO tblWPS (WPSNumber, Revision, BaseMetalType, FillerMetal, WeldingProcess,
                               Position, ApprovedDate, PDFPath, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data['wps_number'], data.get('revision'), data.get('base_metal_type'),
              data.get('filler_metal'), data.get('welding_process'), data.get('position'),
              data.get('approved_date'), data.get('pdf_path'), data.get('status', 'Active')))
        self.db.commit()
        return cursor.lastrowid

    def update(self, wps_id, data):
        """Update WPS"""
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE tblWPS
            SET WPSNumber = ?, Revision = ?, BaseMetalType = ?, FillerMetal = ?,
                WeldingProcess = ?, Position = ?, ApprovedDate = ?, PDFPath = ?, Status = ?
            WHERE WPSID = ?
        """, (data['wps_number'], data.get('revision'), data.get('base_metal_type'),
              data.get('filler_metal'), data.get('welding_process'), data.get('position'),
              data.get('approved_date'), data.get('pdf_path'), data.get('status', 'Active'), wps_id))
        self.db.commit()
        return cursor.rowcount

    def delete(self, wps_id):
        """Delete WPS (with dependency check)"""
        cursor = self.db.cursor()
        # Check if WPS is used in welds
        cursor.execute("SELECT COUNT(*) as count FROM tblWelds WHERE WPSID = ?", (wps_id,))
        count = cursor.fetchone()['count']
        if count > 0:
            raise ValueError(f"Cannot delete WPS. {count} welds are using this WPS.")

        cursor.execute("DELETE FROM tblWPS WHERE WPSID = ?", (wps_id,))
        self.db.commit()
        return cursor.rowcount

    def search(self, query):
        """Search WPS by number or process"""
        cursor = self.db.cursor()
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT * FROM tblWPS
            WHERE WPSNumber LIKE ? OR WeldingProcess LIKE ? OR BaseMetalType LIKE ?
            ORDER BY WPSNumber
        """, (search_pattern, search_pattern, search_pattern))
        return cursor.fetchall()

    def get_by_status(self, status):
        """Get WPS by status"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tblWPS WHERE Status = ? ORDER BY WPSNumber", (status,))
        return cursor.fetchall()

    def get_active_wps(self):
        """Get all active WPS"""
        return self.get_by_status('Active')


class DrawingUnitDAO:
    """Data Access Object for tblDrawingUnits"""

    def __init__(self):
        self.db = DBConnection().get_connection()

    def get_all(self):
        """Get all drawing units"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tblDrawingUnits ORDER BY DrawingNumber")
        return cursor.fetchall()

    def get_by_id(self, drawing_unit_id):
        """Get drawing unit by ID"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tblDrawingUnits WHERE DrawingUnitID = ?", (drawing_unit_id,))
        return cursor.fetchone()

    def create(self, data):
        """Create new drawing unit"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO tblDrawingUnits (DrawingNumber, SerialNumber, UnitDescription, Location, Status)
            VALUES (?, ?, ?, ?, ?)
        """, (data['drawing_number'], data.get('serial_number'), data.get('unit_description'),
              data.get('location'), data.get('status')))
        self.db.commit()
        return cursor.lastrowid

    def update(self, drawing_unit_id, data):
        """Update drawing unit"""
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE tblDrawingUnits
            SET DrawingNumber = ?, SerialNumber = ?, UnitDescription = ?, Location = ?, Status = ?
            WHERE DrawingUnitID = ?
        """, (data['drawing_number'], data.get('serial_number'), data.get('unit_description'),
              data.get('location'), data.get('status'), drawing_unit_id))
        self.db.commit()
        return cursor.rowcount

    def delete(self, drawing_unit_id):
        """Delete drawing unit (with dependency check)"""
        cursor = self.db.cursor()
        # Check if drawing unit has welds
        cursor.execute("SELECT COUNT(*) as count FROM tblWelds WHERE DrawingUnitID = ?", (drawing_unit_id,))
        count = cursor.fetchone()['count']
        if count > 0:
            raise ValueError(f"Cannot delete drawing unit. {count} welds are linked to this drawing.")

        cursor.execute("DELETE FROM tblDrawingUnits WHERE DrawingUnitID = ?", (drawing_unit_id,))
        self.db.commit()
        return cursor.rowcount

    def search(self, query):
        """Search drawing units"""
        cursor = self.db.cursor()
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT * FROM tblDrawingUnits
            WHERE DrawingNumber LIKE ? OR SerialNumber LIKE ? OR UnitDescription LIKE ?
            ORDER BY DrawingNumber
        """, (search_pattern, search_pattern, search_pattern))
        return cursor.fetchall()

    def get_weld_count(self, drawing_unit_id):
        """Get count of welds for a drawing unit"""
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM tblWelds WHERE DrawingUnitID = ?", (drawing_unit_id,))
        return cursor.fetchone()['count']


class WeldDAO:
    """Data Access Object for tblWelds"""

    def __init__(self):
        self.db = DBConnection().get_connection()

    def get_all(self):
        """Get all welds with joined data"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT w.*, wd.FullName as WelderName, wps.WPSNumber, d.DrawingNumber
            FROM tblWelds w
            LEFT JOIN tblWelders wd ON w.WelderID = wd.WelderID
            LEFT JOIN tblWPS wps ON w.WPSID = wps.WPSID
            LEFT JOIN tblDrawingUnits d ON w.DrawingUnitID = d.DrawingUnitID
            ORDER BY w.WeldNumber
        """)
        return cursor.fetchall()

    def get_by_id(self, weld_id):
        """Get weld by ID with joined data"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT w.*, wd.FullName as WelderName, wps.WPSNumber, d.DrawingNumber
            FROM tblWelds w
            LEFT JOIN tblWelders wd ON w.WelderID = wd.WelderID
            LEFT JOIN tblWPS wps ON w.WPSID = wps.WPSID
            LEFT JOIN tblDrawingUnits d ON w.DrawingUnitID = d.DrawingUnitID
            WHERE w.WeldID = ?
        """, (weld_id,))
        return cursor.fetchone()

    def create(self, data):
        """Create new weld"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO tblWelds (WeldNumber, DrawingUnitID, WPSID, WelderID, WeldType,
                                MaterialSpec, Thickness, WeldDate, Status, VisualInspection, Notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data['weld_number'], data.get('drawing_unit_id'), data.get('wps_id'),
              data.get('welder_id'), data.get('weld_type'), data.get('material_spec'),
              data.get('thickness'), data.get('weld_date'), data.get('status', 'Pending'),
              data.get('visual_inspection', 'N/A'), data.get('notes')))
        self.db.commit()
        return cursor.lastrowid

    def update(self, weld_id, data):
        """Update weld"""
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE tblWelds
            SET WeldNumber = ?, DrawingUnitID = ?, WPSID = ?, WelderID = ?, WeldType = ?,
                MaterialSpec = ?, Thickness = ?, WeldDate = ?, Status = ?, VisualInspection = ?, Notes = ?
            WHERE WeldID = ?
        """, (data['weld_number'], data.get('drawing_unit_id'), data.get('wps_id'),
              data.get('welder_id'), data.get('weld_type'), data.get('material_spec'),
              data.get('thickness'), data.get('weld_date'), data.get('status', 'Pending'),
              data.get('visual_inspection', 'N/A'), data.get('notes'), weld_id))
        self.db.commit()
        return cursor.rowcount

    def delete(self, weld_id):
        """Delete weld (cascade deletes NDT requests and material links)"""
        cursor = self.db.cursor()
        # Delete related NDT requests
        cursor.execute("DELETE FROM tblNDTRequests WHERE WeldID = ?", (weld_id,))
        # Update material log (remove weld link)
        cursor.execute("UPDATE tblMaterialLog SET UsedInWeldID = NULL WHERE UsedInWeldID = ?", (weld_id,))
        # Delete weld
        cursor.execute("DELETE FROM tblWelds WHERE WeldID = ?", (weld_id,))
        self.db.commit()
        return cursor.rowcount

    def search(self, query):
        """Search welds"""
        cursor = self.db.cursor()
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT w.*, wd.FullName as WelderName, wps.WPSNumber, d.DrawingNumber
            FROM tblWelds w
            LEFT JOIN tblWelders wd ON w.WelderID = wd.WelderID
            LEFT JOIN tblWPS wps ON w.WPSID = wps.WPSID
            LEFT JOIN tblDrawingUnits d ON w.DrawingUnitID = d.DrawingUnitID
            WHERE w.WeldNumber LIKE ? OR w.MaterialSpec LIKE ? OR w.Notes LIKE ?
            ORDER BY w.WeldNumber
        """, (search_pattern, search_pattern, search_pattern))
        return cursor.fetchall()

    def get_by_status(self, status):
        """Get welds by status"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT w.*, wd.FullName as WelderName, wps.WPSNumber, d.DrawingNumber
            FROM tblWelds w
            LEFT JOIN tblWelders wd ON w.WelderID = wd.WelderID
            LEFT JOIN tblWPS wps ON w.WPSID = wps.WPSID
            LEFT JOIN tblDrawingUnits d ON w.DrawingUnitID = d.DrawingUnitID
            WHERE w.Status = ?
            ORDER BY w.WeldNumber
        """, (status,))
        return cursor.fetchall()

    def get_by_welder(self, welder_id):
        """Get welds by welder"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT w.*, wd.FullName as WelderName, wps.WPSNumber, d.DrawingNumber
            FROM tblWelds w
            LEFT JOIN tblWelders wd ON w.WelderID = wd.WelderID
            LEFT JOIN tblWPS wps ON w.WPSID = wps.WPSID
            LEFT JOIN tblDrawingUnits d ON w.DrawingUnitID = d.DrawingUnitID
            WHERE w.WelderID = ?
            ORDER BY w.WeldDate DESC
        """, (welder_id,))
        return cursor.fetchall()

    def get_by_wps(self, wps_id):
        """Get welds by WPS"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT w.*, wd.FullName as WelderName, wps.WPSNumber, d.DrawingNumber
            FROM tblWelds w
            LEFT JOIN tblWelders wd ON w.WelderID = wd.WelderID
            LEFT JOIN tblWPS wps ON w.WPSID = wps.WPSID
            LEFT JOIN tblDrawingUnits d ON w.DrawingUnitID = d.DrawingUnitID
            WHERE w.WPSID = ?
            ORDER BY w.WeldNumber
        """, (wps_id,))
        return cursor.fetchall()

    def get_by_drawing(self, drawing_unit_id):
        """Get welds by drawing unit"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT w.*, wd.FullName as WelderName, wps.WPSNumber, d.DrawingNumber
            FROM tblWelds w
            LEFT JOIN tblWelders wd ON w.WelderID = wd.WelderID
            LEFT JOIN tblWPS wps ON w.WPSID = wps.WPSID
            LEFT JOIN tblDrawingUnits d ON w.DrawingUnitID = d.DrawingUnitID
            WHERE w.DrawingUnitID = ?
            ORDER BY w.WeldNumber
        """, (drawing_unit_id,))
        return cursor.fetchall()

    def get_statistics(self):
        """Get weld statistics"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT
                COUNT(*) as total_welds,
                SUM(CASE WHEN Status = 'Pending' THEN 1 ELSE 0 END) as pending_welds,
                SUM(CASE WHEN Status = 'Accepted' THEN 1 ELSE 0 END) as accepted_welds,
                SUM(CASE WHEN Status = 'Rejected' THEN 1 ELSE 0 END) as rejected_welds,
                SUM(CASE WHEN Status = 'Repair' THEN 1 ELSE 0 END) as repair_welds,
                ROUND(CAST(SUM(CASE WHEN Status = 'Rejected' THEN 1 ELSE 0 END) AS REAL) /
                      NULLIF(COUNT(*), 0) * 100, 2) as rejection_rate
            FROM tblWelds
        """)
        return cursor.fetchone()


class NDTMethodDAO:
    """Data Access Object for tblNDTMethods"""

    def __init__(self):
        self.db = DBConnection().get_connection()

    def get_all(self):
        """Get all NDT methods"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tblNDTMethods ORDER BY MethodCode")
        return cursor.fetchall()

    def get_by_id(self, method_id):
        """Get NDT method by ID"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tblNDTMethods WHERE MethodID = ?", (method_id,))
        return cursor.fetchone()

    def get_active(self):
        """Get active NDT methods"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tblNDTMethods WHERE IsActive = 1 ORDER BY MethodCode")
        return cursor.fetchall()

    def create(self, data):
        """Create new NDT method"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO tblNDTMethods (MethodCode, MethodName, Description, IsActive)
            VALUES (?, ?, ?, ?)
        """, (data['method_code'], data['method_name'], data.get('description'), data.get('is_active', 1)))
        self.db.commit()
        return cursor.lastrowid

    def update(self, method_id, data):
        """Update NDT method"""
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE tblNDTMethods
            SET MethodCode = ?, MethodName = ?, Description = ?, IsActive = ?
            WHERE MethodID = ?
        """, (data['method_code'], data['method_name'], data.get('description'),
              data.get('is_active', 1), method_id))
        self.db.commit()
        return cursor.rowcount

    def delete(self, method_id):
        """Delete NDT method (with dependency check)"""
        cursor = self.db.cursor()
        # Check if method is used in NDT requests
        cursor.execute("SELECT COUNT(*) as count FROM tblNDTRequests WHERE NDTMethodID = ?", (method_id,))
        count = cursor.fetchone()['count']
        if count > 0:
            raise ValueError(f"Cannot delete NDT method. {count} NDT requests are using this method.")

        cursor.execute("DELETE FROM tblNDTMethods WHERE MethodID = ?", (method_id,))
        self.db.commit()
        return cursor.rowcount


class NDTRequestDAO:
    """Data Access Object for tblNDTRequests"""

    def __init__(self):
        self.db = DBConnection().get_connection()

    def get_all(self):
        """Get all NDT requests with joined data"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT n.*, w.WeldNumber, m.MethodCode, m.MethodName
            FROM tblNDTRequests n
            LEFT JOIN tblWelds w ON n.WeldID = w.WeldID
            LEFT JOIN tblNDTMethods m ON n.NDTMethodID = m.MethodID
            ORDER BY n.RequestDate DESC
        """)
        return cursor.fetchall()

    def get_by_id(self, ndt_id):
        """Get NDT request by ID with joined data"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT n.*, w.WeldNumber, m.MethodCode, m.MethodName
            FROM tblNDTRequests n
            LEFT JOIN tblWelds w ON n.WeldID = w.WeldID
            LEFT JOIN tblNDTMethods m ON n.NDTMethodID = m.MethodID
            WHERE n.NDTID = ?
        """, (ndt_id,))
        return cursor.fetchone()

    def create(self, data):
        """Create new NDT request"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO tblNDTRequests (WeldID, NDTMethodID, RequestDate, InspectionDate,
                                       Inspector, Result, DefectDescription, ReportNumber, ReportPath)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data['weld_id'], data['ndt_method_id'], data['request_date'],
              data.get('inspection_date'), data.get('inspector'), data.get('result', 'Pending'),
              data.get('defect_description'), data.get('report_number'), data.get('report_path')))
        self.db.commit()
        return cursor.lastrowid

    def update(self, ndt_id, data):
        """Update NDT request"""
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE tblNDTRequests
            SET WeldID = ?, NDTMethodID = ?, RequestDate = ?, InspectionDate = ?,
                Inspector = ?, Result = ?, DefectDescription = ?, ReportNumber = ?, ReportPath = ?
            WHERE NDTID = ?
        """, (data['weld_id'], data['ndt_method_id'], data['request_date'],
              data.get('inspection_date'), data.get('inspector'), data.get('result', 'Pending'),
              data.get('defect_description'), data.get('report_number'), data.get('report_path'), ndt_id))
        self.db.commit()
        return cursor.rowcount

    def delete(self, ndt_id):
        """Delete NDT request"""
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM tblNDTRequests WHERE NDTID = ?", (ndt_id,))
        self.db.commit()
        return cursor.rowcount

    def search(self, query):
        """Search NDT requests"""
        cursor = self.db.cursor()
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT n.*, w.WeldNumber, m.MethodCode, m.MethodName
            FROM tblNDTRequests n
            LEFT JOIN tblWelds w ON n.WeldID = w.WeldID
            LEFT JOIN tblNDTMethods m ON n.NDTMethodID = m.MethodID
            WHERE w.WeldNumber LIKE ? OR n.Inspector LIKE ? OR n.ReportNumber LIKE ?
            ORDER BY n.RequestDate DESC
        """, (search_pattern, search_pattern, search_pattern))
        return cursor.fetchall()

    def get_by_weld(self, weld_id):
        """Get NDT requests for a specific weld"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT n.*, w.WeldNumber, m.MethodCode, m.MethodName
            FROM tblNDTRequests n
            LEFT JOIN tblWelds w ON n.WeldID = w.WeldID
            LEFT JOIN tblNDTMethods m ON n.NDTMethodID = m.MethodID
            WHERE n.WeldID = ?
            ORDER BY n.RequestDate DESC
        """, (weld_id,))
        return cursor.fetchall()

    def get_by_result(self, result):
        """Get NDT requests by result"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT n.*, w.WeldNumber, m.MethodCode, m.MethodName
            FROM tblNDTRequests n
            LEFT JOIN tblWelds w ON n.WeldID = w.WeldID
            LEFT JOIN tblNDTMethods m ON n.NDTMethodID = m.MethodID
            WHERE n.Result = ?
            ORDER BY n.RequestDate DESC
        """, (result,))
        return cursor.fetchall()

    def get_pending(self):
        """Get pending NDT requests"""
        return self.get_by_result('Pending')

    def get_statistics(self):
        """Get NDT statistics"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT
                COUNT(*) as total_ndt,
                SUM(CASE WHEN Result = 'Pending' THEN 1 ELSE 0 END) as pending_ndt,
                SUM(CASE WHEN Result = 'Accept' THEN 1 ELSE 0 END) as accepted_ndt,
                SUM(CASE WHEN Result = 'Reject' THEN 1 ELSE 0 END) as rejected_ndt
            FROM tblNDTRequests
        """)
        return cursor.fetchone()


class MaterialLogDAO:
    """Data Access Object for tblMaterialLog"""

    def __init__(self):
        self.db = DBConnection().get_connection()

    def get_all(self):
        """Get all materials"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT m.*, w.WeldNumber
            FROM tblMaterialLog m
            LEFT JOIN tblWelds w ON m.UsedInWeldID = w.WeldID
            ORDER BY m.ReceiveDate DESC
        """)
        return cursor.fetchall()

    def get_by_id(self, material_id):
        """Get material by ID"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT m.*, w.WeldNumber
            FROM tblMaterialLog m
            LEFT JOIN tblWelds w ON m.UsedInWeldID = w.WeldID
            WHERE m.MaterialID = ?
        """, (material_id,))
        return cursor.fetchone()

    def create(self, data):
        """Create new material log entry"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO tblMaterialLog (MaterialType, Specification, HeatNumber, Quantity,
                                       Unit, Supplier, ReceiveDate, UsedInWeldID, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data['material_type'], data.get('specification'), data.get('heat_number'),
              data.get('quantity'), data.get('unit'), data.get('supplier'),
              data.get('receive_date'), data.get('used_in_weld_id'), data.get('status', 'Available')))
        self.db.commit()
        return cursor.lastrowid

    def update(self, material_id, data):
        """Update material"""
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE tblMaterialLog
            SET MaterialType = ?, Specification = ?, HeatNumber = ?, Quantity = ?,
                Unit = ?, Supplier = ?, ReceiveDate = ?, UsedInWeldID = ?, Status = ?
            WHERE MaterialID = ?
        """, (data['material_type'], data.get('specification'), data.get('heat_number'),
              data.get('quantity'), data.get('unit'), data.get('supplier'),
              data.get('receive_date'), data.get('used_in_weld_id'), data.get('status', 'Available'),
              material_id))
        self.db.commit()
        return cursor.rowcount

    def delete(self, material_id):
        """Delete material"""
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM tblMaterialLog WHERE MaterialID = ?", (material_id,))
        self.db.commit()
        return cursor.rowcount

    def search(self, query):
        """Search materials"""
        cursor = self.db.cursor()
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT m.*, w.WeldNumber
            FROM tblMaterialLog m
            LEFT JOIN tblWelds w ON m.UsedInWeldID = w.WeldID
            WHERE m.Specification LIKE ? OR m.HeatNumber LIKE ? OR m.Supplier LIKE ?
            ORDER BY m.ReceiveDate DESC
        """, (search_pattern, search_pattern, search_pattern))
        return cursor.fetchall()

    def get_by_status(self, status):
        """Get materials by status"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT m.*, w.WeldNumber
            FROM tblMaterialLog m
            LEFT JOIN tblWelds w ON m.UsedInWeldID = w.WeldID
            WHERE m.Status = ?
            ORDER BY m.ReceiveDate DESC
        """, (status,))
        return cursor.fetchall()

    def get_available(self):
        """Get available materials"""
        return self.get_by_status('Available')

    def link_to_weld(self, material_id, weld_id):
        """Link material to a weld and mark as used"""
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE tblMaterialLog
            SET UsedInWeldID = ?, Status = 'Used'
            WHERE MaterialID = ?
        """, (weld_id, material_id))
        self.db.commit()
        return cursor.rowcount
