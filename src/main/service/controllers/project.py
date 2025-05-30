from src.main.service import ProjectService


class ProjectController:
    def __init__(self, service=None):
        super().__init__(service or ProjectService())

    def get_all_projects(self):
        return self.execute_service_method('get_all_projects')

    def get_project_by_id(self, project_id):
        return self.execute_service_method('get_project_by_id', project_id)

    def create_project(self, data):
        return self.execute_service_method('create_project', data)

    def update_project(self, project_id, data):
        return self.execute_service_method('update_project', project_id, data)

    def delete_project(self, project_id):
        return self.execute_service_method('delete_project', project_id)

    def search_projects(self, search_term=None, client=None, start_date=None, end_date=None):
        return self.execute_service_method('search_projects', search_term, client, start_date, end_date)

    def get_project_progress(self, project_id):
        return self.execute_service_method('get_project_progress', project_id)

    def get_project_cost(self, project_id):
        return self.execute_service_method('get_project_cost', project_id)

    def get_overdue_projects(self):
        return self.execute_service_method('get_overdue_projects')
