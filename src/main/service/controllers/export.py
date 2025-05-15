from src.main.service.export_service import ExportService
from src.main.service.exceptions import BusinessException
import os
from datetime import datetime


class ExportController:
    def __init__(self):
        super().__init__()
        self.export_service = ExportService()

    def export_report_to_csv(self, report_data, filename=None):
        try:
            if filename is None:
                report_type = report_data.get('report_name', 'report').replace(' ', '_').lower()
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = os.path.join('reports', f'{report_type}_{timestamp}.csv')

            headers, rows = ExportService.format_report_data(report_data)

            result = ExportService.export_to_csv(rows, filename, headers)

            if not result['success']:
                raise BusinessException(f"Ошибка при экспорте в CSV: {result.get('error')}")

            return {
                'success': True,
                'data': result
            }

        except Exception as e:
            return self.handle_exception(e)

    def export_report_to_excel(self, report_data, filename=None):
        try:
            if filename is None:
                report_type = report_data.get('report_name', 'report').replace(' ', '_').lower()
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = os.path.join('reports', f'{report_type}_{timestamp}.xlsx')

            headers, rows = ExportService.format_report_data(report_data)

            result = ExportService.export_to_excel(rows, filename, report_data.get('report_name', 'Отчет'), headers)

            if not result['success']:
                raise BusinessException(f"Ошибка при экспорте в Excel: {result.get('error')}")

            return {
                'success': True,
                'data': result
            }

        except Exception as e:
            return self.handle_exception(e)

    def export_data_to_csv(self, data, headers, filename):
        try:
            result = ExportService.export_to_csv(data, filename, headers)

            if not result['success']:
                raise BusinessException(f"Ошибка при экспорте в CSV: {result.get('error')}")

            return {
                'success': True,
                'data': result
            }

        except Exception as e:
            return self.handle_exception(e)

    def export_data_to_excel(self, data, headers, filename, sheet_name='Данные'):
        try:
            result = ExportService.export_to_excel(data, filename, sheet_name, headers)

            if not result['success']:
                raise BusinessException(f"Ошибка при экспорте в Excel: {result.get('error')}")

            return {
                'success': True,
                'data': result
            }

        except Exception as e:
            return self.handle_exception(e)
