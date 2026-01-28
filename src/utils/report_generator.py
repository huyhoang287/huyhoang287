"""
Report Generator
Generates professional Excel reports for various data analyses
"""

import logging
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, PieChart, Reference
from src.database.models import WeldDAO, WelderDAO, NDTRequestDAO, MaterialLogDAO

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate various reports for the HRSG Weld Management System"""

    def __init__(self):
        self.weld_dao = WeldDAO()
        self.welder_dao = WelderDAO()
        self.ndt_dao = NDTRequestDAO()
        self.material_dao = MaterialLogDAO()

    def generate_welder_performance_report(self, filename):
        """
        Generate Welder Performance Report

        Args:
            filename: Output Excel filename

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Welder Performance"

            # Title
            ws['A1'] = "Welder Performance Report"
            ws['A1'].font = Font(size=16, bold=True)
            ws['A2'] = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            ws['A2'].font = Font(size=10, italic=True)

            # Headers
            headers = ["Welder Code", "Welder Name", "Total Welds", "Accepted", "Rejected", "Pending", "Rejection Rate (%)"]
            row = 4
            for col, header in enumerate(headers, start=1):
                cell = ws.cell(row=row, column=col, value=header)
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="3B82F6", end_color="3B82F6", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")

            # Get data
            welders = self.welder_dao.get_all()
            row = 5

            for welder in welders:
                welds = self.weld_dao.get_by_welder(welder['WelderID'])
                total = len(welds)
                accepted = sum(1 for w in welds if w['Status'] == 'Accepted')
                rejected = sum(1 for w in welds if w['Status'] == 'Rejected')
                pending = sum(1 for w in welds if w['Status'] == 'Pending')
                rejection_rate = (rejected / total * 100) if total > 0 else 0

                ws.cell(row=row, column=1, value=welder['WelderCode'])
                ws.cell(row=row, column=2, value=welder['FullName'])
                ws.cell(row=row, column=3, value=total)
                ws.cell(row=row, column=4, value=accepted)
                ws.cell(row=row, column=5, value=rejected)
                ws.cell(row=row, column=6, value=pending)
                ws.cell(row=row, column=7, value=f"{rejection_rate:.2f}%")

                row += 1

            # Auto-adjust columns
            for col in range(1, 8):
                ws.column_dimensions[chr(64 + col)].width = 20

            wb.save(filename)
            logger.info(f"Welder Performance Report generated: {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to generate Welder Performance Report: {e}")
            return False

    def generate_ndt_summary_report(self, filename):
        """
        Generate NDT Summary Report

        Args:
            filename: Output Excel filename

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "NDT Summary"

            # Title
            ws['A1'] = "NDT Summary Report"
            ws['A1'].font = Font(size=16, bold=True)
            ws['A2'] = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Headers
            headers = ["Weld Number", "NDT Method", "Request Date", "Inspection Date", "Inspector", "Result"]
            row = 4
            for col, header in enumerate(headers, start=1):
                cell = ws.cell(row=row, column=col, value=header)
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="3B82F6", end_color="3B82F6", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")

            # Get data
            ndt_requests = self.ndt_dao.get_all()
            row = 5

            for ndt in ndt_requests:
                ws.cell(row=row, column=1, value=ndt['WeldNumber'])
                ws.cell(row=row, column=2, value=ndt['MethodCode'])
                ws.cell(row=row, column=3, value=ndt['RequestDate'])
                ws.cell(row=row, column=4, value=ndt['InspectionDate'] or 'Pending')
                ws.cell(row=row, column=5, value=ndt['Inspector'] or 'N/A')
                ws.cell(row=row, column=6, value=ndt['Result'])
                row += 1

            # Auto-adjust columns
            for col in range(1, 7):
                ws.column_dimensions[chr(64 + col)].width = 20

            wb.save(filename)
            logger.info(f"NDT Summary Report generated: {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to generate NDT Summary Report: {e}")
            return False

    def generate_project_progress_report(self, filename):
        """
        Generate Project Progress Report

        Args:
            filename: Output Excel filename

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Project Progress"

            # Title
            ws['A1'] = "Project Progress Report"
            ws['A1'].font = Font(size=16, bold=True)
            ws['A2'] = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Get statistics
            stats = self.weld_dao.get_statistics()

            # Summary section
            row = 4
            ws.cell(row=row, column=1, value="Total Welds:").font = Font(bold=True)
            ws.cell(row=row, column=2, value=stats['total_welds'])

            row += 1
            ws.cell(row=row, column=1, value="Accepted Welds:").font = Font(bold=True)
            ws.cell(row=row, column=2, value=stats['accepted_welds'])

            row += 1
            ws.cell(row=row, column=1, value="Rejected Welds:").font = Font(bold=True)
            ws.cell(row=row, column=2, value=stats['rejected_welds'])

            row += 1
            ws.cell(row=row, column=1, value="Pending Welds:").font = Font(bold=True)
            ws.cell(row=row, column=2, value=stats['pending_welds'])

            row += 1
            ws.cell(row=row, column=1, value="Rejection Rate:").font = Font(bold=True)
            ws.cell(row=row, column=2, value=f"{stats['rejection_rate']}%")

            # Auto-adjust columns
            ws.column_dimensions['A'].width = 25
            ws.column_dimensions['B'].width = 15

            wb.save(filename)
            logger.info(f"Project Progress Report generated: {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to generate Project Progress Report: {e}")
            return False

    def generate_material_usage_report(self, filename):
        """
        Generate Material Usage Report

        Args:
            filename: Output Excel filename

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Material Usage"

            # Title
            ws['A1'] = "Material Usage Report"
            ws['A1'].font = Font(size=16, bold=True)
            ws['A2'] = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Headers
            headers = ["Material Type", "Specification", "Heat Number", "Quantity", "Unit", "Status", "Used In Weld"]
            row = 4
            for col, header in enumerate(headers, start=1):
                cell = ws.cell(row=row, column=col, value=header)
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="3B82F6", end_color="3B82F6", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")

            # Get data
            materials = self.material_dao.get_all()
            row = 5

            for material in materials:
                ws.cell(row=row, column=1, value=material['MaterialType'])
                ws.cell(row=row, column=2, value=material['Specification'])
                ws.cell(row=row, column=3, value=material['HeatNumber'])
                ws.cell(row=row, column=4, value=material['Quantity'])
                ws.cell(row=row, column=5, value=material['Unit'])
                ws.cell(row=row, column=6, value=material['Status'])
                ws.cell(row=row, column=7, value=material['WeldNumber'] or 'N/A')
                row += 1

            # Auto-adjust columns
            for col in range(1, 8):
                ws.column_dimensions[chr(64 + col)].width = 18

            wb.save(filename)
            logger.info(f"Material Usage Report generated: {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to generate Material Usage Report: {e}")
            return False
