class BaseController:
    def execute_service_method(self, method_name, *args, **kwargs):
        method = getattr(self.service, method_name, None)
        if not method:
            return {'success': False, 'data': None, 'error': f"Service has no method '{method_name}'"}
        try:
            result = method(*args, **kwargs)
            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'data': None, 'error': str(e)}
