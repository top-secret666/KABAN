from controllers.base_controller import BaseController
from services.export_service import ExportService
from exceptions import BusinessException
import os
from datetime import datetime

class ExportController(BaseController):
    """
    Контроллер для экспорта данных
    """
    def __init__(self):
        """
        Инициализирует контроллер экспорта
        """
        super().__init__()
        self.export_service = ExportService()
    
    def export_report_to_csv(self, report_data, filename=None):
        """
        Экспортирует отчет в CSV-файл
        
        Args:
            report_data: Данные отчета
            filename: Имя файла (если None, генерируется автоматически)
        
        Returns:
            dict: Результат операции
        """
        try:
            # Если имя файла не указано, генерируем его
            if filename is None:
                report_type = report_data.get('report_name', 'report').replace(' ', '_').lower()
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = os.path.join('reports', f'{report_type}_{timestamp}.csv')
            
            # Форматируем данные отчета
            headers, rows = ExportService.format_report_data(report_data)
            
            # Экспортируем данные в CSV
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
        """
        Экспортирует отчет в Excel-файл
        
        Args:
            report_data: Данные отчета
            filename: Имя файла (если None, генерируется автоматически)
        
        Returns:
            dict: Результат операции
        """
        try:
            # Если имя файла не указано, генерируем его
            if filename is None:
                report_type = report_data.get('report_name', 'report').replace(' ', '_').lower()
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = os.path.join('reports', f'{report_type}_{timestamp}.xlsx')
            
            # Форматируем данные отчета
            headers, rows = ExportService.format_report_data(report_data)
            
            # Экспортируем данные в Excel
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
        """
        Экспортирует произвольные данные в CSV-файл
        
        Args:
            data: Данные для экспорта
            headers: Заголовки столбцов
            filename: Имя файла
        
        Returns:
            dict: Результат операции
        """
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
        """
        Экспортирует произвольные данные в Excel-файл
        
        Args:
            data: Данные для экспорта
            headers: Заголовки столбцов
            filename: Имя файла
            sheet_name: Имя листа
        
        Returns:
            dict: Результат операции
        """
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
